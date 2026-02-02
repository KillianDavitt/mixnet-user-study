import os
import sys
import sqlite3
from typing import List, Tuple, Dict, Any
import numpy as np
import pandas as pd
import plotly.graph_objects as go

IDX_GROUP = 3          # x[3]  group/condition id
IDX_PARTICIPANT = 5
IDX_LIKERT = 10        # x[10] perceived time change response

LIKERT_LEVELS = list(range(1, 5 + 1))

EXCLUDE_GROUP_ID = 5

GROUP_LABELS: Dict[Any, str] = {
     0: "No Assistance",
     1000: "1",
     4000: "4",
     7000: "7",
     10000: "10",
}

BACKGROUND_COLOR = "#FFFFFF"
COLORS = [
    "#de425b",  # Much Slower
    "#ea936d",  # Slightly Slower
    "#fbdbb1",  # Neutral
    "#b2b264",  # Slightly Quicker
    "#488f31",  # Much Quicker
]
LIKERT_LABELS = [
    "<b>Much<br>Slower</b>",
    "<b>Slightly Slower</b>",
    "<b>Neutral</b>",
    "<b>Slightly Quicker</b>",
    "<b>Much<br>Quicker</b>",
]

def fetch_rows(db_path):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        rows = cur.execute(f"SELECT * FROM response;").fetchall()
        return rows
    finally:
        conn.close()

def compute_group_percentages(rows):
    group_ids = sorted({r[IDX_GROUP] for r in rows if r is not None})

    if EXCLUDE_GROUP_ID is not None:
        group_ids = [g for g in group_ids if g != EXCLUDE_GROUP_ID]

    counts = np.zeros((len(group_ids), len(LIKERT_LEVELS)), dtype=int)

    group_index = {g: i for i, g in enumerate(group_ids)}

    for r in rows:
        g = r[IDX_GROUP]
        if EXCLUDE_GROUP_ID is not None and g == EXCLUDE_GROUP_ID:
            continue
        if g not in group_index:
            continue

        likert = int((r[IDX_LIKERT]))
        if likert is None or not (1 <= likert <= 5):
            continue

        counts[group_index[g], likert - 1] += 1

    totals = counts.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        perc = np.where(totals == 0, 0.0, counts / totals * 100.0)

    perc = np.round(perc, 1)

    return group_ids, perc

def build_dataframe(group_ids, perc):
    df = pd.DataFrame(perc, columns=["a", "b", "c", "d", "e"])
    labels = [GROUP_LABELS.get(g, str(g)) for g in group_ids]
    df.insert(0, "label", labels)
    return df

def plot_likert_stacked(df, out_path):
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    questions = df["label"].astype(str).tolist()
    vals = df[["a", "b", "c", "d", "e"]].to_numpy(dtype=float)
    row_sums = vals.sum(axis=1)
    correction = 100 - row_sums
    vals[:, -1] += correction

    fig = go.Figure()

    # One trace per Likert category, with text rendered INSIDE the bars
    for i in range(5):
        fig.add_trace(
            go.Bar(
                x=vals[:, i],
                y=questions,
                orientation="h",
                marker=dict(color=COLORS[i]),
                text=np.round(vals[:, i], 1),
                texttemplate="%{text:.1f}%",
                textposition="inside",
                insidetextanchor="middle",
                hoverinfo="skip",
                constraintext="none",
                cliponaxis=False,
            )
        )

    fig.update_layout(
        title="",
        width=1100,
        height=500,
        barmode="stack",
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
        margin=dict(l=180, r=30, t=90, b=60),
        showlegend=False,
        xaxis=dict(
            range=[0, 100],
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            fixedrange=True,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,   # show labels normally (no left annotations needed)
            zeroline=False,
            fixedrange=True,
        ),
#        uniformtext=dict(minsize=10, mode="hide"),  # hide text that won't fit
        uniformtext=dict(minsize=6, mode="show")
    )

    fig.update_xaxes(range=[-1, 100])
    fig.update_yaxes(
        tickfont=dict(
            size=16,        # increase this
            family="Helvetica",
            color="black"
        )
    )
    # Top Likert headers (safe to keep as annotations)
    header_x = np.cumsum(vals[-1, :]) - vals[-1, :] / 2 if len(vals) else np.array([10, 30, 50, 70, 90])
    for i in range(5):
        fig.add_annotation(
            x=float(header_x[i]),
            y=1.12,
            xref="x",
            yref="paper",
            text=LIKERT_LABELS[i],
            showarrow=False,
            font=dict(family="Helvetica", size=14, color="black"),
        )

    fig.write_image(out_path, engine="kaleido", scale=4)


def main():

    db_path = sys.argv[1]
    rows = fetch_rows(db_path)
    group_ids, perc = compute_group_percentages(rows)

    df = build_dataframe(group_ids, perc)


    df = df.iloc[::-1].reset_index(drop=True)

    row_sums = df[["a", "b", "c", "d", "e"]].sum(axis=1)

    plot_likert_stacked(df, out_path="figures/perceived_time_diff.png")



if __name__ == "__main__":
    raise SystemExit(main())
