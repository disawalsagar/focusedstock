# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:48:17 2020

@author: sdisawal
"""
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import plotly.figure_factory as ff
import plotly.graph_objects as go
#%%
ohlc_all_tickers_df = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\stock_Values.csv',
                                  parse_dates=['date'])

ohlc_all_tickers_df_2=ohlc_all_tickers_df.loc[ohlc_all_tickers_df.Ticker=='BA']
fig = px.line(ohlc_all_tickers_df_2, x='date', y="1. open")
plot(fig, auto_open=True)
#%%
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

#%%
fig = px.area(ohlc_all_tickers_df, facet_col="Ticker", x='date', y="1. open",color = 'Ticker',facet_col_wrap=2)
plot(fig, auto_open=True)
#%%

fig = go.Figure()
fig.add_trace(go.Scatter(ohlc_all_tickers_df, x='date',y="1. open", fill='tozeroy',
                    mode='none' # override default markers+lines
                    ))
fig.add_trace(go.Scatter(ohlc_all_tickers_df, x='date',y="1. open", fill='tozeroy',
                    mode='none' # override default markers+lines
                    ))

plot(fig, auto_open=True)
#%%
fig = px.line(ohlc_all_tickers_df, x='date', y="1. open",color = 'Ticker')
plot(fig, auto_open=True)
