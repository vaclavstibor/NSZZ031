from pydantic import BaseModel
from typing import List

from src.models.ticker_with_sentiment import TickerWithSentiment

class Response(BaseModel):
    """
    A class used to represent the Response model.

    Attributes:
        tickers (List[TickerWithSentiment]): A list of tickers with sentiment.
    """

    tickers: List[TickerWithSentiment]