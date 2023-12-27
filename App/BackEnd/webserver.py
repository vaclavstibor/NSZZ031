from flask import Flask, redirect
from flask_restful_swagger_2 import Api
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from db import driver
from models.ticker import Ticker, TickerList
from models.article import Article

app = Flask(__name__)
CORS(app)

api = Api(app, title='Neo4j GlobeSense Demo API', api_version='0.1')
api.add_resource(Ticker, '/api/v0/tickers/<string:name>')
api.add_resource(TickerList, '/api/v0/tickers')

# Article
api.add_resource(Article, '/api/v0/articles/<int:id>')

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
    app.run(debug=True, host='0.0.0.0', port=8080)
