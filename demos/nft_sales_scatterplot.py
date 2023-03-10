from dateutil import parser
import plotly.express as px
import pandas as pd

from demos.utils.api import call_transpose_sql_api
from base import BaseDemo


SQL_QUERY =\
    """
    SELECT timestamp, usd_price, exchange_name FROM ethereum.nft_sales
    WHERE contract_address = '{{contract_address}}'
    AND timestamp >= '{{start_dt}}'
    AND timestamp <= '{{stop_dt}}'
    AND usd_price IS NOT NULL
    AND usd_price > 0
    AND is_multi_token_sale = FALSE
    ORDER BY timestamp ASC;
    """


class NFTSaleScatterplot(BaseDemo):
    """
    This demo takes an NFT collection and a time range and plots 
    a scatterplot of the USD price for all sales in the collection
    during the time range.

    Parameters:
        - api_key: Your Transpose API key.
        - contract_address: The address of the NFT collection contract.
        - start_time: The start time of the time range as a datetime string.
        - stop_time: The stop time of the time range as a datetime string.
    """

    def __init__(self, api_key: str, contract_address: str, start_dt: str, stop_dt: str) -> None:
        super().__init__(api_key=api_key, name="NFT Sale Scatterplot")
        self.api_key = api_key
        self.contract_address = contract_address
        self.start_dt = parser.parse(start_dt)
        self.stop_dt = parser.parse(stop_dt)


    def run(self) -> None:
        
        # fetch NFT sales data
        results = call_transpose_sql_api(self.api_key, SQL_QUERY, {
            'contract_address': self.contract_address,
            'start_dt': self.start_dt.isoformat(),
            'stop_dt': self.stop_dt.isoformat()
        })

        # parse response
        data = pd.DataFrame(results)
        if len(data) == 0:
            print("No data found for this contract address.")
            return
        
        # plot scatterplot
        fig = px.scatter(data_frame=data, x="timestamp", y="usd_price", color="exchange_name")
        fig.show()