import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H4('modularize: 9/6/25'),
    html.Div("9/1/25 - sara gets access to repo and applys her type A mindset to codebase."),

    html.H4('most recent update: 6/3/25'),
    html.Div('-fixed issue where grace wasnt being compared (srry grace)'),
    html.Div('-wrap tables (ty sara)'),
    html.Div('-memories'),
    html.Div('-submit entries for days you may have missed'),

    html.H4('prev update: 3/29/25'),
    html.Div('-reverse table list'),
    html.Div('-date timezone issue'),
    html.Div('-comparison page'),

    html.H4('next major updates (never happening)'),
    html.Div('-calendar with strava bubbles'),
    html.Div('-send encouraging note to fellow quitter'),
    html.Div('-profile picture upload'),
    html.Div('-achievements, for example for most/least depressed, most improved, biggest downward trend'),
    html.Div('-aesthetics (half as good as sara barrows site)'),
    html.Div('-dskafj;lsdkfjsdklfja;ksldfj ji i hate myself'),
    #html.Div('-reverse order of datatable'),
    html.Div('-moving averages')
], style={'margin': '0 40px'})