
import os
from flask import Flask, redirect
from flask_cors import CORS
from flask_restful_swagger_2 import Api, swagger
from flask_swagger_ui import get_swaggerui_blueprint

from dotenv import load_dotenv

# Company Resources
from src.resources.CompanyChart import CompanyChart
from src.resources.CompanyArticleList import CompanyArticleList
from src.resources.CompanyInfo import CompanyInfo
from src.resources.CompanyGraph import CompanyGraph

# Companies Resources
from src.resources.CompaniesNamesAndTickers import CompaniesNamesAndTickers
from src.resources.CompaniesGraphs import CompaniesGraphs

load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

api = Api(app, title='GlobeSense REST API', api_version='0.1', description='A REST API for GlobeSense')

# Company Resources
api.add_resource(CompanyChart, '/api/v0/company/<string:ticker>/chart')
api.add_resource(CompanyArticleList, '/api/v0/company/<string:ticker>/articles')
api.add_resource(CompanyInfo, '/api/v0/company/<string:ticker>/info')
api.add_resource(CompanyGraph, '/api/v0/company/<string:ticker>/graph')

# Companies Resources
api.add_resource(CompaniesNamesAndTickers, '/api/v0/companies/names')
api.add_resource(CompaniesGraphs, '/api/v0/companies/graphs')

SWAGGER_URL = '/api/v0/docs' 
API_URL = '/api/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def index():
    return redirect(SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True, host=SERVER_HOST, port=SERVER_PORT)
    #uvicorn.run("app:app", host=SERVER_HOST, port=SERVER_PORT, reload=True)
