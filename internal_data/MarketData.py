from dataclasses import dataclass


@dataclass
class MarketState:
    bestAskPrice : float
    bestAskDepth : float

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
        self.YESMarketData = MarketState(0.0, 0.0)
        self.NOMarketData = MarketState(0.0, 0.0)
    
    def setYesMarketData(self, price: float, depth: float):
        self.YESMarketData.bestAskPrice = float(price)
        self.YESMarketData.bestAskDepth = float(depth)
        
    
    def setNoMarketData(self, price: float, depth: float):
        self.NOMarketData.bestAskPrice = float(price)
        self.NOMarketData.bestAskDepth = float(depth)

    def getYESStr(self):
        return f"YES ON {self.question} | PRICE {self.getYESPrice()}\n"
    
    def getNOStr(self):
        return f"NO ON {self.question} | PRICE {self.getNOPrice()}\n"

    def getYESPrice(self):
        """
        Fetches most recently stored price for the "Yes" side
        """
        return self.YESMarketData.bestAskPrice

    def getYESDepth(self):
        """
        Fetches most recently stored price for the "Yes" side
        """
        return self.YESMarketData.bestAskDepth

    def getNOPrice(self):
        return self.NOMarketData.bestAskPrice
    
    def getNODepth(self):
        return self.NOMarketData.bestAskDepth

    def __repr__(self):
        """Return a string representation of MarketData"""
        clob_ids_str = str(self.clobTokenIds) if self.clobTokenIds else "None"
        question_short = (self.question[:50] + "...") if self.question and len(self.question) > 50 else self.question
        return (f"MarketData(question='{question_short}', marketId='{self.marketID}', "
                f"groupItemTitle='{self.groupItemTitle}', conditionId='{self.conditionId}', "
                f"clobTokenIds={clob_ids_str})")

    

