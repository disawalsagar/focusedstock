# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 19:36:05 2020

@author: sdisawal
"""

import plotly.express as px



px.defaults.template = "ggplot2"
px.defaults.color_continuous_scale = px.colors.sequential.Blackbody
#px.defaults.width = 500
#px.defaults.height = 275
px.colors.sequential

margin1 = dict( l=1,r=1, b=10,t=1,pad=1)

def get_fig_bar_snp_diff(p_df, sp=True):
    if sp:
        fig_bar_snp_diff = px.bar(p_df
             ,x = 'Symbol'
             ,y = ['S&P', 'Your Stocks']
             , title='Individual Stock vs Index'
             ,barmode='group'
             )
    else: 
        fig_bar_snp_diff = px.bar(p_df
             ,x = 'Symbol'
             ,y = ['S&P', 'Your Stocks']
             , title='Individual Stock vs Index'
             ,barmode='group'
             )
    fig_bar_snp_diff.update_layout(
       # plot_bgcolor ='#e6ffe6',
         margin=margin1
        )
    return fig_bar_snp_diff
    
def get_fig_sunburst_mc(p_df, sp=True):
    
    if sp:
         fig_sunburst_mc = px.sunburst(
            p_df,
            path = ['Sector','Symbol'],
            names='Symbol',
           # values='Market Cap'
        )
    else:    
        fig_sunburst_mc = px.sunburst(
                p_df,
                path = ['marketcap','Sector','Stocks'],
                names='Stocks',
                values='total_val'
            )
    fig_sunburst_mc.update_layout(
            margin=margin1
        )
    return fig_sunburst_mc

def get_fig_treemap_portfolio(p_df, sp=True):
    
    if sp:
        fig_treemap_portfolio = px.treemap(
            p_df, 
            path=['marketcap','Symbol'],
            color='Market Cap',
            color_continuous_scale=px.colors.sequential.Plotly3,
           # values='Market Cap',
           height=750
           ,hover_name='Name'
          ,hover_data={'Market Cap':'Market Cap'}
                       
            )
        fig_treemap_portfolio.data[0].hovertemplate = 'Name=%{Name}<br>%{id}'
    else:
        fig_treemap_portfolio = px.treemap(
            p_df, 
            path=['Stocks'], 
            values='total_val',
            )
    
    fig_treemap_portfolio.update_layout(
        margin=margin1
    )
        
    return  fig_treemap_portfolio
            