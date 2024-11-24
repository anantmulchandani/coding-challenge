# setup.py
import logging
import os,sys
from ingestion import run_ingestion
from analysis import calculate_and_store_statistics

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    
    # set this in .env to skip ingestion and analyis and directly expose APIs (DB is persistent)
    if os.getenv('SKIP_INGESTION_AND_ANALYSIS','').lower()== 'yes' :
        logger.warning("As requested in env, skipping the ingestion and analysis process.")
        sys.exit()

    db_url = os.getenv('DB_URL')
    if db_url: 
        logger.info("Received DB URL from env")
    if not db_url:
        logger.error("DB_URL environment variable is not set.")
        exit(1)

    wx_data_dir = 'wx_data/'

    logger.info("Starting data ingestion...")
    run_ingestion(wx_data_dir, db_url)

    logger.info("Starting data analysis...")
    calculate_and_store_statistics(db_url)

    logger.info(" Data Setup completed successfully.")
