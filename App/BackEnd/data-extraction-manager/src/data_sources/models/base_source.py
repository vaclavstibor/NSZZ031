from abc import ABC, abstractmethod
from typing import List


class BaseSource(ABC):
    """
    Abstract base class for data sources.
    """

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.article_counter: int = 0

    @abstractmethod
    def fetch_data(self, sections: List[str], from_date: str) -> None:
        """
        Fetch data from the source. This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method!")