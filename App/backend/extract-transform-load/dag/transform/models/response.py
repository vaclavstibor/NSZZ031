from typing import List
from pydantic import BaseModel

from .entity import Entity
from .ticker import Ticker

class NamedEntityRecognitionResponse(BaseModel):
    """
    Represents the response of the Named Entity Recognition API.

    Attributes:
        entities (List[Entity]): The extracted entities.
    """

    entities: List[Entity]


class SentimentAnalysisResponse(BaseModel):
    """
    Represents the response of the Sentiment Analysis API.

    Attributes:
        tickers (List[Ticker]): The tickers of the companies mentioned in the text.
    """

    tickers: List[Ticker]