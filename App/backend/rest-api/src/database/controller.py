import os
import json
from dotenv import load_dotenv
import psycopg2
from typing import Generator
import logging
from contextlib import contextmanager
from psycopg2 import pool

from src.database.queries.get_companies_names_and_tickers import (
    get_companies_names_and_tickers,
)
from src.database.queries.get_company_chart import get_company_chart
from src.database.queries.get_company_article_list import get_company_article_list
from src.database.queries.get_company_info import get_company_info
from src.database.queries.get_company_graph import get_company_graph
from src.database.queries.get_companies_graphs import get_companies_graphs

load_dotenv()

# Define connection parameters
ARTICLES_DB = os.getenv("ARTICLES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_PORT = "5434"  # for same docker network port 5432 and postgres; for host machine port 5434 and localhost
HOST = "localhost"


class DatabaseController:
    """
    Database controller class that manages database connections and queries.
    """

    def __init__(self):
        self.conn_pool = pool.SimpleConnectionPool(
            1,
            10,
            dbname=ARTICLES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=HOST,
            port=DB_PORT,
        )

    @contextmanager
    def get_connection(self) -> Generator[psycopg2.extensions.connection, None, None]:
        """
        Gets a connection from the connection pool and returns it to the pool after the context is done.
        """

        try:
            connection = self.conn_pool.getconn()
            if connection:
                try:
                    yield connection
                finally:
                    self.conn_pool.putconn(connection)
            else:
                logging.error("No available database connections.")
        except Exception as e:
            logging.error(f"Failed to get database connection: {e}")

    def is_etl_running(self) -> bool:
        """
        Check if ETL is running by looking for tables with 'temp_' table_prefix.
        """

        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name LIKE 'temp_%');"
            )
            return cursor.fetchone()[0]

    def get_companies_names_and_tickers(self) -> list:
        """
        Calls the get_companies_names_and_tickers query to get the names and tickers of all companies.
        """

        table_prefix = "temp_" if self.is_etl_running() else ""
        with self.get_connection() as connection:
            companies_names_and_tickers = get_companies_names_and_tickers(
                connection=connection, table_prefix=table_prefix
            )
            return companies_names_and_tickers

    def get_company_graph(self, ticker: str):
        """
        Calls the get_company_graph query to get the graph data for a company with the given ticker.
        """

        table_prefix = "temp_" if self.is_etl_running() else ""
        with self.get_connection() as connection:
            company_graph = get_company_graph(
                connection=connection, ticker=ticker, table_prefix=table_prefix
            )
            return company_graph

    def get_companies_graphs(self):
        """
        Calls the get_companies_graphs query to get the graph data for all companies.
        """

        table_prefix = "temp_" if self.is_etl_running() else ""
        with self.get_connection() as connection:
            companies_graphs = get_companies_graphs(
                connection=connection, table_prefix=table_prefix
            )
            return companies_graphs

    def get_company_chart(self, ticker: str):
        """
        Calls the get_company_chart query to get the chart data for a company with the given ticker.
        """

        table_prefix = "temp_" if self.is_etl_running() else ""
        with self.get_connection() as connection:
            company_chart = get_company_chart(
                connection=connection, ticker=ticker, table_prefix=table_prefix
            )
            return company_chart

    def get_company_article_list(self, ticker: str):
        """
        Calls the get_company_article_list query to get the list of articles for a company with the given ticker.
        """

        table_prefix = "temp_" if self.is_etl_running() else ""
        with self.get_connection() as connection:
            company_articles = get_company_article_list(
                connection=connection, ticker=ticker, table_prefix=table_prefix
            )
            return company_articles

    def get_company_info(self, ticker: str):
        """
        Calls the get_company_info query to get the info for a company with the given ticker.
        """

        table_prefix = "temp_" if self.is_etl_running() else ""
        with self.get_connection() as connection:
            ticker_info = get_company_info(
                connection=connection, ticker=ticker, table_prefix=table_prefix
            )
            return ticker_info


db_controller = DatabaseController()
