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

# Add the path to the sys.path so that the modules can be imported (especially for airflow to find the modules)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from extract.data_sources.the_guardian import TheGuardian
from extract.data_sources.the_new_york_times import TheNewYorkTimes
from extract.data_sources.financial_times import FinancialTimes

from transform.named_entity_recognition import apply_ner
from transform.sentiment_analysis import apply_sa

from database.controller import DatabaseController

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
    schedule="0 */4 * * *",  # every 4 hours
    catchup=False,
)
def extract_transform_load() -> None:
    """
    ETL pipeline for extracting, transforming, and loading data from various news sources.
    """
    
    db_controller = DatabaseController()

    @task(task_id="replicate_and_clear_tables")
    def replicate_and_clear_tables() -> None:
        """
        Replicates and clears tables in preparation for new data.
        """
        db_controller.replicate_and_clear_tables()

    @task_group(group_id="the_guardian")
    def the_guardian() -> None:
        """
        Replicates and clear
        """

        source = TheGuardian()

        @task()
        def extract_the_guardian_data() -> None:
            """
            Extracts data from The Guardian.
            """

            # At the beginning of the pipeline for the Guardian, create and clear the directories
            source.create_and_clear_directory()

            try:
                source.fetch_articles(BEGINNING_OF_TIME)
                logging.info("The Guardian data extraction completed.")

            except Exception as e:
                logging.error(f"The Guardian data extraction failed. Error: {str(e)}")
                raise
        
        @task_group(group_id="transform_the_guardian_data")
        def transform_the_guardian_data() -> None:
            """
            Transform the Guardian data. For each section, creates task groups for each directory (section)
            in the extract directory. Each file is processed in a separate pipeline. 
            """
            
            for section in source.sections:
                with TaskGroup(group_id=f"transform_{section}") as section_group:
                    # Get a list of all JSON files in the extract directory
                    files = glob.glob(f'{source.directory}/extract/{section}/*.json')

                    # Create a separate pipeline for each file
                    for file in files:

                        # Get the filename without the extension
                        file_basename = os.path.splitext(os.path.basename(file))[0]

                        # We read files here because we will need them in both NER and SA
                        def read_file(ti, file=file, file_basename=file_basename) -> None:
                            """
                            Reads data from file and pushes it to xcom.
                            """
                            
                            with open(file, 'r') as f:
                                data = json.load(f)

                            ti.xcom_push(key=f'{file_basename}_json_extract_articles', value=data)

                        def save_file(ti, file_basename=file_basename, section=section) -> None:
                            """
                            Saves transformed data to a file.

                            Args:
                                ti (TaskInstance): The task instance.
                                file_basename (str): The basename of the file.
                                section (str): The section of the file.
                            """
                            
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

                        # Read the file
                        read = PythonOperator(task_id=f'read_{file_basename}', python_callable=read_file, op_kwargs={'file_basename': file_basename})
                        # Apply named entity recognition
                        ner = PythonOperator(task_id=f'ner_{file_basename}', python_callable=apply_ner, op_kwargs={'file_basename': file_basename})
                        # Apply sentiment analysis
                        sa = PythonOperator(task_id=f'sa_{file_basename}', python_callable=apply_sa, op_kwargs={'file_basename': file_basename})
                        # Save the file
                        save = PythonOperator(task_id=f'save_{file_basename}', python_callable=save_file, op_kwargs={'file_basename': file_basename, 'section': section})

                        read >> ner >> sa >> save

        @task_group(group_id="load_the_guardian_data")
        def load_the_guardian_data() -> None:
            """
            Loads The Guardian data into the database. Each section one by one is 
            loaded into the database.
            """

            previous_section_group = None

            def load_file(file_path, section_name):
                @task(task_id=f"load_{os.path.splitext(os.path.basename(file_path))[0]}_to_db")
                def task_func():
                    db_controller.load_data_to_db("the_guardian", section_name, file_path)
                    logging.info(f"Loaded {os.path.basename(file_path)} to the database.")
                return task_func()

            for section in source.sections:
                with TaskGroup(group_id=f"load_{section}") as section_group:
                    files = glob.glob(f'{source.directory}/transform/{section}/*.json')
                    previous_task = None

                    for file in files:
                        load_task = load_file(file, section)
                        
                        if previous_task:
                            previous_task >> load_task
                        previous_task = load_task

                if previous_section_group:
                    previous_section_group >> section_group

                previous_section_group = section_group

        extract = extract_the_guardian_data()
        transform = transform_the_guardian_data()
        load = load_the_guardian_data()

        extract >> transform >> load

    # The New York Times and Financial Times task groups follow a similar pattern     

    @task(task_id="insert_additional_company_data_to_db")
    def insert_additional_company_data():
        db_controller.insert_additional_company_data()
        logging.info("Additional company data inserted to the database.")

    @task(task_id="delete_articles_without_companies")
    def delete_articles_without_companies():
        db_controller.delete_articles_without_companies()
        logging.info("Articles without companies deleted.")

    @task(task_id="delete_replicated_tables")
    def delete_replicated_tables() -> None:
        db_controller.delete_replicated_tables()
        logging.info("Replicated tables deleted.")

    #replicate_and_clear_tables() >> [the_guardian(), the_new_york_times(), the_financial_times()] >> insert_additional_company_data() >> delete_articles_without_companies() >> delete_replicated_tables()
    # For now, only The Guardian is used
    replicate_and_clear_tables() >> [the_guardian()] >> insert_additional_company_data() >> delete_articles_without_companies() >> delete_replicated_tables()

extract_transform_load()

"""
Template for another sources

@task_group(group_id="the_new_york_times")
def the_new_york_times() -> None:
    @task()
    def extract_the_new_york_times():
        # ...
        logging.info("The New York Times data extraction completed.")

    @task()
    def transform_the_new_york_times_data():
        logging.info("The New York Times data transformation completed.")

    @task()
    def load_the_new_york_times_data():
        logging.info("The New York Times data loading completed.")

    extract_the_new_york_times() >> transform_the_new_york_times_data() >> load_the_new_york_times_data()

@task_group(group_id="the_financial_times")
def the_financial_times() -> None:
    @task()
    def extract_the_financial_times():
        # ...
        logging.info("The Financial Times data extraction completed.")

    @task()
    def transform_the_financial_times_data():
        # ...
        logging.info("The Financial Times data transformation completed.")

    @task()
    def load_the_financial_times_data():
        # ...
        logging.info("The Financial Times data loading completed.")

    extract_the_financial_times() >> transform_the_financial_times_data() >> load_the_financial_times_data()
"""