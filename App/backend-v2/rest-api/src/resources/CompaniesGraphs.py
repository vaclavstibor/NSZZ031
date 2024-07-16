from flask_restful_swagger_2 import Resource, swagger
from src.database.controller import db_controller

from src.schemata.CompaniesGraphs import CompaniesGraphs as CompaniesGraphsSchema

class CompaniesGraphs(Resource):

    @swagger.doc({
        'tags': ['Companies Graphs'],
        'summary': 'Fetches all companies\' graphs from a database.',
        'description': 'Returns a companies\' graphs data to be displayed in a graph.',
        'responses': {
            '200': {
                'description': 'Successful',
                'schema': CompaniesGraphsSchema,
            },
            '404': {
                'description': 'Not found'
            },
        }
    })

    def get(self):
        companies_graphs = db_controller.get_companies_graphs()

        if not companies_graphs:
            return {'message': 'Not found'}, 404
        
        return companies_graphs