import feedparser
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from IPython.display import display

rss_channel = "https://finance.yahoo.com/news/rss"

titles = []
links = []
dates = []
symbols = []

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
                return unique_tickers

            else:
                return "No tickers mentioned in the article."

        else:
            return "Article content not found on the page."

    else:
        return "Error fetching the article. Status code:" + str(response.status_code)

def parse_rss(url):
    feed = feedparser.parse(url)

    if feed.get("bozo_exception"):
        print("Error: ", feed.bozo_exception)
        return

    for entry in feed.entries:
        titles.append(entry.title)
        links.append(entry.link)
        dates.append(entry.published)
        #symbols.append(get_related_tickers(entry.link))

    data = {
        'title': titles,
        'link':  links,
        'date': dates,
    }

    df = pd.DataFrame(data)
    df = df.sort_values('link')

    display(df)

if __name__ == "__main__":
    parse_rss(rss_channel)
