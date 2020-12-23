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


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv',parse_dates=['Date'])

p_df = get_df_with_mc(df)

ohlc_all_tickers_df = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\stock_Values.csv',
                                  parse_dates=['date'])
ohlc_all_tickers_df.rename(columns= {'4. close' : 'close'},inplace = True)

def get_min_max(p_df):
    return (p_df.year.min(), p_df.year.max()) 


@app.callback(
    Output(component_id='example-graph2', component_property='figure'),
    Input(component_id='my-slider', component_property='value'))

def get_pie(value=2020):
    p_df['year']= p_df['year'].astype('int64') 
    p_df_1=p_df[p_df['year'] <= value]
    fig = px.pie(p_df_1, values='total_val',
                 names='Stocks',
                 hole = 0.3,
                 title='Portfolio Distribution', template="plotly_dark")
    return fig

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
        path = ['marketcap','Stocks'],
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
        values='total_val'
        
        )
    fig_treemap_portfolio.update_layout(
        plot_bgcolor ='red'
        )
    
    return (fig_bar_snp_diff,fig_sunburst_mc,fig_sunburst_sector,fig_treemap_portfolio)
            

app.layout = html.Div([

      dbc.Container([
          
                  dbc.Row([
                       dbc.Col(dcc.Graph(id='example-graph1',figure=get_figs(p_df)[3]),width=8),
                       dbc.Col([dcc.Graph(id='example-graph2'),daq.Slider(id='my-slider',
                                                                           min=get_min_max(p_df)[0],
                                                                            max=get_min_max(p_df)[1],
                                                                            handleLabel={"showCurrentValue": True,"label": "Year"},
                                                                            value=2020,)],width=4)
                         ],no_gutters=False,style={ "border-style": "hidden"})
       
                    ,dbc.Row([
                        dbc.Col(dcc.Graph(id='example-graph564364',figure=get_figs(p_df)[1])),
                        dbc.Col(dcc.Graph(id='example-graph34344',figure=get_figs(p_df)[2]))
                       ],no_gutters=True,style={ "border-style": "hidden"})
        
                    ,dbc.Row([
                        dbc.Col(dcc.Graph(id='example-graph',figure=get_figs(p_df)[0]),width=6),
                        dbc.Col(dcc.Graph( id='example-graph4',figure=px.line(ohlc_all_tickers_df, x='date', y="1. open",color = 'Ticker')),
                                width=6)
                        ],no_gutters=False,style={ "border-style": "hidden"})
                    ,html.Br()
                      ,dbc.Row([ 
                          dbc.Col(
                             dbc.Card([
                                 dbc.CardBody(
                                    [
                                         html.H5("Stocks Distributed in the Portfolio", className="card-title")
                                        ,dcc.Graph( id='example-graph4345634343453453535',figure=px.line(ohlc_all_tickers_df, x='date', y="1. open",color = 'Ticker')),
                                        
                                    ]),
                                 ],outline=True)
                             ,width=6)
                         ,dbc.Col(
                             dbc.Card([
                             dbc.CardHeader("Stocks Distributed in the Portfolio"),
                             dbc.CardBody(
                                [
                                    dcc.Graph( id='example-graph4345653535',figure=px.line(ohlc_all_tickers_df, x='date', y="1. open",color = 'Ticker', template="plotly_dark")),
                                    
                                ]),
                             ], color="secondary", inverse=True)
                              ,width=6)
                      ],no_gutters=False,style={ "border-style": "dash"})
         
        ],style={ "border-style": "groove", "width":"99%","background-color":"#d5e6ca"}, fluid =True)
    
   
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)