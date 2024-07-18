import logging
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection as psycopg2_connection

def get_companies_names_and_tickers(connection: psycopg2_connection, table_prefix: str):
    """
    Fetches all companies' names and tickers from a database.

    Args:
        connection (psycopg2_connection): A connection object to the database.
        table_prefix (str): The prefix used to identify the correct table within the database.

    Returns:
        list: A list of dictionaries, where each dictionary contains 'shortName' and 'ticker' keys for a company.

    Raises:
        Logs an error message if an exception occurs during database access.
    """

    try:
        with connection.cursor() as cursor:
            # Safely create a table identifier with the prefix
            table_name = sql.Identifier(f"{table_prefix}companies")
            query = sql.SQL("SELECT shortName, ticker FROM {}").format(table_name)
            
            cursor.execute(query)
            companies_names_and_tickers = cursor.fetchall()
            
            companies_names_and_tickers = [{'shortName': company_name, 'ticker': company_ticker} for company_name, company_ticker in companies_names_and_tickers]
            
        return companies_names_and_tickers
    
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error fetching companies names and tickers: {error}")
        return []