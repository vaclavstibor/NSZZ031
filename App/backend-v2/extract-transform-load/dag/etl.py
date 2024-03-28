import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, List

from airflow.decorators import dag, task, task_group
from airflow.utils.task_group import TaskGroup

# Add the path to the sys.path so that the modules can be imported (especially for airflow to find the modules)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from extract.data_sources.the_guardian import TheGuardian
from extract.data_sources.the_new_york_times import TheNewYorkTimes
from extract.data_sources.financial_times import FinancialTimes

# https://github.com/apache/airflow/discussions/24463 (for macOS)
os.environ["NO_PROXY"] = "*"

BEGINNING_OF_TIME = os.getenv("BEGINNING_OF_TIME")

THE_GUARDIAN_SECTIONS = os.getenv("THE_GUARDIAN_SECTIONS").split(",")
# another sources' sections...

default_args = {
    "owner": "admin",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="extract_transform_load",
    default_args=default_args,
    start_date=datetime(2024, 3, 27),
    schedule="@daily",
    catchup=False,
)
def extract_transform_load():
    @task()
    def extract_the_guardian_data():
        logging.info("The Guardian data extraction started.")
        source = TheGuardian()
        try:
            source.fetch_articles(THE_GUARDIAN_SECTIONS, BEGINNING_OF_TIME)
            logging.info("The Guardian data extraction completed.")
        except Exception as e:
            logging.error(f"The Guardian data extraction failed. Error: {str(e)}")
            raise

    @task()
    def transform_the_guardian_data():
        logging.info("The Guardian data transformation completed.")

    @task()
    def load_the_guardian_data():
        logging.info("The Guardian data loading completed.")

    with TaskGroup(group_id="the_guardian") as guardian:
        extract = extract_the_guardian_data()
        transform = transform_the_guardian_data()
        load = load_the_guardian_data()
        extract >> transform >> load

    @task()
    def extract_the_new_york_times():
        logging.info("The New York Times data extraction started.")
        source = TheNewYorkTimes()
        # ...
        logging.info("The New York Times data extraction completed.")

    @task()
    def transform_the_new_york_times_data():
        logging.info("The New York Times data transformation completed.")

    @task()
    def load_the_new_york_times_data():
        logging.info("The New York Times data loading completed.")

    with TaskGroup(group_id="the_new_york_times") as new_york_times:
        extract = extract_the_new_york_times()
        transform = transform_the_new_york_times_data()
        load = load_the_new_york_times_data()
        extract >> transform >> load

    @task()
    def extract_financial_times():
        logging.info("The Financial Times data extraction started.")
        source = FinancialTimes()
        # ...
        logging.info("The Financial Times data extraction completed.")

    @task()
    def transform_financial_times_data():
        logging.info("The Financial Times data transformation completed.")

    @task()
    def load_financial_times_data():
        logging.info("The Financial Times data loading completed.")

    with TaskGroup(group_id="financial_times") as financial_times:
        extract = extract_financial_times()
        transform = transform_financial_times_data()
        load = load_financial_times_data()
        extract >> transform >> load

    guardian and new_york_times and financial_times

extract_transform_load()

"""
def extract_transform_load():
    @task_group(group_id="extract")
    def extract() -> None:
        @task()
        def extract_the_guardian_data():
            logging.info("The Guardian data extraction started.")
            source = TheGuardian()
            try:
                source.fetch_articles(THE_GUARDIAN_SECTIONS, BEGINNING_OF_TIME)
                logging.info("The Guardian data extraction completed.")
            except Exception as e:
                logging.error(f"The Guardian data extraction failed. Error: {str(e)}")
                raise

        @task()
        def extract_the_new_york_times():
            logging.info("The New York Times data extraction started.")
            source = TheNewYorkTimes()
            # ...
            logging.info("The New York Times data extraction completed.")
            pass

        @task()
        def extract_financial_times():
            logging.info("The Financial Times data extraction started.")
            source = FinancialTimes()
            # ...
            logging.info("The Financial Times data extraction completed.")
            pass

        extract_the_guardian_data() and extract_the_new_york_times() and extract_financial_times()  # and more sources...

    @task_group(group_id="transform")
    def transform() -> None:
        @task()
        def transform_the_guardian_data():
            logging.info("The Guardian data transformation completed.")

        @task()
        def transform_the_new_york_times_data():
            logging.info("The New York Times data transformation completed.")

        @task()
        def transform_financial_times_data():
            logging.info("The Financial Times data transformation completed.")

        transform_the_guardian_data() and transform_the_new_york_times_data() and transform_financial_times_data()  # and more sources...

    @task_group(group_id="load")
    def load() -> None:
        @task()
        def load_the_guardian_data():
            logging.info("The Guardian data loading completed.")

        @task()
        def load_the_new_york_times_data():
            logging.info("The New York Times data loading completed.")

        @task()
        def load_financial_times_data():
            logging.info("The Financial Times data loading completed.")

        load_the_guardian_data() and load_the_new_york_times_data() and load_financial_times_data()

    extract() >> transform() >> load()


extract_transform_load()
"""
