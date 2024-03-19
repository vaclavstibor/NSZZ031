import requests
import json
import os

import logging

from src.utils.helpers import setup_logger
from dotenv import load_dotenv
import time

import pandas as pd

##
TICKER = 'AMZN'
LIMIT = 1000 # max 1000
API_KEY = '' #'0JV1305HSHHJ3MNH'


url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={TICKER}&limit={LIMIT}&apikey={API_KEY}'
##

setup_logger()
load_dotenv()

DATA_DIRECTORY = os.getenv("DATA_DIRECTORY")
THE_GUARDIAN = os.getenv("THE_GUARDIAN")
THE_GUARDIAN_SECTIONS = os.getenv("THE_GUARDIAN_SECTIONS").split(",")

source_sections_map = {
    THE_GUARDIAN : THE_GUARDIAN_SECTIONS
}

class FileManager:
    """
    """
    @staticmethod 
    def load_file_to_df(source: str, section: str, retries=5, delay=5) -> pd.DataFrame:
        """
        Load the section files with articles from the source.
        """
        # TODO - delete retries and set dependency on the task after
        file_name = f"{DATA_DIRECTORY}/{source}/{section}/{section}-1.json"
        for _ in range(retries):
            try:
                logging.info(f"Reading file.. {file_name}")
                
                # reading file..
                return pd.read_json(file_name, encoding='utf-8')
            except FileNotFoundError:
                logging.warning(f"File {file_name} not found, retrying in {delay} seconds...")
                time.sleep(delay)
        
        message = f"Failed to load the file after {retries} attempts."
        logging.error(message)
        raise Exception(message)

    @staticmethod
    def save_file(ticker: str, data):
        file_name = f'{ticker}.json'
        try:
            with open(f'/Users/stiborv/Documents/ZS2324/NPRG045/App/BackEnd/AV/data/search/{file_name}', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"[INFO] Data has been saved into file {file_name}.")
        except:
            raise Exception(f"[ERROR] in FileManager.save()")

if __name__ == '__main__':

    try:
        r = requests.get(url)
        data = r.json()
        print(data)
        FileManager.save_file(TICKER, data)
    except Exception as e:
        print(e)