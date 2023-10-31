import feedparser
import requests
from bs4 import BeautifulSoup
import re

rss_channels = ["https://rss.nytimes.com/services/xml/rss/nyt/World.xml"]

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

if __name__ == "__main__":
    for rss in rss_channels:
        parse_rss(rss)
