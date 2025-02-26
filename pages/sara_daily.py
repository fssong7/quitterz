import dash
from dash import Dash, html, dcc, callback,callback_context,Output, Input
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div([
    html.H4('welcome sara',style={'textAlign':'center'}),
    html.Div(style={'padding': '20px'}),
    html.Div('how depressed are you today (1-10)?',style={'textAlign':'center'}),
    html.Div(style={'padding': '5px'}),
    dbc.Col(
        dbc.Select(id="depressionlvl",placeholder="depression level",
            options=[
                {"label": "1","value": "1"},
                {"label": "2","value": "2"},
                {"label": "3","value": "3"},
                {"label": "4","value": "4"},
                {"label": "5","value": "5"},
                {"label": "6","value": "6"},
                {"label": "7","value": "7"},
                {"label": "8","value": "8"},
                {"label": "9","value": "9"},
                {"label": "10","value": "10"},
            ],
        ),
        width={"size":2,"offset":5},
    ),
    html.Div(style={'padding': '10px'}),
    html.Div('and why is that? (optional)',style={'textAlign':'center'}),
    dbc.Col(dbc.Input(id="reason",type="text",placeholder="your 13th reason"),width={"size":4,"offset":4}),
    
    html.Div(style={'padding': '20px'}),
    dbc.Button(
        "submit", id="btn-submit", size = "lg",className="d-grid gap-1 col-2 mx-auto", n_clicks=0,
    ),
])

@callback(
    Output('dval','value'),
    Input('depressionlvl','value')
)
def rating(depressionlvl):
    return depressionlvl

@callback(
    Output('dreason','data'),
    Input('reason','value')
)
def rating(reason):
    return reason

@callback(
    Output('dbtn','data'),
    Input('dval','value'),
    Input('btn-submit', 'n_clicks'),
)
def rating(btn,dval):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-submit' in changed_id and dval is not None:
        print("submitted")
    return

# rating dropdown
# note(optional)
# submit btn
# back to home