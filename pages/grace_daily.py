import dash
from dash import Dash, html, dcc, callback,callback_context,Output, Input,State
import dash_bootstrap_components as dbc
from mongoDB import database
from datetime import date,datetime
import pytz

dash.register_page(__name__)
data_base = database()

layout = html.Div([
    html.H4('welcome grace',style={'textAlign':'center'}),
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
        width={"size":8,"offset":2},
    ),
    html.Div(style={'padding': '10px'}),
    html.Div('and why is that? (optional)',style={'textAlign':'center'}),
    dbc.Col(dbc.Input(id="reason",type="text",placeholder="your 13th reason"),width={"size":10,"offset":1}),
    
    html.Div(style={'padding': '20px'}),
    dbc.Button(
        "submit", id="btn_submit", size = "lg",className="d-grid gap-1 col-6 mx-auto", n_clicks=0,
    ),
    html.Div(id='dbtn'),
    dcc.Store(id='gdval'),
    dcc.Store(id='gdreason'),
    dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("thanks for submitting grace")),
        dbc.ModalBody("hopefully tomorrow is a better day :)"),
        dbc.ModalFooter(
            dcc.Link("return to home",href='/'),#dash.page_registry['pages.ahome']['path']),
        ),
    ],
    id="gmodal",
    is_open=False,
),
])

@callback(
    Output('gdval','data'),
    Input('depressionlvl','value')
)
def rating(depressionlvl):
    return depressionlvl

@callback(
    Output('gdreason','data'),
    Input('reason','value')
)
def rating(reason):
    return reason

@callback(
    Output('gmodal','is_open'),
    Input('btn_submit', 'n_clicks'),
    Input('gdval','data'),
    Input('gdreason','data'),
    [State("gmodal", "is_open")],
    allow_duplicate=True
)
def rating(btn_submit,gdval,gdreason,is_open):
    #changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    
    if btn_submit and gdval is not None:
        print(gdval)
        print(gdreason)
        eastern_tz = pytz.timezone("US/Eastern")
        submitted_date = datetime.now(eastern_tz).strftime("%Y-%m-%d")
        #submitted_date = date.today().strftime("%Y-%m-%d")
        data = {
            'name': 'grace',
            'dval': int(gdval),
            'dreason': gdreason,
            'date': submitted_date
        }
        
        data_base.collection.insert_one(data)
        return not is_open
    return is_open
