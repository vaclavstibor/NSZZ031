from flask_restful_swagger_2 import Schema


class CompaniesGraphs(Schema):
    type = "object"
    properties = {
        "nodes": {
            "type": "array",
            "items": {
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "format": "uuid"},
                            "node_type": {"type": "string", "enum": ["article"]},
                            "title": {"type": "string"},
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
                            "companies": {"type": "array", "format": "int"},
                        },
                    },
                    {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "node_type": {"type": "string", "enum": ["company"]},
                            "short_name": {"type": "string"},
                            "ticker": {"type": "string"},
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
                            "articles": {"type": "array", "format": "uuid"},
                        },
                    },
                ]
            },
        },
        "links": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source": {"type": "string", "format": "uuid"},
                    "target": {"type": "integer"},
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
