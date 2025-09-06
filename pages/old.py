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
            id='date_picker-old',
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
        dbc.Select(id="name-old",placeholder="your name",
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
        dbc.Select(id="depressionlvl-old",placeholder="depression level",
            options=[
                {"label": f"{i}","value": f"{i}"} for i in range(1,11)
            ],
        ),
        width={"size":8,"offset":2},
    ),
    html.Div(style={'padding': '5px'}),
    html.Div('reason (optional)',style={'textAlign':'center'}),
    dbc.Col(dbc.Input(id="reason-old",type="text",placeholder="your 13th reason"),width={"size":10,"offset":1}),
    
    html.Div(style={'padding': '20px'}),
    dbc.Button(
        "submit", id="btn_submit-old", size = "lg",className="d-grid gap-1 col-6 mx-auto", n_clicks=0,
    ),
    # html.Div(id='dbtn'),
    # dcc.Store(id='idname'),
    # dcc.Store(id='iddate'),
    # dcc.Store(id='idval'),
    # dcc.Store(id='idreason'),
    dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("thanks for submitting")),
        dbc.ModalBody("ur cool :)"),
        dbc.ModalFooter(
            dcc.Link("return to home",href='/'),#dash.page_registry['pages.ahome']['path']),
        ),
    ],
    id="modal-old",
    is_open=False,
),
])

@callback(
    Output('date_picker-old', 'date'),
    Input('url', 'pathname')  # or any input that triggers on page load
)
def update_date_picker(pathname):
    return datetime.today().strftime('%Y-%m-%d')


@callback(
    Output('modal-old','is_open'),
    Input('btn_submit-old', 'n_clicks'),
    State('name-old','value'),
    State('date_picker-old','date'),
    State('depressionlvl-old','value'),
    State('reason-old','value'),
    prevent_initial_call=True
    
)
def rating(btn_submit,name,date_picker,depression_lvl,reason):
    #changed_id = [p['prop_id'] for p in callback_context.triggered][0]
  
    if btn_submit and name and date_picker and depression_lvl is not None:
        print(name)
        print(date_picker)
        print(depression_lvl)
        print(reason)
        # eastern_tz = pytz.timezone("US/Eastern")
        # submitted_date = datetime.now(eastern_tz).strftime("%Y-%m-%d")
        #submitted_date = date.today().strftime("%Y-%m-%d")
        data = {
            'name': name,
            'dval': int(depression_lvl),
            'dreason': reason,
            'date': date_picker#submitted_date
        }
        
        data_base.collection.insert_one(data)
        return True
    return False



