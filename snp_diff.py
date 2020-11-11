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
#del p_df["No"]
 
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
v_date.rename(columns= {'4. close' : 'close'},inplace = True)
v_date['Ticker'] = 'VOO'
#%% Today's return of all stocks

tickers = set((p_df["Symbol"]).to_list())
tickers.add('VOO')
t_df = pd.DataFrame()
i = 1
for ticker in tickers:
        print("Getting values for {}, {}".format(i, ticker))
        if i == 5:
            time.sleep(60) 
            i = 0
        data, metadata = ts.get_daily(symbol=ticker, outputsize='full')
        data['Ticker'] = ticker
        t_df = t_df.append(data)
        i= i+1

#%%
t_df.rename(columns= {'4. close' : 'close'},inplace = True)
#%%
t_df.reset_index().to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\stock_Values.csv', header=True, index=False)

#%%
t_df = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\stock_Values.csv')

#%%
print(p_df.columns)
p_df = p_df[['Stocks', 'Symbol', 'Quantity','Bought Price','Date']]
p_df.merge[t_df]








