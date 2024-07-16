from flask_restful_swagger_2 import Resource, swagger

from src.schemata.CompanyChart import CompanyChart as CompanyChartSchema
from src.database.controller import db_controller

class CompanyChart(Resource):
    @swagger.doc({
        'tags': ['Company Chart'],
        'summary': 'Fetches a company\'s chart data from a database and Yahoo Finance.',
        'description': 'Returns a company\'s data to be displayed in a chart.',
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
                'schema': CompanyChartSchema,
            },
            '404': {
                'description': 'Not found'
            },
        }
    })

    def get(self, ticker):
        company_chart = db_controller.get_company_chart(ticker)

        if not company_chart:
            return {'message': 'Not found'}, 404
        
        return company_chart