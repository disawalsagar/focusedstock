# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from snp_diff import get_df_with_mc
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.io as pio

pio.templates.default = "simple_white"

px.defaults.template = "plotly_white"
px.defaults.color_continuous_scale = px.colors.sequential.Blackbody



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv',parse_dates=['Date'])

p_df = get_df_with_mc(df)

ohlc_all_tickers_df = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\stock_Values.csv',
                                  parse_dates=['date'])
ohlc_all_tickers_df.rename(columns= {'4. close' : 'close'},inplace = True)

def get_min_max(p_df):
    return (p_df.year.min(), p_df.year.max()) 

style1={ "justify":"center","margin-left": "2px",
    "margin-right": "2px"}



def get_figs(p_df):
    fig_bar_snp_diff = px.bar(p_df
         ,x = 'Symbol'
         ,y = ['S&P', 'Your Stocks']
         , title='Individual Stock vs Index'
         ,barmode='group'
         )
    fig_bar_snp_diff.update_layout(
        plot_bgcolor ='#e6ffe6'
        )
    fig_sunburst_mc =px.sunburst(
        p_df,
        path = ['marketcap','Sector','Stocks'],
        names='Stocks',
        values='total_val'
    )
    fig_sunburst_sector =px.sunburst(
        p_df,
        path = ['Sector', 'Stocks'],
        names='Stocks',
        values='total_val'
    )
    fig_treemap_portfolio = px.treemap(
        p_df, 
        path=['Stocks'], 
        values='total_val',
        
        )
    fig_treemap_portfolio.update_layout(
        plot_bgcolor ='red'
        )
    
    return (fig_bar_snp_diff,fig_sunburst_mc,fig_sunburst_sector,fig_treemap_portfolio)
            

app.layout = html.Div([
    
    

      dbc.Container([
              
                  dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                 dbc.CardHeader("Portfolio heat map", style={"border-color": "black"}),
                                 dbc.CardBody([dcc.Graph(id='example-graph1',figure=get_figs(p_df)[3]),]),
                                  ],color="dark", outline=True),width={   "size" :6  },)
                        ,dbc.Col(
                            dbc.Card([
                                 dbc.CardHeader("Market-Cap & Sector wise breakup"),
                                 dbc.CardBody([dcc.Graph(id='example-graph564364',figure=get_figs(p_df)[1]),], style=style1,),
                                  ], color="dark", outline=True ),width={   "size" :6  }, )
                       
                         ],no_gutters=False,style={ "border-style": "dash"})
                    
                    ,html.Br()
                                        
                    ,dbc.Row([ 
                          dbc.Col(
                             dbc.Card([
                                 dbc.CardHeader("Individial Stocks vs S&P 500"),
                                 dbc.CardBody([dcc.Graph(id='example-graph',figure=get_figs(p_df)[0]),]),
                                 ], color="dark", outline=True),width=5,)
                         ,dbc.Col(
                             dbc.Card([
                             dbc.CardHeader("Stocks Distributed in the Portfolio"),
                             dbc.CardBody(
                                [dcc.Graph( id='example-graph4345653535',
                                           figure=px.line(ohlc_all_tickers_df, x='date', 
                                                          y="1. open",color = 'Ticker', 
                                                          width=400,height=300,line_shape='vhv' ,
                                                         )),], style=style1,),
                             ],color="dark", outline=True),width=5,)
                      ],no_gutters=False,style={ "border-style": "dash"})
         
        ],style={ "border-style": "groove", "width":"99%","background-color":"white"}, fluid =True)
    
   
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)