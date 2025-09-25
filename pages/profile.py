import dash
from dash import dcc,dash_table,html,callback
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate

from statCalculator import dataAnalyzer
from inputs import people

for person in people:
    dash.register_page(__name__, path_template='/<profile_id>-profile')

analyzers = {person["name_first"]: dataAnalyzer() for person in people}

init_df = pd.DataFrame({
    'name': [],
    'depression value': [],
    'reason': []
})

layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='profile-container', style={'textAlign': 'center'}),
    dcc.Store(id='profile-name'),
])


@callback(
    Output('profile-name', 'data'),
    Input('url', 'pathname')
)
def fetch_person(pathname):
    # if not pathname:
    #     return {}  # instead of None, return empty dict
    # profile_id = pathname.strip('/')
    # name_first = profile_id.split('-')[0]
    # return next((p for p in people if p['name_first'] == name_first), {})
    if not pathname:
        return {}  # no URL yet
    
    profile_id = pathname.strip('/')
    name_first = profile_id.split('-')[0]

    # 🔹 Try to find existing person
    person = next((p for p in people if p['name_first'] == name_first), None)

    if not person:
        # 🔹 If not found, create a new one
        person = {
            "name_first": name_first,
            "name_last": "",   # or fetch from input later
            "pronoun_sub": "they",
            "pronoun_obj": "their"
        }
        people.append(person)  # keep it in memory
        analyzers[name_first] = dataAnalyzer()  # give them a fresh analyzer

    return person

@callback(
    Output('profile-container', 'children'),
    Input('profile-name', 'data'),
    
)
def update_profile(person):

    if not person:
        return html.Div("Profile not found.", style={'textAlign': 'center'})

    return html.Div([
        html.H2(f"""{person["name_first"]}'s profile""",style={'textAlign':'center'}),
        html.Div(f"""check out how sad {person["pronoun_sub"]} is""",style={'textAlign':'center','marginBottom': '40px'}),

        html.H4("today's entry",style={'textAlign':'center'}),
        html.Div(id=f"""todays-info""",style={'textAlign':'center','marginBottom': '40px'}), #'type': 'todays-info', 'name_first': person["name_first"], 'name_last': person["name_last"]
        

        dcc.Tabs([
            dcc.Tab(label='last 7 days', children=[
                html.Div([
                    dcc.Graph(id=f"""graph-1"""),
                    dcc.Interval(id=f"""interval-1""", interval=10000, n_intervals=0)
                ]),
            ]),
            dcc.Tab(label='last 30 days', children=[
                html.Div([
                    dcc.Graph(id=f"""graph-2"""),
                    dcc.Interval(id=f"""interval-2""", interval=10000, n_intervals=0)
                ]),
            ]),
            dcc.Tab(label='all time', children=[
                html.Div([
                    dcc.Graph(id=f"""graph-3"""),
                    dcc.Interval(id=f"""interval-3""", interval=10000, n_intervals=0)
                ]),
            ])
        ]),
        html.Div(style={'padding': '20px'}),
        html.Div([
            dcc.Graph(id="curve"),
            dcc.Interval(id=f"""interval-4""", interval=10000, n_intervals=0)
        ]),
        html.Div(style={'padding': '20px'}),
        dash_table.DataTable(
            id=f"""table""",
            columns=[
                {"name": col, "id": col} for col in init_df.keys()  # Dynamically create column headers
            ],
            data=init_df.to_dict('records'),  # Convert DataFrame to list of dictionaries
            style_table={
                'width': '98%',  # Make table take full width of its container
                #'overflowX': 'auto',
                #'overflowY': 'auto',
                #'height': '400px'  # Allows horizontal scrolling if needed
            },
            style_cell={'whiteSpace': 'normal','textAlign': 'center', 'height':'auto','padding': '10px', 'wordBreak': 'break-word','maxWidth': '80vw'
            },  # Style for table cells
            style_header={'backgroundColor': '#f5f5f5', 'fontWeight': 'bold'},  # Header style
            style_data={'backgroundColor': '#f9f9f9'},  # Data row style
        ),
    ])



@callback(
    Output(f"""todays-info""",'children'),
    Input('profile-name', 'data'),
    allow_duplicate=True
)
def rating(person):
    analyzers[person["name_first"]].update_db()
    df = analyzers[person["name_first"]].db[person["name_first"]]
    index = analyzers[person["name_first"]].todays_entry(df)
    #print(index)
    if index == -1:
        return f"""{person["name_first"]} has yet to submit {person["pronoun_obj"]} rating for today :("""
    else:
        dval = df.loc[index,'dval']
        dreason = df.loc[index,'dreason']
        return f'{person["name_first"]} is feeling at a {dval} out of 10, and {person["pronoun_obj"]} reason is "{dreason}"'

@callback(
    Output(f"""graph-1""", 'figure'),
    Input(f"""interval-1""", 'n_intervals'),
    State("profile-name", "data")
)
def update_graph_1(n_intervals, personn):
    if not personn:
        raise PreventUpdate
    
    name = personn["name_first"]
    analyzers[name].update_db()
    
    df,mean,std = analyzers[name].seven_days(analyzers[name].db[name])
    figure = {
        'data': [
            go.Scatter(x=df['date'], y=df['dval'], mode='lines+markers', name='y vs x')
        ],
        'layout': go.Layout(
            title=f"depression over the last week<br>with an avg rating of {round(mean,2)} and std of {round(std,2)}",
            xaxis={'title': 'date'},
            yaxis={'title': 'depression level', 'range': [0, 11]},
            template="plotly_white",
            title_x=0.5
        )
    }
    return figure

@callback(
    Output(f"""graph-2""", 'figure'),
    Input(f"""interval-2""", 'n_intervals'),
    State("profile-name", "data")
)
def update_graph_2(n_intervals, person):
    name = person["name_first"]
    analyzers[name].update_db()
    
    df,mean,std = analyzers[name].thirty_days(analyzers[name].db[name])

    figure = {
        'data': [
            go.Scatter(x=df['date'], y=df['dval'], mode='lines+markers', name='y vs x')
        ],
        'layout': go.Layout(
            title=f"depression over the last thirty days<br>with an avg rating of {round(mean,2)} and std of {round(std,2)}",
            xaxis={'title': 'date'},
            yaxis={'title': 'depression level', 'range': [0, 11]},
            template="plotly_white",
            title_x=0.5
        )
    }
    return figure

@callback(
    Output(f"""graph-3""", 'figure'),
    Input(f"""interval-3""", 'n_intervals'),
    State("profile-name", "data")
)
def update_graph_3(n_intervals, person):
    name = person["name_first"]
    analyzers[name].update_db()
    
    df,mean,std = analyzers[name].all_time(analyzers[name].db[name])
    figure = {
        'data': [
            go.Scatter(x=df['date'], y=df['dval'], mode='lines+markers', name='y vs x')
        ],
        'layout': go.Layout(
            title=f"depression over the entire history<br>with an avg rating of {round(mean,2)} and std of {round(std,2)}",
            xaxis={'title': 'date'},
            yaxis={'title': 'depression level', 'range': [0, 11]},
            template="plotly_white",
            title_x=0.5
        )
    }
    return figure

@callback(
    Output("curve", 'figure'),
    Input(f"""interval-4""", 'n_intervals'),
    State("profile-name", "data")
)
def update_graph_4(n_intervals, person):
    name = person["name_first"]
    analyzers[name].update_db()
    
    df,mean,std = analyzers[name].all_time(analyzers[name].db[name])
    
    counts = df['dval'].value_counts().sort_index()
    figure = {
        'data': [
            go.Bar(x=counts.index, y=counts.values, name='y vs x'),
            go.Scatter(x=counts.index, y=counts.values, mode='lines+markers', name='y vs x',
                       line=dict(shape='spline', smoothing=1.3, color='red'))
            
        ],
        
        'layout': go.Layout(
            title=f"distribution of depression over the entire history",
            xaxis={'title': 'rating','range': [0, 11]},
            yaxis={'title': 'count',},
            template="plotly_white",
            showlegend=False,
            title_x=0.5
        )
    }
    return figure


@callback(
    Output(f"""table""",'data'),
    Output(f"""table""",'columns'),
    Input('profile-name', 'data')
)
def display_data_on_load(person):
    analyzers[person["name_first"]].update_db()
    df,mean,std = analyzers[person["name_first"]].all_time(analyzers[person["name_first"]].db[person["name_first"]])
    data = df[['date','dval','dreason','name']]
    column = 'name'
    if column in data:
        data = data.drop(column,axis=1)
    data = data.rename(columns={'date':'date','dval':'depression level','dreason':'reason'})
    columns = [{"name": col, "id": col} for col in data.columns]
    return data.to_dict('records'),columns
