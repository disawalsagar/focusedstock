# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import base64
import datetime
import io
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
from dash.dependencies import Input, Output, State
from snp_diff import get_df_with_mc
import dash_daq as daq
import dash_bootstrap_components as dbc

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#app = dash.Dash(__name__)
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv',parse_dates=['Date'])
p_df = get_df_with_mc(df)

ohlc_all_tickers_df = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\stock_Values.csv',
                                  parse_dates=['date'])
ohlc_all_tickers_df.rename(columns= {'4. close' : 'close'},inplace = True)

def get_min_max(p_df):
    return (p_df.year.min(), p_df.year.max()) 

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')),parse_dates=['Date'])
            
            p_df = get_df_with_mc(df)
            print(p_df)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr()
        
       
        ])
@app.callback(
    Output(component_id='example-graph2', component_property='figure'),
    Input(component_id='my-slider', component_property='value'))

def get_pie(value=2020):
    p_df['year']= p_df['year'].astype('int64') 
    p_df_1=p_df[p_df['year'] <= value]
    fig = px.pie(p_df_1, values='total_val',
                 names='Stocks',
                 hole = 0.3,
                 title='Portfolio Distribution')
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


            
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

style={
                'width': '25%',
                'borderWidth': '1px',
                'textAlign': 'center',
                'margin': '10px'
            },

app.layout = html.Div([
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
      ,dbc.Container([
          
                  dbc.Row([
                       dbc.Col(dcc.Graph(id='example-graph1',figure=get_figs(p_df)[3]),width=8),
                       dbc.Col([dcc.Graph(id='example-graph2'),daq.Slider(id='my-slider',
                                                                           min=get_min_max(p_df)[0],
                                                                            max=get_min_max(p_df)[1],
                                                                            handleLabel={"showCurrentValue": True,"label": "Year"},
                                                                            value=2020,)],width=4)
                         ],no_gutters=True,style={ "border-style": "hidden"})
       
                    ,dbc.Row([
                        dbc.Col(dcc.Graph(id='example-graph564364',figure=get_figs(p_df)[1])),
                        dbc.Col(dcc.Graph(id='example-graph34344',figure=get_figs(p_df)[2]))
                       ],no_gutters=True,style={ "border-style": "hidden"})
        
                    ,dbc.Row([
                        dbc.Col(dcc.Graph(id='example-graph',figure=get_figs(p_df)[0]),width=6),
                        dbc.Col(dcc.Graph( id='example-graph4',figure=px.line(ohlc_all_tickers_df, x='date', y="1. open",color = 'Ticker')),
                                width=6)
                        ],no_gutters=True,style={ "border-style": "hidden"})
       
         
        ],style={ "border-style": "groove"})
      
      ,dbc.Card(
    [
        dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    style={"width": "18rem"},
)
   
 
         
    
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)