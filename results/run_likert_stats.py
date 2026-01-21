#!/usr/bin/env python
# coding: utf-8

import sys
import sqlite3
import pandas as pd
from pingouin import pairwise_gameshowell
pd.options.display.float_format = '{:.3f}'.format


con = sqlite3.connect(sys.argv[1])
cur = con.cursor()
res = cur.execute("SELECT rating,speed_rating,adapted,delay FROM response where delay !=5;")
r = res.fetchall()
df = pd.DataFrame(r)


df = df.rename(columns={0: 'rating', 1: 'speed_rating', 2: 'adapted', 3: 'delay'}) 
df['delay'] = df['delay']/1000

print("\nUser frustration rating depending on delay:")

x =pairwise_gameshowell(data=df, dv='rating', between='delay').round(3)
x=x[0:4]
print(x[['A','B','diff','pval','hedges']].map(lambda x: ('%f' % x).rstrip('0').rstrip('.')).to_latex(index=False))

print("\nUser speed rating depending on delay:")
x = pairwise_gameshowell(data=df, dv='speed_rating', between='delay').round(3)
x=x[0:4]
print(x[['A','B','diff','pval','hedges']].map(lambda x: ('%f' % x).rstrip('0').rstrip('.')).to_latex(index=False))

