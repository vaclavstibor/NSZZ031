from pydantic import BaseModel

from src.models.sentiment import Sentiment

class EntityWithSentiment(BaseModel):
    """
    A class used to represent the entities with sentiment model.

    Attributes:
        text (str): The text of the entity.
        ticker (str): The ticker of the entity.
        sentiment (str): The sentiment of the entity.
    """

    text: str
    ticker: str
    sentiment: Sentiment   