# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from snp_diff import get_df_with_mc
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.io as pio
import fig_factory as ff
import base64
import io
import snp_list as sl

pio.templates.default = "simple_white"

px.defaults.template = "ggplot2"
px.defaults.color_continuous_scale = px.colors.sequential.Blackbody
px.defaults.width = 500
px.defaults.height = 275



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv',parse_dates=['Date'])

#p_df = get_df_with_mc(df)

ohlc_all_tickers_df = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\stock_Values.csv',
                                  parse_dates=['date'])
ohlc_all_tickers_df.rename(columns= {'4. close' : 'close'},inplace = True)

def get_min_max(p_df):
    return (p_df.year.min(), p_df.year.max()) 


style2= {       'top':'50%',
                'width': '75%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': 'auto',
                'justify':'center',
                'align-content': 'center'
            }
style3= {
                'width': '25%',
                'margin': 'auto',
            }
style1={ 
       # "margin-left": "auto",
    #"margin-right": "auto", 
    "margin":"auto","height":300, "justify-content": "center"}

p_df=sl.get_snp_list()

table_header = [
    html.Thead(html.Tr([ html.Th('Symbol' ),html.Th('Quantity'),html.Th('Bought Price'),html.Th('Date')]))
]                      
sample_row = html.Tr([html.Td("Dis"), html.Td("10"), html.Td("100"), html.Td("2018-08-06")])
table_body = [html.Tbody([sample_row])]
table_caption = [html.Caption("Sample format for the file")]

app.layout = html.Div([
    dbc.Container([
                  dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                 dbc.CardHeader("Portfolio heat map", style={"border-color": "black"}),
                                 dbc.CardBody([dcc.Graph(id='fig_treemap_portfolio',figure=ff.get_fig_treemap_portfolio(p_df), config= {'displayModeBar' : False}, style={"justify":"end"})], style=style1,),
                                  ],color="dark", outline=True),
                            #width={"size" :5}, 
                            )
                        ,dbc.Col(
                            dbc.Card([
                                 dbc.CardHeader("Market-Cap & Sector wise breakup", style={"border-color": "black"}),
                                 dbc.CardBody([dcc.Graph(id='fig_sunburst_mc',figure=ff.get_fig_sunburst_mc(p_df), config= {'displayModeBar' : False}),], style=style1,),
                                  ], color="dark", outline=True ),
                            #width={"size" :5}, 
                            )
                       
                         ],no_gutters=False,style= { "border-style": "dash"},justify="center",)
                    
                    ,html.Br()
                                        
                    ,dbc.Row([ 
                          dbc.Col(
                             dbc.Card([
                                 dbc.CardHeader("Individial Stocks vs S&P 500", style={"border-color": "black"}),
                                 dbc.CardBody([dcc.Graph(id='fig_bar_snp_diff',figure=ff.get_fig_bar_snp_diff(p_df), config= {'displayModeBar' : False}),], style=style1,),
                                 ], color="dark", outline=True),
                             #width=5,
                             )
                         ,dbc.Col(
                             dbc.Card([
                             dbc.CardHeader("Stocks Distributed in the Portfolio", style={"border-color": "black"}),
                             dbc.CardBody(
                                [dcc.Graph( id='example-graph4345653535',
                                           figure=px.line(ohlc_all_tickers_df, x='date', 
                                                          y="1. open",color = 'Ticker', 
                                                          width=500,line_shape='vhv' ,
                                                         ), config= {'displayModeBar' : False}),], style=style1,),
                             ],color="dark", outline=True),
                             #width=5,
                             )
                      ],no_gutters=False,style={ "border-style": "dash"},justify="center",)
         
        ], style={ "border-style": "hidden",
                  "width":"auto",
                  "background-color":"white"}, fluid =True)
    ])


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)