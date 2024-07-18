from pydantic import BaseModel

from .sentiment import Sentiment

class Ticker(BaseModel):
    """

    """

    ticker: str
    sentiment: Sentiment