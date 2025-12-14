from dataclass import dataclass

class MarketData:
    question: str | None
    clobTokenIds: list[str] | None
    YESMarketData: MarketState | None
    NOMarketData: MarketState | None

    def __init__(self, question: str, clobTokens: list[str], conditionID: str, marketId: str):
        self.question = question
        self.clobTokenIds = clobTokens
        self.conditionID = conditionId 
        self.marketID = marketId
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

    def getNODepth():
        pass



@dataclass
class MarketState:
    bestAskPrice : float
    bestAskDepth : float
    bestAskVolume : float
    

