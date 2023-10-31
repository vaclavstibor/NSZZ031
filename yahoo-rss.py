import feedparser
import requests
from bs4 import BeautifulSoup
import re

rss_channels = ["https://finance.yahoo.com/news/rss"]

def get_related_tickers(url: str):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the main content of the article (you may need to inspect the HTML structure to locate it)
        article_content = soup.find('div', {'class': 'caas-body'})

        if article_content:
            # Extract and print tickers mentioned in the article
            article_text = article_content.get_text()
            tickers = re.findall(r'\b[A-Z]{2,5}\b', article_text)
            
            if tickers:
                unique_tickers = list(set(tickers))  # Remove duplicates
                print("Tickers mentioned in the article:", unique_tickers)
            else:
                print("No tickers mentioned in the article.")

        else:
            print("Article content not found on the page.")

    else:
        print('Error fetching the article. Status code:', response.status_code)

def parse_rss(url):
    limit = 0
    feed = feedparser.parse(url)

    if feed.get("bozo_exception"):
        print("Error: ", feed.bozo_exception)
        return

    for entry in feed.entries:
        print(entry.title)
        print(entry.link)
        print(entry.published)
        print("\n")
        get_related_tickers(entry.link)

if __name__ == "__main__":
    for rss in rss_channels:
        parse_rss(rss)
