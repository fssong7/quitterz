import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H4('last update: 3/11/25'),
    html.H4('updates to do'),
    html.Div('-sidebar'),
    html.Div('-calendar with strava bubbles'),
    html.Div('-last 30 day and 7 day avg'),
    html.Div('-send encouraging note to fellow quitter'),
    html.Div('-enable profile picture upload'),
    html.Div('-achievements, for example for most/least depressed, most improved, biggest downward trend'),
    html.Div('-aesthetics (half as good as sara barrows site)'),
])