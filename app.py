import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


from inputs import people, styles


class MainApp():

    def __init__(self, app):
        super().__init__()
        self.app = app 
        # self.server = self.app.server


        self.app.layout = html.Div([
            self.ahome()
        ])
        
    


    def ahome(self):
        return html.Div([
                html.H1('quitterz depression tracker',style=styles["center"]),
                html.Div('keeping tabs on how we feel until we become happy or die',style=styles["center"]),
                html.Div(
                    children=[
                        html.Div([
                            html.Div(
                                dcc.Link('home', href='/', style=styles["no_text_decoration"]),
                                style=styles["home_button"]
                            ),
                            html.Div([
                                html.Div(
                                    dcc.Link(f"""{person["name_first"]}'s profile""", href=f'/{person["name_first"]}-profile', style=styles["no_text_decoration"]),
                                    style=styles["home_button"]
                                ) for person in people
                            ], 
                            style=styles["home_buttons"]),
                            

                            html.Div(
                                dcc.Link("compare", href='/compare', style=styles["no_text_decoration"]),
                                style=styles["home_button"]
                            ),
                            html.Div(
                                dcc.Link("old", href='/old', style=styles["no_text_decoration"]),
                                style=styles["home_button"]
                            ),
                            html.Div(
                                dcc.Link("memories", href='/memories', style=styles["no_text_decoration"]),
                                style=styles["home_button"]
                            ),  
                            html.Div(
                                dcc.Link("updates", href='/updates', style=styles["no_text_decoration"]),
                                style=styles["home_button"]
                            ),               
                        ], style=styles["one"]),
                    ],
                    style=styles["two"]
                ),

                
                html.Div(style=styles["padding_20px"]),
                dash.page_container,
            ])


if __name__ == '__main__':
    dash_app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH], use_pages=True, suppress_callback_exceptions=True)
    server = dash_app.server  # keep the server
    app = MainApp(dash_app)   # wrap dash app in your class
    dash_app.run_server(debug=True, port=8063)
