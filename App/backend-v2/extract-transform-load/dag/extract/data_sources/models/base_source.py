from abc import ABC, abstractmethod
from typing import List


class BaseSource(ABC):
    """
    BaseSource is an abstract base class that outlines the necessary methods and attributes for any data source class.
    It provides a structured way to fetch and save articles from different data sources.

    Attributes:
        base_url (str): The base URL of the data source.
        api_key (str): The API key for accessing the data source.
        directory (str): The directory where the fetched data will be stored.
        article_counter (int): A counter to keep track of the number of articles processed.
    """

    def __init__(self):
        """
        Initialize BaseSource class with base_url, api_key, directory, and article_counter.
        """
        self.base_url: str
        self.api_key: str
        self.directory: str
        self.article_counter: int = 0

    @abstractmethod
    def fetch_articles(self, sections: List[str], from_date: str) -> None:
        """
        Fetch data from the source.

        Args:
            sections (List[str]): The sections of the source to fetch articles from.
            from_date (str): The date from which to fetch articles.

        Raises:
            NotImplementedError: If this method is not overridden by a subclass.
        """
        raise NotImplementedError("Subclasses should implement this method!")

    @abstractmethod
    def save_to_json(self, data: List[dict], section: str, page: int) -> None:
        """
        Save the data to a JSON file.

        Args:
            data (List[dict]): The data to save.
            section (str): The section of the source the data is from.
            page (int): The page number of the data.

        Raises:
            NotImplementedError: If this method is not overridden by a subclass.
        """
        raise NotImplementedError("Subclasses should implement this method!")
