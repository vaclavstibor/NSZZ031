import logging
import os
from contextlib import contextmanager
from typing import Generator

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as psycopg2_connection

from database.queries.delete_replicated_tables import delete_replicated_tables
from database.queries.replicate_and_clear_tables import replicate_and_clear_tables

from load.load_data_to_db import load_data_to_db
from load.insert_additional_company_data import insert_additional_company_data
from load.delete_articles_without_companies import delete_articles_without_companies

load_dotenv()

ARTICLES_DB = os.getenv("ARTICLES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_PORT = "5432"  # TODO for same docker network port 5432 and postgres; for host machine port 5434 and localhost


class DatabaseController:
    """
    Manages database connections and operations for articles data.

    This controller provides methods to manage the lifecycle of data within the articles database,
    including loading data, replicating and clearing tables, and deleting replicated tables.
    """

    def __init__(self):
        """
        Initializes the DatabaseController with a connection string.
        """
        self.conn_string = f"dbname='{ARTICLES_DB}' user='{POSTGRES_USER}' password='{POSTGRES_PASSWORD}' host='postgres' port='{DB_PORT}'"

    @contextmanager
    def get_connection(self) -> Generator[psycopg2_connection, None, None]:
        """
        Context manager for database connections.

        This method provides a context manager that automatically handles opening and closing
        database connections.

        Yields:
            psycopg2.extensions.connection: A connection to the database.

        Raises:
            Exception: If the connection fails, an exception is raised.
        """
        try:
            connection = psycopg2.connect(self.conn_string)
            if connection:
                try:
                    yield connection
                finally:
                    connection.close()
        except Exception as e:
            logging.error(f"Failed to get database connection: {e}")

    def replicate_and_clear_tables(self) -> None:
        """
        Replicates and clears tables in the database.

        This method uses the `replicate_and_clear_tables` function from queries
        to replicate and clear tables within the database.
        """

        logging.info("Deleting data from the database.")
        with self.get_connection() as connection:
            replicate_and_clear_tables(connection=connection)

    def delete_replicated_tables(self) -> None:
        """
        Deletes replicated tables from the database.

        This method uses the `delete_replicated_tables` function from queries
        to delete temporary tables within the database.
        """

        logging.info("Deleting temporary tables.")
        with self.get_connection() as connection:
            delete_replicated_tables(connection=connection)

    def load_data_to_db(self, source: str, section: str, file_path: str) -> None:
        """
        Loads data from a file to the database.

        Args:
            source (str): The source of the data.
            section (str): The section of the data.
            file_path (str): The file path of the data to be loaded.

        This method uses the `load_data_to_db` function from load phase to load data
        from the specified file into the database.
        """

        logging.info(f"Loading data from {file_path} to the database.")
        with self.get_connection() as connection:
            load_data_to_db(
                connection=connection,
                source=source,
                section=section,
                file_path=file_path,
            )

    def insert_additional_company_data(self) -> None:
        """
        Inserts additional company data into the database from Yahoo Finance.

        This method uses the `insert_additional_company_data` function from load phase 
        to insert additional company data into the database from Yahoo Finance.
        """
        
        logging.info("Inserting additional company data from Yahoo Finance.")
        with self.get_connection() as connection:
            insert_additional_company_data(connection=connection)

    def delete_articles_without_companies(self) -> None:
        """
        Deletes articles that do not have any associated companies in the database.

        This method uses the `delete_articles_without_companies` function from load phase
        to delete articles that do not have any associated companies.
        """

        logging.info("Deleting articles without companies.")
        with self.get_connection() as connection:
            delete_articles_without_companies(connection=connection)

