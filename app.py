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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
p_df = pd.DataFrame()


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
        
        ,dcc.Graph(
         id='example-graph1',
        figure=get_figs(p_df)[1]
        )
        ,dcc.Graph(
         id='example-graph2',
         figure=get_figs(p_df)[2]
         )
        ,dcc.Graph(
         id='example-graph3',
         figure=get_figs(p_df)[3]
         )
        ,dcc.Graph(
         id='example-graph',
         figure=get_figs(p_df)[0]
         )
        ])


def get_figs(p_df):
    fig = px.bar(p_df
         ,x = 'Symbol'
         ,y = ['S&P', 'Your Stocks']
         , title='Individual Stock vs Index'
         ,barmode='group'
         )
    fig1 = px.pie(p_df, values='total_val',
                 names='Stocks',
                 hole = 0.8,
                 title='Portfolio Distribution')
    fig3 =px.sunburst(
        p_df,
        path = ['marketcap','Stocks'],
        names='Stocks',
        #parents='marketcap',
        values='total_val'
    )
    fig4 = px.treemap(
        p_df, 
        path=['Stocks'], 
        values='total_val'
        )
    return (fig,fig1,fig3,fig4)

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
    
    
])

if __name__ == '__main__':
    app.run_server(debug=True)