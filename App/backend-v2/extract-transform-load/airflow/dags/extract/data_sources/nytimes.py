from .models.base_source import BaseSource
from typing import List


class NYTimes(BaseSource):
    def __init__(self):
        self.base_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?"
        self.api_key = f"api-key=H2d4Rz8G1B5Ic6XG5Y2A2D2B1B1G2A2A"
        self.article_counter = 0

    def fetch_articles(self, sections: List[str], from_date: str) -> None:
        pass
