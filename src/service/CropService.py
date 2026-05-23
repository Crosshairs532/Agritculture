from config.db import DBConnection
from src.logger import get_logger
from src.exception import CustomException
import pandas as pd


logger = get_logger("CropService")

class CropService: 
    def __init__(self):
        self.db_connection = DBConnection()
    def _get_data(self, view_name):
        logger.info("Reading Crop Data from database")
        try:
            df = pd.read_sql(f'SELECT * FROM {view_name}', self.db_connection.engine)
            if df.empty:
                logger.warning("No data found in the database.")
            else:
                logger.info(f"Data retrieved successfully with {len(df)} records.")
            return df
            
        except Exception as e:
            logger.error(f"Error in _get_data: {e}")
            raise CustomException("Error in _get_data",e)