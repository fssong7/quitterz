import dash
from dash import dcc,dash_table,html,callback
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate

# from statCalculator import dataAnalyzer
from inputs import people

for person in people:
    dash.register_page(__name__, path_template='/<profile_id>-profile')

# analyzers = {person["name_first"]: dataAnalyzer(person) for person in people}

init_df = pd.DataFrame({
    'name': [],
    'depression value': [],
    'reason': []
})

layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='profile-container', style={'textAlign': 'center'}),
   
])

@callback(
    Output('profile-container', 'children'),
    Input('url', 'pathname')
)
def update_profile(pathname):

    profile_id = pathname.strip('/')
    name_first = profile_id.split('-')[0]
    person = next((p for p in people if p['name_first'] == name_first), None)

    if not person:
        return html.Div("Profile not found.", style={'textAlign': 'center'})

    return html.Div([
        html.H2(f"""{person["name_first"]}'s profile""",style={'textAlign':'center'}),
        html.Div(f"""check out how sad {person["pronoun_sub"]} is""",style={'textAlign':'center'}),
        html.Div(style={'padding': '20px'}),
        html.H4("today's entry",style={'textAlign':'center'}),
        html.Div(id=f"""todays-info-{person["name_first"]}-{person["name_last"]}""",style={'textAlign':'center'}), #'type': 'todays-info', 'name_first': person["name_first"], 'name_last': person["name_last"]
        
        html.Div(style={'padding': '20px'}),
        dcc.Tabs([
            dcc.Tab(label='last 7 days', children=[
                html.Div([
                    dcc.Graph(id=f"""graph-1-{person["name_first"]}-{person["name_last"]}"""),
                    dcc.Interval(id=f"""interval-1-{person["name_first"]}-{person["name_last"]}""", interval=10000, n_intervals=0)
                ]),
            ]),
            dcc.Tab(label='last 30 days', children=[
                html.Div([
                    dcc.Graph(id=f"""graph-2-{person["name_first"]}-{person["name_last"]}"""),
                    dcc.Interval(id=f"""interval-2-{person["name_first"]}-{person["name_last"]}""", interval=10000, n_intervals=0)
                ]),
            ]),
            dcc.Tab(label='all time', children=[
                html.Div([
                    dcc.Graph(id=f"""graph-3-{person["name_first"]}-{person["name_last"]}"""),
                    dcc.Interval(id=f"""interval-3-{person["name_first"]}-{person["name_last"]}""", interval=10000, n_intervals=0)
                ]),
            ])
        ]),
        html.Div(style={'padding': '20px'}),
        dash_table.DataTable(
            id=f"""table-{person["name_first"]}-{person["name_last"]}""",
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



# @callback(
#     Output('ftodays info','children'),
#     Input('url','href'),
#     allow_duplicate=True
# )
# def rating(href):
#     forest_calc.update_db()
#     index = forest_calc.todays_entry(forest_calc.forestdb)
#     #print(index)
#     if index == -1:
#         return "forest has yet to submit his rating for today :("
#     else:
#         dval = forest_calc.forestdb.loc[index,'dval']
#         return f'forest is feeling at a {dval} out of 10, and his reason is "' + str(forest_calc.forestdb.loc[index,'dreason']) + '"'

# @callback(
#     Output('fgraph-1', 'figure'),
#     Input('interval-1', 'n_intervals')
# )
# def update_graph_1(n_intervals):
#     forest_calc.update_db()
#     df,mean,std = forest_calc.seven_days(forest_calc.forestdb)
#     figure = {
#         'data': [
#             go.Scatter(x=df['date'], y=df['dval'], mode='lines+markers', name='y vs x')
#         ],
#         'layout': go.Layout(
#             title=f"depression over the last week<br>with an avg rating of {round(mean,2)} and std of {round(std,2)}",
#             xaxis={'title': 'date'},
#             yaxis={'title': 'depression level'}
#         )
#     }
#     return figure

# @callback(
#     Output('fgraph-2', 'figure'),
#     Input('interval-2', 'n_intervals')
# )
# def update_graph_2(n_intervals):
#     forest_calc.update_db()
#     df,mean,std = forest_calc.thirty_days(forest_calc.forestdb)
#     figure = {
#         'data': [
#             go.Scatter(x=df['date'], y=df['dval'], mode='lines+markers', name='y vs x')
#         ],
#         'layout': go.Layout(
#             title=f"depression over the last thirty days<br>with an avg rating of {round(mean,2)} and std of {round(std,2)}",
#             xaxis={'title': 'date'},
#             yaxis={'title': 'depression level'}
#         )
#     }
#     return figure

# @callback(
#     Output('fgraph-3', 'figure'),
#     Input('interval-3', 'n_intervals')
# )
# def update_graph_3(n_intervals):
#     forest_calc.update_db()
#     df,mean,std = forest_calc.all_time(forest_calc.forestdb)
#     figure = {
#         'data': [
#             go.Scatter(x=df['date'], y=df['dval'], mode='lines+markers', name='y vs x')
#         ],
#         'layout': go.Layout(
#             title=f"depression over the entire history<br>with an avg rating of {round(mean,2)} and std of {round(std,2)}",
#             xaxis={'title': 'date'},
#             yaxis={'title': 'depression level'}
#         )
#     }
#     return figure

# @callback(
#     Output('ftable','data'),
#     Output('ftable','columns'),
#     Input('url','href')
# )
# def display_data_on_load(data):
#     forest_calc.update_db()
#     df,mean,std = forest_calc.all_time(forest_calc.forestdb)
#     data = df[['date','dval','dreason','name']]
#     column = 'name'
#     if column in data:
#         data = data.drop(column,axis=1)
#     data = data.rename(columns={'date':'date','dval':'depression level','dreason':'reason'})
#     columns = [{"name": col, "id": col} for col in data.columns]
#     return data.to_dict('records'),columns
