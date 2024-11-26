import os
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
import nltk
import uvicorn
from contextlib import asynccontextmanager

from src.models.query import Query
from src.models.response import Response

from src.sa.model import Model, analyse_sentiment
from src.utils.helpers import setup_logger
nltk.download("punkt")

setup_logger()
load_dotenv()

FINABSA_MODEL_NAME = os.getenv("FINABSA_MODEL_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))

app = FastAPI()

@app.on_event("startup")
async def startup_event() -> None:
    app.state.model = Model(ckpt_path=FINABSA_MODEL_NAME)


@app.post("/analyse-sentiment", response_model=Response)
async def analyse(
    in_query: Query,
    model: Model = Depends(lambda: app.state.model),
) -> Response:
    """
    Asynchronously analyse sentiment from the input query.

    This function takes in a Query object, analyses sentiment of given entities within the content from the query,
    and returns a Response object containing the list of tickers with sentiment.

    Args:
        in_query (Query): The input query.
        model (Model, optional): The model used for sentiment analysis. Defaults to the model in the application state.

    Returns:
        Response: A Response object containing the list of tickers with sentiment.
    """

    content = in_query.content
    entities = in_query.entities

    tickers_with_sentiment = await analyse_sentiment(
        model=model, content=content, entities=entities
    )

    return Response(tickers=tickers_with_sentiment)


if __name__ == "__main__":
    uvicorn.run("app:app", host=SERVER_HOST, port=SERVER_PORT, reload=True)
