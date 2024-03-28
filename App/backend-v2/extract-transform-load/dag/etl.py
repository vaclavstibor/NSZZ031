import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, List

from airflow.decorators import dag, task, task_group

from extract.data_sources.the_guardian import TheGuardian

# Add the path to the sys.path so that the modules can be imported.
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))

os.environ['NO_PROXY'] = '*'  # disable proxy

THE_GUARDIAN_SECTIONS = os.getenv("THE_GUARDIAN_SECTIONS").split(",")
# another sources' sections...

BEGINNING_OF_TIME = os.getenv("BEGINNING_OF_TIME")

default_args = {
    "owner": "admin",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="extract_transform_load_remote",
    default_args=default_args,
    start_date=datetime(2024, 3, 27),
    schedule='@daily',
    catchup=False,
)
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
        def extract_the_new_york_times_data():
            # ...
            pass

        extract_the_guardian_data() and extract_the_new_york_times_data()  # and more sources...

    @task_group(group_id="transform")
    def transform() -> None:
        @task()
        def transform_the_guardian_data():
            logging.info("The Guardian data transformation completed.")

        @task()
        def transform_the_new_york_times_data():
            logging.info("The New York Times data transformation completed.")

        transform_the_guardian_data() and transform_the_new_york_times_data()

    @task_group(group_id="load")
    def load() -> None:
        @task()
        def load_the_guardian_data():
            logging.info("The Guardian data loading completed.")

        @task()
        def load_the_new_york_times_data():
            logging.info("The New York Times data loading completed.")

        load_the_guardian_data() and load_the_new_york_times_data()

    extract() >> transform() >> load()


extract_transform_load()
