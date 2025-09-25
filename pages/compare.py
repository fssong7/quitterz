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
        html.Div(id=f'info-comp', style={'textAlign': 'center'})
    ]),


    html.Div(id='saddest-comp',style={'textAlign':'center'}),
    dcc.Location(id='url-comp', refresh=False),
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
    html.Div(style={'padding': '20px'}),
    html.Div([
        dcc.Graph(id="curve-comp"),
        dcc.Interval(id=f"""interval-4""", interval=10000, n_intervals=0)
    ])

])


@callback(
    Output('info-comp','children'),
    Input('url-comp','href'),
    allow_duplicate=True
)
def rating(href):
    for analyzer in compare.values():
        analyzer.update_db()

    messages=[]

    for name, analyzer in compare.items():
        # print("analyzer.db:", analyzer.db)

        df = analyzer.db[name]  
        
        # print(df.head())
        index = analyzer.todays_entry(df)
        # print(index)
        if index == -1:
            # print("nothign submitted")
            messages.append(f"{name} has yet to submit their rating for today :(")
        else:
            # print("from today")
            dval = df.loc[index,'dval']
            dreason = df.loc[index,'dreason']
            messages.append(f"{name} is feeling at a {dval} out of 10, and their reason is \"{dreason}\"")

    return html.Div([html.P(msg) for msg in messages])
    
@callback(
    Output('saddest-comp','children'),
    Input('url-comp','href'),
    allow_duplicate=True
)
def sad_compare(href):
    # print("running sad_compare on compar")
    
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
        return "Nobody had submitted their ratings for today."
    lowest_val = min(submitted.values())
    saddest = [name for name, val in submitted.items() if val == lowest_val]
    if len(saddest) == 1:
        return f"Good job {saddest[0]}, you are the saddest today!"
    elif len(saddest) == len(submitted) and len(submitted) == len(people):
        return "Wow, we all had the same rating, we're like triplets!"
    elif len(saddest) == len(submitted):
        tied_names = " & ".join(saddest)
        return f"Wow, there's a tie for saddest today between {tied_names}!"
        
    

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
         
        hover_text = [
            f"Date: {row['date'].strftime('%Y-%m-%d')}<br>"
            f"Name: {row['name']}<br>"
            f"Value: {row['dval']}<br>"
            f"Reason: {'<br>'.join([str(row['dreason'])[i:i+80] for i in range(0, len(str(row['dreason'])), 80)])}"
            for _, row in recent_df.iterrows()
        ]
            

        fig.add_trace(go.Scatter(
            x=recent_df["date"],
            y=recent_df["dval"],
            mode='lines+markers',
            name=name,
            text=hover_text,
            hoverinfo='text',
            hoverlabel=dict(
                bgcolor="white",
                bordercolor="black",
                font_size=12,
                font_family="Arial",
                align="left"
            )
        ))
        titles.append(f"{name}: avg rating of {round(mean,2)} and std of {round(std,2)}")

    fig.update_layout(title=f"quitterz over the last 7 days<br>" + "<br>".join(titles),
                    xaxis={'title': 'date'},
                    yaxis={'title': 'depression level', 'range': [0, 11]},
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
            
            hover_text = [
                f"Date: {row['date'].strftime('%Y-%m-%d')}<br>"
                f"Name: {row['name']}<br>"
                f"Value: {row['dval']}<br>"
                f"Reason: {'<br>'.join([str(row['dreason'])[i:i+80] for i in range(0, len(str(row['dreason'])), 80)])}"
                for _, row in recent_df.iterrows()
            ]
                

            fig.add_trace(go.Scatter(
                x=recent_df["date"],
                y=recent_df["dval"],
                mode='lines+markers',
                name=name,
                text=hover_text,
                hoverinfo='text',
                hoverlabel=dict(
                    bgcolor="white",
                    bordercolor="black",
                    font_size=12,
                    font_family="Arial",
                    align="left"
                )
            ))
            titles.append(f"{name}: avg rating of {round(mean,2)} and std of {round(std,2)}")

        fig.update_layout(title=f"quitterz over the last 30 days<br>" + "<br>".join(titles),
                        xaxis={'title': 'date'},
                        yaxis={'title': 'depression level', 'range': [0, 11]},
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

            recent_df['date'] = pd.to_datetime(recent_df['date'])
            recent_df = recent_df.set_index('date')
            weekly_df = recent_df['dval'].resample('W').mean()

            moving_avg = weekly_df.rolling(window=1, center=True).mean()

            fig.add_trace(go.Scatter(
                x=weekly_df.index,
                y=weekly_df.values,
                mode='markers+lines',
                name=f"{name} weekly avg",
                line=dict(shape='spline', smoothing=1)
            ))
            # fig.add_trace(go.Scatter(
            #     x=moving_avg.index,
            #     y=moving_avg.values,
            #     mode='lines',
            #     name=f"{name} 4-week MA",
            #     line=dict(dash='dash')
            # ))

            titles.append(f"{name}: avg rating of {round(mean,2)} and std of {round(std,2)}")
            
        #     fig.add_trace(go.Scatter(x=moving_avg.index, y=moving_avg.values, mode='lines+markers', name=name))
        #     titles.append(f"{name}: avg rating of {round(mean,2)} and std of {round(std,2)}")

        # fig.update_layout(title=f"quitterz throughout history<br>" + "<br>".join(titles),
        #                 xaxis={'title': 'date'},
        #                 yaxis={'title': 'depression level', 'range': [0, 11]},
        #                 template="plotly_white",
        #                 title_font_color="royalblue",
        #                 title_x = 0.5,
        #                 title_font=dict(size=14),
        #                 legend=dict(
        #                     yanchor="top",
        #                     y = 0.5)
        #                 )
        return fig



@callback(
    Output("curve-comp", 'figure'),
    Input(f"""interval-4""", 'n_intervals'),
)
def update_graph_4(n_intervals):
        titles=[]
        for analyzer in compare.values():
            analyzer.update_db()

        ratings = range(1, 11)
        data = {}
        
        

        for name, analyzer in compare.items():
            df = analyzer.db[name]
            recent_df, _, _ = analyzer.all_time(df)
            counts = recent_df['dval'].value_counts().reindex(ratings, fill_value=0)
            data[name] = counts
        
        df_counts = pd.DataFrame(data, index=ratings)
        fig = go.Figure()

        for i, name in enumerate(df_counts.columns):
            fig.add_trace(go.Bar(
                x=df_counts.index,
                y=df_counts[name],
                name=name,
                
            ))
        
        fig.add_trace(go.Scatter(
            x=df_counts.index,
            y=df_counts.sum(axis=1),
            mode='lines+markers',
            line=dict(shape='spline', smoothing=1.3, color="black")))


        fig.update_layout(
            title="distribution of depression over the entire history by quitter",
            xaxis={'title': 'rating','range': [0, 11]},
            yaxis={'title': 'count'},
            template="plotly_white",
            title_font_color="royalblue",
            title_x=0.5,
            legend=dict(
                yanchor="top",
                y = 0.5),
            barmode="stack" #group
        )
            
            


        
        return fig

