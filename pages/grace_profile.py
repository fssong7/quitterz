import dash
from dash import dcc,dash_table,html,callback
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
from statCalculator import dataAnalyzer
import plotly.graph_objs as go

dash.register_page(__name__)
grace_calc = dataAnalyzer()
init_df = pd.DataFrame({
    'name': [],  # Empty list for names
    'depression value': [],  # Empty list for depression values
    'reason': []  # Empty list for reasons
})

layout = html.Div([
    html.H2("grace's profile",style={'textAlign':'center'}),
    html.Div('check out how sad she is',style={'textAlign':'center'}),
    html.Div(style={'padding': '20px'}),
    html.H4("today's entry",style={'textAlign':'center'}),
    html.Div(id='gtodays info',style={'textAlign':'center'}),
    dcc.Location(id='url', refresh=False),
    html.Div(style={'padding': '20px'}),
    dcc.Tabs([
        dcc.Tab(label='last 7 days', children=[
            dcc.Graph(id='ggraph-1'),
            dcc.Interval(id='interval-1', interval=10000, n_intervals=0)
        ]),
        dcc.Tab(label='last 30 days', children=[
            dcc.Graph(id='ggraph-2'),
            dcc.Interval(id='interval-2', interval=10000, n_intervals=0)
        ]),
        dcc.Tab(label='all time', children=[
            dcc.Graph(id='ggraph-3'),
            dcc.Interval(id='interval-3', interval=10000, n_intervals=0)
        ])
    ]),
    html.Div(style={'padding': '20px'}),
    dash_table.DataTable(
        id='gtable',
        columns=[
            {"name": col, "id": col} for col in init_df.keys()  # Dynamically create column headers
        ],
        data=init_df.to_dict('records'),  # Convert DataFrame to list of dictionaries
        style_table={'height': '400px', 'overflowY': 'auto'},  # Optional: Make table scrollable
        style_cell={'textAlign': 'center', 'padding': '10px'},  # Style for table cells
        style_header={'backgroundColor': '#f5f5f5', 'fontWeight': 'bold'},  # Header style
        style_data={'backgroundColor': '#f9f9f9'},  # Data row style
    ),
])

@callback(
    Output('gtodays info','children'),
    Input('url','href'),
    allow_duplicate=True
)
def rating(href):
    grace_calc.update_db()
    index = grace_calc.todays_entry(grace_calc.gracedb)
    #print(index)
    if index == -1:
        return "grace has yet to submit her rating for today :("
    else:
        dval = grace_calc.gracedb.loc[index,'dval']
        return f'grace is feeling at a {dval} out of 10, and her reason is "' + str(grace_calc.gracedb.loc[index,'dreason']) + '"'

@callback(
    Output('ggraph-1', 'figure'),
    Input('interval-1', 'n_intervals')
)
def update_graph_1(n_intervals):
    grace_calc.update_db()
    df,mean,std = grace_calc.seven_days(grace_calc.gracedb)
    figure = {
        'data': [
            go.Scatter(x=df['date'], y=df['dval'], mode='lines', name='y vs x')
        ],
        'layout': go.Layout(
            title=f"depression over the last week<br>with an avg rating of {round(mean,2)} and std of {round(std,2)}",
            xaxis={'title': 'date'},
            yaxis={'title': 'depression level'}
        )
    }
    return figure

@callback(
    Output('ggraph-2', 'figure'),
    Input('interval-2', 'n_intervals')
)
def update_graph_2(n_intervals):
    grace_calc.update_db()
    df,mean,std = grace_calc.thirty_days(grace_calc.gracedb)
    figure = {
        'data': [
            go.Scatter(x=df['date'], y=df['dval'], mode='lines', name='y vs x')
        ],
        'layout': go.Layout(
            title=f"depression over the last thirty days<br>with an avg rating of {round(mean,2)} and std of {round(std,2)}",
            xaxis={'title': 'date'},
            yaxis={'title': 'depression level'}
        )
    }
    return figure

@callback(
    Output('ggraph-3', 'figure'),
    Input('interval-3', 'n_intervals')
)
def update_graph_3(n_intervals):
    grace_calc.update_db()
    df,mean,std = grace_calc.all_time(grace_calc.gracedb)
    figure = {
        'data': [
            go.Scatter(x=df['date'], y=df['dval'], mode='lines', name='y vs x')
        ],
        'layout': go.Layout(
            title=f"depression over the entire history<br>with an avg rating of {round(mean,2)} and std of {round(std,2)}",
            xaxis={'title': 'date'},
            yaxis={'title': 'depression level'}
        )
    }
    return figure

@callback(
    Output('gtable','data'),
    Output('gtable','columns'),
    Input('url','href')  # Trigger callback based on data in the table
)
def display_data_on_load(data):
    # Simply display the entire table data when the page loads
    grace_calc.update_db()
    df,mean,std = grace_calc.all_time(grace_calc.gracedb)
    data = df[['date','dval','dreason','name']]
    column = 'name'
    if column in data:
        data = data.drop(column,axis=1)
    data = data.rename(columns={'date':'date','dval':'depression level','dreason':'reason'})
    columns = [{"name": col, "id": col} for col in data.columns]
    return data.to_dict('records'),columns
