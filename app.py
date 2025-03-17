import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH],use_pages=True,suppress_callback_exceptions=True)
server = app.server
app.layout = html.Div([
    html.H1('quitterz depression tracker',style={'textAlign':'center'}),
    html.Div('keeping tabs on how we feel until we become happy or die',style={'textAlign':'center'},),
    
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container,
])

if __name__ == '__main__':
    app.run(debug=True)

# Enter: check in page, select name
# Once entered, input selection for rating, optional
# submitted page -> option to check out other quitter ratings, your own
# GE0SsNARhMKigDzv