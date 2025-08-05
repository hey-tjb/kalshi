import requests
import pandas as pd
import time
from tqdm import tqdm
import json

BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"

def get_all_series():
    """Fetches a list of active markets."""
    response = requests.get(f"{BASE_URL}/series")
    if response.ok:
        return response.json()
    else:
        raise Exception(f"Failed to fetch series: {response.status_code} {response.text}")

s = get_all_series()

categories = []
for i in s['series']:
    categories.append(i['category'])

from collections import Counter

counts = Counter(categories)

print(counts)

s['series'][0]
def get_market(series_ticker):
    """Fetch individual market details."""
    url = f"{BASE_URL}/markets?series_ticker={series_ticker}&limit=100"
    response = requests.get(url)
    if not response.ok:
        print(f"[Warning] Failed to fetch market {series_ticker}: {response.status_code}")
        return None
    return response.json()

def get_order_book(series_ticker):
    """Fetch the order book for a market."""
    url = f"{BASE_URL}/markets/{series_ticker}/orderbook"
    response = requests.get(url)
    if not response.ok:
        print(f"[Warning] Failed to fetch order book for {series_ticker}: {response.status_code}")
        return None
    return response.json()

def get_data():
    print("Fetching all series...")
    series = get_all_series()
    s = series['series']
    market_results = []
    orderbook_results = []
    print(f"Found {len(s)} series. Fetching market and order book data...\n")
    # for entry in series['series']:
    for entry in tqdm(s, desc="Fetching market data"):
        market_ticker = entry.get("ticker")
        market_data = get_market(market_ticker)
        order_book = get_order_book(market_ticker)
        if market_data:# and order_book:
            market_results.append(market_data)
        if order_book:
            orderbook_results.append(order_book)
        time.sleep(0.2)  # To avoid rate limiting
    return market_results, orderbook_results

m, o = get_data()
len(m)
len(o)

with open('kalshi_ob_data.json', 'w') as f:
    json.dump(o, f, indent=2)
