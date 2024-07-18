from enum import Enum

class SentimentClassification(str, Enum):
    NEUTRAL = "NEUTRAL"
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"