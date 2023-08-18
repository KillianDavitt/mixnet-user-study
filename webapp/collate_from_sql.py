import sqlite3


def collate(r1,r2,r3,r4,r5):
    r = []
    t1 = r1[7]-r1[6]
    t2 = r2[7]-r2[6]
    t3 = r3[7]-r3[6]
    t4 = r4[7]-r4[6]
    t5 = r5[7]-r5[6]
    #temporarily removed r[9] (automerge data)
    r.append([r1[2], r1[8], r1[3], r1[4], r1[5], t1, r1[10], r1[11], r2[3], r2[4], r2[5], t2, r2[10],r2[11],r3[3],r3[4], r3[5], t3, r3[10], r3[11],r4[3],r4[4], r4[5], t4, r4[10], r4[11],r5[3],r5[4], r5[5], t5, r5[10], r5[11]])
    return r


conn = sqlite3.connect('db.sqlite')
#conn.row_factory = sqlite3.Row
cur = conn.cursor()
row_results = cur.execute("SELECT * FROM response;").fetchall()


result_list = [list(x) for x in row_results]

prolific_results = [x[2] for x in result_list]
prolific_ids = set(prolific_results)

grouped_results = []

# id|created|prolific_id|delay|review|rating|start_time|end_time|education|automerge_data|speed_rating|adapted
for pid in prolific_ids:
    res = [x for x in result_list if x[2]==pid]
    res = sorted(res, key= lambda x: x[3])
    grouped_results.append(collate(res[0],res[1],res[2],res[3],res[4]))


# Print delay with time
dt = [[x[2],x[5],x[8],x[11],x[14],x[17],x[20],x[23],x[26],x[29]] for [x] in grouped_results]
for item in dt:
    print(item)
