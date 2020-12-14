# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 14:25:52 2020

@author: sdisawal
"""

import sys
sys.path.append(r'C:\Users\sdisawal\python_projects\focusedstock')
import pandas as pd
from snp_diff import get_df_with_mc 

#%%

df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv',parse_dates=['Date'])
p_df = get_df_with_mc(df)

#%%
p_df['year']= p_df['bought_date'].dt.year
#%%
p_df.sort_values(by=['bought_date'], inplace=True)
p_df['cumsum'] = p_df.total_val.cumsum()
#p_df_g = p_df_g.groupby('year').cumsum()



