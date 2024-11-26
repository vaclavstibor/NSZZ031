from pydantic import BaseModel

from .sentiment import Sentiment


class Ticker(BaseModel):
    """
    Represents the ticker and sentiment of a company. Due to consistency its named Ticker and not company.

    Attributes:
        ticker (str): The ticker of the company.
        sentiment (Sentiment): The sentiment of the company.
    """

    ticker: str
    sentiment: Sentiment
