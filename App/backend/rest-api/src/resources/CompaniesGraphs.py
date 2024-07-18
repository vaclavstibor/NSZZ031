from flask_restful_swagger_2 import Resource, swagger
from src.database.controller import db_controller

from src.schemata.CompaniesGraphs import CompaniesGraphs as CompaniesGraphsSchema


class CompaniesGraphs(Resource):
    @swagger.doc(
        {
            "tags": ["Companies Graphs"],
            "summary": "Fetches all companies' graphs from a database.",
            "description": "The data is processed to form a graph representation consisting of nodes (representing companies and articles) and links (representing relationships between them), including sentiment analysis for each node. The function also computes average sentiment scores for articles based on associated company sentiments. Due to troubles with (oneOf) field in schema, swagger is not able to load schema of artilce and node to the documentation, so check the code for better understanding. The result is a dictionary containing the graph structure, which is returned as a JSON response. If no companies are found, a 404 response is returned.",
            "responses": {
                "200": {
                    "description": "Successful",
                    "schema": CompaniesGraphsSchema,
                },
                "404": {"description": "Not found"},
            },
        }
    )
    def get(self):
        companies_graphs = db_controller.get_companies_graphs()

        if not companies_graphs:
            return {"message": "Not found"}, 404

        return companies_graphs
