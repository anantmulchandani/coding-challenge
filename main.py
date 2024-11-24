from flask import Flask
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
import logging
import os

from db_model import db
# from ingestion import run_ingestion
# from analysis import calculate_and_store_statistics
from api import WeatherAPI, WeatherStatsAPI

logger = logging.getLogger(__name__)

def create_app(db_url, config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config:
        app.config.update(config)

    db.init_app(app)
    return app


if __name__ == '__main__':
    # PostgreSQL connection URL

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    db_url = os.getenv('DB_URL')

    app = create_app(db_url)
    api = Api(app)

    api.add_resource(WeatherAPI, '/api/weather')
    api.add_resource(WeatherStatsAPI, '/api/weather/stats')

    # Configure Swagger
    SWAGGER_URL = '/swagger'
    API_URL = '/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Running the application
    app.run(host='0.0.0.0', debug=True, port= 6200)