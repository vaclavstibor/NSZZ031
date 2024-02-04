# NPRG045

## Úvod

V dnešní době informační exploze a neustálého toku informací se stává časově náročné udržet přehled o asociacích a porozumět obsahu, který se šíří prostřednictvím médií a online zpravodajství. Analýza sentimentu, tedy schopnost identifikovat a vyhodnotit emocionální náboj obsahu, se stala klíčovým nástrojem pro pochopení názorů, postojů a obecné atmosféry kolem různých (napříč?) témat. Tato práce se zaměřuje na vývoj aplikace, která umožňuje uživatelům vizualizovat a analyzovat sentiment zpráv v reálném čase, s využitím konceptu knowledge grafové sítě.

Knowledge grafy se stávají stále populárnějším nástrojem pro reprezentaci a propojení informací. V naší aplikaci jsou využity k tomu, aby uživatelům umožnily nejen sledovat sentiment jednotlivých zpráv, ale také propojovat a vizualizovat vztahy mezi společnostmi prostřednictvím článků. Tímto způsobem mohou uživatelé získat holistický pohled na dění ve světě a porozumět interakcím mezi různými subjekty(?).

V práci se budeme zabývat jak technickými aspekty analýzy sentimentu, tak i návrhem a implementací aplikace, která tyto informace přenáší uživatelům co nejefektivněji. Cílem je poskytnout uživatelům nástroj, který jim umožní nejen pasivně konzumovat zprávy, ale aktivně sledovat a analyzovat tok informací s ohledem na emocionální podtón, a to v reálném čase.

## Data
Grafová síť tvořená společnostmi vyskytujících se v článku (relevenatní vrcholy grafu reprezentuje průnik s FORTUNE 500, momentálně za rok 2022). Každý vrchol představuje jednu společnost. Společnost o sobě nese několik infromací, jejichž soubor můžeme/nažýváme kontextem. Společnosti jsou mezi sebou pospojovány na základě vytvořených vztahů/hran z článku. Každá společnost má odkaz na id článku, který je zaznamenán (například) v .json s analyzovaným sentimentem (nejlépe z pohledu každé společnosti zmíněné v článku) a dalšími atributy.

New York Times Api nám přináší výhodu ve formě vybraných společností, které článek zmiňuje. Za nevýhodu bych mohli brát to, že se nejedná o stream dat, tj. nemůžeme se připojit na server a aktivně odchytávat nově zveřejněné články/publikace. V našem případě tento fakt není (domněnka) důležitý, protože se jedná (spíše) o predikce v delším časovém horizontu. Jiná situace by byla, pokud bychom analyzovali například pouze titulky. Vystačíme si s periodickým dotazováním API (perioda zatím nastavena na 1D).

# Project Path
```
├─bert_crf_train.ipynb     ---BERT-CRF training  
│  bert_softmax_train.ipynb ---BERT training  
│  config.py                ---Model config for BERT-CRF and BERT  
│  mic.ipynb                ---Calculate the maximum information coefficient  
│  model_bert_crf           ---A fine-tuning pre-trained BERT-CRF model   
│  openai.ipynb             ---Train for chatgpt 3.5  
│  predict_by_crf.ipynb     ---Extract entities from financial news  
│  price_predict.ipynb      ---Use Case in Cryptocurrency Market  
│  readme.md  
│  
├─crypto_data 
│  │  btc_corr.xls          ---Mic data for Bitcoin   
│  │  doge_corr.xls         ---Mic data for Dogecoin   
│  │  eth_corr.xls          ---Mic data for Ethereum  
│  │  finentity_lstm.xls    ---Data for LSTM with entity-level sentiment   
│  │  toned_lstm.xls        ---Data for LSTM with sequence-level sentiment   
│  └─ xrp_corr.xls   
│  
├─data  
│  └─ FinEntity.json        ---FinEntity data  
│                               
├─data_process  
│  │  fleiss_kappa.ipynb    ---process the data with fleiss kappa
│  └─ Jaccard_vote.ipynb    ---process the data with Jaccard similarity  
│   
├─example  
│  │  finbert_tone_lstm.py  ---LSTM use FinBert-tone  
│  └─ finentity_lstm.py     ---LSTM use fine-tuning FinBert-CRF  
│                  
├─model  
│  │  bert_crf.py           ---Model for BERT-CRF  
│  │  lstm_model.py         ---Model for LSTM  
│  │  
│  └─layers  
│    └─  crf.py             ---CRF layer  
│    
├─news_data   
│  │  20230105.json              ---News from 20230105  
│  │  20230106to20230201.json    ---News from 20230106 to 20230201  
│  │  BTC_USD.csv           ---OHLC of Bitcoin  
│  │  doge_USD.csv          ---OHLC of Dogecoin  
│  │  eth_USD.csv           ---OHLC of Ethereum  
│  │  lstm_no.csv         
│  │  lstm_sentiment.csv  
│  │  ltc_USD.csv           ---OHLC of Litecoin  
│  │  news20220520to20221130.json  
│  │  xrp_USD.csv           ---OHLC of Ripple  
│  │  
│  │
│  ├─news_entity            ---Entities recognized  
│  │  │  20220520to20221130_entity.json  
│  │  │  20230105_entity.json
│  │  └─ 20230106to20230201_entity.json
│  │
│  └─news_url               ---News with url  
│          20220520to20221130.xlsb
│          20230105.xlsb
│          20230106to20230201.xlsb
│
├─sequence_aligner          ---Data preprocessing   
│  │  alignment.py 
│  │  containers.py  
│  │  dataset.py  
│  │  labelset.py 
│  └─  __init__.py   
│   
│  
├─util                      ---Model Training Tool Module  
│  │  adversairal.py  
│  │  process.py  
│  │  train.py   
│  └─  __init__.py 
   
```

## Pages skeleton 
### Home
- For random ticker with headline **Why (GlobeSense)?** https://github.com/janlukasschroeder/netflix-stock-price-impacted-by-news/blob/master/Netflix%20-%20how%20news%20impacts%20stock%20prices.ipynb
### Ticker detail
- https://github.com/janlukasschroeder/netflix-stock-price-impacted-by-news/blob/master/Netflix%20-%20how%20news%20impacts%20stock%20prices.ipynb


NewsArticle schema.org - https://schema.org/NewsArticle
This code is not well structured but provides a good example of using Neo4j with Flask.
- https://github.com/neo4j-examples/neo4j-movies-template/blob/master/flask-api/app.py
- https://github.com/soerface/flask-restful-swagger-2.0/tree/master/example
- https://nicolewhite.github.io/neo4j-flask/pages/the-data-model.html
- https://realpython.com/flask-connexion-rest-api/

Papers
- Real-Time Sentiment Analysis of Twitter Streaming data for Stock Prediction
    - https://www.sciencedirect.com/science/article/pii/S1877050918308433
    - 
- Stock trend prediction using sentiment analysis
    - https://peerj.com/articles/cs-1293/
- Detection of temporality at discourse level on financial news by combining Natural Language Processing and Machine Learning
    - https://www.sciencedirect.com/science/article/pii/S095741742200135X?via%3Dihub
- Dynamic ensemble selection for multi-class imbalanced datasets
    - https://www.sciencedirect.com/science/article/pii/S0020025518301725?via%3Dihub
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
- !! [https://neo4j.com/blog/5-ways-to-tackle-big-graph-data-keylines-neo4j/]
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