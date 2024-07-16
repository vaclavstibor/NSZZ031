from flask_restful_swagger_2 import Schema

class CompanyInfo(Schema):
    type = "object"
    properties = {
        "shortName": {"type": "string"},
        "ticker": {"type": "string"},
        "website": {"type": "string"},
        "industry": {"type": "string"},
        "dayHigh": {"type": "number"},
        "dayLow": {"type": "number"},
        "volume": {"type": "number"},
        "sentiment": {
            "type": "object",
            "properties": {
                "classification": {"type": "string", "enum": ["POSITIVE", "NEUTRAL", "NEGATIVE"]},
                "positive": {"type": "number"},
                "neutral": {"type": "number"},
                "negative": {"type": "number"},
            },
        }
    }
