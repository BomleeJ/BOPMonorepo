import httpx
import pprint

import httpx

# url = "https://gamma-api.polymarket.com/events/slug/will-draftkings-launch-a-prediction-market-in-2025"


url = "https://gamma-api.polymarket.com/events/slug/democratic-presidential-nominee-2028"

res = httpx.get(url)

print(res.json())
"""

from py_clob_client.client import ClobClient
import asyncio

client = ClobClient(
    host="https://clob.polymarket.com",
    chain_id=137
)

markets = client.get_market("0xf723d076576a434c0b92914608ab73ba9c56b2197f5bd9476ccd48a2c6dee12b")

pprint.pprint(markets)

"""