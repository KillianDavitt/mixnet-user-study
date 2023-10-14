import sqlite3
import sys
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect(sys.argv[1])
cur = conn.cursor()
row_results = cur.execute("SELECT * FROM response;").fetchall()


result_list = [list(x) for x in row_results]

groups = set([x[3] for x in result_list])
groups = sorted(groups)
#groups.remove(5)
g1 = [(x[3],x[4]) for x in result_list if x[3]==groups[0]]

g2 = [(x[3],x[4]) for x in result_list if x[3]==groups[1]]

g3 = [(x[3],x[4]) for x in result_list if x[3]==groups[2]]

g4 = [(x[3],x[4]) for x in result_list if x[3]==groups[3]]
g5 = [(x[3],x[4]) for x in result_list if x[3]==groups[4]]

#print(g1[0:5])


prolific_results = [x[2] for x in result_list]
prolific_ids = set(prolific_results)



grouped_results = []
# id|created|prolific_id|delay|review|rating|start_time|end_time|education|automerge_data|speed_rating|adapted
for pid in prolific_ids:
    res = [x for x in result_list if x[2]==pid]
    #res = sorted(res, key= lambda x: x[3])
    new_item = []
    for i in res:
        new_item.append(i[3])
        new_item.append(i[4])
    try:
        grouped_results.append(new_item)
    except Exception as e:
        print(e)

print('id,d1,r1,d2,r2,d3,r3,d4,r4,d5,r5,d6,r6')

for x,i in enumerate(grouped_results):
    print(str(x) + ', ',end='')
    for j in i[0:-1]:
        if len(str(j))<1:
            print('"nil", ', end='')
        else:
            
            print('"' + str(j).replace(',','').strip() + '", ', end='') 
    print('"' + str(i[-1]).replace(',','').strip() + '"')


