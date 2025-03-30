import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H4('last bug fixes update: 3/29/25'),
    html.Div('-reverse table list'),
    html.Div('-date timezone issue'),
    html.Div('-comparison page'),

    html.H4('next major updates'),
    html.Div('-calendar with strava bubbles'),
    html.Div('-send encouraging note to fellow quitter'),
    html.Div('-profile picture upload'),
    html.Div('-achievements, for example for most/least depressed, most improved, biggest downward trend'),
    html.Div('-aesthetics (half as good as sara barrows site)'),
    html.Div('-dskafj;lsdkfjsdklfja;ksldfj ji i hate myself'),
    #html.Div('-reverse order of datatable'),
    html.Div('-moving averages')
])