from flask import request, jsonify
from flask_restful import Api, Resource
import json

from db_model import db, WeatherRecord, YearlyWeatherStatistics
from alchemy_encoder import AlchemyEncoder
#from sqlalchemy import extract

# Pagination helper function
def paginate_query(query, page, per_page):
    total = query.count()
    results = query.offset((page - 1) * per_page).limit(per_page).all()
    #print(results)
    return {
        "data": json.loads(json.dumps(results, cls=AlchemyEncoder)),
        "total": total,
        "page": page,
        "per_page": per_page
    }

# Weather records endpoint
class WeatherAPI(Resource):
    def get(self):
        station_id = request.args.get('station_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 100))

        query = WeatherRecord.query
        if station_id:
            query = query.filter(WeatherRecord.station_id == station_id)
        if start_date:
            query = query.filter(WeatherRecord.date >= start_date)
        if end_date:
            query = query.filter(WeatherRecord.date <= end_date)

        print(query)
        return paginate_query(query, page, per_page)

# Weather statistics endpoint
class WeatherStatsAPI(Resource):
    def get(self):
        station_id = request.args.get('station_id')
        year = request.args.get('year')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = YearlyWeatherStatistics.query
        if station_id:
            query = query.filter(YearlyWeatherStatistics.station_id == station_id)
        if year:
            query = query.filter(YearlyWeatherStatistics.year == int(year))

        return paginate_query(query, page, per_page)
