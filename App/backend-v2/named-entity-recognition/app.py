import os
import uvicorn

from typing import List
import logging

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from src.ner.model import Model, SPARQLWikidataConnector, extract_entities
from src.utils.helpers import setup_logger
from dotenv import load_dotenv

setup_logger()
load_dotenv()

SPACY_MODEL_NAME = os.getenv("SPACY_MODEL_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))


class Query(BaseModel):
    """
    A class used to represent the Query model.

    Attributes:
        content (str): The content of the query.
    """

    content: str


class Entity(BaseModel):
    """
    A class used to represent the Entity model.

    Attributes:
        text (str): The text of the entity.
        ticker (str): The ticker of the entity.
    """

    text: str
    ticker: str


class Response(BaseModel):
    """
    A class used to represent the Response model.

    Attributes:
        entities (List[Entity]): A list of Entity objects.
    """

    entities: List[Entity]


app = FastAPI()


@app.on_event("startup")
def startup_event():
    """
    A startup event handler that initializes the model and connector.

    This function is called when the FastAPI application starts up. It initializes
    the model and connector and stores them in the application state.
    """
    app.state.model = Model(model_name=SPACY_MODEL_NAME)
    app.state.connector = SPARQLWikidataConnector()


@app.post("/extract-entities", response_model=Response)
async def extract(
    in_query: Query,
    model: Model = Depends(lambda: app.state.model),
    connector: SPARQLWikidataConnector = Depends(lambda: app.state.connector),
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
    entities = extract_entities(
        model=model, connector=connector, content=in_query.content
    )

    return Response(entities=[Entity(**x) for x in entities])


if __name__ == "__main__":
    uvicorn.run("app:app", host=SERVER_HOST, port=SERVER_PORT, reload=True)
