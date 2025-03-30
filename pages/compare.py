import dash
from dash import dcc,dash_table,html,callback
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
from statCalculator import dataAnalyzer
import plotly.graph_objs as go

dash.register_page(__name__)
compare = dataAnalyzer()

layout = html.Div([
    html.H2("comparison",style={'textAlign':'center'}),
    html.Div("check out who's the saddest",style={'textAlign':'center'}),
    html.Div(style={'padding': '20px'}),
    html.H4("today's entries",style={'textAlign':'center'}),
    html.Div(id='sara info',style={'textAlign':'center'}),
    html.Div(id='grace info',style={'textAlign':'center'}),
    html.Div(id='forest info',style={'textAlign':'center'}),
    html.Div(style={'padding': '10px'}),
    html.Div(id='saddest',style={'textAlign':'center'}),
    dcc.Location(id='url', refresh=False),
    html.Div(style={'padding': '20px'}),
    dcc.Tabs([
        dcc.Tab(label='last 7 days', children=[
            dcc.Graph(id='graph-seven'),
            dcc.Interval(id='interval-1', interval=10000, n_intervals=0)
        ]),
        dcc.Tab(label='last 30 days', children=[
            dcc.Graph(id='graph-thirty'),
            dcc.Interval(id='interval-2', interval=10000, n_intervals=0)
        ]),
        dcc.Tab(label='all time', children=[
            dcc.Graph(id='graph-all'),
            dcc.Interval(id='interval-3', interval=10000, n_intervals=0)
        ])
    ]),

])
@callback(
    Output('sara info','children'),
    Input('url','href'),
    allow_duplicate=True
)
def srating(href):
    compare.update_db()
    index = compare.todays_entry(compare.saradb)
    #print(index)
    if index == -1:
        return "sara has yet to submit her rating for today :("
    else:
        dval = compare.saradb.loc[index,'dval']
        return f'sara is feeling at a {dval} out of 10, and her reason is "' + str(compare.saradb.loc[index,'dreason']) + '"'
    
@callback(
    Output('grace info','children'),
    Input('url','href'),
    allow_duplicate=True
)
def grating(href):
    compare.update_db()
    index = compare.todays_entry(compare.gracedb)
    #print(index)
    if index == -1:
        return "grace has yet to submit her rating for today :("
    else:
        dval = compare.gracedb.loc[index,'dval']
        return f'grace is feeling at a {dval} out of 10, and her reason is "' + str(compare.gracedb.loc[index,'dreason']) + '"'
@callback(
    Output('forest info','children'),
    Input('url','href'),
    allow_duplicate=True
)
def frating(href):
    compare.update_db()
    index = compare.todays_entry(compare.forestdb)
    #print(index)
    if index == -1:
        return "forest has yet to submit his rating for today :("
    else:
        dval = compare.forestdb.loc[index,'dval']
        return f'forest is feeling at a {dval} out of 10, and his reason is "' + str(compare.forestdb.loc[index,'dreason']) + '"'

@callback(
    Output('saddest','children'),
    Input('url','href'),
    allow_duplicate=True
)
def sad_compare(href):
    sindex = compare.todays_entry(compare.saradb)
    try:
        sval = compare.saradb.loc[sindex,'dval']
    except(KeyError):
        sval = 0
    gindex = compare.todays_entry(compare.gracedb)
    try:
        gval = compare.gracedb.loc[sindex,'dval']
    except(KeyError):
        gval = 0
    findex = compare.todays_entry(compare.forestdb)
    try:
        fval = compare.forestdb.loc[findex,'dval']
    except(KeyError):
        fval = 0
    vals = [sval,gval,fval]
    if (sindex == -1 and gindex == -1 and findex == -1):
        return 'nobody had submitted their ratings for today'
    else:
        highest_val = max(num for num in vals if num == num)
        max_indices = [i for i, num in enumerate(vals) if num == highest_val]
        if len(max_indices) == 1:
            if (max_indices[0] == 0):
                return 'good job sara, you are the saddest today!'
            elif (max_indices[0] == 1):
                return 'good job grace, you are the saddest today!'
            else:
                return 'good job forest, you are the saddest today!'
        elif len(max_indices == 2):
            return "wow there's a tie, it's too annoying to code this"
        else:
            return "wow we all had the same rating, we're like triplets"
        
@callback(
    Output('graph-seven', 'figure'),
    Input('interval-1', 'n_intervals')
)
def update_graph_1(n_intervals):
    compare.update_db()
    dfs,smean,sstd = compare.seven_days(compare.saradb)
    dfg,gmean,gstd = compare.seven_days(compare.gracedb)
    dff,fmean,fstd = compare.seven_days(compare.forestdb)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dfs["date"], y=dfs["dval"], mode='lines+markers', name="sara"))
    fig.add_trace(go.Scatter(x=dfg["date"], y=dfg["dval"], mode='lines+markers', name="grace",opacity=0.8))
    fig.add_trace(go.Scatter(x=dff["date"], y=dff["dval"], mode='lines+markers', name="forest",opacity=0.6))

    fig.update_layout(title=f"quitterz over the last 7 days<br>sara: avg rating of {round(smean,2)} and std of {round(sstd,2)}<br>grace: avg rating of {round(gmean,2)} and std of {round(gstd,2)}<br>forest: avg rating of {round(fmean,2)} and std of {round(fstd,2)}",
                    xaxis={'title': 'date'},
                    yaxis={'title': 'depression level'},
                    template="plotly_white",
                    title_font_color="royalblue",
                    legend=dict(
                        yanchor="top",
                        y = 0.5)
                    )
    return fig

@callback(
    Output('graph-thirty', 'figure'),
    Input('interval-2', 'n_intervals')
)
def update_graph_2(n_intervals):
    compare.update_db()
    dfst,smean,sstd = compare.thirty_days(compare.saradb)
    dfgt,gmean,gstd = compare.thirty_days(compare.gracedb)
    dfft,fmean,fstd = compare.thirty_days(compare.forestdb)
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dfst["date"], y=dfst["dval"], mode='lines+markers', name="sara"))
    fig.add_trace(go.Scatter(x=dfgt["date"], y=dfgt["dval"], mode='lines+markers', name="grace",opacity=0.8))
    fig.add_trace(go.Scatter(x=dfft["date"], y=dfft["dval"], mode='lines+markers', name="forest",opacity=0.6))

    fig.update_layout(title=f"depression over the last 30 days<br>sara: avg rating of {round(smean,2)} and std of {round(sstd,2)}<br>grace: avg rating of {round(gmean,2)} and std of {round(gstd,2)}<br>forest: avg rating of {round(fmean,2)} and std of {round(fstd,2)}",
                    xaxis={'title': 'date'},
                    yaxis={'title': 'depression level'},
                    template="plotly_white",
                    title_font_color="royalblue",
                    legend=dict(
                        yanchor="top",
                        y = 0.5)
                    )
    return fig

@callback(
    Output('graph-all', 'figure'),
    Input('interval-3', 'n_intervals')
)
def update_graph_3(n_intervals):
    compare.update_db()
    dfsa,smean,sstd = compare.all_time(compare.saradb)
    dfga,gmean,gstd = compare.all_time(compare.gracedb)
    dffa,fmean,fstd = compare.all_time(compare.forestdb)
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dfsa["date"], y=dfsa["dval"], mode='lines+markers', name="sara"))
    fig.add_trace(go.Scatter(x=dfga["date"], y=dfga["dval"], mode='lines+markers', name="grace",opacity=0.8))
    fig.add_trace(go.Scatter(x=dffa["date"], y=dffa["dval"], mode='lines+markers', name="forest",opacity=0.6))


    fig.update_layout(title=f"quitterz throughout history<br>sara: avg rating of {round(smean,2)} and std of {round(sstd,2)}<br>grace: avg rating of {round(gmean,2)} and std of {round(gstd,2)}<br>forest: avg rating of {round(fmean,2)} and std of {round(fstd,2)}",
                    xaxis={'title': 'date'},
                    yaxis={'title': 'depression level'},
                    template="plotly_white",
                    title_font_color="royalblue",
                    legend=dict(
                        yanchor="top",
                        y = 0.5)
                    )
    return fig
