import logging

import psycopg2
from psycopg2.extensions import connection as psycopg2_connection
import yfinance as yf


def insert_additional_company_data(connection: psycopg2_connection) -> None:
    """
    Inserts additional data for companies from Yahoo Finance into the database.
    Deletes the company if the fetched data is empty.

    Args:
        connection (psycopg2_connection): The database connection.
    """

    try:
        with connection.cursor() as cursor:
            keys_of_interest = ["shortName", "industry", "website"]

            cursor.execute("SELECT ticker FROM companies;")
            tickers = cursor.fetchall()
            tickers = [ticker[0] for ticker in tickers]

            for ticker in tickers:
                cursor.execute("SELECT id FROM companies WHERE ticker = %s;", (ticker,))
                company_id = cursor.fetchone()

                if company_id:
                    # Fetch company info from Yahoo Finance
                    company_info = yf.Ticker(ticker).info
                    additional_data = {
                        key: company_info.get(key, None) for key in keys_of_interest
                    }

                    # If fetched data is not empty
                    # is not a number check due to some of bug in Yahoo Finance library
                    if (
                        any(additional_data.values())
                        and additional_data["shortName"].isdigit() is not True
                    ):
                        # Update the company record with additional data
                        update_query = """
                        UPDATE companies
                        SET shortName = %s, industry = %s, website = %s
                        WHERE ticker = %s;
                        """
                        cursor.execute(
                            update_query,
                            (
                                additional_data["shortName"],
                                additional_data["industry"],
                                additional_data["website"],
                                ticker,
                            ),
                        )
                    else:
                        # Delete the company if fetched data is empty
                        delete_query = "DELETE FROM companies WHERE ticker = %s;"
                        cursor.execute(delete_query, (ticker,))

        connection.commit()
        logging.info("Additional company data insertion completed.")

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error during additional data insertion: {error}")
        connection.rollback()
    finally:
        cursor.close()
