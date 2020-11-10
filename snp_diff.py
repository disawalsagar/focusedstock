# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 21:58:32 2020

@author: sdisawal
"""
#%%
import sys
sys.path.append(r'C:\Users\sdisawal\Desktop\Stocks\Code')
sys.path.append(r'C:\Users\sdisawal\PycharmProjects\LearnApi\alpha_vantage')
#print(sys.path)


#%% Import Statements
import secrets_key as sk
from alpha_vantage.fundamentaldata  import FundamentalData 
from alpha_vantage.timeseries  import TimeSeries 
import pandas as pd
import time
from functools import reduce
import numpy as np

#%% Generate api key
api_key = sk.fmp_api_key()

#%%
fd = FundamentalData(key=api_key, output_format='pandas')
ts = TimeSeries(key=api_key, output_format='pandas')


#%% 
p_df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv', index_col='Symbol')
del p_df["No"]
 
#%%
snp = ts.get_daily('VOO', outputsize='full')

#%%
snp[0].reset_index().to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\snp.csv', header=True, index=False)

#%%
snp = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\snp.csv')
p_df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv')
#%%

dt_fltr = p_df.loc[:,'Date']
v_date = snp[snp['date'].isin(dt_fltr)][['date','4. close']].reset_index(drop=True)







