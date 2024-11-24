import os
import pandas as pd
import logging
from datetime import datetime
import numpy as np

from db_model import get_db_session, WeatherRecord

# Configure logging
logger = logging.getLogger(__name__)

def parse_file(filepath):
    """
    Parse the weather data file into a pandas DataFrame.
    Replace -9999 values with NaN for handling missing data.
    """
    station_id = os.path.basename(filepath).replace('.txt', '')

    # Read the file using pandas
    df = pd.read_csv(
        filepath,
        sep='\t',
        header=None,
        names=['date', 'max_temp', 'min_temp', 'precipitation'],
        dtype={'date': str, 'max_temp': float, 'min_temp': float, 'precipitation': float},
        na_values=-9999  # Replace -9999 with NaN
    )

    # Convert date format and scale temperature/precipitation values
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df['max_temp'] = df['max_temp'] / 10.0
    df['min_temp'] = df['min_temp'] / 10.0
    df['precipitation'] = df['precipitation'] / 10.0
    df['station_id'] = station_id

    df= df.replace({np.nan: None})

    return df

# def insert_records(session, records):
#     """
#     Insert records into the database, avoiding duplicates.
#     """
#     session.bulk_save_objects(records)

def ingest_file(filepath, session):
    """
    Parse a single file and ingest its records into the database.
    """
    logger.info(f"Processing file: {filepath}")
    try:
        df = parse_file(filepath)

        # Convert the DataFrame to a list of WeatherRecord objects
        records = [
            WeatherRecord(
                station_id=row['station_id'],
                date=row['date'],
                max_temp=row['max_temp'],
                min_temp=row['min_temp'],
                precipitation=row['precipitation']
            )
            for i, row in df.iterrows()
        ]

        # Insert the records
        session.bulk_save_objects(records)
        session.commit()
        logger.info(f"Completed file: {filepath}, Records: {len(records)}")
    except Exception as e:
        logger.error(f"Error processing file {filepath}: {e}")
        session.rollback()

def run_ingestion(wx_data_dir, db_url, max_workers=5):
    """
    Main function to handle ingestion from all files in the directory.
    """
    session_factory = get_db_session(db_url)
    session = session_factory()

    start_time = datetime.now()
    logger.info(f"Starting ingestion at {start_time}")

    # Get list of all text files in the directory
    files = [os.path.join(wx_data_dir, f) for f in os.listdir(wx_data_dir) if f.endswith('.txt')]

    # Process files using ThreadPoolExecutor

    for filepath in files:
        ingest_file(filepath, session)

    end_time = datetime.now()
    logger.info(f"Completed ingestion at {end_time}")
    logger.info(f"Duration: {end_time - start_time}")
    session.close()
