from .models.base_source import BaseSource
from typing import List


class TheNewYorkTimes(BaseSource):
    """
    A class for fetching and saving articles to JSON from The New York Times.

    Attributes:
        base_url (str): The base URL of the New York Times API.
        api_key (str): The API key for accessing the New York Times API.
        directory (str): The directory where the fetched data will be stored.
        article_counter (int): A counter to keep track of the number of articles processed.
    """

    def __init__(self):
        """
        Initialize TheNewYorkTimes class with base_url, api_key, directory, and article_counter.
        """
        self.base_url = f"The New York Times API URL here"
        self.api_key = f"The New York Times API key here"
        self.directory = f"Directory for New York Times data here"
        self.article_counter = 0

    def fetch_articles(self, sections: List[str], from_date: str) -> None:
        """
        Fetch articles from the New York Times.

        Args:
            sections (List[str]): The sections of the New York Times to fetch articles from.
            from_date (str): The date from which to fetch articles.
        """
        pass

    def save_to_json(self, data: List[dict], section: str, page: int) -> None:
        """
        Save New York Times articles to JSON.

        Args:
            data (List[dict]): The data to save.
            section (str): The section of the New York Times the data is from.
            page (int): The page number of the data.
        """
        pass
