from dotenv import load_dotenv
import os

from demos.nft_sales_scatterplot import NFTSaleScatterplot
from demos.token_price_chart import TokenPriceChart
from demos.dex_price_viewer import DEXPriceViewer


if __name__ == "__main__":
    load_dotenv()

    # DEMO 1: NFT Sale Scatterplot
    # NFTSaleScatterplot(
    #     api_key=os.getenv("TRANSPOSE_API_KEY"),
    #     contract_address="0xe2e27b49e405f6c25796167B2500C195F972eBac",
    #     start_dt='2023-03-04',
    #     stop_dt='2023-03-05'
    # ).run()
    
    # DEMO 2: Token Price Chart
    # TokenPriceChart(
    #     api_key=os.getenv("TRANSPOSE_API_KEY"),
    #     chain="canto",
    #     token_address="0x826551890Dc65655a0Aceca109aB11AbDbD7a07B",
    #     timeframe='hour',
    #     window='2 weeks'
    # ).run()

    # DEMO 3: DEX Price Viewer
    DEXPriceViewer(
        api_key=os.getenv("TRANSPOSE_API_KEY")
    ).run()
