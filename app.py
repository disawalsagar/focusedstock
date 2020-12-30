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

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        list_of_contents_type, list_of_contents_string = list_of_contents.split(',')
        decoded = base64.b64decode(list_of_contents_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')),parse_dates=['Date'])
        p_df = get_df_with_mc(df)
        return [
    
    
     dbc.Container([
                  dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                 dbc.CardHeader("Portfolio heat map", style={"border-color": "black"}),
                                 dbc.CardBody([dcc.Graph(id='fig_treemap_portfolio',figure=ff.get_fig_treemap_portfolio(p_df), config= {'displayModeBar' : False}, style={"justify":"end"})], style=style1,),
                                  ],color="dark", outline=True),width={"size" :5}, )
                        ,dbc.Col(
                            dbc.Card([
                                 dbc.CardHeader("Market-Cap & Sector wise breakup", style={"border-color": "black"}),
                                 dbc.CardBody([dcc.Graph(id='fig_sunburst_mc',figure=ff.get_fig_sunburst_mc(p_df), config= {'displayModeBar' : False}),], style=style1,),
                                  ], color="dark", outline=True ),width={"size" :5}, )
                       
                         ],no_gutters=False,style= { "border-style": "dash"},justify="center",)
                    
                    ,html.Br()
                                        
                    ,dbc.Row([ 
                          dbc.Col(
                             dbc.Card([
                                 dbc.CardHeader("Individial Stocks vs S&P 500", style={"border-color": "black"}),
                                 dbc.CardBody([dcc.Graph(id='fig_bar_snp_diff',figure=ff.get_fig_bar_snp_diff(p_df), config= {'displayModeBar' : False}),], style=style1,),
                                 ], color="dark", outline=True),width=5,)
                         ,dbc.Col(
                             dbc.Card([
                             dbc.CardHeader("Stocks Distributed in the Portfolio", style={"border-color": "black"}),
                             dbc.CardBody(
                                [dcc.Graph( id='example-graph4345653535',
                                           figure=px.line(ohlc_all_tickers_df, x='date', 
                                                          y="1. open",color = 'Ticker', 
                                                          width=500,line_shape='vhv' ,
                                                         ), config= {'displayModeBar' : False}),], style=style1,),
                             ],color="dark", outline=True),width=5,)
                      ],no_gutters=False,style={ "border-style": "dash"},justify="center",)
         
        ], style={ "border-style": "groove",
                  "width":"auto",
                  "background-color":"white"}, fluid =True)
    
   ]
table_header = [
    html.Thead(html.Tr([ html.Th('Symbol', style={'fontSize':20, 'font-family':'sans-serif'} ),html.Th('Quantity'),html.Th('Bought Price'),html.Th('Date')]))
]                      
sample_row = html.Tr([html.Td("Dis"), html.Td("10"), html.Td("100"), html.Td("2018-08-06")])
table_body = [html.Tbody([sample_row])]
table_caption = [html.Caption("Sample format for the file")]

app.layout = html.Div([
    
    html.Div(
        [
     html.Div(dcc.Markdown('''
                  Welcome! Visualize your portfolio now!
                  Upload your portfolio file using the format described and get started
                  ''' , style={'padding':'5px','height':'auto'}), style={'position': 'relative',
                                                                      'top': '25px', 'height':'auto'})
    ,html.Br()
    
    ,html.Div(id='portfolio file description', children=dbc.Table(table_caption + table_header + table_body , bordered=True,style={
                'width': '95%',
                'height':'10px',
                #'border':'1px solid green',
                #'margin': 'auto',
                #'padding':'2px',
                'table-layout': 'fixed'
            },
        className="table table-sm"
        ), style={'position': 'relative','top': '25px','height':'auto','border':'1px solid red'})
    
    ,html.Br()
    
    ,html.Div(
        dcc.Upload(id='upload-data',children=html.Div(['Drag and Drop or ', html.A('Select your portfolio file')]),style=style2, multiple=False),
       style= {'top': '30px' , 'position': 'relative'})
    ], style={'border':'1px solid blue','float':'left', 'width':'15%', 'height': '700px', 'margin':'5px'})
    
    ,html.Div(id='output-data-upload', style={'border':'1px solid red','float':'right', 'width':'84%','height': 'auto'})
    ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)