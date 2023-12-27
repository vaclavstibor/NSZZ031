from flask_restful_swagger_2 import Schema, Resource, swagger
from db import driver

def serialize_ticker(ticker):
    return {
        'name': ticker['name']
    }

class TickerModel(Schema):

    # id >> DEPRECATED << name is good enough
    type = 'object'
    properties = {
        'label': {
            'type': 'string',
        },        
        'id': {
            'type': 'integer',
        },
        'name': {
            'type': 'string',
        },
        'overall_sentiment_score': {
            'type': 'integer',
        },
        'overall_sentiment_label': {
            'type': 'string',
        },
        'articles': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'label': {
                        'type': 'string',
                    },                    
                    'id': {
                        'type': 'integer',
                    },
                    'title': {
                        'type': 'string',
                    },
                    'ticker_sentiment_score': {
                        'type': 'integer',
                    },
                    'ticker_sentiment_label': {
                        'type': 'string',
                    },
                    'article_sentiment_score': {
                        'type': 'integer',
                    },
                    'article_sentiment_label': {
                        'type': 'string',
                    }
                }
            }
        }
    }

class TickerGraphModel(Schema):
    type = 'object'
    properties = {
        'nodes': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'integer',
                    },
                    'label': {
                        'type': 'string',
                    },
                    'name': {
                        'type': 'string',
                    },
                    'overall_sentiment_score': {
                        'type': 'integer',
                    },
                    'overall_sentiment_label': {
                        'type': 'string',
                    }
                }
            }
        },
        'links': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'source': {
                        'type': 'integer',
                    },
                    'target': {
                        'type': 'integer',
                    },
                    'ticker_sentiment_score': {
                        'type': 'integer',
                    },
                    'ticker_sentiment_label': {
                        'type': 'string',
                    }
                }
            }
        }
    }


class Ticker(Resource):

    @swagger.doc({
        'tags': ['ticker'],
        'summary': 'Find ticker by name',
        'description': 'Returns a ticker',
        'parameters': [
            {
                'name': 'name',
                'description': 'ticker name',
                'in': 'path',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'A ticker',
                'schema': TickerModel,
            },
            '404': {
                'description': 'ticker not found'
            },
        }
    })

    def get(self, name):
        def get_ticker_by_name(tx, ticker_name):
            return list(tx.run(
            """
            MATCH (ticker:Ticker {name: $name})
            OPTIONAL MATCH (ticker)-[is_mentioned_in:IS_MENTIONED_IN]->(article:Article)
            RETURN DISTINCT 
            {
                label: head(labels(ticker)), 
                id: id(ticker), 
                name: ticker.name 
            } as ticker,
            collect(DISTINCT 
            { 
                label: head(labels(article)),             
                id: id(article), 
                title: article.title, 
                ticker_sentiment_score: is_mentioned_in.ticker_sentiment_score,
                ticker_sentiment_label: is_mentioned_in.ticker_sentiment_label,
                article_sentiment_score: article.overall_sentiment_score,
                article_sentiment_label: article.overall_sentiment_label
            }) AS articles
            """, {'name': ticker_name}
            ))
        results = driver.session().read_transaction(get_ticker_by_name, name)

        if len(results) == 0:
            return {'message': 'ticker not found'}, 404

        result = results[0]
        ticker = result['ticker']
        articles = result['articles']

        return {
            'label': ticker['label'],
            'id': ticker['id'],
            'name': ticker['name'],
            'overall_sentiment_score': 0,
            'overall_sentiment_label': 'none',
            'articles': [
                {
                    'label': article['label'],
                    'id': article['id'],
                    'title': article['title'],
                    'ticker_sentiment_score': article['ticker_sentiment_score'],
                    'ticker_sentiment_label': article['ticker_sentiment_label'],
                    'article_sentiment_score': article['article_sentiment_score'],
                    'article_sentiment_label': article['article_sentiment_label'],
                }
                for article in articles
            ]
        }
    
class TickerList(Resource):
# For tickers list we only need the name 

    @swagger.doc({
        'tags': ['tickers'],
        'summary': 'Find all tickers',
        'description': 'Returns a list of tickers',
        'responses': {
            '200': {
                'description': 'A list of tickers',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'name': {
                                'type': 'string',
                            },
                        }
                    },
                }
            }
        }
    })

    def get(self):
        def get_tickers(tx):
            return list(tx.run(
                """
                MATCH (ticker:Ticker) RETURN ticker
                """
            ))
        results = driver.session().read_transaction(get_tickers)

        if len(results) == 0:
            return {'message': 'tickers not found'}, 404

        return [
                record['ticker']['name']
        
            for record in results
        ]

class TickerGraph(Resource):
    @swagger.doc({
        'tags': ['tickers'],
        'summary': 'Get ticker graph',
        'description': 'Returns lists of nodes and links',
        'responses': {
            '200': {
                'description': 'A list of tickers',
                'schema': TickerGraphModel,
            }
        }
    })

    def get(self):
        def get_tickers(tx):
            return list(tx.run(
                """
                MATCH (ticker:Ticker) RETURN ticker
                """
            ))
        results = driver.session().read_transaction(get_tickers)

        if len(results) == 0:
            return {'message': 'tickers not found'}, 404

        return {
            'nodes': [
                {
                    'id': record['ticker'].id,
                    'label': record['ticker'].labels[0],
                    'name': record['ticker']['name'],
                    'overall_sentiment_score': record['ticker']['overall_sentiment_score'],
                    'overall_sentiment_label': record['ticker']['overall_sentiment_label']
                }
                for record in results
            ],
            'links': [
                {
                    'source': record['ticker'].id,
                    'target': record['article'].id,
                    'ticker_sentiment_score': record['is_mentioned_in']['ticker_sentiment_score'],
                    'ticker_sentiment_label': record['is_mentioned_in']['ticker_sentiment_label']
                }
                for record in results
            ]
        }