"""
We use the FastAPI because BaseModel is a Pydantic model that is used to define the request and response models for the FastAPI endpoints.

TODO:
 - pip install spacy-transformers [x]
 - pip install spacy-entity-linker [x]
 - python3 -m spacy download en_core_web_trf [x]
 - python3 -m spacy_entity_linker "download_knowledge_base" [x]
 - pip install pywikibot [x]
 - pip install colorlog [x]
 - then change it in requirements.txt

 
"""

from typing import List
import logging

from fastapi import FastAPI
from pydantic import BaseModel

from src.model import predict_entities
from src.utils.helpers import setup_logger

setup_logger()

class Query(BaseModel):
    text: str


class Entity(BaseModel):
    ticker: str
    exchange: str
    text: str
    label: str
    start_idx: int
    end_idx: int


class Response(BaseModel):
    entities: List[Entity]


app = FastAPI()


@app.post("/predict/", response_model=Response)
async def predict(in_query: Query):
    """
    Asynchronously predict the entities in the input text.
    By using async def instead of def: this function should be run in a separate thread, allowing FastAPI to take other requests while this function is running.
    """
    entities = predict_entities(in_query.text)
    
    return Response(entities=[Entity(**x) for x in entities])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)