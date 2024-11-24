import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func, extract
from db_model import get_db_session, WeatherRecord, YearlyWeatherStatistics

# Configure logging
logger = logging.getLogger(__name__)

def calculate_and_store_statistics(db_url):
    """
    Calculate yearly statistics for each weather station and store the results in the database.
    """
    session_factory = get_db_session(db_url)
    session = session_factory()

    try:
        # Query to calculate yearly statistics

                # SELECT 
                #     station_id, 
                #     EXTRACT(year FROM date) AS year, 
                #     ROUND(AVG(max_temp), 2) AS avg_max_temp, 
                #     ROUND(AVG(min_temp), 2) AS avg_min_temp, 
                #     ROUND(SUM(precipitation), 2) AS total_precipitation 
                # FROM weather_records 
                # GROUP BY station_id, EXTRACT(year FROM date) 

        logger.info("Calculating yearly statistics...")

        results = (
            session.query(
                WeatherRecord.station_id,
                extract('year', WeatherRecord.date).label('year'),
                func.avg(WeatherRecord.max_temp).label('avg_max_temp'),
                func.avg(WeatherRecord.min_temp).label('avg_min_temp'),
                func.sum(WeatherRecord.precipitation).label('total_precipitation'),
            )
            .group_by(WeatherRecord.station_id, extract('year', WeatherRecord.date))
            .all()
        )

        # Transform results into YearlyWeatherStatistics objects
        statistics = []
        for result in results:
            statistics.append(
                YearlyWeatherStatistics(
                    station_id=result.station_id,
                    year=int(result.year),
                    avg_max_temp=result.avg_max_temp,
                    avg_min_temp=result.avg_min_temp,
                    total_precipitation=result.total_precipitation / 10.0  # Convert mm to cm
                    if result.total_precipitation is not None else None,
                )
            )

        # Insert results into yearly_weather_statistics table
        logger.info(f"Inserting {len(statistics)} rows into yearly_weather_statistics table...")
        for stat in statistics:
            # Use merge to avoid duplicates on station_id and year
            session.merge(stat)
        session.commit()
        logger.info("Yearly statistics calculation and storage completed successfully.")

    except Exception as e:
        session.rollback()
        logger.error(f"An error occurred: {e}")
    finally:
        session.close()
