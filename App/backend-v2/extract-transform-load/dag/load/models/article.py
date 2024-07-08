from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from uuid import UUID

from load.models.ticker import Ticker


@dataclass
class Article:
    """
    Data class that represents an article with metadata and associated company tickers. 
    (without content field which is not to be used stored in the database)

    Attributes:
        id (UUID): The unique identifier for the article.
        type (str): The type/category of the article (liveblog, article, story,...).
        section (str): The section of the publication where the article is located.
        url (str): The URL to the article.
        title (str): The title of the article.
        author (str): The author of the article.
        published_date (datetime): The date and time when the article was published.
        tickers (List[Ticker]): A list of company tickers associated with the article, if any.
    """

    id: UUID
    type: str
    section: str
    url: str
    title: str
    author: str
    published_date: datetime
    tickers: List[Ticker] = field(default_factory=list)
