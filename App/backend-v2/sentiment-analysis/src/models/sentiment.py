from pydantic import BaseModel

from src.models.sentiment_classification import SentimentClassification

class Sentiment(BaseModel):
    classification: SentimentClassification
    positive: float
    negative: float
    neutral: float  