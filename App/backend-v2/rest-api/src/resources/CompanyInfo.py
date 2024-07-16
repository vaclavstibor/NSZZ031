from flask_restful_swagger_2 import Resource, swagger

from src.database.controller import db_controller
from src.schemata.CompanyInfo import CompanyInfo as CompanyInfoSchema

class CompanyInfo(Resource):
    @swagger.doc({
        'tags': ['Company Info'],
        'summary': 'Fetches a company\'s info from a database and Yahoo Finance.',
        'description': 'Returns a company\'s info.',
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
                'schema': CompanyInfoSchema,
            },
            '404': {
                'description': 'Not found'
            },
        }
    })

    def get(self, ticker):
        company_info = db_controller.get_company_info(ticker)

        if not company_info:
            return {'message': 'Not found'}, 404
        
        return company_info