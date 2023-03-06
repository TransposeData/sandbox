from demos.nft_sales_scatterplot import NFTSaleScatterplot


if __name__ == '__main__':
    demo = NFTSaleScatterplot(
        api_key='',
        contract_address='0xe2e27b49e405f6c25796167B2500C195F972eBac',
        start_dt='2023-03-04T00:00:00Z',
        stop_dt='2023-03-06T00:00:00Z'
    )

    demo.run()