#%%
import sys
sys.path.append(r'C:\Users\sdisawal\Desktop\Stocks\Code')
sys.path.append(r'C:\Users\sdisawal\PycharmProjects\LearnApi\alpha_vantage')
import secrets_key as sk
from alpha_vantage.fundamentaldata  import FundamentalData 
from alpha_vantage.timeseries  import TimeSeries 
import pandas as pd
import time
import snp_list as sl
#%%Read portfolio file
portfolio_df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv', 
                           parse_dates=['Date'])
portfolio_df = portfolio_df[['Stocks', 'Symbol', 'Quantity','Bought Price','Date']]
portfolio_df.rename(columns = {'Date': 'bought_date'},inplace = True)


#%% Generate api key
api_key = sk.fmp_api_key()

#%% Data Generation
fd = FundamentalData(key=api_key, output_format='pandas')
ts = TimeSeries(key=api_key, output_format='pandas')

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
tickers = set((portfolio_df["Symbol"]).to_list())
ohlc_all_tickers_df.reset_index().to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\stock_Values.csv', header=True, index=False)
#%%
portfolio_df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv', 
                           parse_dates=['Date'])
portfolio_df = portfolio_df[['Stocks', 'Symbol', 'Quantity','Bought Price','Date']]
portfolio_df.rename(columns = {'Date': 'bought_date'},inplace = True)
portfolio_df.replace(to_replace='CGX', value='CGC', inplace=True)

#%%
snp_list =sl.get_snp_list()
tickers = set((snp_list["Symbol"]).to_list())
ohlc_all_tickers_df=pd.DataFrame()
i = 1
for ticker in tickers:
        print("Getting values for {}, {}".format(i, ticker))
        if i == 5:
            time.sleep(60) 
            i = 0
        data, metadata = ts.get_daily(symbol=ticker, outputsize='full')
        data['Ticker'] = ticker
        ohlc_all_tickers_df  = ohlc_all_tickers_df.append(data)
        i= i+1