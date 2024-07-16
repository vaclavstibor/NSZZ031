from flask_restful_swagger_2 import Schema

class CompaniesNamesAndTickers(Schema):
    type = 'array'
    items = {
        'type': 'object',
        'properties': {
            'shortName': {
                'type': 'string'
            },
            'ticker': {
                'type': 'string'
            }
        }
    }