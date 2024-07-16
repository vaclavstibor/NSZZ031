import logging
import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
import nltk
from pydantic import BaseModel
import uvicorn

from src.models.entity import Entity
from src.models.query import Query
from src.models.entity_with_sentiment import EntityWithSentiment
from src.models.response import Response

from src.sa.model import Model, analyse_sentiment
from src.utils.helpers import setup_logger

# Download in root due to possibility of multiple workers of server
nltk.download("punkt")

setup_logger()
load_dotenv()

FINABSA_MODEL_NAME = os.getenv("FINABSA_MODEL_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))

app = FastAPI()


@app.on_event("startup")
def startup_event():
    """
    A startup event handler that initializes the model and connector.

    This function is called when the FastAPI application starts up. It initializes
    the model and connector and stores them in the application state.
    """
    app.state.model = Model(ckpt_path=FINABSA_MODEL_NAME)


@app.post("/analyse-sentiment", response_model=Response)
async def analyse(
    in_query: Query,
    model: Model = Depends(lambda: app.state.model),
) -> Response:
    """
    Asynchronously extract entities from the input query.

    This function takes in a Query object, extracts entities from the query content,
    and returns a Response object containing the extracted entities.

    Args:
        in_query (Query): The input query.
        model (Model, optional): The model used for entity extraction. Defaults to the model in the application state.
        connector (SPARQLWikidataConnector, optional): The connector used for entity extraction. Defaults to the connector in the application state.

    Returns:
        Response: A Response object containing the extracted entities.
    """

    content = in_query.content
    entities = in_query.entities

    tickers_with_sentiment = await analyse_sentiment(
        model=model, content=content, entities=entities
    )

    return Response(tickers=tickers_with_sentiment)


if __name__ == "__main__":
    uvicorn.run("app:app", host=SERVER_HOST, port=SERVER_PORT, reload=True)
