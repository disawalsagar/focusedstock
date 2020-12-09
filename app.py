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
import snp_diff as sf


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\final_port.csv')

fig = px.histogram(df
     ,x = 'Symbol'
     ,y = ['S&P', 'Your Stocks']
     , title='Individual Stock vs Index'
     )
fig1 = px.pie(df, values='total_val',
             names='Stocks',
             hole = 0.8,
             title='Portfolio Distribution')
fig3 =px.sunburst(
    df,
    path = ['marketcap','Stocks'],
    names='Stocks',
    #parents='marketcap',
    values='total_val'
)
fig4 = px.treemap(
    df, 
    path=['Stocks'], 
    values='total_val'
    )
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
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

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])
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
    
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
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
         html.Div(id='output-data-upload'),
    
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
    ,dcc.Graph(
        id='example-graph1',
        figure=fig1
    )
    ,dcc.Graph(
        id='example-graph2',
        figure=fig3
    )
    ,dcc.Graph(
        id='example-graph3',
        figure=fig4
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)