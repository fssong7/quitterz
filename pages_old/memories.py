import dash
from dash import dcc,dash_table,html,callback
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
from statCalculator import dataAnalyzer
import plotly.graph_objs as go

dash.register_page(__name__)
forest_calc = dataAnalyzer()
init_df = pd.DataFrame({
    'name': [],
    'depression value': [],
    'reason': []
})

layout = html.Div([
    html.H2("memories",style={'textAlign':'center'}),
    html.Div(style={'padding': '20px'}),
    
    html.Img(src='/assets/squad.jpg', style={'width': '70%', 'height': 'auto','display': 'block', 'margin': '0 auto'}),
    html.Div(style={'padding': '5px'}),
    html.Img(src='/assets/biking.jpg', style={'width': '70%', 'height': 'auto','display': 'block', 'margin': '0 auto'}),
    html.Div(style={'padding': '5px'}),
    html.Img(src='/assets/dawson.jpg', style={'width': '70%', 'height': 'auto','display': 'block', 'margin': '0 auto'}),
    html.Div(style={'padding': '5px'}),
    html.Img(src='/assets/gun.jpg', style={'width': '70%', 'height': 'auto','display': 'block', 'margin': '0 auto'}),
    html.Div(style={'padding': '5px'}),
    html.Img(src='/assets/drunk.jpg', style={'width': '70%', 'height': 'auto','display': 'block', 'margin': '0 auto'}),
    html.Div(style={'padding': '5px'}),
    html.Img(src='/assets/sideeye.jpg', style={'width': '70%', 'height': 'auto','display': 'block', 'margin': '0 auto'}),
    html.Div(style={'padding': '5px'}),
    html.Img(src='/assets/alpha.jpg', style={'width': '70%', 'height': 'auto','display': 'block', 'margin': '0 auto'}),
    html.Div(style={'padding': '5px'}),
    html.Img(src='/assets/waterfall.jpg', style={'width': '70%', 'height': 'auto','display': 'block', 'margin': '0 auto'}),
    html.Div(style={'padding': '5px'}),
    html.Img(src='/assets/mc.jpg', style={'width': '70%', 'height': 'auto','display': 'block', 'margin': '0 auto'}),
    html.Div(style={'padding': '10px'}),

    html.Div('happy times. i feel safe and at ease here. but also scared. im afraid of when it will end. even so, at least ill have these',style={'textAlign':'center'}),
])

