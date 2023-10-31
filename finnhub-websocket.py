import requests
from bs4 import BeautifulSoup

# URL Yahoo Finance, kde jsou zprávy (upravte podle potřeby)
url = 'https://finance.yahoo.com/'

# Získání obsahu webové stránky
response = requests.get(url)

if response.status_code == 200:
    # Parsujeme HTML obsah
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Najdeme zprávy na stránce (upravte podle aktuálního HTML)
    news_elements = soup.find_all('article')  # Předpokládáme, že zprávy jsou ve značkách <article>

    # Procházení a tisk zpráv
    for news in news_elements:
        # Zde můžete provádět další analýzu a extrakci dat, například název, datum, obsah atd.
        title = news.find('h3').text  # Předpokládáme, že název zprávy je ve značce <h3>
        print('Název zprávy:', title)
        print('---------------------')

else:
    print('Chyba při stahování webové stránky. Stavový kód:', response.status_code)
