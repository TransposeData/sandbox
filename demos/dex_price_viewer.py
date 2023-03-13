from dash import Dash, dcc, html, Input, Output, State
from dash import dcc
from dash import html

from demos.utils.api import call_transpose_custom_endpoint
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
        title = "DEX Price Viewer"
        description =\
            """
            This webapp demos a simple project built with Transpose custom endpoints
            that allows you to view a price chart for any on-chain token asset given its symbol.
            Simply enter a token symbol and the webapp will leverage a first custom endpoint
            to fetch the most popular contract address given the inputted symbol, and then a
            second custom endpoint to fetch the hourly OHLC data over the last week for 
            that contract address.
            """
        
        # create Dash app and layout
        app = Dash(__name__)
        app.layout = html.Div(children=[
            html.H1(children=title, style={'margin': '20px'}),
            html.P(children=description, style={'margin-left': '40px', 'margin-bottom': '30px', 'width': '700px'}),
            html.Div(children=[
                html.Label('Token Symbol:', style={'margin-left': '70px', 'font-weight': 'bold'}),
                dcc.Input(id='token-symbol', placeholder='ETH', type='text', style={'margin-left': '10px', 'width': '100px'}),
                html.Button('Submit', id='submit-button', style={'margin-left': '2px'})
            ]),
            html.P(id='error-message', style={'display': 'none'}),
            dcc.Graph(id='price-chart', style={'display': 'none'})
        ])

        # add callback to update chart on input
        @app.callback(
            [Output('price-chart', 'figure'), Output('price-chart', 'style'), Output('error-message', 'children'), Output('error-message', 'style')], 
            [Input('submit-button', 'n_clicks')], [State('token-symbol', 'value')]
        )
        def update_chart(n_clicks, input_value):
            if n_clicks is None: return {}, {'display': 'none'}, '', {'display': 'none'}

            # add default return values
            figure = {}
            figure_style = {'display': 'none'}
            error_message = ''
            error_message_style = {'display': 'none'}

            # process symbol input
            symbol = input_value.upper().replace(' ', '').strip()
            if symbol is None or symbol == '':
                error_message = 'Please enter a token symbol.'
                error_message_style = {'margin-left': '70px', 'color': 'red'}
                return figure, figure_style, error_message, error_message_style

            # run endpoint 1: get contract address from symbol
            try:
                contract_addresses = call_transpose_custom_endpoint(api_key=self.api_key, endpoint_name='token-symbol-to-address', params={'symbol': symbol})
                if len(contract_addresses) == 0:
                    error_message = f'No contract address with recent activity found for symbol {symbol}.'
                    error_message_style = {'margin-left': '70px', 'color': 'red'}
                    return figure, figure_style, error_message, error_message_style
                contract_address = contract_addresses[0]['contract_address']
            except Exception as e:
                error_message = f'Error fetching contract address for symbol {symbol}: {str(e)}'
                error_message_style = {'margin-left': '70px', 'color': 'red'}
                return figure, figure_style, error_message, error_message_style

            # run endpoint 2: get OHLC data from contract address
            try:
                ohlc_data = call_transpose_custom_endpoint(api_key=self.api_key, endpoint_name='token-ohlc-prices', params={'token_address': contract_address, 'timeframe': 'hour', 'window': '7 days'})
                if len(ohlc_data) == 0:
                    error_message = f'No OHLC data found for symbol {symbol}.'
                    error_message_style = {'margin-left': '70px', 'color': 'red'}
                    return figure, figure_style, error_message, error_message_style
            except Exception as e:
                error_message = f'Error fetching OHLC data for symbol {symbol}: {str(e)}'
                error_message_style = {'margin-left': '70px', 'color': 'red'}
                return figure, figure_style, error_message, error_message_style
            
            # update chart
            figure = {
                'data': [{
                    'x': [row['_date'] for row in ohlc_data],
                    'open': [row['_open'] for row in ohlc_data],
                    'high': [row['_high'] for row in ohlc_data],
                    'low': [row['_low'] for row in ohlc_data],
                    'close': [row['_close'] for row in ohlc_data],
                    'type': 'candlestick',
                    'name': symbol
                }],
                'layout': {
                    'title': f'Last week OHLC bars for {symbol} ({contract_address})',
                    'yaxis': {'title': 'Price (USD)'}
                }
            }
            figure_style = {'margin-left': '70px', 'width': '1500px', 'height': '500px'}
            return figure, figure_style, error_message, error_message_style
        
        # run server
        app.run_server(debug=True)