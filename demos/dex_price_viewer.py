import dash
from dash import dcc
from dash import html

from base import BaseDemo


class DEXPriceViewer(BaseDemo):
    """
    This demo launches a simple web application that allows you to
    view a price chart of an on-chain token asset given its symbol.

    Parameters:
        - api_key: Your Transpose API key.
    """

    def __init__(self, api_key: str) -> None:
        super().__init__(api_key=api_key, name="DEX Price Viewer")
        
    
    def run(self) -> None:
        
        # create Dash app
        app = dash.Dash(__name__)
        app.layout = html.Div(children=[
            html.H1(children='Hello Dash'),
            html.Div(children='''
                Dash: A web application framework for Python.
            '''),
            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                    ],
                    'layout': {
                        'title': 'Dash Data Visualization'
                    }
                }
            )
        ])
        app.run_server(debug=True)