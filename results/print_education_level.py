import sqlite3
import sys

conn = sqlite3.connect(sys.argv[1])
cur = conn.cursor()
row_results = cur.execute("SELECT * FROM response;").fetchall()


result_list = [list(x) for x in row_results]

groups = set([x[3] for x in result_list])

groups = sorted(groups)
groups.remove(5)
group1 = [x[8] for x in result_list if x[3]==groups[0] and x[8]!=None]
print(group1)
levels = sorted(set(group1))

lookup = dict({"1":"None", "2":"A levels, gsce", "3":"BA", "4":"postgrad"})
for l in levels:
    print(lookup[l] + ': ', end='')
    print(len([x for x in group1 if x==l]))
