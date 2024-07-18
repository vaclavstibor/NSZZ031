from flask_restful_swagger_2 import Resource, swagger

from src.schemata.CompanyInfo import CompanyInfo as CompanyInfoSchema
from src.database.controller import db_controller


class CompanyInfo(Resource):
    @swagger.doc(
        {
            "tags": ["Company Info"],
            "summary": "Fetches a company's info from a database and Yahoo Finance.",
            "description": "The data is processed to form a dictionary containing company information such as short name, sector, industry, and website. The function also fetches additional information from Yahoo Finance, such as volume, daily high and low, volume. Additionaly it computes average daily sentiment based on its sentiments from the beggining of day. If no company info is found, a 404 response is returned. The result is returned as a JSON response.",
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
                    "schema": CompanyInfoSchema,
                },
                "404": {"description": "Not found"},
            },
        }
    )

    def get(self, ticker):
        company_info = db_controller.get_company_info(ticker)

        if not company_info:
            return {"message": "Not found"}, 404

        return company_info
