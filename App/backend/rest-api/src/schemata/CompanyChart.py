from flask_restful_swagger_2 import Schema


class CompanyChart(Schema):
    type = "object"
    properties = {
        "price_data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "format": "date-time"},
                    "adj_close": {"type": "number"},
                },
            },
        },
        "sentiment_data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "format": "date-time"},
                    "adj_close": {"type": "number"},
                    "sentiment": {
                        "type": "object",
                        "properties": {
                            "classification": {
                                "type": "string",
                                "enum": ["POSITIVE", "NEUTRAL", "NEGATIVE"],
                            },
                            "positive": {"type": "number"},
                            "neutral": {"type": "number"},
                            "negative": {"type": "number"},
                        },
                    },
                },
            },
        },
    }
