import httpx
from internal_data.ArbGroup import ArbGroup
from internal_data.MarketData import MarketData
from data_output.emailsend import send_email
from py_clob_client.client import ClobClient, BookParams
import time
import asyncio
import csv
from dotenv import load_dotenv
import os
import json

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
    
    return arbGroups

def load_settings():
    with open("setting.json") as f:
        settings = json.load(f)
    return settings

def main():
    csv = "din.csv"
    ArbGroups = read_csv(csv)
    settings = load_settings()

    TIMER_THRES = settings.get("cooldown_seconds")
    ArbThres = settings.get("threshold")
    fetch_frequency = settings.get("fetch_frequency")
    emails = settings.get("emails")

    
    YesMarketCLOBIds = []
    NoMarketClobIds = [] 

    conditionID_to_marketMap = {}

    for ArbGroup in ArbGroups:
        for market in ArbGroup:
            yesClobId = market.clobTokenIds[0]
            noClobId = market.clobTokenIds[1]
            conditionID_to_marketMap[market.conditionId] = market
            YesMarketCLOBIds.append(BookParams(token_id=yesClobId))
            NoMarketClobIds.append(BookParams(token_id=noClobId))
    
    client = ClobClient(
        host="https://clob.polymarket.com",
        chain_id=137
    )
    count = 0
    seen = set()

    last_sent = time.monotonic()

    while True:
        print("Fetching Data...")
        YesOrderBooks = client.get_order_books(YesMarketCLOBIds)
        NoOrderBooks = client.get_order_books(NoMarketClobIds)
        
        
        for orderbook in YesOrderBooks:
            conditionID = orderbook.market
            bestAskSummary = min(orderbook.asks, key=lambda x : x.price)
            price, depth = bestAskSummary.price, bestAskSummary.size
            
            market = conditionID_to_marketMap[conditionID]
            market.setYesMarketData(price, depth)
        
        for orderbook in NoOrderBooks:
            conditionID = orderbook.market
            bestAskSummary = min(orderbook.asks, key=lambda x : x.price)
            
            price, depth = bestAskSummary.price, bestAskSummary.size
            
            market = conditionID_to_marketMap[conditionID]
            market.setNoMarketData(price, depth)

        for arbGroup in ArbGroups:
            if arbGroup.hasArb(ArbThres) and arbGroup not in seen:
                email_body = arbGroup.getArbStr()
                for email in emails:
                    send_email(email_body, email)

        
        time.sleep(fetch_frequency)

        if time.monotonic() - last_sent > TIMER_THRES:
            seen = set()
        

    

if __name__ == '__main__':
    main()
    
