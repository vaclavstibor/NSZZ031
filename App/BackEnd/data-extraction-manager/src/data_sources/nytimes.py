from .models.base_source import BaseSource

class NYTimes(BaseSource):
    def __init__(self):
        self.base_url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
        self.api_key = f'api-key=H2d4Rz8G1B5Ic6XG5Y2A2D2B1B1G2A2A'
        self.article_counter = 0
"""
    def fetch_data(self, sections: List[str], from_date: str=BEGINNING_OF_TIME, page_size: int=200):
        pages = {section: self.get_total_pages(section) for section in sections}

        with ThreadPoolExecutor() as executor:
            for section, total_pages in pages.items():
                executor.map(lambda page: self.get_articles(section, page), range(1, total_pages + 1))

    def get_total_pages(self, section: str, from_date: str=BEGINNING_OF_TIME, page_size: int=200) -> int:
        url = f'{self.base_url}fq=section_name:("{section}")&begin_date={from_date}&page=1&page-size={page_size}&{self.api_key}'
        request = requests.get(url,timeout=5)
        data = json.loads(request.text)
        hits = data['response']['meta']['hits']
        return math.ceil(hits / page_size)

    def get_articles(self, section: str, page: int, from_date: str=BEGINNING_OF_TIME, page_size: int=200) -> List[Article]:
        url = f'{self.base_url}fq=section_name:("{section}")&begin_date={from_date}&page={page}&page-size={page_size}&{self.api_key}'
        request = requests.get(url,timeout=5)
        data = json.loads(request.text)
        articles = data['response']['docs']
        return [self.parse_article(article) for article in articles]

    def parse_article(self, article: Dict[str, Any]) -> Article:
        return Article(
            id=article['_id'],
            title=article['headline']['main'],
            section=article['section_name'],
            date=article['pub_date'],
            body=article['abstract'],
            url=article['web_url']
        )
"""