import os
from dotenv import load_dotenv

from typing import List
import requests
import logging
from airflow.models import TaskInstance

from .models.response import NamedEntityRecognitionResponse as NERResponse

load_dotenv()

NER_MODEL_API_URL = os.getenv("NER_MODEL_API_URL")


def apply_ner(ti: TaskInstance, file_basename: str) -> None:
    """
    Function to apply Named Entity Recognition (NER) to the articles content.
    It pulls the data from the xcom, applies the NER model to the content of the articles and pushes the result back to the xcom.

    Args:
        ti (TaskInstance): The task instance object.
        file_basename (str): The base name of the file.
    """

    # Extract data (file) from xcom
    data = ti.xcom_pull(key=f"{file_basename}_json_extract_articles")

    articles_entities = post_request(data)

    logging.info(f"Articles entities {articles_entities}")
    logging.info(f"pushing into {file_basename}_articles_entities")

    ti.xcom_push(key=f"{file_basename}_articles_entities", value=articles_entities)


def post_request(data: List[dict]) -> List[NERResponse]:
    """
    Function to post request to the NER model API and get the entities.
    It pulls the data from the xcom, applies the NER model to the content of the articles and pushes the result back to the xcom.

    Args:
        data (List[dict]): The list of articles.

    Returns:
        List[NERResponse]: The list of entities extracted from the articles.
    """
    articles_entities = []

    for article in data:
        article_content = article["content"]

        try:
            response = requests.post(
                NER_MODEL_API_URL, json={"content": article_content}
            )
            response.raise_for_status()

            entities = response.json()["entities"]
            articles_entities.append(entities)
        except Exception as e:
            logging.error(f"Failed post request to NER model. Error: {str(e)}")
            raise

    return articles_entities
