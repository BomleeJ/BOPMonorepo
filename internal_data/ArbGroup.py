from urllib.parse import urlparse

class ArbGroup:
    def __init__(self, eventURLs: list[str]):
        self.eventURLs = None # list[str]
        self.eventQuestion = None # str
        self.market = [] # List[MarketData]
    
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

    def initializeData(self):
        pass

