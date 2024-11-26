import os
from dotenv import load_dotenv

from typing import List
import requests
import logging
from airflow.models import TaskInstance

from .models.entity import Entity
from .models.response import SentimentAnalysisResponse as SAResponse

load_dotenv()

SA_MODEL_API_URL = os.getenv("SA_MODEL_API_URL")


def apply_sa(ti: TaskInstance, file_basename: str) -> None:
    """ 
    Function to apply Sentiment Analysis to the articles content.
    It pulls the data from the xcom, applies the Sentiment Analysis model to the content of the articles and pushes the result back to the xcom.

    Args:
        ti (TaskInstance): The task instance object.
        file_basename (str): The base name of the file.
    """

    # Extract data (file) from xcom
    data = ti.xcom_pull(key=f"{file_basename}_json_extract_articles")
    # Extract entities from xcom
    articles_entities = ti.xcom_pull(key=f"{file_basename}_articles_entities")

    articles_tickers = post_request(data, articles_entities)

    logging.info(f"Articles tickers {articles_tickers}")
    logging.info(f"pushing into {file_basename}_articles_tickers")

    ti.xcom_push(key=f"{file_basename}_articles_tickers", value=articles_tickers)


def post_request(
    data: List[dict], articles_entities: List[Entity]
) -> List[SAResponse]:
    """ 
    Function to post request to the Sentiment Analysis model API and get the tickers.
    It pulls the data from the xcom, applies the Sentiment Analysis model to the content of the articles and pushes the result back to the xcom.

    Args: 
        data (List[dict]): The list of articles.
        articles_entities (List[Entity]): The list of entities extracted from the articles.
    """
    articles_tickers = []

    # Process each article and its entities
    for article, entities in zip(data, articles_entities):
        article_content = article["content"]

        if len(entities) == 0:
            logging.info(
                f"No entities for article {article['id']}, appending empty list"
            )
            articles_tickers.append([])
            continue

        try:

            logging.info(f"Request: ('content'=str, 'entities'={entities})")

            response = requests.post(
                SA_MODEL_API_URL,
                json={"content": article_content, "entities": entities},
            )

            logging.info(f"Response: {response.json()}")
            response.raise_for_status()

            tickers = response.json()["tickers"]
            articles_tickers.append(tickers)
        except Exception as e:
            articles_tickers.append([])
            logging.error(f"Error processing article {article['id']}: {str(e)}")

    return articles_tickers
