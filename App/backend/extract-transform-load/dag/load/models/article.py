from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from uuid import UUID

from load.models.company import Company


@dataclass
class Article:
    """
    Data class that represents an article with metadata and associated companies. 
    (without content field which is not to be used stored in the database)

    Attributes:
        id (UUID): The unique identifier for the article.
        type (str): The type/category of the article (liveblog, article, story,...).
        section (str): The section of the publication where the article is located.
        url (str): The URL to the article.
        title (str): The title of the article.
        author (str): The author of the article.
        published_date (datetime): The date and time when the article was published.
        compnies (List[Company]): A list of companies associated with the article, if any.
    """

    id: UUID
    type: str
    section: str
    url: str
    title: str
    author: str
    published_date: datetime
    companies: List[Company] = field(default_factory=list)
