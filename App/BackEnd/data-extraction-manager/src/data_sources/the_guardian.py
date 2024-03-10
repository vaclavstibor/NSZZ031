import logging
import uuid
import os
import time
import json
from typing import Any, Dict, List
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import colorlog
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

from .models.article import Article
from .models.base_source import BaseSource
from dotenv import find_dotenv

def setup_logger():
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )

    logger = colorlog.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

setup_logger()

load_dotenv(find_dotenv())

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

    def fetch_data(
        self,
        sections: List[str],
        from_date: str = BEGINNING_OF_TIME,
    ):
        for section in sections:
            os.makedirs(f"{THE_GUARDIAN_DIRECTORY}/{section}", exist_ok=True)

        pages = {section: self.get_total_pages(section) for section in sections}

        with ThreadPoolExecutor() as executor:
            for section, total_pages in pages.items():
                executor.map(
                    lambda page: self.get_articles(section, page),
                    range(1, total_pages + 1),
                )

    def get_total_pages(
        self, section: str, from_date: str = BEGINNING_OF_TIME, page_size: int = 200
    ) -> int:
        url = f"{self.base_url}/search?section={section}&from-date={from_date}&show-fields=body&page=1&page-size={page_size}&api-key={self.api_key}"
        try:
            request = requests.get(url, timeout=5)
            request.raise_for_status()  # This will raise an HTTPError if the status is 4xx or 5xx

            data = request.json()
            return data["response"]["pages"]

        except Exception as e:
            message = f"Failed to get total pages from The Guardian API. Error: {str(e)}"
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

            file_path = f"{THE_GUARDIAN_DIRECTORY}/{section}/{section}-{page}.json"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                json.dump(articles, f, ensure_ascii=False, indent=4)

        except Exception as e:
            message = f"Failed to get articles from The Guardian API. Error: {str(e)}"
            logging.error(message)
            raise Exception(message)


if __name__ == "__main__":
    guardian = TheGuardian()
    guardian.fetch_data(sections=THE_GUARDIAN_SECTIONS, from_date=BEGINNING_OF_TIME)
