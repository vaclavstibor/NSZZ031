"""
This is prepared to be used as a template for the Financial Times class as another source.
"""

from typing import List

from .models.base_source import BaseSource
from .models.article import Article


class FinancialTimes(BaseSource):
    """
    A class for fetching and saving articles to JSON from the Financial Times.

    Attributes:
        base_url (str): The base URL of the Financial Times API.
        api_key (str): The API key for accessing the Financial Times API.
        directory (str): The directory where the fetched data will be stored.
        sections (List[str]): The sections of the Financial Times to fetch articles from.
        article_counter (int): A counter to keep track of the number of articles processed.
    """

    def __init__(self):
        """
        Initialize TheFinancialTimes class with base_url, api_key, directory, and article_counter.
        """
        self.base_url = f"The Financial Times API URL here"
        self.api_key = f"The Financial Times API key here"
        self.directory = f"Directory for Financial Times data here"
        self.sections = ["section1", "section2", "section3"]
        self.article_counter = 0

    def fetch_articles(self, from_date: str) -> None:
        """
        Fetch articles from the Financial Times.

        Args:
            from_date (str): The date from which to fetch articles.
        """
        pass

    def save_to_json(self, data: List[Article], section: str, page: int) -> None:
        """
        Save Financial Times articles to JSON.

        Args:
            data (List[dict]): The data to save.
            section (str): The section of the Financial Times the data is from.
            page (int): The page number of the data.
        """
        pass
