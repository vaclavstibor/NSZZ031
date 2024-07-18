from flask_restful_swagger_2 import Resource, swagger

from src.schemata.CompanyGraph import CompanyGraph as CompanyGraphSchema
from src.database.controller import db_controller


class CompanyGraph(Resource):
    @swagger.doc(
        {
            "tags": ["Company Graph"],
            "summary": "Fetches a company's graph data from a database.",
            "description": "The data is processed to form a graph representation consisting of nodes (representing companies and articles) and links (representing relationships between them), including sentiment analysis for each node. The function also computes average daily sentiment score for ticker based its sentiment in articles from the beggining of the day. Which is also used in ticker info. The result is a dictionary containing the graph structure, which is returned as a JSON response. If no company is found, a 404 response is returned.",
            "parameters": [
                {
                    "name": "ticker",
                    "description": "The company's ticker symbol",
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
