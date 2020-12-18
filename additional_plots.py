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
#%%
html.Div(
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        ),
    
    html.Div(id='output-data-upload')
    
        ,dcc.Graph(
         id='example-graph1',
        figure=get_figs(p_df)[3]
        )
        ,dcc.Graph(
         id='example-graph2'
         )
       ,daq.Slider(
            id='my-slider',
            min=get_min_max(p_df)[0],
            max=get_min_max(p_df)[1],
            handleLabel={"showCurrentValue": True,"label": "Year"},
            value=2020,
        )
        ,html.Div(id='slider-output-container')
        ,html.Div(
        [dcc.Graph(
         id='example-graph3',
         figure=get_figs(p_df)[2]
         )
        ,dcc.Graph(
         id='example-graph67',
         figure=get_figs(p_df)[1]
         )
        ])
        ,html.Div([
        dbc.Row(
            [
            dbc.Col(dcc.Graph(id='example-graph564364',figure=get_figs(p_df)[1]),width=6),
            dbc.Col(dcc.Graph(id='example-graph34344',figure=get_figs(p_df)[2]),width=6)
           ] 
        )
        ])
        ,dcc.Graph(
         id='example-graph',
         figure=get_figs(p_df)[0]
         )
        ,dcc.Graph(
         id='example-graph4',
         figure=px.line(ohlc_all_tickers_df, x='date', y="1. open",color = 'Ticker')
         ),
        
   
     html.Div(
    [dbc.Row(dbc.Col(html.Div("A single column"))),
        dbc.Row([dbc.Col(html.Div("One of three columns"),width=True),
                dbc.Col(html.Div("One of three columns"),width=True),
                dbc.Col(html.Div("One of three columns"),width=True)]),
        ],
    )
     
     , dbc.Card(
        dbc.CardBody([
            dbc.Row([dbc.Col(html.Div("One of tsadkjbfsadhe columns"),width=4),
                dbc.Col(html.Div("One of three columns"),width=True),
                dbc.Col(html.Div("One of three columns"),width=True)], align='center'),
            ])
        )

        