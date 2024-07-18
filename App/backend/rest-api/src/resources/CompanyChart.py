from flask_restful_swagger_2 import Resource, swagger

from src.schemata.CompanyChart import CompanyChart as CompanyChartSchema
from src.database.controller import db_controller


class CompanyChart(Resource):
    @swagger.doc(
        {
            "tags": ["Company Chart"],
            "summary": "Fetches a company's chart data from a database and Yahoo Finance.",
            "description": "The data is processed to form a chart representation consisting of historical data for the company. For each day to the past 3 months the data contains adjusted close price, volume, and sentiment score. Sentiment data are average for each day and are calculated based on the sentiment of articles from the beggining of the day. Additional price data in sentiment are for purpose of visualisation. The result is a dictionary containing the chart data, which is returned as a JSON response. If no company is found, a 404 response is returned.",
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
                    "schema": CompanyChartSchema,
                },
                "404": {"description": "Not found"},
            },
        }
    )
    def get(self, ticker):
        company_chart = db_controller.get_company_chart(ticker)

        if not company_chart:
            return {"message": "Not found"}, 404

        return company_chart
