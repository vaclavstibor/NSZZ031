from src.utils.file_manager import FileManager
from src.utils.helpers import setup_logger

import logging

setup_logger

file = FileManager.load_file_to_df("the-guardian", "business")

logging.info(file)
logging.info("file read")