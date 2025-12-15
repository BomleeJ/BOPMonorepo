import httpx
import pprint
from internal_data.ArbGroup import ArbGroup
from internal_data.MarketData import MarketData
import csv

def read_csv(csv_name: str) -> list[ArbGroup]:
    arbGroups = []
    with open(csv_name, newline='') as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)
        it = iter(reader)
        for row1, row2 in zip(it, it):
            arb_id = row1[0]
            eventURL1 = row1[1]
            eventURL2 = row2[1]

            groupItemTitles1 = { row1[i] for i in range(2, len(row1)) if row1[i] }
            groupItemTitles2 = { row2[i] for i in range(2, len(row2)) if row2[i] }

            if not groupItemTitles1:
                groupItemTitles1 = None

            if not groupItemTitles2:
                groupItemTitles2 = None
            a = ArbGroup(eventURL1, eventURL2, groupItemTitles1, groupItemTitles2)
            arbGroups.append(a)
            print(a)
    
    return arbGroups

if __name__ == '__main__':
    read_csv("din.csv")


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