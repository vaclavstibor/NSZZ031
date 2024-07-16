from flask_restful_swagger_2 import Schema, Resource, swagger

from src.schemata.CompaniesNamesAndTickers import CompaniesNamesAndTickers as CompaniesNamesAndTickersSchema
from src.database.controller import db_controller

class CompaniesNamesAndTickers(Resource):
    @swagger.doc({
        'tags': ['Companies Names and Tickers'],
        'summary': 'Fetches all companies\' names and tickers from a database.',
        'description': 'Returns a list of all companies\' names and tickers.',
        'responses': {
            '200': {
                'description': 'Successful',
                'schema': CompaniesNamesAndTickersSchema
            },
            '404': {
                'description': 'Not found'
            }
        }
    })

    def get(self):
        companies_names_and_tickers = db_controller.get_companies_names_and_tickers()

        if len(companies_names_and_tickers) == 0:
            return {'message': 'Not found'}, 404

        return companies_names_and_tickers