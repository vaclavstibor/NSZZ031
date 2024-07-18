import logging
import uuid
import os
import json
from typing import Any, Dict, List
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
import requests

from .models.article import Article
from .models.base_source import BaseSource

load_dotenv()


class TheGuardian(BaseSource):
    """
    A class for fetching and saving (to JSON) articles from The Guardian's Open Platform API.

    Attributes:
        base_url (str): The base URL of The Guardian API.
        api_key (str): The API key for accessing The Guardian API.
        directory (str): The directory where the fetched data will be stored.
        sections (List[str]): The sections of The Guardian to fetch articles from.
        article_counter (int): A counter to keep track of the number of articles processed.
    """

    def __init__(self):
        """
        Initialize TheGuardian class with base_url, api_key, directory, sections, and article_counter.
        """

        self.base_url = os.getenv("THE_GUARDIAN_BASE_URL")
        self.api_key = os.getenv("THE_GUARDIAN_API_KEY")
        self.directory = os.getenv("THE_GUARDIAN_DIRECTORY")
        self.sections = os.getenv("THE_GUARDIAN_SECTIONS").split(",")
        self.article_counter = 0

        logging.info(
            f"TheGuardian initialized with base_url: {self.base_url}, directory: {self.directory}, and sections: {self.sections}"
        )

    def fetch_articles(self, from_date: str) -> None:
        """
        Fetch articles from The Guardian API for the given sections and from the given date.

        Args:
            from_date (str): The date from which to fetch articles.
        """

        # Get the total number of pages for each section
        pages = {
            section: self.get_total_pages(section, from_date)
            for section in self.sections
        }

        # Fetch articles from each page in parallel using a ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            for section, total_pages in pages.items():
                executor.map(
                    lambda page: self.get_articles(section, page, from_date),
                    range(1, total_pages + 1),
                )

    def save_to_json(self, articles: List[Article], section: str, page: int) -> None:
        """
        Save the given articles to a JSON file in the directory for the given section.

        Args:
            articles (List[Article]): The articles to save.
            section (str): The section of The Guardian the articles are from.
            page (int): The page number of the articles.

        Raises:
            Exception: If any error occurs during the file operations, it raises an exception.
        """

        try:
            articles = [
                article.to_dict() for article in articles if article is not None
            ]

            extract_file_path = (
                f"{self.directory}/extract/{section}/{section}_{page}.json"
            )

            with open(extract_file_path, "w") as f:
                json.dump(articles, f, ensure_ascii=False, indent=4)

            # Transform phase temporarily saves empty articles
            empty_articles = []

            transform_file_path = (
                f"{self.directory}/transform/{section}/{section}_{page}.json"
            )

            with open(transform_file_path, "w") as f:
                json.dump(empty_articles, f, ensure_ascii=False, indent=4)

        except Exception as e:
            raise Exception(
                f"Failed to save data from The Guardian API to JSON. Error: {str(e)}"
            )

    def get_total_pages(
        self, section: str, from_date: str, page_size: int = 200
    ) -> int:
        """
        Get the total number of pages of articles for the given section and from the given date.
        The Guardian API returns a maximum of 200 articles per page. This method takes the total
        number of pages from one request and returns it.

        Args:
            section (str): The section of The Guardian to get the total pages from.
            from_date (str): The date from which to get the total pages.
            page_size (int, optional): The number of articles per page. Defaults to 200.

        Returns:
            int: The total number of pages.

        Raises:
            Exception: If any error occurs during the request, it raises an exception.
        """
        url = f"{self.base_url}/search?section={section}&from-date={from_date}&show-tags=contributor&show-fields=bodyText&page=1&page-size={page_size}&api-key={self.api_key}"
        try:
            response = requests.get(url)
            # Raise an HTTPError if the status is 4xx or 5xx
            response.raise_for_status()

            data = response.json()
            return data["response"]["pages"]

        except Exception as e:
            raise Exception(
                f"Failed to get total pages from The Guardian API. Error: {str(e)}"
            )

    def process_article(self, article: Dict[str, Any]) -> Article:
        """
        Process the given article data and return an Article object.

        Args:
            article (Dict[str, Any]): The article data to process.

        Returns:
            Article: The processed Article object.
        """

        body_text = article["fields"]["bodyText"]

        if body_text is None or body_text == "":
            return

        id = str(uuid.uuid4())

        # Published date ISO 8601 format
        published_date = str(article["webPublicationDate"]).replace("Z", "+00:00")

        # Extract the first (article can have multiple authors) author if available
        author = ""
        author_tags = [
            tag for tag in article.get("tags", []) if tag.get("type") == "contributor"
        ]
        if author_tags:
            author = author_tags[0].get("webTitle", "")

        self.article_counter += 1

        logging.info(f"Article [{self.article_counter}] FINISHED {article['id']}.")

        return Article(
            id=id,
            type=article["type"],
            section=article["sectionId"],
            url=article["webUrl"],
            title=article["webTitle"],
            content=body_text,
            author=author,
            published_date=published_date,
        )

    def get_articles(
        self,
        section: str,
        page: int,
        from_date: str,
        page_size: int = 200,
    ) -> None:
        """
        Get articles from The Guardian API for the given section and from the given date.

        Args:
            section (str): The section of The Guardian to get articles from.
            page (int): The page number to get articles from.
            from_date (str): The date from which to get articles.
            page_size (int, optional): The number of articles per page. Defaults to 200.

        Raises:
            Exception: If any error occurs during the request, it raises an exception.
        """

        url = f"{self.base_url}/search?section={section}&from-date={from_date}&show-tags=contributor&show-fields=bodyText&page={page}&page-size={page_size}&api-key={self.api_key}"

        try:
            response = requests.get(url, timeout=5)
            # Raise an HTTPError if the status is 4xx or 5xx
            response.raise_for_status()

            data = response.json()
            articles = [
                self.process_article(article) for article in data["response"]["results"]
            ]

            self.save_to_json(articles, section, page)

        except Exception as e:
            raise Exception(
                f"Failed to get articles from The Guardian API. Error: {str(e)}"
            )
