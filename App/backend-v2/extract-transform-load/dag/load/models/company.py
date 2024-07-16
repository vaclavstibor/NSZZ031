from dataclasses import dataclass, field
from typing import Optional

from load.models.sentiment import Sentiment

@dataclass
class Company:
    """
    Data class that represents a company with metadata and associated sentiment. Optional attributes are added via `insert_additional_company_data`, so that 
    initial insertion of companies can be done with only `ticker`.   

    Attributes:
        ticker (str): The stock market ticker symbol associated with the company.
        sentiment (Sentiment): An instance of Sentiment class representing sentiment analysis results.
        shortName (Optional[str]): The shortName of the company. Optional.
        industry (Optional[str]): The industry sector the company operates in. Optional.
        website (Optional[str]): The URL to the company's website. Optional.
    """

    ticker: str
    sentiment: Sentiment
    shortName: Optional[str] = field(default=None)
    industry: Optional[str] = field(default=None)
    website: Optional[str] = field(default=None)