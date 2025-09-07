import dash
from dash import dcc,dash_table,html,callback
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from inputs import people
from statCalculator import dataAnalyzer

dash.register_page(__name__)

compare = {person["name_first"]: dataAnalyzer() for person in people}

layout = html.Div([
    html.H2("comparison",style={'textAlign':'center'}),
    html.Div("check out who's the saddest",style={'textAlign':'center'}),
    html.Div(style={'padding': '20px'}),
    html.H4("today's entries",style={'textAlign':'center'}),
    html.Div([
        html.Div([
            html.Div(id=f'{person["name_first"]} info', style={'textAlign': 'center'}),
            html.Div(style={'padding': '5px'}),
        ]) for person in people
    ]),


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
    Output('info','children'),
    Input('url','href'),
    allow_duplicate=True
)
def rating(href):
    for analyzer in compare.values():
        analyzer.update_db()

    messages=[]

    for name, analyzer in compare.items():
        df = analyzer.db[name]  
        index = analyzer.todays_entry(df)
        if index == -1:
            messages.append(f"{name} has yet to submit their rating for today :(")
        else:
            dval = df.loc[index,'dval']
            dreason = df.loc[index,'dreason']
            messages.append(f"{name} is feeling at a {dval} out of 10, and their reason is \"{dreason}\"")

    return html.Div([html.P(msg) for msg in messages])
    
@callback(
    Output('saddest','children'),
    Input('url','href'),
    allow_duplicate=True
)
def sad_compare(href):
    print("running sad_compare on compar")
    vals = {}

    for name, analyzer in compare.items():
        df = analyzer.db[name]  
        index = analyzer.todays_entry(df)
        try:
            dval = df.loc[index, 'dval'] if index != -1 else None
        except (KeyError, IndexError):
            dval = None
        vals[name] = dval

        submitted = {name: val for name, val in vals.items() if val is not None}

    if not submitted:
        return "nobody had submitted their ratings for today"
    
    lowest_val = min(submitted.values())
    saddest = [name for name, val in submitted.items() if val == lowest_val]

    if len(saddest) == 1:
        return f"good job {saddest[0]}, you are the saddest today!"
    elif len(saddest) == len(submitted):
        return "wow we all had the same rating, we're like triplets"
    else:
        tied_names = ", ".join(saddest)
        return f"Wow, there's a tie for saddest today: {tied_names}!"
    

@callback(
    Output('graph-seven', 'figure'),
    Input('interval-1', 'n_intervals')
)
def update_graph_1(n_intervals):
    titles=[]
    for analyzer in compare.values():
        analyzer.update_db()


    fig = go.Figure()

    for name, analyzer in compare.items():
        df = analyzer.db[name]
        recent_df, mean, std = analyzer.seven_days(df)
        fig.add_trace(go.Scatter(x=recent_df["date"], y=recent_df["dval"], mode='lines+markers', name=name))
        titles.append(f"{name}: avg rating of {round(mean,2)} and std of {round(std,2)}")

    fig.update_layout(title=f"quitterz over the last 7 days<br>" + "<br>".join(titles),
                    xaxis={'title': 'date'},
                    yaxis={'title': 'depression level'},
                    template="plotly_white",
                    title_font_color="royalblue",
                    title_x = 0.5,
                    title_font=dict(size=14),
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
        titles=[]
        for analyzer in compare.values():
            analyzer.update_db()


        fig = go.Figure()

        for name, analyzer in compare.items():
            df = analyzer.db[name]
            recent_df,mean,std = analyzer.thirty_days(df)
            fig.add_trace(go.Scatter(x=recent_df["date"], y=recent_df["dval"], mode='lines+markers', name=name))
            titles.append(f"{name}: avg rating of {round(mean,2)} and std of {round(std,2)}")

        fig.update_layout(title=f"quitterz over the last 30 days<br>" + "<br>".join(titles),
                        xaxis={'title': 'date'},
                        yaxis={'title': 'depression level'},
                        template="plotly_white",
                        title_font_color="royalblue",
                        title_x = 0.5,
                        title_font=dict(size=14),
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
        titles=[]
        for analyzer in compare.values():
            analyzer.update_db()


        fig = go.Figure()

        for name, analyzer in compare.items():
            df = analyzer.db[name]
            recent_df,mean,std = analyzer.all_time(df)
            fig.add_trace(go.Scatter(x=recent_df["date"], y=recent_df["dval"], mode='lines+markers', name=name))
            titles.append(f"{name}: avg rating of {round(mean,2)} and std of {round(std,2)}")

        fig.update_layout(title=f"quitterz throughout history<br>" + "<br>".join(titles),
                        xaxis={'title': 'date'},
                        yaxis={'title': 'depression level'},
                        template="plotly_white",
                        title_font_color="royalblue",
                        title_x = 0.5,
                        title_font=dict(size=14),
                        legend=dict(
                            yanchor="top",
                            y = 0.5)
                        )
        return fig
    