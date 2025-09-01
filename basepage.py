import dash
from dash import Dash, html, dcc, callback,callback_context,Output, Input

from inputs import people

class BasePage():

    def __init__(self):
        self.variables()
        self.styles()


    def variables(self):
        self.names_first=[person['name_first'] for person in people]
        self.names_last = [person['name_last'] for person in people]



    def styles(self):
        
        self.style_center={'textAlign':'center'}


        self.style_home_button={'display': 'flex',
            'flexDirection': 'row',
            'border': '1px solid', 
            'padding': '10px',
            'borderRadius': '5px',
            'margin': '5px',
            'textAlign': 'center'
        }

        self.style_home_buttons={
            'display': 'flex',
            'flexDirection': 'row',  
            'alignItems': 'center',
            'justifyContent': 'center',
            'flexWrap': 'wrap' 
        }

        self.style_padding_20px={'padding': '20px'}
        
        self.style_1={'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'flexWrap': 'wrap',
            'width': '100%'
        }

        self.style_2={'padding': '10px 20px',
            'width': '100%',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'flexWrap': 'wrap',
        }

        self.style_no_text_decoration={'textDecoration': 'none'}

    # def register(self, path, name=__name__):
    #     dash.register_page(name, path=path)


    # def create_layout(self):
    #     return html.Div()
    
    # def callbacks(self):
    #     pass