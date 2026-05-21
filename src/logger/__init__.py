import logging
import os
from datetime import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

file_handler = logging.FileHandler(LOG_FILE_PATH, mode='a')
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

def get_logger(name: str):

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger