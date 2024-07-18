from pydantic import BaseModel
from typing import List

from src.models.entity import Entity

class Query(BaseModel):
    """
    A class used to represent the Query model.

    Attributes:
        content (str): The content of the query.
        entities (List[Entity]): A list of entities in content.
    """

    content: str
    entities: List[Entity]