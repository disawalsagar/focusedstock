# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 21:58:32 2020

@author: sdisawal
"""
#%%
import sys
sys.path.append(r'C:\Users\sdisawal\Desktop\Stocks\Code')
sys.path.append(r'C:\Users\sdisawal\PycharmProjects\LearnApi\alpha_vantage')
import plotly.express as px
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
t_df = t_df.rename(columns= {'4. close' : 'close'}).reset_index(drop=True)

#%%
#print(p_df.columns)
p_df = p_df[['Stocks', 'Symbol', 'Quantity','Bought Price','Date']]
p_df = p_df.rename(columns = {'Date': 'org_date'})
t_df_VOO = t_df[t_df['Ticker'] == 'VOO'][['Ticker','date','close']]
t_df_VOO = t_df_VOO.rename(columns = {'close': 'voo_close', 'Ticker': 'voo_Ticker'})
df_merge1 = p_df.merge(t_df_VOO, left_on = ['org_date'], right_on=['date'], how='left')
#df_merge1.rename(columns= {'Date' : 'Date_stock', },inplace = True)
df_merge1 = df_merge1.drop('date', axis=1)

#%%
def lat_dts(df):
    df_1 = df.groupby(by=["Ticker"], as_index=False).apply(lambda x: x.sort_values(["date"], ascending = False)).reset_index(drop=True)
    df_srtd = df_1.groupby('Ticker').head(1).reset_index(drop=True)
    return df_srtd
#%%
t_df_srtd = lat_dts(t_df)[['date', 'close', 'Ticker']]
t_df_srtd = t_df_srtd.rename(columns = {'date' : 'latest_date', 'close': 'latest_close'}).reset_index(drop=True)

#%%
df_merge = df_merge1.merge(t_df_srtd, left_on = ['Symbol'], right_on=['Ticker'], how='left')
voo_latest_price = t_df_srtd.loc[t_df_srtd['Ticker'] == 'VOO', 'latest_close'].values[0]
df_merge = df_merge.drop('Ticker', axis=1)
df_merge['voo_latest_price'] = voo_latest_price 
df_merge['s_p/l'] = (df_merge['latest_close'] - df_merge['Bought Price']) * df_merge.Quantity
df_merge['v_p/l'] = (df_merge['voo_latest_price'] - df_merge['voo_close'])
df_merge['total_val'] = df_merge['Bought Price'] * df_merge.Quantity
#%%
df_merge.to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\final_port.csv', header=True, index=False)



#%%
from plotly.offline import plot
import plotly.figure_factory as ff
#%%
fig = ff.create_table(df_merge)
#%%
fig = px.histogram(data_frame=df_merge
     ,x = 'Symbol'
     ,y = ['s_p/l', 'v_p/l']
     , title="Individual Stock vs Index"
     , template='plotly'
     )
plot(fig, auto_open=True)

#%%
fig = px.histogram(data_frame=df_merge
     ,x = 'Symbol'
     ,y = ['s_p/l', 'v_p/l']
     , title="Individual Stock vs Index"
     , template='plotly'
     )
plot(fig, auto_open=True)

#%%
fig = px.pie(df_merge, values='total_val',
             names='Stocks',
             hole = 0.8,
             title='Portfolio Distribution')
plot(fig, auto_open=True)








