from src.data_sources.the_guardian import TheGuardian
from src.data_sources.models.base_source import BaseSource

from src.utils.helpers import setup_logger

from dotenv import load_dotenv
from typing import List

import os
import logging

setup_logger()
load_dotenv()

THE_GUARDIAN_SECTIONS = os.getenv("THE_GUARDIAN_SECTIONS").split(",")
BEGGINING_OF_TIME = os.getenv("BEGGINING_OF_TIME")


class DataExtractionManager:
    """ """

    def __init__(self, source: BaseSource):
        self.source = source

    def fetch_data(self, sections: List[str], from_date: str) -> None:
        self.source.fetch_articles(sections, from_date)

def fetch_data():
    """
    Fetch data to .json files from the sources.
    """
    guardian = DataExtractionManager(TheGuardian())
    guardian.fetch_data(THE_GUARDIAN_SECTIONS, BEGGINING_OF_TIME)
    logging.info("The Guardian data extraction completed.")
    
if __name__ == "__main__":
    fetch_data()
        
