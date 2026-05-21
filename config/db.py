from Agriculture.config.configFiles import ConfigFiles
from sqlalchemy import create_engine
from Agriculture.src.logger import get_logger
logger = get_logger("DBConnection")

class DBConnection:
    engine = None
    def __init__(self):
        self.config_files = ConfigFiles()
        if DBConnection.engine is None:
            logger.info("Creating new database engine.")
            DBConnection.engine = create_engine(self.config_files.DATABASE_URI, pool_pre_ping=True)
            logger.info("Database engine created successfully.")
        
