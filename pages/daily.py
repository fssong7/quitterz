import dash
from dash import Dash, html, dcc, callback,callback_context,Output, Input,State
import dash_bootstrap_components as dbc
from mongoDB import database
from datetime import date,datetime
import pytz


from statCalculator import dataAnalyzer

from inputs import people

for person in people:
    dash.register_page(__name__, path_template='/<daily_id>-daily')

data_base = database()

layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='daily-container', style={'textAlign': 'center'}),
    dcc.Store(id='daily-name'),
   
])

@callback(
    Output('daily-name', 'data'),
    Input('url', 'pathname')
)
def fetch_person(pathname):
    # if not pathname:
    #     return {}  # instead of None, return empty dict
    # profile_id = pathname.strip('/')
    # name_first = profile_id.split('-')[0]
    # return next((p for p in people if p['name_first'] == name_first), {})
  
    if not pathname:
        return {}  # no URL yet
    
    profile_id = pathname.strip('/')
    name_first = profile_id.split('-')[0]

    # 🔹 Try to find existing person
    person = next((p for p in people if p['name_first'] == name_first), None)

    if not person:
        # 🔹 If not found, create a new one with default pronouns
        person = {
            "name_first": name_first,
            "name_last": "",
            "pronoun_sub": "they",
            "pronoun_obj": "their"
        }
        people.append(person)
        analyzers[name_first] = dataAnalyzer()

    return person



@callback(
    Output('daily-container', 'children'),
    Input('daily-name', 'data')
)
def update_profile(person):

    # profile_id = pathname.strip('/')
    # name_first = profile_id.split('-')[0]
    # person = next((p for p in people if p['name_first'] == name_first), None)

    if not person:
        return html.Div("Daily not found.", style={'textAlign': 'center'})
    # print(person["name_first"])
    
    return html.Div([
        html.H4(f'welcome {person["name_first"]}', id='welcome',style={'textAlign':'center', 'marginBottom': '40px'}),
        
        html.Div('how depressed are you today (1-10)?',style={'textAlign':'center', 'marginBottom': '10px'}),
        
        html.Div(dbc.Col(
            dbc.Select(id="depressionlvl",placeholder="depression level",
                options=[
                    {"label": f"{i}","value": f"{i}"} for i in range(1,11)
                ],
            ),
            width={"size":8,"offset":2},
        ), style={'marginBottom': '20px'}),

        html.Div('and why is that? (optional)',style={'textAlign':'center'}),

        html.Div(
            dbc.Col(dbc.Input(id="reason",type="text",placeholder="your 13th reason"),width={"size":10,"offset":1}),
        style={'marginBottom': '40px'}),
        
        dbc.Button(
            "submit", id="btn_submit", size = "lg",className="d-grid gap-1 col-6 mx-auto", n_clicks=0,
        ),

        # html.Div(id='dbtn'),
        # dcc.Store(id='dval'),
        # dcc.Store(id='dreason'),

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



@callback(
    Output('modal','is_open'),
    Input('btn_submit', 'n_clicks'),
    State("daily-name", "data"),
    State('depressionlvl','value'),
    State('reason','value'),
    prevent_initial_call=True
)
def rating(btn_submit,name,depressionlvl,reason):
    #changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    
    if btn_submit and depressionlvl is not None:
        print(depressionlvl)
        print(reason)
        eastern_tz = pytz.timezone("US/Eastern")
        submitted_date = datetime.now(eastern_tz).strftime("%Y-%m-%d")
        #submitted_date = date.today().strftime("%Y-%m-%d")
        data = {
            'name': name["name_first"],
            'dval': int(depressionlvl),
            'dreason': reason,
            'date': submitted_date
        }
        data_base.collection.insert_one(data)
        return True
        
        
    return False

