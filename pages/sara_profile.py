import dash
from dash import dcc,dash_table,html,callback
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
from scipy import stats
import dash_bootstrap_components as dbc
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoDB import database
from statCalculator import dataAnalyzer
import plotly.graph_objs as go

dash.register_page(__name__)
sara_calc = dataAnalyzer()

layout = html.Div([
    html.H4("sara's profile",style={'textAlign':'center'}),
    html.Div('check out how sad she is',style={'textAlign':'center'}),
    html.Div(style={'padding': '20px'}),
    html.H6("today's entry",style={'textAlign':'center'}),
    html.Div(id='todays info',style={'textAlign':'center'}),
    dcc.Location(id='url', refresh=False),
    html.Div(style={'padding': '20px'}),
    dcc.Tabs([
        dcc.Tab(label='last 7 days', children=[
            dcc.Graph(id='graph-1'),
            dcc.Interval(id='interval-1', interval=10000, n_intervals=0)
        ]),
        dcc.Tab(label='last 30 days', children=[
            dcc.Graph(id='graph-2'),
            dcc.Interval(id='interval-2', interval=10000, n_intervals=0)
        ]),
        dcc.Tab(label='all time', children=[
            dcc.Graph(id='graph-3'),
            dcc.Interval(id='interval-3', interval=10000, n_intervals=0)
        ])
    ]),
    html.Div(id='tabs-content')
    # Todays input
    # 7 day stats
    # 1 month stats
    # all time
    # query/look at old stats
    #plot
])

@callback(
    Output('todays info','children'),
    Input('url','href'),
    allow_duplicate=True
)
def rating(href):
    index = sara_calc.todays_entry(sara_calc.saradb)
    #print(index)
    if index == -1:
        return "sara has yet to submit her rating for today :("
    else:
        dval = sara_calc.saradb.loc[index,'dval']
        return f'sara is feeling at a {dval} out of 10, and her reason is "' + str(sara_calc.saradb.loc[index,'dreason']) + '"'

@callback(
    Output('graph-1', 'figure'),
    Input('interval-1', 'n_intervals')
)
def update_graph_1(n_intervals):
    df,mean,std = sara_calc.seven_days(sara_calc.saradb)
    figure = {
        'data': [
            go.Scatter(x=df['date'], y=df['dval'], mode='lines', name='y vs x')
        ],
        'layout': go.Layout(
            title=f"depression over the last week, with an avg rating of {mean} and std of {std}",
            xaxis={'title': 'date'},
            yaxis={'title': 'depression level'}
        )
    }
    return figure

@callback(
    Output('graph-2', 'figure'),
    Input('interval-2', 'n_intervals')
)
def update_graph_2(n_intervals):
    df,mean,std = sara_calc.thirty_days(sara_calc.saradb)
    figure = {
        'data': [
            go.Scatter(x=df['date'], y=df['dval'], mode='lines', name='y vs x')
        ],
        'layout': go.Layout(
            title=f"depression over the last thirty days, with an avg rating of {mean} and std of {std}",
            xaxis={'title': 'date'},
            yaxis={'title': 'depression level'}
        )
    }
    return figure

@callback(
    Output('graph-3', 'figure'),
    Input('interval-3', 'n_intervals')
)
def update_graph_3(n_intervals):
    df,mean,std = sara_calc.all_time(sara_calc.saradb)
    figure = {
        'data': [
            go.Scatter(x=df['date'], y=df['dval'], mode='lines', name='y vs x')
        ],
        'layout': go.Layout(
            title=f"depression over the entire history, with an avg rating of {mean} and std of {std}",
            xaxis={'title': 'date'},
            yaxis={'title': 'depression level'}
        )
    }
    return figure