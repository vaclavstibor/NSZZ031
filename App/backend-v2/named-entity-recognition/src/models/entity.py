from pydantic import BaseModel

class Entity(BaseModel):
    """
    A class used to represent the Entity model.

    Attributes:
        text (str): The text of the entity.
        ticker (str): The ticker of the entity.
    """

    text: str
    ticker: str