import dash
from dash import Dash, html, dcc, callback,callback_context,Output, Input
import dash_bootstrap_components as dbc

from inputs import people

dash.register_page(__name__, path='/')

layout = html.Div(
    [
        html.Div([
            dcc.Link(
                dbc.Button(
                    f"{person['name_first']} {person['name_last']}",
                    id=f"btn-nclicks-{person['name_first']}-{person['name_last']}",
                    size="lg",
                    className="d-grid gap-1 col-8 mx-auto",
                    n_clicks=0,
                ),
                href=f"/{person['name_first']}-daily",
                style={"text-decoration": "none"},
            ),
            html.Div(style={'padding': '5px'}),
        ])
        for person in people
    ] +
    [html.Div(id='empty_container')]
)

@callback(
    Output('empty_container', 'children'),
    [Input(f"""btn-nclicks-{person["name_first"]}-{person["name_last"]}""",'n_clicks') for person in people],

)

def displayClick(*btns):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    for person in people:
        btn_id = f'btn-nclicks-{person["name_first"]}-{person["name_last"]}'
        if btn_id in changed_id:
            print(f'{person["name_first"]} pressed')
    return 