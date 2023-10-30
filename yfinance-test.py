import yfinance as yf

aapl = yf.Ticker('AAPL')

# Get all stock news
news_data = aapl.news

for article in news_data:
    print(article)
    print("\n")

# Print news attributes in a structured format
for article in news_data:
    print("Title: " + article['title'])
    print("Publisher: " + article['publisher'])
    print("Link: " + article['link'])
    print("Related Tickers: " + ', '.join(article['relatedTickers']))
    print("\n")
