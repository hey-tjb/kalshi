from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY
from dotenv import dotenv_values
import requests
import pandas as pd
import time
import json
config = dotenv_values('.env')

host: str = "https://clob.polymarket.com"
key: str = config['MAGIC_PRIVATE_KEY'] #This is your Private Key. Export from https://reveal.magic.link/polymarket or from your Web3 Application
chain_id: int = 137 #No need to adjust this
POLYMARKET_PROXY_ADDRESS: str = config['POLYMARKET_ADDRESS'] #This is the address listed below your profile picture when using the Polymarket site.

### Initialization of a client using a Polymarket Proxy associated with a Browser Wallet(Metamask, Coinbase Wallet, etc)
client = ClobClient(host, key=key, chain_id=chain_id, signature_type=2, funder=POLYMARKET_PROXY_ADDRESS)

response = requests.get('https://data-api.polymarket.com/trades')
response.json()

resp = client.get_markets(next_cursor = "")
print(resp)
len(resp['data'])

# Gamma API endpoint to get historical and current level market data
def get_all_markets():
    all_markets = []
    offset = 0
    limit = 100  # max allowed
    while True:
        response = requests.get(
            "https://gamma-api.polymarket.com/markets",
            params={"offset": offset, "limit": limit},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        all_markets.extend(data)
        if len(data) < limit:
            break  # last page
        offset += limit
        time.sleep(0.2)  # rate limit protection
    return all_markets


a = get_all_markets()
import gzip
with open('data/polymarket_data.json', 'w') as f:
    json.dump(a, f, indent=2)

with gzip.open("data/polymarket_data.json.gz", "wt", encoding="utf-8") as f:
    json.dump(a, f)
