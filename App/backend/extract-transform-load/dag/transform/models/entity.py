from pydantic import BaseModel


class Entity(BaseModel):
    """
    Entity model to represent the extracted entities.

    Attributes:
        text (str): The text of the entity.
        ticker (str): The ticker of the entity.
    """

    text: str
    ticker: str
