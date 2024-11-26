from enum import Enum
from pydantic import BaseModel


class SentimentClassification(str, Enum):
    """
    An enumeration to classify sentiment as positive, negative, or neutral.
    """

    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"


class Sentiment(BaseModel):
    """
    Represents the sentiment of ticker in the text.

    Attributes:
        classification (SentimentClassification): The sentiment classification.
        positive (float): The positive sentiment score.
        negative (float): The negative sentiment score.
        neutral (float): The neutral sentiment score.
    """

    classification: SentimentClassification
    positive: float
    negative: float
    neutral: float
