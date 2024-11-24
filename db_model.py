from sqlalchemy import create_engine #, Column, String, Float, Integer, Date, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, sessionmaker

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the SQLAlchemy base
Base = declarative_base()

# WeatherRecord model
class WeatherRecord(db.Model):
    __tablename__ = 'weather_records'

    station_id = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    max_temp = db.Column(db.Float, nullable=True)
    min_temp = db.Column(db.Float, nullable=True)
    precipitation = db.Column(db.Float, nullable=True)

    # composite primary key for faster queries
    __table_args__ = (db.PrimaryKeyConstraint('station_id', 'date'),)

class YearlyWeatherStatistics(db.Model):
    __tablename__ = 'yearly_weather_statistics'

    station_id = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avg_max_temp = db.Column(db.Float, nullable=True)
    avg_min_temp = db.Column(db.Float, nullable=True)
    total_precipitation = db.Column(db.Float, nullable=True)

    __table_args__ = (
        db.PrimaryKeyConstraint('station_id', 'year'),
    )

# Database setup
def get_db_session(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    Session = sessionmaker(bind=engine)
    return Session
