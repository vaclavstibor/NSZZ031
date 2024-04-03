import os
import sys
import glob
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List

from airflow.decorators import dag, task, task_group
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import TaskInstance

# Add the path to the sys.path so that the modules can be imported (especially for airflow to find the modules)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from extract.data_sources.models.base_source import BaseSource
from extract.data_sources.the_guardian import TheGuardian
from extract.data_sources.the_new_york_times import TheNewYorkTimes
from extract.data_sources.financial_times import FinancialTimes

from transform.named_entity_recognition import apply_ner
#from transform.named_entity_recognition import NER, apply_model
#from transform.sentiment_analysis import SA, apply_model

# https://github.com/apache/airflow/discussions/24463 (for macOS)
os.environ["NO_PROXY"] = "*"

BEGINNING_OF_TIME = os.getenv("BEGINNING_OF_TIME")

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
def extract_transform_load() -> None:
    @task_group(group_id="the_guardian")
    def the_guardian() -> None:
        source = TheGuardian()

        @task()
        def extract_the_guardian_data() -> None:
            # At the beginning of the pipeline, create and clear the directories
            source.create_and_clear_directory()
            logging.info("The Guardian data extraction started.")
            try:
                source.fetch_articles(BEGINNING_OF_TIME)
                logging.info("The Guardian data extraction completed.")
            except Exception as e:
                logging.error(f"The Guardian data extraction failed. Error: {str(e)}")
                raise
        
        @task_group(group_id="transform_the_guardian_data")
        def transform_the_guardian_data() -> None:
            for section in source.sections:
                with TaskGroup(group_id=f"transform_{section}") as section_group:
                    # Get a list of all JSON files in the extract directory
                    files = glob.glob(f'{source.directory}/extract/{section}/*.json')

                    # Create a separate pipeline for each file
                    for file in files:

                        # Get the filename without the extension
                        file_basename = os.path.splitext(os.path.basename(file))[0]

                        def load_file(ti: TaskInstance, file=file, file_basename=file_basename):
                            with open(file, 'r') as f:
                                data = json.load(f)

                            ti.xcom_push(key=f'{file_basename}_json_extract_articles', value=data)

                        """
                        def apply_ner_model(ti):
                            data = ti.xcom_pull(key='json_extract_articles')
                            entities = apply_ner(data)
                            # Apply NER model to data
                            # ...
                        

                        def apply_sentiment_analysis(ti):
                            data = ti.xcom_pull(key=f'{file_basename}_json_extract_articles')
                            entities = ti.xcom_pull(key=f'{file_basename}_articles_entities')                            
                            # Apply sentiment analysis to data
                            # ...
                        """

                        def save_file(ti: TaskInstance, file_basename=file_basename, section=section):
                            data = ti.xcom_pull(key=f'{file_basename}_json_extract_articles')
                            entities = ti.xcom_pull(key=f'{file_basename}_articles_entities')
                            
                            # Create a list to hold all articles and their entities
                            all_articles = []

                            # Save the data to a file
                            for article, entity in zip(data, entities):
                                article['entities'] = entity
                                all_articles.append(article)

                            with open(f'{source.directory}/transform/{section}/{file_basename}.json', 'w') as f:
                                json.dump(all_articles, f, ensure_ascii=False, indent=4)
                            
                            logging.info(f"Saved {len(all_articles)} articles to {section}/{file_basename}.json")

                        # Define the pipeline for this file
                        load = PythonOperator(task_id=f'load_{file_basename}', python_callable=load_file, op_kwargs={'file_basename': file_basename})
                        ner = PythonOperator(task_id=f'ner_{file_basename}', python_callable=apply_ner, op_kwargs={'file_basename': file_basename})
                        #sentiment = PythonOperator(task_id=f'sentiment_{file_basename}', python_callable=apply_sentiment_analysis, op_kwargs={'file_basename': file_basename})
                        save = PythonOperator(task_id=f'save_{file_basename}', python_callable=save_file, op_kwargs={'file_basename': file_basename, 'section': section})
                        
                        #load >> ner >> #sentiment >> save
                        load >> ner >> save

        @task()
        def load_the_guardian_data() -> None:
            logging.info("The Guardian data loading completed.")

        extract_the_guardian_data() >> transform_the_guardian_data() >> load_the_guardian_data()

    @task_group(group_id="the_new_york_times")
    def the_new_york_times() -> None:
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

        extract_the_new_york_times() >> transform_the_new_york_times_data() >> load_the_new_york_times_data()

    @task_group(group_id="financial_times")
    def financial_times() -> None:
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

        extract_financial_times() >> transform_financial_times_data() >> load_financial_times_data()

    the_guardian() #and the_new_york_times() and financial_times()

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
