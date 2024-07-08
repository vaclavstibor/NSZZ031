from typing import List
import requests
import logging
from airflow.models import TaskInstance
from pydantic import BaseModel
from enum import Enum

from .models.entity import Entity
from .models.ticker import Ticker
from .models.response import SentimentAnalysisResponse as SAResponse

#SA_MODEL_API_URL = 'http://host.docker.internal:5052/analyse-sentiment'
SA_MODEL_API_URL = 'http://acheron.ms.mff.cuni.cz:42046/analyse-sentiment'
    
def apply_sa(ti: TaskInstance, file_basename: str) -> None:
    """
    """

    # Extract data (file) from xcom
    data = ti.xcom_pull(key=f'{file_basename}_json_extract_articles')
    # Extract entities from xcom
    articles_entities = ti.xcom_pull(key=f'{file_basename}_articles_entities')

    articles_tickers = post_request(data, articles_entities)

    logging.info(f"Articles tickers {articles_tickers}")
    logging.info(f"pushing into {file_basename}_articles_tickers")

    ti.xcom_push(key=f'{file_basename}_articles_tickers', value=articles_tickers)

def post_request(data: List[dict], articles_entities: List[Entity]) -> List[List[Ticker]]:
    """
    """
    articles_tickers = []

    # Process each article and its entities
    for article, entities in zip(data, articles_entities):
        article_content = article['content']
        #entities_payload = [{"text": entity['text'], "ticker": entity['ticker']} for entity in entities]

        try:
            logging.info(f"Request: ('content'=str, 'entities'={entities})")
            
            response = requests.post(SA_MODEL_API_URL, json={'content': article_content, 'entities': entities})
            
            logging.info(f"Response: {response.json()}")
            response.raise_for_status()

            tickers = response.json()['tickers']
            articles_tickers.append(tickers)
        except Exception as e:
            logging.error(f"Error processing article {article['id']}: {str(e)}")
    
    return articles_tickers