from dataclasses import dataclass


@dataclass
class Sentiment:
    """
    Data class that represents the sentiment of an ticker.

    Attributes:
        classification (str): The classification of the sentiment (positive, negative, neutral).
        positive (float): The positive sentiment score.
        negative (float): The negative sentiment score.
        neutral (float): The neutral sentiment score.
    """

    classification: str
    positive: float
    negative: float
    neutral: float
