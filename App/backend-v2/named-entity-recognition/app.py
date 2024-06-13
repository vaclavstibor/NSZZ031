"""
We use the FastAPI because BaseModel is a Pydantic model that is used to define the request and response models for the FastAPI endpoints.

 - add to Microsoft Azure https://www.youtube.com/watch?v=HyCO6nMdxC0&t=2s
 
"""

from typing import List
import logging

from fastapi import FastAPI
from pydantic import BaseModel

from src.ner.model import extract_entities
from src.utils.helpers import setup_logger

setup_logger()

class Query(BaseModel):
    content: str


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


@app.post("/extract-entities", response_model=Response)
async def extract(in_query: Query):
    """
    Asynchronously predict the entities in the input content.
    By using async def instead of def: this function should be run in a separate thread, allowing FastAPI to take other requests while this function is running.
    """
    entities = extract_entities(in_query.content)

    return Response(entities=[Entity(**x) for x in entities])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5051, reload=True)