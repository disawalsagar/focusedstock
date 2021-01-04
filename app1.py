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




app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

p_df=sl.get_snp_list()



app.layout = html.Div([
    dcc.Graph(id='fig_treemap_portfolio',figure=ff.get_fig_treemap_portfolio(p_df), 
                                                         config= {'displayModeBar' : False})
    ,dcc.Graph(id='fig_sunburst_mc',figure=ff.get_fig_sunburst_mc(p_df),
                                                         config= {'displayModeBar' : False})
  
    ])


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)