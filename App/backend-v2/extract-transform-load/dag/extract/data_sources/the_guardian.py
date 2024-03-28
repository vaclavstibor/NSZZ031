import logging
import uuid
import os
import json
from typing import Any, Dict, List
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

from dotenv import load_dotenv
import requests

from .models.article import Article
from .models.base_source import BaseSource

load_dotenv()

THE_GUARDIAN_DIRECTORY = "/Users/stiborv/Documents/ZS2324/NPRG045/App/backend-v2/extract-transform-load/data"  # os.getenv("THE_GUARDIAN_DIRECTORY")


class TheGuardian(BaseSource):
    def __init__(self):
        self.base_url = os.getenv("THE_GUARDIAN_BASE_URL")
        self.api_key = os.getenv("THE_GUARDIAN_API_KEY")
        self.article_counter = 0
        logging.info(f"TheGuardian initialized with base_url: {self.base_url} and api_key: {self.api_key}")

    def fetch_articles(self, sections: List[str], from_date: str) -> None:
        """ """
        logging.info("The Guardian started fetching articles.")

        for section in sections:
            os.makedirs(f"{THE_GUARDIAN_DIRECTORY}/{section}", exist_ok=True)

        pages = {
            section: self.get_total_pages(section, from_date) for section in sections
        }
        
        """
        with ThreadPoolExecutor() as executor:
            for section, total_pages in pages.items():
                executor.map(
                    lambda page: self.get_articles(section, page, from_date),
                    range(1, total_pages + 1),
                )
        """
        
        for section in sections:
            logging.info(f"Processing section: {section}")
            total_pages = self.get_total_pages(section, from_date)
            logging.info(f"Total pages for section {section}: {total_pages}")
            for page in range(1, total_pages + 1):
                logging.info(f"Processing page {page} for section {section}")
                self.get_articles(section, page, from_date)
                logging.info(f"Completed processing page {page} for section {section}")
            logging.info(f"Completed processing section: {section}")
        

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
        self, section: str, from_date: str, page_size: int = 200
    ) -> int:
        """ """
        url = f"{self.base_url}/search?section={section}&from-date={from_date}&show-fields=bodyText&page=1&page-size={page_size}&api-key={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # This will raise an HTTPError if the status is 4xx or 5xx
            
            data = response.json()
            return data["response"]["pages"]

        except Exception as e:
            message = (
                f"Failed to get total pages from The Guardian API. Error: {str(e)}"
            )
            logging.error(message)
            raise

    def process_article(self, article: Dict[str, Any]) -> Article:
        body_text = article["fields"]["bodyText"]

        if body_text is None or body_text == "":
            return

        id = str(uuid.uuid4())

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
            content=body_text,
        ).to_dict()

    def get_articles(
        self,
        section: str,
        page: int,
        from_date: str,
        page_size: int = 200,
    ):
        url = f"{self.base_url}/search?section={section}&from-date={from_date}&show-fields=bodyText&page={page}&page-size={page_size}&api-key={self.api_key}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()
            articles = [
                self.process_article(article) for article in data["response"]["results"]
            ]

            self.save_to_json(articles, section, page)

        except Exception as e:
            message = f"Failed to get articles from The Guardian API. Error: {str(e)}"
            logging.error(message)
            raise
