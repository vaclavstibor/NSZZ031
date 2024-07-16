from flask_restful_swagger_2 import Resource, swagger
from src.database.controller import db_controller

from src.schemata.CompanyGraph import CompanyGraph as CompanyGraphSchema


class CompanyGraph(Resource):
    @swagger.doc(
        {
            "tags": ["Company Graph"],
            "summary": "Fetches a company's graph data from a database.",
            "description": "Returns a company's graph data to be displayed in a graph.",
            "parameters": [
                {
                    "name": "ticker",
                    "description": "The ticker of the company.",
                    "in": "path",
                    "type": "string",
                    "required": True,
                }
            ],
            "responses": {
                "200": {
                    "description": "Successful",
                    "schema": CompanyGraphSchema,
                },
                "404": {"description": "Not found"},
            },
        }
    )
    def get(self, ticker):
        company_graph = db_controller.get_company_graph(ticker)

        if not company_graph:
            return {"message": "Not found"}, 404

        return company_graph
