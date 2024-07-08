from dataclasses import dataclass

from load.models.sentiment import Sentiment

@dataclass
class Ticker:
    """
    Data class that represents a company ticker with associated sentiment.
    TODO ticker -> name pozor na zmenu v load_data_to_db.py

    Attributes:
        ticker (str): The company ticker symbol.
        sentiment (Sentiment): The sentiment associated with the ticker.
    """
    ticker: str
    sentiment: Sentiment