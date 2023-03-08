from dotenv import load_dotenv
import os

from demos.nft_sales_scatterplot import NFTSaleScatterplot
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

    # DEMO 2: DEX Price Viewer
    DEXPriceViewer(
        api_key=os.getenv("TRANSPOSE_API_KEY")
    ).run()
