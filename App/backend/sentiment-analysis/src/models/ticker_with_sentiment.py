from pydantic import BaseModel

from src.models.sentiment import Sentiment

class TickerWithSentiment(BaseModel):
    """
    A class used to represent the TickerWithSentiment model containing its ticker the sentiment of the ticker.
    """

    ticker: str
    sentiment: Sentiment