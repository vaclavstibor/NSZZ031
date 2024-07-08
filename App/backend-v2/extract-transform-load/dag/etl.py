import os
import sys
import time
import glob
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List

from airflow.decorators import dag, task, task_group
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.sensors.filesystem import FileSensor
from airflow.models import TaskInstance

# Add the path to the sys.path so that the modules can be imported (especially for airflow to find the modules)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from extract.data_sources.the_guardian import TheGuardian
from extract.data_sources.the_new_york_times import TheNewYorkTimes
from extract.data_sources.financial_times import FinancialTimes

from transform.named_entity_recognition import apply_ner
from transform.sentiment_analysis import apply_sa

from database.controller import DatabaseController

# https://github.com/apache/airflow/discussions/24463 (for macOS)
os.environ["NO_PROXY"] = "*"

#BEGINNING_OF_TIME = os.getenv("BEGINNING_OF_TIME")
BEGINNING_OF_TIME = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')

default_args = {
    "owner": "admin",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    dag_id="extract_transform_load",
    default_args=default_args,
    start_date=datetime(2024, 6, 11),
    schedule="0 */12 * * *",  # every 12 hours
    catchup=False,
)
def extract_transform_load() -> None:
    
    db_controller = DatabaseController()

    @task(task_id="replicate_and_clear_tables")
    def replicate_and_clear_tables() -> None:
        db_controller.replicate_and_clear_tables()

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

                        # We read files here because we will need them in both NER and SA
                        def read_file(ti, file=file, file_basename=file_basename):
                            with open(file, 'r') as f:
                                data = json.load(f)

                            ti.xcom_push(key=f'{file_basename}_json_extract_articles', value=data)

                        def save_file(ti, file_basename=file_basename, section=section):
                            data = ti.xcom_pull(key=f'{file_basename}_json_extract_articles')
                            tickers = ti.xcom_pull(key=f'{file_basename}_articles_tickers')
                            
                            # Create a list to hold all articles and their entities
                            all_articles = []

                            # Save the data to a file
                            for article, tickers in zip(data, tickers):
                                article['tickers'] = tickers
                                article.pop('content', None)
                                all_articles.append(article)

                            with open(f'{source.directory}/transform/{section}/{file_basename}.json', 'w') as f:
                                json.dump(all_articles, f, ensure_ascii=False, indent=4)
                            
                            logging.info(f"Saved {len(all_articles)} articles to {section}/{file_basename}.json")

                        #logging.info(f'{source.directory}/extract/{section}/{file_basename}.json')

                        # Read the file
                        read = PythonOperator(task_id=f'read_{file_basename}', python_callable=read_file, op_kwargs={'file_basename': file_basename})
                        # Apply named entity recognition
                        ner = PythonOperator(task_id=f'ner_{file_basename}', python_callable=apply_ner, op_kwargs={'file_basename': file_basename})
                        # Apply sentiment analysis
                        sa = PythonOperator(task_id=f'sa_{file_basename}', python_callable=apply_sa, op_kwargs={'file_basename': file_basename})
                        # Save the file
                        save = PythonOperator(task_id=f'save_{file_basename}', python_callable=save_file, op_kwargs={'file_basename': file_basename, 'section': section})

                        # read file >> ner >> sa >> save file
                        read >> ner >> sa >> save

        @task_group(group_id="load_the_guardian_data")
        def load_the_guardian_data() -> None:
            previous_section_group = None

            for section in source.sections:
                with TaskGroup(group_id=f"load_{section}") as section_group:
                    files = glob.glob(f'{source.directory}/transform/{section}/*.json')
                    #logging.info(f"Found {len(files)} files in {section} section for loading.")
                    previous_task = None
                    for file in files:
                        file_basename = os.path.splitext(os.path.basename(file))[0]

                        @task(task_id=f"load_{file_basename}_to_db")
                        def load_file(file_path=file, section_name=section):
                            db_controller.load_data_to_db("the_guardian", section_name, file_path)
                            logging.info(f"Loaded {file_basename} to the database.")

                        load = load_file(file_path=file, section_name=section)

                        if previous_task:
                            previous_task >> load  # Set the current task to execute after the previous task completes (we do not want deadlocks)

                        previous_task = load  # Update the previous_task to the current task for the next iteration

                    if previous_section_group:
                        previous_section_group >> section_group  # Ensure the current section group executes after the previous section group completes
                    
                    previous_section_group = section_group  # Update the previous_section_group to the current section group


        extract = extract_the_guardian_data()
        transform = transform_the_guardian_data()
        load = load_the_guardian_data()

        extract >> transform >> load

    @task(task_id="delete_replicated_tables")
    def delete_replicated_tables() -> None:
        db_controller.delete_replicated_tables()

    replicate_and_clear_tables() >> [the_guardian()] >> delete_replicated_tables()
    #replicate_and_clear_tables() >> the_guardian() >> delete_replicated_tables() and the_new_york_times() and financial_times() >> delete_replicated_tables()

extract_transform_load()

"""
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

"""