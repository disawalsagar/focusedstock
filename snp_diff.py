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


#%% Generate api key
api_key = sk.fmp_api_key()

#%% Data Generation
fd = FundamentalData(key=api_key, output_format='pandas')
ts = TimeSeries(key=api_key, output_format='pandas')


#%% 
portfolio_df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv', index_col='Symbol')
#del p_df["No"]
 
#%%
snp = ts.get_daily('VOO', outputsize='full')
snp[0].reset_index().to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\snp.csv', header=True, index=False)

#%%
snp = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\snp.csv')
snp.rename(columns= {'4. close' : 'close'},inplace = True)
portfolio_df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv')
#%%
dt_fltr = portfolio_df['Date']
voo_df = snp[snp['date'].isin(dt_fltr)][['date','close']].reset_index(drop=True)
voo_df['Ticker'] = 'VOO'
#%% Today's return of all stocks

tickers = set((portfolio_df["Symbol"]).to_list())
tickers.add('VOO')
ohlc_all_tickers_df = pd.DataFrame()
i = 1
for ticker in tickers:
        print("Getting values for {}, {}".format(i, ticker))
        if i == 5:
            time.sleep(60) 
            i = 0
        data, metadata = ts.get_daily(symbol=ticker, outputsize='full')
        data['Ticker'] = ticker
        ohlc_all_tickers_df  = ohlc_all_tickers_df .append(data)
        i= i+1

#%%
ohlc_all_tickers_df.reset_index().to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\stock_Values.csv', header=True, index=False)

#%%
ohlc_all_tickers_df = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\stock_Values.csv')
ohlc_all_tickers_df.rename(columns= {'4. close' : 'close'},inplace = True)

#%%
#Figure out VOO stock price on the day of stock bought date
portfolio_df = portfolio_df[['Stocks', 'Symbol', 'Quantity','Bought Price','Date']]
portfolio_df.rename(columns = {'Date': 'bought_date'},inplace = True)
t_df_VOO = ohlc_all_tickers_df[ohlc_all_tickers_df['Ticker'] == 'VOO'][['Ticker','date','close']]
t_df_VOO.rename(columns = {'close': 'voo_close', 'Ticker': 'voo_Ticker'},inplace = True)
df_merge1 = portfolio_df.merge(t_df_VOO, left_on = ['bought_date'], right_on=['date'], how='left')
df_merge1 = df_merge1.drop('date', axis=1)

#%%
def lat_dts(df):
    df_1 = df.groupby(by=["Ticker"], as_index=False).apply(lambda x: x.sort_values(["date"], ascending = False)).reset_index(drop=True)
    df_srtd = df_1.groupby('Ticker').head(1).reset_index(drop=True)
    return df_srtd
#%%
#getting the recent price of every stock
ohlc_all_tickers_srtd_df = lat_dts(ohlc_all_tickers_df)[['date', 'close', 'Ticker']]
ohlc_all_tickers_srtd_df.rename(columns = {'date' : 'latest_date', 'close': 'latest_close'},inplace = True)

#%%
#join the table to have bought price, VOO price on the bought date and recent price of stock and VOO in the same table
df_merge = df_merge1.merge(ohlc_all_tickers_srtd_df, left_on = ['Symbol'], right_on=['Ticker'], how='left')
voo_latest_price = ohlc_all_tickers_srtd_df.loc[ohlc_all_tickers_srtd_df['Ticker'] == 'VOO', 'latest_close'].values[0]
df_merge = df_merge.drop('Ticker', axis=1)
df_merge['voo_latest_price'] = voo_latest_price 
df_merge['total_val'] = df_merge['Bought Price'] * df_merge.Quantity
#%%
#calculating the difference between recent and bough price
df_merge['s_p/l'] = (df_merge['latest_close'] - df_merge['Bought Price']) * df_merge.Quantity
df_merge['v_p/l'] = (df_merge['voo_latest_price'] - df_merge['voo_close'])

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








