import unittest
from main import app
from db_model import db, WeatherRecord, YearlyWeatherStatistics
import os

class WeatherAPITestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    STATION_ID = 'USC00253365'

    def test_weather_endpoint(self):
        STATION_ID = 'USC00253365'
        response = self.app.get(f'/api/weather?station_id={STATION_ID}&page=1&per_page=10')
        self.assertEqual(response.status_code, 200)

    def test_weather_stats_endpoint(self):
        STATION_ID = 'USC00253365'
        response = self.app.get(f'/api/weather/stats?station_id={STATION_ID}&year=2000')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
