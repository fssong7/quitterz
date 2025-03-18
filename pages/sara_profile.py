import dash
from dash import dcc,dash_table,html,callback
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
from statCalculator import dataAnalyzer
import plotly.graph_objs as go

dash.register_page(__name__)
sara_calc = dataAnalyzer()
init_df = pd.DataFrame({
    'name': [],
    'depression value': [], 
    'reason': []
})

layout = html.Div([
    html.H2("sara's profile",style={'textAlign':'center'}),
    html.Div('check out how sad she is',style={'textAlign':'center'}),
    html.Div(style={'padding': '20px'}),
    html.H4("today's entry",style={'textAlign':'center'}),
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
    html.Div(style={'padding': '20px'}),
    dash_table.DataTable(
        id='table',
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
    Output('todays info','children'),
    Input('url','href'),
    allow_duplicate=True
)
def rating(href):
    sara_calc.update_db()
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
    sara_calc.update_db()
    df,mean,std = sara_calc.seven_days(sara_calc.saradb)
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
    Output('graph-2', 'figure'),
    Input('interval-2', 'n_intervals')
)
def update_graph_2(n_intervals):
    sara_calc.update_db()
    df,mean,std = sara_calc.thirty_days(sara_calc.saradb)
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
    Output('graph-3', 'figure'),
    Input('interval-3', 'n_intervals')
)
def update_graph_3(n_intervals):
    sara_calc.update_db()
    df,mean,std = sara_calc.all_time(sara_calc.saradb)
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
    Output('table','data'),
    Output('table','columns'),
    Input('url','href')  # Trigger callback based on data in the table
)
def display_data_on_load(data):
    # Simply display the entire table data when the page loads
    sara_calc.update_db()
    df,mean,std = sara_calc.all_time(sara_calc.saradb)
    data = df[['date','dval','dreason','name']]
    column = 'name'
    if column in data:
        data = data.drop(column,axis=1)
    data = data.rename(columns={'date':'date','dval':'depression level','dreason':'reason'})
    columns = [{"name": col, "id": col} for col in data.columns]
    return data.to_dict('records'),columns
