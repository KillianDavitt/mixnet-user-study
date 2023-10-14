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
g1 = [(x[5],x[10]) for x in result_list if x[3]==groups[0]]

g2 = [(x[5],x[10]) for x in result_list if x[3]==groups[1]]

g3 = [(x[5],x[10]) for x in result_list if x[3]==groups[2]]

g4 = [(x[5],x[10]) for x in result_list if x[3]==groups[3]]
g5 = [(x[5],x[10]) for x in result_list if x[3]==groups[4]]

groups= [g1,g2,g3,g4,g5]

options = [0,0,0,0,0]

group_options = []

for g in groups:
    new_options = options.copy()
    for x in g:
        new_options[x[0]-1]+=1
    
    group_options.append(new_options)
    

print(group_options)

for x in group_options:
    for i in range(4):
        print(str(x[i]) + ' & ',end='')
    print('\\\\')



delays = ["No Assistance", "1,000", "4,000", "7,000",
              "10,000"]
rating = ["1", "2", "3",
           "4", "5"]

data = np.array(group_options)

"""
fig, ax = plt.subplots()
im = ax.imshow(harvest)

# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(farmers)), labels=farmers)
ax.set_yticks(np.arange(len(vegetables)), labels=vegetables)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(vegetables)):
    for j in range(len(farmers)):
        text = ax.text(j, i, harvest[i, j],
                       ha="center", va="center", color="w")

"""
fig = plt.figure(figsize = (5, 5))
sns.heatmap(data, 
            cmap = 'Greens', 
            fmt=".0f", 
            annot = True , 
            square = True, 
            xticklabels = rating, 
            yticklabels = delays, 
            cbar = False,
            annot_kws={"fontsize":12})
plt.xlabel('Frustration Level')
plt.ylabel('Delay Level (ms)')


"""       
ax.set_xlabel('Frustration Level')
ax.set_ylabel('Delay Level (ms)')
ax.set_title("")
fig.tight_layout()
"""
plt.savefig("frustration.png",dpi=600)
plt.show()

## Time

options = [0,0,0,0,0]
group_options = []
for g in groups:
    new_options = options.copy()
    for x in g:
        new_options[x[1]-1]+=1
    
    group_options.append(new_options)
    
delays = ["No Assistance", "1,000", "4,000", "7,000",
              "10,000"]
rating = ["-2", "-1", "0",
           "1", "2"]

data = np.array(group_options)


"""

fig, ax = plt.subplots()
im = ax.imshow(harvest)

# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(rating)), labels=rating)
ax.set_yticks(np.arange(len(delays)), labels=delays)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(rating)):
    for j in range(len(delays)):
        text = ax.text(j, i, harvest[i, j],
                       ha="center", va="center", color="w")
ax.set_xlabel('Perceived Collaborative Time Assistance')
ax.set_ylabel('Delay Level (ms)')
ax.set_title("")
"""






fig = plt.figure(figsize = (5, 5))
sns.barplot(data, 
            #cmap = 'Blues', 
            #fmt=".0f", 
            #annot = True , 
            #square = True, 
            #xticklabels = rating, 
            #yticklabels = delays, 
            #cbar = False,
            #annot_kws={"fontsize":12}
)
sns.despine(left=True, bottom=True)

plt.yticks(rotation = 90)
plt.xlabel('Perceived Collaborative Time Assistance')
plt.ylabel('Delay Level (ms)')

fig.tight_layout()
plt.savefig("timing.png",dpi=600)
plt.show()
