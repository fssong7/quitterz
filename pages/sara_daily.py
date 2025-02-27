import dash
from dash import Dash, html, dcc, callback,callback_context,Output, Input,State
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
        width={"size":6,"offset":3},
    ),
    html.Div(style={'padding': '10px'}),
    html.Div('and why is that? (optional)',style={'textAlign':'center'}),
    dbc.Col(dbc.Input(id="reason",type="text",placeholder="your 13th reason"),width={"size":10,"offset":1}),
    
    html.Div(style={'padding': '20px'}),
    dbc.Button(
        "submit", id="btn_submit", size = "lg",className="d-grid gap-1 col-6 mx-auto", n_clicks=0,
    ),
    html.Div(id='dbtn'),
    dcc.Store(id='dval'),
    dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("thanks for submitting sara")),
        dbc.ModalBody("hopefully tomorrow is a better day :)"),
        dbc.ModalFooter(
            dcc.Link("return to home",href=dash.page_registry['pages.home']['path']),
        ),
    ],
    id="modal",
    is_open=False,
),
])

@callback(
    Output('dval','data'),
    Input('depressionlvl','value')
)
def rating(depressionlvl):
    return depressionlvl

@callback(
    Output('dreason','value'),
    Input('reason','value')
)
def rating(reason):
    return reason

@callback(
    Output('modal','is_open'),
    Input('btn_submit', 'n_clicks'),
    Input('dval','data'),
    [State("modal", "is_open")],
)
def rating(btn_submit,dval,is_open):
    #changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    
    if btn_submit and dval is not None:
        print(dval)
        return not is_open
    return is_open


# rating dropdown
# note(optional)
# submit btn
# back to home