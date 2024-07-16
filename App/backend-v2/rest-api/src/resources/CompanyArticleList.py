from flask_restful_swagger_2 import Resource, swagger
from src.database.controller import db_controller

from src.schemata.CompanyArticleList import CompanyArticleList as CompanyArticleListSchema

class CompanyArticleList(Resource):
    @swagger.doc({
        'tags': ['Company Article List'],
        'summary': 'Fetches a company\'s articles from a database.',
        'description': 'Returns a company\'s articles.',
        'parameters': [
            {
                'name': 'ticker',
                'description': 'The ticker of the company.',
                'in': 'path',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'Successful',
                'schema': CompanyArticleListSchema,
            },
            '404': {
                'description': 'Not found'
            },
        }
    })

    def get(self, ticker):
        company_articles = db_controller.get_company_article_list(ticker)
        
        if not company_articles:
            return {'message': 'Not found'}, 404

        return company_articles