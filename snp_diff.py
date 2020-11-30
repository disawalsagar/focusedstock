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


# Import Statements
import secrets_key as sk
from alpha_vantage.fundamentaldata  import FundamentalData 
from alpha_vantage.timeseries  import TimeSeries 
import pandas as pd
import time
from datetime import datetime, timedelta, date


# Generate api key
api_key = sk.fmp_api_key()

# Data Generation
fd = FundamentalData(key=api_key, output_format='pandas')
ts = TimeSeries(key=api_key, output_format='pandas')

#%%Read portfolio file
portfolio_df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv', 
                           parse_dates=['Date'])
portfolio_df = portfolio_df[['Stocks', 'Symbol', 'Quantity','Bought Price','Date']]
portfolio_df.rename(columns = {'Date': 'bought_date'},inplace = True)
portfolio_df.replace('CGX', value = 'CGC')

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
#portfolio_df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv', index_col='Symbol')

snp = ts.get_daily('VOO', outputsize='full')
snp[0].reset_index().to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\snp.csv', header=True, index=False)

#%% Read the snp file 
snp = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\snp.csv')
#,
                  #parse_dates=['date'])
snp.rename(columns= {'4. close' : 'close'},inplace = True)
snp['date'] = snp.apply(lambda x: (datetime.strptime(x.date, "%Y-%m-%d")), axis = 1)
#portfolio_df  = portfolio_df.apply(lambda row: (datetime.strptime(row['Date'], '%Y-%m-%d').date()), axis = 1)
#portfolio_df.loc[:,'Date'] = pd.to_datetime(portfolio_df['Date']).dt.date
#%% filter the dates from the portfolio
#filter snp df to have only those dates
#dt_fltr = portfolio_df['bought_date']
#voo_df = snp[snp['date'].isin(dt_fltr)][['date','close']].reset_index(drop=True)
#voo_df['Ticker'] = 'VOO'

#%% Read ohlc file of all stocks in portolio
ohlc_all_tickers_df = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\stock_Values.csv',
                                  parse_dates=['date'])
ohlc_all_tickers_df.rename(columns= {'4. close' : 'close'},inplace = True)
#%%Figure out VOO stock price on the day of stock bought date
t_df_VOO = ohlc_all_tickers_df[ohlc_all_tickers_df['Ticker'] == 'VOO'][['Ticker','date','close']]
t_df_VOO.rename(columns = {'close': 'voo_close', 'Ticker': 'voo_Ticker'},inplace = True)
df_merge1 = portfolio_df.merge(t_df_VOO, left_on = ['bought_date'], right_on=['date'], how='left')
df_merge1 = df_merge1.drop('date', axis=1)

#%%
def get_missing_val(row):
    if any((row.isna()) | (row.isnull())):
        row.voo_Ticker = 'VOO'
        b_dt = row.bought_date
        while (ohlc_all_tickers_df[(ohlc_all_tickers_df['date'] == b_dt) & (ohlc_all_tickers_df['Ticker'] == 'VOO')]['close'].empty):
            b_dt = b_dt + timedelta(days=1)
            
        #print(type(b_dt))#bought_date = datetime.strptime(row.bought_date, '%Y-%m-%d').date()
        
# =============================================================================
#         while ~(b_dt in list(ohlc_all_tickers_df['date'].values)):
#             b_dt = b_dt + timedelta(days=1)
#             print(type(b_dt))
# =============================================================================
        row.voo_close = ohlc_all_tickers_df[(ohlc_all_tickers_df['date'] == b_dt) & (ohlc_all_tickers_df['Ticker'] == 'VOO')]['close'].values[0]
    return row

#%% Get missing values where Voo value was missing. 
df_merge1 = df_merge1.apply(lambda row : get_missing_val(row), axis = 1)
#%%
def lat_dts(df):
    df_1 = df.groupby(by=["Ticker"], as_index=False).apply(lambda x: x.sort_values(["date"], ascending = False)).reset_index(drop=True)
    df_srtd = df_1.groupby('Ticker').head(1).reset_index(drop=True)
    return df_srtd
#%%getting the recent price of every stock
ohlc_all_tickers_srtd_df = lat_dts(ohlc_all_tickers_df)[['date', 'close', 'Ticker']]
ohlc_all_tickers_srtd_df.rename(columns = {'date' : 'latest_date', 'close': 'latest_close'},inplace = True)
#%%
#join the table to have bought price, VOO price on the bought date and recent price of stock and VOO in the same table
df_merge = df_merge1.merge(ohlc_all_tickers_srtd_df, left_on = ['Symbol'], right_on=['Ticker'], how='left')
voo_latest_price = ohlc_all_tickers_srtd_df.loc[ohlc_all_tickers_srtd_df['Ticker'] == 'VOO', 'latest_close'].values[0]
df_merge = df_merge.drop('Ticker', axis=1)
df_merge['voo_latest_price'] = voo_latest_price 
#%%
df_merge['total_val'] = df_merge['Bought Price'] * df_merge.Quantity
df_merge['real_voo_qty'] = df_merge['total_val']/df_merge['voo_close']

#%%
#calculating the difference between recent and bough price
df_merge['S&P'] = (df_merge['latest_close'] - df_merge['Bought Price']) * df_merge.Quantity
df_merge['Your Stocks'] = (df_merge['voo_latest_price'] - df_merge['voo_close']) * df_merge['real_voo_qty'] 

#%%
df_merge.to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\final_port.csv', header=True, index=False)

#%%
from plotly.offline import plot
import plotly.figure_factory as ff
#%%
fig = ff.create_table(df_merge)
plot(fig, auto_open=True)
#%%
fig = px.histogram(data_frame=df_merge
     ,x = 'Symbol'
     ,y = ['S&P', 'Your Stocks']
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

#%%
df_qte = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\qte.csv')

#%%
df_qte = df_qte.loc[:,['Symbol','MarketCapitalization']]
df_with_marketcap=df_merge.merge(df_qte, on='Symbol', how='inner')
#%%
fd.get_company_overview(symbol='CGX')








