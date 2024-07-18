from flask_restful_swagger_2 import Resource, swagger

from src.schemata.CompanyArticleList import (
    CompanyArticleList as CompanyArticleListSchema,
)
from src.database.controller import db_controller


class CompanyArticleList(Resource):
    @swagger.doc(
        {
            "tags": ["Company Article List"],
            "summary": "Fetches a company's articles from a database.",
            "description": "The data is processed to form a list of dictionaries, where each dictionary contains data for an article. If no articles are found, a 404 response is returned. The result is returned as a JSON response.",
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
                    "schema": CompanyArticleListSchema,
                },
                "404": {"description": "Not found"},
            },
        }
    )
    def get(self, ticker):
        company_articles = db_controller.get_company_article_list(ticker)

        if not company_articles:
            return {"message": "Not found"}, 404

        return company_articles
