import dash
from dash import Dash, html, dcc, callback,callback_context,Output, Input,State
import dash_bootstrap_components as dbc
from mongoDB import database
from datetime import date,datetime
import pytz

from inputs import people

for person in people:
    dash.register_page(__name__, path_template='/<daily_id>-daily')
# data_base = database()

layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='daily-container', style={'textAlign': 'center'}),
   
])

@callback(
    Output('daily-container', 'children'),
    Input('url', 'pathname')
)
def update_profile(pathname):

    profile_id = pathname.strip('/')
    name_first = profile_id.split('-')[0]
    person = next((p for p in people if p['name_first'] == name_first), None)

    if not person:
        return html.Div("Daily not found.", style={'textAlign': 'center'})

    return html.Div([
    html.H4(f'welcome {person["name_first"]}',style={'textAlign':'center'}),
    html.Div(style={'padding': '20px'}),
    html.Div('how depressed are you today (1-10)?',style={'textAlign':'center'}),
    html.Div(style={'padding': '5px'}),
    dbc.Col(
        dbc.Select(id="depressionlvl",placeholder="depression level",
            options=[
                {"label": f"{i}","value": f"{i}"} for i in range(1,11)
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
    dcc.Store(id='dval'),
    dcc.Store(id='dreason'),
    dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle(f"""thanks for submitting {person["name_first"]}""")),
        dbc.ModalBody("hopefully tomorrow is a better day :)"),
        dbc.ModalFooter(
            dcc.Link("return to home",href='/'),#dash.page_registry['pages.ahome']['path']),
        ),
    ],
    id="modal",
    is_open=False,
),
])

# @callback(
#     Output('dval','data'),
#     Input('depressionlvl','value')
# )
# def rating(depressionlvl):
#     return depressionlvl

# @callback(
#     Output('dreason','data'),
#     Input('reason','value')
# )
# def rating(reason):
#     return reason

# @callback(
#     Output('modal','is_open'),
#     Input('btn_submit', 'n_clicks'),
#     Input('dval','data'),
#     Input('dreason','data'),
#     [State("modal", "is_open")],
#     allow_duplicate=True
# )
# def rating(btn_submit,dval,dreason,is_open):
#     #changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    
#     if btn_submit and dval is not None:
#         print(dval)
#         print(dreason)
#         eastern_tz = pytz.timezone("US/Eastern")
#         submitted_date = datetime.now(eastern_tz).strftime("%Y-%m-%d")
#         #submitted_date = date.today().strftime("%Y-%m-%d")
#         data = {
#             'name': 'sara',
#             'dval': int(dval),
#             'dreason': dreason,
#             'date': submitted_date
#         }
        
#         data_base.collection.insert_one(data)
#         return not is_open
#     return is_open
