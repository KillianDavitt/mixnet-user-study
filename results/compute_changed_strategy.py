import sqlite3
import sys
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import matplotlib as mpl
import seaborn as sns


conn = sqlite3.connect(sys.argv[1])
cur = conn.cursor()
row_results = cur.execute("SELECT * FROM response;").fetchall()


result_list = [list(x) for x in row_results]

groups = set([x[3] for x in result_list])
groups = sorted(groups)
groups.remove(5)
g1 = [x[11] for x in result_list if x[3]==groups[0]]

g2 = [x[11] for x in result_list if x[3]==groups[1]]

g3 = [x[11] for x in result_list if x[3]==groups[2]]

g4 = [x[11] for x in result_list if x[3]==groups[3]]
g5 = [x[11] for x in result_list if x[3]==groups[4]]

groups= [g1,g2,g3,g4,g5]

options = [0,0]

group_options = []
print(groups[3][59])
for g in groups:
    new_options = options.copy()
    for x in g:
        new_options[x-1]+=1
    new_options.reverse()
    group_options.append(new_options)
    

print(group_options)
for x in group_options:
    for i in range(2):
        print(str(x[i]) + ' & ',end='')
    print('\\\\')



delays = ["No assistance", "1000", "4000", "7000",
              "10,000"]
rating = ["No", "Yes"]

data = np.array(group_options)

fig = plt.figure(figsize = (5, 2))
sns.heatmap(data, 
            cmap = 'Reds', 
            fmt=".0f", 
            annot = True , 
            square = True, 
            xticklabels = rating, 
            yticklabels = delays, 
            cbar = False,
            annot_kws={"fontsize":12})
plt.xlabel('Adapted Actions?')
plt.ylabel('Delay Level (ms)')


"""       
ax.set_xlabel('Frustration Level')
ax.set_ylabel('Delay Level (ms)')
ax.set_title("")
fig.tight_layout()
"""
plt.savefig("strategy.png",dpi=600)
plt.show()

