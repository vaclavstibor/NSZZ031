import logging
import uuid
import os
import json
from typing import Any, Dict, List
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

from .models.article import Article
from .models.base_source import BaseSource

load_dotenv()

BEGINNING_OF_TIME = os.getenv("BEGINNING_OF_TIME")
THE_GUARDIAN_DIRECTORY = os.getenv("THE_GUARDIAN_DIRECTORY")
THE_GUARDIAN_SECTIONS = os.getenv("THE_GUARDIAN_SECTIONS").split(",")
THE_GUARDIAN_BASE_URL = os.getenv("THE_GUARDIAN_BASE_URL")
GUARDIAN_API_KEY = os.getenv("THE_GUARDIAN_API_KEY")


class TheGuardian(BaseSource):
    def __init__(self):
        self.base_url = os.getenv("THE_GUARDIAN_BASE_URL")
        self.api_key = os.getenv("THE_GUARDIAN_API_KEY")
        self.article_counter = 0

    def fetch_articles(self, sections: List[str], from_date: str) -> None:
        """ """
        for section in sections:
            os.makedirs(f"{THE_GUARDIAN_DIRECTORY}/{section}", exist_ok=True)

        pages = {section: self.get_total_pages(section) for section in sections}

        with ThreadPoolExecutor() as executor:
            for section, total_pages in pages.items():
                executor.map(
                    lambda page: self.get_articles(section, page),
                    range(1, total_pages + 1),
                )

    def save_to_json(self, articles: List[dict], section: str, page: int) -> None:
        """
        Save the data to a JSON file.
        """
        try:
            file_path = f"{THE_GUARDIAN_DIRECTORY}/{section}/{section}-{page}.json"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                json.dump(articles, f, ensure_ascii=False, indent=4)
        except Exception as e:
            message = f"Failed to save data to JSON. Error: {str(e)}"
            logging.error(message)
            raise Exception(message)

    def get_total_pages(
        self, section: str, from_date: str = BEGINNING_OF_TIME, page_size: int = 200
    ) -> int:
        """ """
        url = f"{self.base_url}/search?section={section}&from-date={from_date}&show-fields=body&page=1&page-size={page_size}&api-key={self.api_key}"
        try:
            request = requests.get(url, timeout=5)
            request.raise_for_status()  # This will raise an HTTPError if the status is 4xx or 5xx

            data = request.json()
            return data["response"]["pages"]

        except Exception as e:
            message = (
                f"Failed to get total pages from The Guardian API. Error: {str(e)}"
            )
            logging.error(message)
            raise Exception(message)

    def process_article(self, article: Dict[str, Any]) -> Article:
        html_body = article["fields"]["body"]

        if html_body is None or html_body == "":
            return

        id = str(uuid.uuid4())

        content = BeautifulSoup(html_body, "html.parser").get_text()

        # Published date ISO 8601 format
        published_date = str(article["webPublicationDate"]).replace("Z", "+00:00")

        self.article_counter += 1

        logging.info(f"Article [{self.article_counter}] FINISHED {article['id']}.")

        return Article(
            id=id,
            type=article["type"],
            section=article["sectionId"],
            url=article["webUrl"],
            title=article["webTitle"],
            author="",
            published_date=published_date,
            content=content,
        ).to_dict()

    def get_articles(
        self,
        section: str,
        page: int,
        from_date: str = BEGINNING_OF_TIME,
        page_size: int = 200,
    ):
        url = f"{self.base_url}/search?section={section}&from-date={from_date}&show-fields=body&page={page}&page-size={page_size}&api-key={self.api_key}"
        try:
            request = requests.get(url, timeout=5)
            request.raise_for_status()

            data = request.json()
            articles = [
                self.process_article(article) for article in data["response"]["results"]
            ]

            self.save_to_json(articles, section, page)

        except Exception as e:
            message = f"Failed to get articles from The Guardian API. Error: {str(e)}"
            logging.error(message)
            raise Exception(message)
