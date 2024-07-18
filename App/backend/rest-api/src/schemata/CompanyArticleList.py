from flask_restful_swagger_2 import Schema


class CompanyArticleList(Schema):
    type = "array"
    items = {
        "type": "object",
        "properties": {
            "id": {"type": "string", "format": "uuid"},
            "title": {"type": "string"},
            "type": {"type": "string"},
            "section": {"type": "string"},
            "published_date": {"type": "string", "format": "date-time"},
            "url": {"type": "string", "format": "uri"},
            "author": {"type": "string", "x-nullable": True},
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
    }
