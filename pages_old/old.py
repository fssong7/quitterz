import dash
from dash import Dash, html, dcc, callback,callback_context,Output, Input,State
import dash_bootstrap_components as dbc
from mongoDB import database
from datetime import date,datetime
import pytz

today = datetime.today().strftime('%Y-%m-%d')
dash.register_page(__name__)
data_base = database()

layout = html.Div([
    html.H2('welcome quitter',style={'textAlign':'center'}),
    html.Div(style={'padding': '5px'}),
    html.Div('this is for entering ratings for old dates, or overwriting entries',style={'textAlign':'center'}),
    html.Div(style={'padding': '20px'}),

    html.Div(
    style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'},
    children=[
        dcc.DatePickerSingle(
            id='date_picker',
            date=today,  # Set the default date
            display_format='YYYY-MM-DD',  # Format of the date
            style={
                    'fontSize': '15px',
                    'textAlign': 'center',
            }
        ),
    ]
    ),
    html.Div(style={'padding': '5px'}),
    dbc.Col(
        dbc.Select(id="name",placeholder="your name",
            options=[
                {"label": "sabby barr","value": "sara"},
                {"label": "gabby patty","value": "grace"},
                {"label": "trash","value": "forest"},
            ],
        ),
        width={"size":8,"offset":2},
    ),

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
    html.Div(style={'padding': '5px'}),
    html.Div('reason (optional)',style={'textAlign':'center'}),
    dbc.Col(dbc.Input(id="reason",type="text",placeholder="your 13th reason"),width={"size":10,"offset":1}),
    
    html.Div(style={'padding': '20px'}),
    dbc.Button(
        "submit", id="btn_submit", size = "lg",className="d-grid gap-1 col-6 mx-auto", n_clicks=0,
    ),
    html.Div(id='dbtn'),
    dcc.Store(id='idname'),
    dcc.Store(id='iddate'),
    dcc.Store(id='idval'),
    dcc.Store(id='idreason'),
    dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("thanks for submitting")),
        dbc.ModalBody("ur cool :)"),
        dbc.ModalFooter(
            dcc.Link("return to home",href='/'),#dash.page_registry['pages.ahome']['path']),
        ),
    ],
    id="imodal",
    is_open=False,
),
])

@callback(
    Output('idname','data'),
    Input('name','value')
)
def rating(name):
    return name

@callback(
    Output('iddate','data'),
    Input('date_picker','date')
)
def rating(date_picker):
    return date_picker

@callback(
    Output('idval','data'),
    Input('depressionlvl','value')
)
def rating(depressionlvl):
    return depressionlvl

@callback(
    Output('idreason','data'),
    Input('reason','value')
)
def rating(reason):
    return reason

@callback(
    Output('imodal','is_open'),
    Input('btn_submit', 'n_clicks'),
    Input('idname','data'),
    Input('iddate','data'),
    Input('idval','data'),
    Input('idreason','data'),
    [State("imodal", "is_open")],
    allow_duplicate=True
)
def rating(btn_submit,idname,iddate,idval,idreason,is_open):
    #changed_id = [p['prop_id'] for p in callback_context.triggered][0]
  
    if btn_submit and idname and iddate and idval is not None:
        print(idname)
        print(iddate)
        print(idval)
        print(idreason)
        # eastern_tz = pytz.timezone("US/Eastern")
        # submitted_date = datetime.now(eastern_tz).strftime("%Y-%m-%d")
        #submitted_date = date.today().strftime("%Y-%m-%d")
        data = {
            'name': idname,
            'dval': int(idval),
            'dreason': idreason,
            'date': iddate#submitted_date
        }
        
        data_base.collection.insert_one(data)
        return not is_open
    return is_open
