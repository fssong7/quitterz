import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H4('last update: 3/18/25'),
    html.H4('updates to do'),
    html.Div('-calendar with strava bubbles'),
    html.Div('-send encouraging note to fellow quitter'),
    html.Div('-profile picture upload'),
    html.Div('-achievements, for example for most/least depressed, most improved, biggest downward trend'),
    html.Div('-aesthetics (half as good as sara barrows site)'),
    html.Div('-dskafj;lsdkfjsdklfja;ksldfj ji i hate myself'),
])