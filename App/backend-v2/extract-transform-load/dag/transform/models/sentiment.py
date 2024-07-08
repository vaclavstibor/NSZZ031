from enum import Enum
from pydantic import BaseModel

class SentimentClassification(str, Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"

class Sentiment(BaseModel):
    classification: SentimentClassification
    positive: float
    negative: float
    neutral: float