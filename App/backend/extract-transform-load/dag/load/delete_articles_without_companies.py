import logging

import psycopg2
from psycopg2.extensions import connection as psycopg2_connection


def delete_articles_without_companies(connection: psycopg2_connection) -> None:
    """
    Deletes articles that do not have any associated companies in the database.

    Args:
        connection (psycopg2_connection): The database connection.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM articles
                WHERE id NOT IN (
                    SELECT DISTINCT article_id FROM article_companies
                );
            """
            )

            connection.commit()
            logging.info("Articles without companies deleted successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error during deletion of articles without companies: {error}")
        connection.rollback()
    finally:
        cursor.close()
