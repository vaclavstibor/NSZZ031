from pydantic import BaseModel
from typing import List

from src.models.entity import Entity

class Response(BaseModel):
    """
    A class used to represent the Response model.

    Attributes:
        entities (List[Entity]): A list of Entity objects.
    """

    entities: List[Entity]