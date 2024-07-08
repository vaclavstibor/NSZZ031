from typing import List
from pydantic import BaseModel

from .entity import Entity
from .ticker import Ticker

class NamedEntityRecognitionResponse(BaseModel):
    """

    """

    entities: List[Entity]


class SentimentAnalysisResponse(BaseModel):
    """

    """

    tickers: List[Ticker]