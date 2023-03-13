import pandas as pd
from plotly.graph_objects import Figure, Candlestick

from demos.utils.api import call_transpose_sql_api
from base import BaseDemo


SQL_QUERY =\
    """
    SELECT
        agg._date,
        agg._low,
        agg._high,
        MAX.price AS _open,
        MIN.price AS _close
    FROM
        (
            SELECT
                DATE_TRUNC('{{timeframe}}', TIMESTAMP) AS _date,
                MIN(price) AS _low,
                MAX(price) AS _high,
                MIN(block_number) AS lbn,
                MAX(block_number) AS gbn
            FROM
                {{chain}}.token_prices
            WHERE
                token_address = '{{token_address}}'
                AND TIMESTAMP >= NOW() - INTERVAL '{{window}}'
            GROUP BY
                _date
        ) AS agg
        JOIN {{chain}}.token_prices AS MAX ON token_address = '{{token_address}}'
        AND block_number = agg.lbn
        JOIN {{chain}}.token_prices AS MIN ON MIN.token_address = '{{token_address}}'
        AND MIN.block_number = agg.gbn
    ORDER BY
        _date DESC
    """


class TokenPriceChart(BaseDemo):
    """
    This demo charts the price of a token over time on any chain.

    Parameters:
        - api_key: Your Transpose API key.
        - chain: The chain to query.
        - token_address: The token address to query.
    """

    def __init__(self, api_key: str, chain: str, token_address: str, timeframe: str, window: str) -> None:
        super().__init__(api_key=api_key, name="DEX Price Viewer")
        self.chain = chain
        self.token_address = token_address
        self.timeframe = timeframe
        self.window = window

    
    def run(self) -> None:

        # fetch token price data
        data = call_transpose_sql_api(
            api_key=self.api_key,
            query=SQL_QUERY,
            params={
                'chain': self.chain,
                'token_address': self.token_address,
                'timeframe': self.timeframe,
                'window': self.window
            }
        )

        # parse response
        data = pd.DataFrame(data)
        if len(data) == 0:
            print("No data found for this token address.")
            return
        
        # plot candlestick chart
        fig = Figure(
            data=[
                Candlestick(
                    x=data['_date'],
                    open=data['_open'],
                    high=data['_high'],
                    low=data['_low'],
                    close=data['_close']
                )
            ]
        )
        fig.update_layout(
            title=f"Price of {self.token_address} on {self.chain}",
            xaxis_title="Date",
            yaxis_title="Price (USD)"
        )
        fig.show()