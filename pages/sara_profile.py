import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H4("sara's profile"),
    html.Div('check out how sad she is'),
])