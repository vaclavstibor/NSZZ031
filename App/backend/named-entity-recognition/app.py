import os
import uvicorn
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from src.models.response import Response
from src.models.query import Query
from src.ner.model import Model, SPARQLWikidataConnector, extract_entities
from src.utils.helpers import setup_logger
from dotenv import load_dotenv

setup_logger()
load_dotenv()

SPACY_MODEL_NAME = os.getenv("SPACY_MODEL_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler that initializes the model and connector.

    This function is called when the FastAPI application starts up. It initializes
    the model and connector and stores them in the application state.
    """
    app.state.model = Model(model_name=SPACY_MODEL_NAME)
    app.state.connector = SPARQLWikidataConnector()
    yield

app.router.lifespan = lifespan

@app.post("/extract-entities", response_model=Response)
async def extract(
    query: Query,
    model: Model = Depends(lambda: app.state.model),
    connector: SPARQLWikidataConnector = Depends(lambda: app.state.connector),
) -> Response:
    """
    Asynchronously extract entities from the input query.

    This function takes in a Query object, extracts entities from the query content,
    and returns a Response object containing the list of extracted entities.

    Args:
        query (Query): The input query.
        model (Model, optional): The model used for entity extraction. Defaults to the model in the application state.
        connector (SPARQLWikidataConnector, optional): The connector used for entity extraction. Defaults to the connector in the application state.

    Returns:
        Response: A Response object containing the list of extracted entities.
    """
    content = query.content
    entities = await extract_entities(model=model, connector=connector, content=content)
    return Response(entities=entities)

if __name__ == "__main__":
    uvicorn.run("app:app", host=SERVER_HOST, port=SERVER_PORT, reload=True)
