from dataclasses import dataclass


@dataclass
class MarketState:
    bestAskPrice : float
    bestAskDepth : float
    bestAskVolume : float

class MarketData:
    question: str | None
    clobTokenIds: list[str] | None
    groupItemTitle: str
    marketId: str
    YESMarketData: MarketState | None
    NOMarketData: MarketState | None

    def __init__(self, question: str, clobTokens: list[str], groupItemTitle: str, conditionID: str, marketId: str):
        self.question = question
        self.marketID = marketId
        self.clobTokenIds = clobTokens
        self.groupItemTitle = groupItemTitle
        self.conditionId = conditionID 
        self.YESMarketData = None
        self.NOMarketData = None
    
    def getYESPrice():
        """
        Fetches most recently stored price for the "Yes" side
        """

    def getYESDepth():
        """
        Fetches most recently stored price for the "Yes" side
        """
        pass

    def getNODepth():
        pass



    

