# NPRG045
## APIs
- https://www.linkedin.com/pulse/10-alternatives-newsapi-newsdata-bing-news-yahoo-more-vikash/
### MBOUM

### yfinance
- Nemezený počet dotazů
#### News
- Poskytuje
    - Titulek
    - Publisher
    - Link na článek
    - Related tickers
    - ```
        {'uuid': '50b7811e-82a0-31ff-8916-781fa5678d5a', 
         'title': 'Earnings, Fed Decision, Jobs Data Are Key This Week. One Thing’s More Important.', 
         'publisher': 'Barrons.com', 
         'link': 'https://finance.yahoo.com/m/50b7811e-82a0-31ff-8916-781fa5678d5a/earnings%2C-fed-decision%2C-jobs.html', 
         'providerPublishTime': 1698662160, 
         'type': 'STORY', 
         'thumbnail': {'resolutions': [{'url': 'https://s.yimg.com/uu/api/res/1.2/iXgzsWpiRgKbrTNXnh6jqw--~B/aD02NDA7dz0xMjc5O2FwcGlkPXl0YWNoeW9u/https://media.zenfs.com/en/Barrons.com/fa92d09e55c95de75a80bed7faaa9e0b', 'width': 1279, 'height': 640, 'tag': 'original'}, {'url': 'https://s.yimg.com/uu/api/res/1.2/VmOvcAxXCZLy6y92AMv56Q--~B/Zmk9ZmlsbDtoPTE0MDtweW9mZj0wO3c9MTQwO2FwcGlkPXl0YWNoeW9u/https://media.zenfs.com/en/Barrons.com/fa92d09e55c95de75a80bed7faaa9e0b', 'width': 140, 'height': 140, 'tag': '140x140'}]}, 
         'relatedTickers': ['AAPL', 'AMD', '^GSPC', 'STLAM.MI', 'F']}
        ```


## Implementační návrhy
- Zachytávání ceny v čase zveřejnění článku. Pro analýzu/vizualizaci možného dopadu. Dobré také jako mini featura v detailu.

## News filter 
- Filtrování na základě klíčových slov (https://scanz.com/smart-ways-to-create-keyword-based-news-scans/)