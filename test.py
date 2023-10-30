import requests

# Nahraďte "demo" v URL adrese za svůj vlastní API klíč, pokud ho máte.
url = "https://mboum.com/api/v1/ne/news/?symbol=AAPL&apikey=demo"
r = requests.get(url)
data = r.json()

# Získejte relevantní informace z dat
for item in data['data']['item']:
    title = item['title']
    description = item['description']
    pubDate = item['pubDate']
    link = item['link']

    # Vypište tyto informace
    print("Název článku:", title)
    print("Popis:", description)
    print("Datum publikace:", pubDate)
    print("Odkaz:", link)
    print()
