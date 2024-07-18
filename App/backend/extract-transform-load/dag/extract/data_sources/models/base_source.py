import os
from abc import ABC, abstractmethod
from typing import List

from .article import Article


class BaseSource(ABC):
    """
    An abstract base class that outlines the necessary methods and attributes for any data source class.
    It provides a structured way to fetch and save articles from different data sources.

    Attributes:
        base_url (str): The base URL of the data source.
        api_key (str): The API key for accessing the data source.
        directory (str): The directory where the fetched data will be stored.
        sections (List[str]): The sections of the source to fetch articles from.
        article_counter (int): A counter to keep track of the number of articles processed.
    """

    def __init__(self):
        """
        Initialize BaseSource class with base_url, api_key, directory, sections, and article_counter.
        """
        self.base_url: str
        self.api_key: str
        self.directory: str
        self.sections: List[str]
        self.article_counter: int = 0

    def create_and_clear_directory(self) -> None:
        """
        Creates and clears directories for each section.

        For each section, two directories are created: an extract directory and a transform directory.
        If these directories already exist, all files within them are removed.

        Directories are structured as follows:
        - {self.directory}/extract/{section}
        - {self.directory}/transform/{section}

        Where {self.directory} is the base directory, and {section} is the name of the section.

        Raises:
            PermissionError: If the process does not have sufficient permissions to create or delete the directories.
        """
        try:
            for section in self.sections:
                extract_dir = f"{self.directory}/extract/{section}"
                transform_dir = f"{self.directory}/transform/{section}"

                if not os.path.exists(extract_dir):
                    os.makedirs(extract_dir)
                else:
                    files = os.listdir(extract_dir)
                    for file in files:
                        os.remove(os.path.join(extract_dir, file))

                if not os.path.exists(transform_dir):
                    os.makedirs(transform_dir)
                else:
                    files = os.listdir(transform_dir)
                    for file in files:
                        os.remove(os.path.join(transform_dir, file))
        except PermissionError as e:
            raise PermissionError(f"Permission denied. {str(e)}")                

    @abstractmethod
    def fetch_articles(self, from_date: str) -> None:
        """
        Fetch data from the source.

        Args:
            from_date (str): The date from which to fetch articles.

        Raises:
            NotImplementedError: If this method is not overridden by a subclass.
        """
        raise NotImplementedError("Subclasses should implement this method!")

    @abstractmethod
    def save_to_json(self, data: List[Article], section: str, page: int) -> None:
        """
        Save the data to a JSON file.

        Args:
            data (List[Article]): The data to save.
            section (str): The section of the source the data is from.
            page (int): The page number of the data.

        Raises:
            NotImplementedError: If this method is not overridden by a subclass.
        """
        raise NotImplementedError("Subclasses should implement this method!")
