# NPRG045

## Data
Grafová síť tvořená společnostmi vyskytujících se v článku (relevenatní vrcholy grafu reprezentuje průnik s FORTUNE 500, momentálně za rok 2022). Každý vrchol představuje jednu společnost. Společnost o sobě nese několik infromací, jejichž soubor můžeme/nažýváme kontextem. Společnosti jsou mezi sebou pospojovány na základě vytvořených vztahů/hran z článku. Každá společnost má odkaz na id článku, který je zaznamenán (například) v .json s analyzovaným sentimentem (nejlépe z pohledu každé společnosti zmíněné v článku) a dalšími atributy.

New York Times Api nám přináší výhodu ve formě vybraných společností, které článek zmiňuje. Za nevýhodu bych mohli brát to, že se nejedná o stream dat, tj. nemůžeme se připojit na server a aktivně odchytávat nově zveřejněné články/publikace. V našem případě tento fakt není (domněnka) důležitý, protože se jedná (spíše) o predikce v delším časovém horizontu. Jiná situace by byla, pokud bychom analyzovali například pouze titulky. Vystačíme si s periodickým dotazováním API (perioda zatím nastavena na 1D).

Vizualizace
- KeyLens - placené
- 3d-force-graph (WebGL)
- Forced-directed tree (SVG) [https://observablehq.com/@d3/force-directed-tree?intent=fork]
- Cosmograph/cosmos - neposkytuje timeline, není příliš spolehlivou knihovnou
- Sigma 
- D3 [https://stackoverflow.com/questions/50789482/is-it-possible-visualize-large-graph-in-d3]
- https://npmtrends.com/3d-force-graph-vs-d3-vs-d3.js-vs-mxgraph-vs-sigma
- https://imld.de/cnt/uploads/Horak-2018-Graph-Performance.pdf
- https://neo4j.com/developer-blog/15-tools-for-visualizing-your-neo4j-graph-database/
---
https://eoddata.com/symbols.aspx
- List of Symbols for New York Stock Exchange [NYSE]
- List of Symbols for NASDAQ Stock Exchange [NASDAQ]
---
Bloomberg - https://www.bloomberg.com/professional/product/event-driven-feeds/
- Přístup k real-time datum lze získat pouze přes vyučujícího.
DB
- Neo4j (lpg)
- https://medium.com/geekculture/labeled-vs-typed-property-graphs-all-graph-databases-are-not-the-same-efdbc782f099

- Pokračování s rss kanály yahoo, nutné získat related tickers
## APIs
- [https://www.linkedin.com/pulse/10-alternatives-newsapi-newsdata-bing-news-yahoo-more-vikash/]
- MBOUM
- yfinance (non official Yahoo!)
    - Nemezený počet dotazů
    - `news()`
    - Proč nepoužívat yfinance pro analýzu sentimentu [https://analyzingalpha.com/yfinance-python]
    - Is there an alternative to Yahoo Finance? Being an unofficial library, it is not uncommon for yfinance to suddenly stop working. Thus, having another free alternative is essential.
    
    - Although less popular, YahooQuery is another open-source Python library that fetches data from Yahoo Finance. You can install it simply by typing “pip install yahooquery” on your terminal. The library is also actively maintained and decently documented (Github / Documentation).
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
- Finnhub

## Optimlaizace skenování RSS kanálu
Začneme na jednom skenování denně.

## GDELT - knowledge graph
- Updatování databáze každých 15 min - https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/
- Použít jako https://odupuis.medium.com/consuming-the-gdelt-projects-events-database-13e4b7def2ce a updatovat vlastní databázy
- Vizualizace pomocí three js https://medium.com/neo4j/visualizing-graphs-in-3d-with-webgl-9adaaff6fe43 možná https://www.esri.com/arcgis-blog/products/js-api-arcgis/3d-gis/interactive-3d-globe/
- Vizualizace Země - https://isotropic.co/3d-globe-on-website/ 

## Proč není API  tomto případě ideální?
API funguje na principu dotazování, to znamená že bychom se museli neustále dotazovat. Websockety by byly lepším řešení, pokud se bavíme o vytvoření API, jenž by bylo možné poskytovat vnějším systémům pro obchodování. Pokud by se jednalo pouze o vizuální webovou aplikaci pro uživatele postačilo by nám API, které by se dotázalo pokaždé po otevření stránky s detailem daného symbolu.

## RSS, WebSub, Atom

## Implementační návrhy
- Zachytávání ceny v čase zveřejnění článku. Pro analýzu/vizualizaci možného dopadu. Dobré také jako mini featura v detailu.

## News filter 
- Filtrování na základě klíčových slov (https://scanz.com/smart-ways-to-create-keyword-based-news-scans/)

### Poznámky
Jakmile se kvantita stane hlavním důrazem, kvalita nevyhnutelně trpí. 