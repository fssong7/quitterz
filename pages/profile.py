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
    if not pathname:
        return {}  # instead of None, return empty dict
    profile_id = pathname.strip('/')
    name_first = profile_id.split('-')[0]
    return next((p for p in people if p['name_first'] == name_first), {})


@callback(
    Output('profile-container', 'children'),
    Input('profile-name', 'data')
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
            style_cell={'whiteSpace': 'normal','textAlign': 'center', 'height':'auto','padding': '10px'},  # Style for table cells
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
    index = analyzers[person["name_first"]].todays_entry(analyzers[person["name_first"]].forestdb)
    #print(index)
    if index == -1:
        return "forest has yet to submit his rating for today :("
    else:
        dval = analyzers[person["name_first"]].forestdb.loc[index,'dval']
        return f'forest is feeling at a {dval} out of 10, and his reason is "' + str(analyzers[person["name_first"]].forestdb.loc[index,'dreason']) + '"'

@callback(
    Output(f"""graph-1""", 'figure'),
    Input(f"""interval-1""", 'n_intervals')
)
def update_graph_1(n_intervals):
    analyzers[person["name_first"]].update_db()
    df,mean,std = analyzers[person["name_first"]].seven_days(analyzers[person["name_first"]].forestdb)
    figure = {
        'data': [
            go.Scatter(x=df['date'], y=df['dval'], mode='lines+markers', name='y vs x')
        ],
        'layout': go.Layout(
            title=f"depression over the last week<br>with an avg rating of {round(mean,2)} and std of {round(std,2)}",
            xaxis={'title': 'date'},
            yaxis={'title': 'depression level'}
        )
    }
    return figure

@callback(
    Output(f"""graph-2""", 'figure'),
    Input(f"""interval-2""", 'n_intervals')
)
def update_graph_2(n_intervals):
    analyzers[person["name_first"]].update_db()
    df,mean,std = analyzers[person["name_first"]].thirty_days(analyzers[person["name_first"]].forestdb)
    figure = {
        'data': [
            go.Scatter(x=df['date'], y=df['dval'], mode='lines+markers', name='y vs x')
        ],
        'layout': go.Layout(
            title=f"depression over the last thirty days<br>with an avg rating of {round(mean,2)} and std of {round(std,2)}",
            xaxis={'title': 'date'},
            yaxis={'title': 'depression level'}
        )
    }
    return figure

@callback(
    Output(f"""graph-3""", 'figure'),
    Input(f"""interval-3""", 'n_intervals')
)
def update_graph_3(n_intervals):
    analyzers[person["name_first"]].update_db()
    df,mean,std = analyzers[person["name_first"]].all_time(analyzers[person["name_first"]].forestdb)
    figure = {
        'data': [
            go.Scatter(x=df['date'], y=df['dval'], mode='lines+markers', name='y vs x')
        ],
        'layout': go.Layout(
            title=f"depression over the entire history<br>with an avg rating of {round(mean,2)} and std of {round(std,2)}",
            xaxis={'title': 'date'},
            yaxis={'title': 'depression level'}
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
    df,mean,std = analyzers[person["name_first"]].all_time(analyzers[person["name_first"]].forestdb)
    data = df[['date','dval','dreason','name']]
    column = 'name'
    if column in data:
        data = data.drop(column,axis=1)
    data = data.rename(columns={'date':'date','dval':'depression level','dreason':'reason'})
    columns = [{"name": col, "id": col} for col in data.columns]
    return data.to_dict('records'),columns
