from db import driver
from flask_restful_swagger_2 import Schema, Resource, swagger

class ArticleModel(Schema):

    type = 'object'
    properties = {
        'label': {
            'type': 'string',
        },
        'id': {
            'type': 'integer',
        },
        'title': {
            'type': 'string',
        },
        'url': {
            'type': 'string',
        },
        'time_published': {
            'type': 'string',
        },
        'overall_sentiment_score': {
            'type': 'integer',
        },
        'overall_sentiment_label': {
            'type': 'string',
        },
        'abstract': {
            'type': 'string',
        },
        'body': {
            'type': 'string', # Get from MongoDB by ID
        },
        'ticker_sentiment': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'ticker': {
                        'type': 'string',
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

class Article(Resource):

    @swagger.doc({
        'tags': ['article'],
        'summary': 'Find article by id',
        'description': 'Returns an article',
        'parameters': [
            {
                'name': 'id',
                'description': 'article id',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'An article',
                'schema': ArticleModel,
            },
            '404': {
                'description': 'article not found'
            },
        }
    })

    
    def get(self, id):
        def get_article_by_id(tx, article_id):
            return list(tx.run(
            """
            MATCH (a:Article {id: $id})
            RETURN DISTINCT
            {
                label: head(labels(a)),
                id: id(a),
                title: a.title,
                url: a.url,
                time_published: a.time_published,
                overall_sentiment_score: a.overall_sentiment_score,
                overall_sentiment_label: a.overall_sentiment_label,
                abstract: a.abstract,
                body: a.body,
                ticker_sentiment: [(t)<-[m:MENTIONS]-(a) | {ticker: t.name, ticker_sentiment_score: m.sentiment_score, ticker_sentiment_label: m.sentiment_label}]
            } as article
            """, {'id': article_id}
            ))
        results = driver.session().read_transaction(get_article_by_id, id)
        
        if len(results) == 0:
            return {'message': 'Article not found'}, 404
        
        return results[0]['article'], 200