# This script analyses the Likert question for "Perceived time change", i.e. "what effect did the second user have on how long it felt to complete the task"
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math

import sqlite3
import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import matplotlib as mpl
import seaborn as sns

import re
def number_shaver(ch,
                  regx = re.compile('(?<![\d.])0*(?:'
                                    '(\d+)\.?|\.(0)'
                                    '|(\.\d+?)|(\d+\.\d+?)'
                                    ')0*(?![\d.])')  ,
                  repl = lambda mat: mat.group(mat.lastindex)
                                     if mat.lastindex!=3
                                     else '0' + mat.group(3) ):
    return regx.sub(repl,ch)

conn = sqlite3.connect(sys.argv[1])
cur = conn.cursor()
row_results = cur.execute("SELECT * FROM response;").fetchall()


result_list = [list(x) for x in row_results]

groups = set([x[3] for x in result_list])
groups = sorted(groups)
groups.remove(5)
g1 = [(x[5],x[10]) for x in result_list if x[3]==groups[0]]

g2 = [(x[5],x[10]) for x in result_list if x[3]==groups[1]]

g3 = [(x[5],x[10]) for x in result_list if x[3]==groups[2]]

g4 = [(x[5],x[10]) for x in result_list if x[3]==groups[3]]
g5 = [(x[5],x[10]) for x in result_list if x[3]==groups[4]]

groups= [g1,g2,g3,g4,g5]

options = [0,0,0,0,0]

options = [0,0,0,0,0]
group_options = []
for g in groups:
    new_options = options.copy()
    for x in g:
        new_options[x[1]-1]+=1
    
    group_options.append(new_options)
normalised_data = []
print(group_options)
for group in group_options:
    total = sum(group)
    normalised_row = [float(number_shaver(str(round((x/total)*100,1)))) for x in group]
    normalised_data.append(normalised_row)



data = np.array(normalised_data)



# Upload your data as a CSV and load as a DataFrame
df = pd.DataFrame(data, columns = ['a','b','c','d','e'])
#df = df[df.columns[::-1]]
df.insert(0,'label',pd.array(['No Assistance',' 1',  ' 4',' 7',' 10'],dtype=str))
df = df.iloc[::-1]

print(df)
# Check that the rows add up to 100
values = df.iloc[:, 1:6].values.tolist()
print(values)
#for v in values:
#    if not sum(v) == 100:
#        raise ValueError("There is a row that does not add up to 100%.")

# ----------------------------------------------#
# Fill out steps 1-4 to customize your diagram: #
# ----------------------------------------------#

# 1. Set title text 
title = ""

# 2. (Optional) Set width and height
width = 1100
height = 500

# 3. (Optional) Set colors for the...
background_color = "#FFFFFF" # Background
colors = [
   "#de425b",  # Strongly Disagree bars
    "#ea936d",  # Disagree bar
   
    "#fbdbb1",  # "Neutral" bars

    
    "#b2b264",  # "Agree" bars
      "#488f31",  # "Strongly Agree" bars
]

# 4. (Optional) Customize font settings of plot annontations
title_font = dict(family="Helvetica", size=20, color="black")
questions_font = dict(family="Helvetica", size=14, color="black")
likert_scale_font = dict(family="Helvetica", size=14, color="black")
percent_font = dict(family="Helvetica", size=16, color="#434343")

# ------------------------------------------#
# Code to create stacked bar chart begins!  #
# ------------------------------------------#

# Define Likert scale labels with formatting
labels = [
    "<b>Much<br>Slower<b>",
    "<b>Slightly Slower<b>",
    "<b>Neutral<b>",
    "<b>Slightly Quicker<b>",
    "<b>Much<br>Quicker<b>",
]

# Add line breaks to questions after fifth word
questions = []
qs = df.iloc[:,0].tolist()
print(qs)
for q in qs:
    words = q
    #for w in range(1, int(math.ceil((len(words) / 5)))):
    #    words.insert(w * 5, "<br>")
    questions.append(words)

print(questions)
# The following code was taken and modified from:
# https://plotly.com/python/horizontal-bar-charts/#color-palette-for-bar-chart

# Create a Plotly Graph object
fig = go.Figure()

# Create a bar for each question and label with the correct color
for i in range(0, len(values[0])):
    for xd, yd in zip(values, questions):
        fig.add_trace(
            go.Bar(
                x=[xd[i]],
                y=[yd],
                orientation="h",
                marker=dict(color=colors[i]),
            )
        )

# Create a horizontal stacked bar chart
fig.update_layout(
    title=title,
    title_font=title_font,
    width=width, 
    height=height,
    barmode="stack",
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
    margin=dict(l=1, r=180, t=100, b=80),
    showlegend=False,
    hovermode=False,
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        domain=[0.15, 1],
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
    ),
)

# Create and add annotations to plot
annotations = []

for yd, xd in zip(questions, values):
    # Label the y-axis with the questions
    
    annotations.append(
        dict(
            xref="paper",
            yref="y",
            x=0.14,
            y=yd,
            xanchor="right",
            text=str(yd),
            font=questions_font,
            showarrow=False,
            align="right",
        )
    )
    # Label the first percentage of the questions on the x-axis
    annotations.append(
        dict(
            xref="x",
            yref="y",
            x=(xd[0]) / 2,
            y=yd,
            text=str(xd[0]) + "%",
            font=percent_font,
            showarrow=False,
        )
    )
    # Label the first Likert scale on the top
    if yd == questions[-1]:
        annotations.append(
            dict(
                xref="x",
                yref="paper",
                x= (xd[0]) / 2,
                y=1.15,
                text=labels[0],
                font=likert_scale_font,
                showarrow=False,
            )
        )
    space = xd[0]
    for i in range(1, len(xd)):
        # Label the rest of the percentages of the questions on the x-axis
        annotations.append(
            dict(
                xref="x",
                yref="y",
                x=space + (xd[i] / 2),
                y=yd,
                text=str(xd[i]) + "%",
                font=percent_font,
                showarrow=False,
            )
        )
        # Label the rest of the Likert scale on the top
        if yd == questions[-1]:
            annotations.append(
                dict(
                    xref="x",
                    yref="paper",
                    x=space + (xd[i] / 2),
                    y=1.15,
                    text=labels[i],
                    font=likert_scale_font,
                    showarrow=False,
                )
            )
        space += xd[i]
fig.update_layout(annotations=annotations)

# Show figure
fig.write_image('figures/perceived_time_diff.png', scale=10)

