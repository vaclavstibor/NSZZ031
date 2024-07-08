import logging
import psycopg2
from psycopg2.extensions import connection as psycopg2_connection


def delete_replicated_tables(connection: psycopg2_connection) -> None:
    """
    Deletes all temporary tables (tables prefixed with "temp_") from the public schema
    of the database as a single transaction.

    Args:
        connection (psycopg2_connection): A connection to the database.
    """
    try:
        connection.autocommit = False
        cursor = connection.cursor()

        # Select all table names in the public schema
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        )
        table_names = [row[0] for row in cursor.fetchall()]

        for table_name in table_names:
            # Check it the table is temporary and drop it if it is
            if table_name.startswith("temp_"):
                cursor.execute(f"DROP TABLE {table_name} CASCADE")

        connection.commit()
        logging.info("Temporary table deletion completed.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error: {error}")
        connection.rollback()
    finally:
        cursor.close()
