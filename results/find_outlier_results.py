import sqlite3
import sys
from scipy import stats
import numpy as np


conn = sqlite3.connect(sys.argv[1])
cur = conn.cursor()
row_results = cur.execute("SELECT * FROM response;").fetchall()

result_list = [list(x) for x in row_results]

all_ids = set([x[2] for x in result_list if x[3]!=5])

results_by_id = []

for p in all_ids:
    result = [x for x in result_list if x[2]==p]
    results_by_id.append(result)


cols = 0 
    
for r in results_by_id:
    times = [x[7]-x[6] for x in r]
    z = stats.zscore(times)
    if any(x > 2.1 for x in z):
        #print(r[0][2])
        print(times)
        print(z)
        cols +=1
print(cols)
