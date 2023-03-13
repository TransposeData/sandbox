import requests


def call_transpose_sql_api(api_key: str, query: str, params: dict) -> list:

    # fetch NFT sales data
    response = requests.post(
        url='https://api.transpose.io/sql',
        headers={
            'X-Api-Key': api_key
        },
        json={
            'sql': query,
            'parameters': params
        }
    )

    # parse response
    response.raise_for_status()
    results = response.json()['results']
    return results


def call_transpose_custom_endpoint(api_key: str, endpoint_name: str, params: dict) -> dict:
    param_string = '&'.join([f'{k}={v}' for k, v in params.items()])

    # fetch NFT sales data
    response = requests.get(
        url=f'https://api.transpose.io/endpoint/{endpoint_name}?{param_string}',
        headers={'X-Api-Key': api_key}
    )

    # parse response
    response.raise_for_status()
    results = response.json()['results']
    return results