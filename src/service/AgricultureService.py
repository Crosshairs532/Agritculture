from Agriculture.config.db import DBConnection
from Agriculture.src.logger import get_logger
from Agriculture.src.exception import CustomException
import pandas as pd
import sys

logger = get_logger("AgricultureService")
class AgricultureService:
    def __init__(self):
        self.db_connection = DBConnection()
        logger.info(f"URI : {self.db_connection.config_files.DATABASE_URI}")
    def _get_data(self):
        try:
            df = pd.read_sql('SELECT * FROM vw_harvest_full LIMIT 5', self.db_connection.engine)
            if df.empty:
                logger.warning("No data found in the database.")
            else:
                logger.info(f"Data retrieved successfully with {len(df)} records.")
            return df
            
        except Exception as e:
            logger.error(f"Error in _get_data: {e}")
            raise CustomException("Error in _get_data",e)
    def get_farm_summary(self, region=None, farm_type=None, year=None, season=None):
        try:
            df = self._get_data()
            print(df.head(5))
        except Exception as e:
            logger.error(f"Error in get_farm_summary: {e}")
            raise CustomException("Error in get_farm_summary",e)