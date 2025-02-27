import dash
from dash import Dash, html, dcc, callback,callback_context,Output, Input
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/')

layout = html.Div([
    html.H4('what is your name?',style={'textAlign':'center'}),
    dcc.Link(
        dbc.Button(
            "sara barrows", id="btn-nclicks-1", size = "lg",className="d-grid gap-1 col-8 mx-auto", n_clicks=0,
        ),href="/sara-daily",style={"text-decoration": "none"},),
    html.Div(style={'padding': '5px'}),
    
    dcc.Link(
        dbc.Button(
            "grace patterson", id="btn-nclicks-2", size = "lg",className="d-grid gap-1 col-8 mx-auto", n_clicks=0,
        ),href="/grace-daily",style={"text-decoration": "none"},),
    html.Div(style={'padding': '5px'}),
    
    dcc.Link(
        dbc.Button(
            "forest song", id="btn-nclicks-3", size = "lg",className="d-grid gap-1 col-8 mx-auto", n_clicks=0,
        ),href="/forest-daily",style={"text-decoration": "none"},),
    html.Div(style={'padding': '5px'}),
    html.Div(id='empty_container'),
])

@callback(
    Output('empty_container', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
)

def displayClick(btn1,btn2,btn3):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        print("sara pressed")
    elif 'btn-nclicks-2' in changed_id:
        print("grace pressed")
    elif 'btn-nclicks-3' in changed_id:
        print("forest pressed")
    return