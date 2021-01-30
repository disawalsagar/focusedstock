# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import dash_bootstrap_components as dbc
import plotly.io as pio
import fig_factory as ff

import snp_list as sl

pio.templates.default = "simple_white"

px.defaults.template = "ggplot2"
px.defaults.color_continuous_scale = px.colors.sequential.Blackbody




app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

p_df=sl.get_prepare_index_data()

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return dcc.Graph(id='fig_treemap_portfolio',figure=ff.get_fig_treemap_portfolio(p_df),config= {'displayModeBar' : False})


app.layout = html.Div([
    html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'S&P 500', 'value': 'SNP'},
            {'label': 'Russell 1000', 'value': 'MTL'},
            {'label': 'Dow Jon Industrial Average', 'value': 'SF'}
        ],
        value='SNP'
    ),
    
], style={'width':'40%','margin':'auto'}),
    html.Br()
    ,html.Div(id='dd-output-container', style={'width':'95%','margin':'auto','height': '900px'}
    )
    ,dcc.Graph(id='fig_sunburst_mc', figure=ff.get_fig_sunburst_mc(p_df),
                                                         config= {'displayModeBar' : False})
  
    ])


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)