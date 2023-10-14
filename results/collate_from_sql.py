import sqlite3
import sys

def collate(r1,r2,r3,r4,r5,r6):
    r = []
    t1 = r1[7]-r1[6]
    t2 = r2[7]-r2[6]
    t3 = r3[7]-r3[6]
    t4 = r4[7]-r4[6]
    t5 = r5[7]-r5[6]
    t6 = r6[7]-r6[6]
     #temporarily removed r[9] (automerge data)
    r.append([r1[2], r1[8], r1[3], r1[4], r1[5], t1, r1[10], r1[11], r2[3], r2[4], r2[5], t2, r2[10],r2[11],r3[3],r3[4], r3[5], t3, r3[10], r3[11],r4[3],r4[4], r4[5], t4, r4[10], r4[11],r5[3],r5[4], r5[5], t5, r5[10], r5[11], r6[3],r6[4],r6[5],t6,r6[10],r6[11],r6[12]])
    return r


def listify(l):
    l = l.replace('[','')
    l = l.replace(']','')
    return l.split(',')

def qualify(d):
    delays = [int(x) for x in d]
    if len(set(delays))<3:
        return

conn = sqlite3.connect(sys.argv[3])
cur = conn.cursor()
row_results = cur.execute("SELECT * FROM response where prolific_id!='60cc44df7ace0035ac0d133b';").fetchall()

delays = [0,5,4000,7000,10000]
result_list = [list(x) for x in row_results]


# find broken rows where we dont have 6 completed delays
#broken_list = [x for x in result_list if len(listify(x[14]))<6]
#result_list = [x for x in result_list if len(listify(x[14]))==6]


#broken_prolific_ids = set([x[2] for x in broken_list])
#print(broken_prolific_ids)

# find broken rows where the delays aren't unique
#nonunique_delays = [x for x in result_list if len(set(listify(x[14])))!=6]
#print(len(nonunique_delays))

#print(len(set(listify(result_list[4][14]))))



#bad_ids = ['5eebc01d1b53c11438f3405b','645eb0f76e08c281f4b9d895','5fb7df07d137543e4ca86861','642d521dfa462780d6ef7fc5','5c5df0475b87820001c4f21c']


bad_ids = ['60cc44df7ace0035ac0d133b',
'5eebc01d1b53c11438f3405b',
'63039add5b36e081a5387f95',
'5ceac2dd06aa230001363420',
'645eb0f76e08c281f4b9d895',
'5e4db49d96e3c32079f64790',
'5fb7df07d137543e4ca86861',
'641360353f433383779b3dbc',
'642d521dfa462780d6ef7fc5',
'6229e1544f1fe9d69b8d1272',
'5c5df0475b87820001c4f21c']

#result_list = [x for x in result_list if x[2] not in bad_ids]

prolific_results = [x[2] for x in result_list]
prolific_ids = set(prolific_results)



grouped_results = []
# id|created|prolific_id|delay|review|rating|start_time|end_time|education|automerge_data|speed_rating|adapted
for pid in prolific_ids:
    res = [x for x in result_list if x[2]==pid]
    res = sorted(res, key= lambda x: x[3])
    try:
        grouped_results.append(collate(res[0],res[1],res[2],res[3],res[4], res[5]))
    except Exception as e:
        print(e)


print(len(grouped_results))
# Print delay with time
dt = [[x[2],x[5],x[8],x[11],x[14],x[17],x[20],x[23],x[26],x[29],x[32],x[35]] for [x] in grouped_results]

if sys.argv[1]=='p':
    for item in dt:
        print(item)

from scipy import stats


#group1 = [x[7]-x[6] for x in result_list if x[3]==250]
groups = set([x[3] for x in result_list])
groups = sorted(groups)
groups.remove(5)
#groups.remove(250)
group1 = [x[7]-x[6] for x in result_list if x[3]==groups[0]]

group2 = [x[7]-x[6] for x in result_list if x[3]==groups[1]]

group3 = [x[7]-x[6] for x in result_list if x[3]==groups[2]]

group4 = [x[7]-x[6] for x in result_list if x[3]==groups[3]]
group5 = [x[7]-x[6] for x in result_list if x[3]==groups[4]]

#perform Friedman Test
x = stats.friedmanchisquare(group1, group2, group3,  group4)
print(x)

g1 = []
g2=[]
g3=[]
g4=[]
g5 = []
for i,x in enumerate(group1):
    g1.append([i,int(x),(groups[0])])

for i,x in enumerate(group2):
    g2.append([i,int(x),(groups[1])])
for i,x in enumerate(group3):
    g3.append([i,int(x),(groups[2])])


for i,x in enumerate(group4):
    g4.append([i,int(x),groups[3]])


for i,x in enumerate(group5):
    g5.append([i,int(x),groups[4]])


test_data = g1+g2+g3+g4+g5

import numpy as np
import pandas as pd
import numpy_indexed as npi
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.libqsturng import qsturng, psturng
from hypothetical.descriptive import var

from itertools import combinations
#print(test_data[:3])

x = pd.DataFrame(test_data)
test_data = x.to_numpy()
#test_data = np.array(test_data)
print(test_data[:3])
#print(list(np.unique(test_data[:,2])))

#plt.figure(figsize=(8, 4))

box = sns.boxplot(x=test_data[:,2], y=test_data[:,1], hue=test_data[:,2], palette="Set3")
plt.yscale('log')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.tight_layout()
plt.savefig('boxplot.png')
plt.show()
sprays = test_data
alpha = 0.05
k = len(np.unique(sprays[:,2]))

group_means = dict(npi.group_by(sprays[:, 2], sprays[:, 1], np.mean))
group_obs = dict(npi.group_by(sprays[:, 2], sprays[:, 1], len))
group_variance = dict(npi.group_by(sprays[:, 2], sprays[:, 1], var))

combs = list(combinations(np.unique(sprays[:, 2]), 2))

list_of_delays = sorted(np.unique(sprays[:, 2]))
combs = []
for i in range(len(list_of_delays)-1):
    z_com = (list_of_delays[0],list_of_delays[i+1])
    combs.append(z_com)

"""for i in range(len(list_of_delays)-2):
    n_com = (list_of_delays[i+1],list_of_delays[i+2])
    combs.append(n_com)
"""

print(combs)

group_comps = []
mean_differences = []
degrees_freedom = []
t_values = []
p_values = []
std_err = []
up_conf = []
low_conf = []

for comb in combs:
    # Mean differences of each group combination
    diff = group_means[comb[1]] - group_means[comb[0]]
    
    # t-value of each group combination
    t_val = np.abs(diff) / np.sqrt((group_variance[comb[0]] / group_obs[comb[0]]) + 
                                   (group_variance[comb[1]] / group_obs[comb[1]]))
    
    # Numerator of the Welch-Satterthwaite equation
    df_num = (group_variance[comb[0]] / group_obs[comb[0]] + group_variance[comb[1]] / group_obs[comb[1]]) ** 2
    
    # Denominator of the Welch-Satterthwaite equation
    df_denom = ((group_variance[comb[0]] / group_obs[comb[0]]) ** 2 / (group_obs[comb[0]] - 1) +
                (group_variance[comb[1]] / group_obs[comb[1]]) ** 2 / (group_obs[comb[1]] - 1))
    
    # Degrees of freedom
    df = df_num / df_denom
    
    # p-value of the group comparison
    p_val = psturng(t_val * np.sqrt(2), k, df)

    # Standard error of each group combination
    se = np.sqrt(0.5 * (group_variance[comb[0]] / group_obs[comb[0]] + 
                        group_variance[comb[1]] / group_obs[comb[1]]))
    
    # Upper and lower confidence intervals
    upper_conf = diff + qsturng(1 - alpha, k, df)
    lower_conf = diff - qsturng(1 - alpha, k, df)
    
    # Append the computed values to their respective lists.
    mean_differences.append(diff)
    degrees_freedom.append(df)
    t_values.append(t_val)
    p_values.append(p_val)
    std_err.append(se)
    up_conf.append(upper_conf)
    low_conf.append(lower_conf)
    group_comps.append(str(comb[0]) + ' : ' + str(comb[1]))


result_df = pd.DataFrame({'groups': group_comps,
                          'mean_difference': mean_differences,
                          'std_error': std_err,
                          't_value': t_values,
                          'p_value': p_values})
                          #'upper_limit': up_conf,
                          #'lower limit': low_conf})

print(result_df)


#from scipy.stats import tukey_hsd

#tukey_hsd(g1,g2)
import math
def cohend(d1, d2):
   # calculate the size of samples
   n1, n2 = len(d1), len(d2)
   # calculate the variance of the samples
   s1, s2 = np.var(d1, ddof=1), np.var(d2, ddof=1)
   # calculate the pooled standard deviation
   s = math.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
   # calculate the means of the samples
   u1, u2 = np.mean(d1), np.mean(d2)
   # calculate the effect size
   return (u1 - u2) / s

t1 = [x[1] for x in g1]
t2 = [x[1] for x in g2]
t3 = [x[1] for x in g3]
t4 = [x[1] for x in g4]

plt.hist(t1)
plt.savefig("dist.png")
groups = [g1,g2,g3,g4,g5]
print('')
for i,x in enumerate(groups):
    print(str(groups[0][3][2]) + " " +str(x[3][2]) + ': ', end='')    
    print(cohend([w[1] for w in groups[0]],[v[1] for v in x]))

print(group_means)
plt_combs = [x[1] for x in combs]
plt_means = [abs(x) for x in mean_differences]
plt.figure(2)
plt.plot(plt_combs,plt_means)
plt.ylabel("time advantage over lone user")
plt.xlabel("delay")
plt.ylim(ymin=0)
plt.savefig("mean_difference.png",dpi=300)
plt.show()

