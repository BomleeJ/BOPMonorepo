from urllib.parse import urlparse
from internal_data.MarketData import MarketData
import httpx
import json

class ArbGroupFactory():
    def __init__(self, eventURL):
        self.eventURL = eventURL
        self.polymarketData = self.getPolyMarketData()
        self.marketData = self.get("markets")
        

    def getPolyMarketData(self):
        slug = self.getSlug(self.eventURL)
        
        url = f"https://gamma-api.polymarket.com/events/slug/{slug}"
        res = httpx.get(url)  
           
        if res.status_code != 200:
            raise Exception(f"Unable to fetch market data for {self.eventURL}")

        return res.json()

    def get(self, key: str):
        return self.polymarketData.get(key)

    def getMarketDataWrapper(self, itemTitles):
        if itemTitles:
            return self.createMarketDataObjects(itemTitles)
        return [self.createMarketDataObject()]

    def createMarketDataObjects(self, groupItemTitles: str):
        markets = []
        for m in self.marketData:
            groupTitle = m.get("groupItemTitle")
            if groupTitle in groupItemTitles:
                markets.append(self.createMarketDataObject(m))
                groupItemTitles.remove(groupTitle)

        if groupItemTitles:
            print(f"WARNING: NOT ALL MARKETS REPRESENTED for {self.polymarketData.get("title")} MISSING DATA FOR ")

            for t in groupItemTitles:
                print(f"{t}", end=" ")

        return markets
            
        
    def createMarketDataObject(self, individualMarketData = None):
        if not individualMarketData:
            individualMarketData = self.marketData[0]
            
        question = individualMarketData.get("question")
        marketID = individualMarketData.get("id")
        groupTitle = individualMarketData.get("groupItemTitle")
        conditionId = individualMarketData.get("conditionId")
        clobIdString = individualMarketData.get("clobTokenIds")
        clobIds = json.loads(clobIdString)
        return MarketData(
            question=question,
            marketId=marketID,
            clobTokens=clobIds,
            groupItemTitle=groupTitle,
            conditionID=conditionId
        )
        


    def getSlug(self, url: str) -> str:
        """
        Extracts the slug from a Polymarket event URL.
        
        Args:
            url: A Polymarket URL in the format:
                 https://polymarket.com/event/{slug} or
                 https://polymarket.com/event/{slug}?tid=...
        
        Returns:
            The slug (the part after /event/ and before any query parameters)
        
        Example:
            getSlug("https://polymarket.com/event/will-draftkings-launch-a-prediction-market-in-2025?tid=1765738013669")
            Returns: "will-draftkings-launch-a-prediction-market-in-2025"
        """
        parsed = urlparse(url)
        parts = parsed.path.strip("/").split("/")
        if len(parts) < 2 or parts[0] != "event":
            raise ValueError("URL is not a Polymarket event URL")

        return parts[1]

class ArbGroup:
    def __init__(self, eventURL1: str, eventURL2: str, groupItemTitles1: set[str] | None = None, groupItemTitles2: set[str] | None = None ):
        self.eventURLs = [eventURL1, eventURL2] # list[str]

        factory1 = ArbGroupFactory(eventURL1)
        factory2 = ArbGroupFactory(eventURL2)


        self.eventTitles = [factory1.get("title"), factory2.get("title")] # str
        self.marketGroup1 = factory1.getMarketDataWrapper(groupItemTitles1)
        self.marketGroup2 = factory2.getMarketDataWrapper(groupItemTitles2)
    
    def __repr__(self):
        """Return a string representation of ArbGroup"""
        market_count_1 = len(self.marketGroup1) if isinstance(self.marketGroup1, list) else 1 if self.marketGroup1 else 0
        market_count_2 = len(self.marketGroup2) if isinstance(self.marketGroup2, list) else 1 if self.marketGroup2 else 0
        
        return (f"ArbGroup(eventTitles={self.eventTitles}, "
                f"marketGroup1_count={market_count_1}, marketGroup2_count={market_count_2}, "
                f"eventURLs={self.eventURLs})")

    def getTotalM1YesPrice(self):
        price = 0.0
        for market in self.marketGroup1:
            price += market.getYESPrice()
        return price
    
    def getTotalM2YesPrice(self):
        price = 0.0
        for market in self.marketGroup2:
            price += market.getYESPrice()
        return price

    def getTotalM2YESPrice(self):
        price = 0.0
        for market in self.marketGroup2:
            price += market.getNOPrice()
        return price
    
    def getTotalM2NoPrice(self):
        price = 0.0
        for market in self.marketGroup2:
            price += market.getNOPrice()
        return price

    def hasArb(self):
        return (
            self.getTotalM1YesPrice() + 
            self.getTotalM2NoPrice() < 1.0 
        or 
            self.getTotalM1NOPrice() + 
            self.getTotalM2YESPrice() < 1.0
        )
        
        



        
    def __iter__(self):
        yield from self.marketGroup1
        yield from self.marketGroup2
    
    


