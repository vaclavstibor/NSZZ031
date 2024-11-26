import logging
import psycopg2
from psycopg2.extensions import connection as psycopg2_connection


def replicate_and_clear_tables(connection: psycopg2_connection) -> None:
    """
    Replicates data from original tables to temporary tables and delete data from (clears)
    the original tables as a single transaction.

    This function performs several operations in a transaction:
    1. Creates temporary tables to replicate the structure of the original tables.
    2. Copies data from the original tables to the corresponding temporary tables.
    3. Recreates foreign key constraints in the temporary tables.
    4. Deletes data from the original tables.
    5. Resets the serial ID sequence for tables with serial ID columns.

    Args:
        connection (psycopg2_connection): A connection to the database.

    Raises:
        Exception: If any database operation fails, an exception is logged, and the transaction is rolled back.
    """

    try:
        connection.autocommit = False
        cursor = connection.cursor()

        # Create temporary tables
        cursor.execute(
            """
            CREATE TABLE temp_articles (
                id UUID PRIMARY KEY,
                type VARCHAR(50) NOT NULL,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                author VARCHAR(255),
                published_date TIMESTAMP WITH TIME ZONE NOT NULL
            );

            CREATE TABLE temp_companies (
                id SERIAL PRIMARY KEY,
                shortName VARCHAR(100),
                ticker VARCHAR(10) NOT NULL UNIQUE,
                industry VARCHAR(100),
                website VARCHAR(255)
            );

            CREATE TABLE temp_article_companies (
                article_id UUID NOT NULL,
                company_id INT NOT NULL,
                PRIMARY KEY (article_id, company_id),
                FOREIGN KEY (article_id) REFERENCES temp_articles(id) ON DELETE CASCADE,
                FOREIGN KEY (company_id) REFERENCES temp_companies(id) ON DELETE CASCADE
            );

            CREATE TABLE temp_sentiments (
                id SERIAL PRIMARY KEY,
                article_id UUID NOT NULL,
                company_id INT NOT NULL,
                classification VARCHAR(50),
                positive NUMERIC(5,5),
                negative NUMERIC(5,5),
                neutral NUMERIC(5,5),
                FOREIGN KEY (article_id, company_id) REFERENCES temp_article_companies(article_id, company_id) ON DELETE CASCADE,
                UNIQUE (article_id, company_id)
            );

            CREATE TABLE temp_sections (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            );

            CREATE TABLE temp_article_sections (
                article_id UUID NOT NULL,
                section_id INT NOT NULL,
                PRIMARY KEY (article_id, section_id),
                FOREIGN KEY (article_id) REFERENCES temp_articles(id) ON DELETE CASCADE,
                FOREIGN KEY (section_id) REFERENCES temp_sections(id) ON DELETE CASCADE
            );
        """
        )

        # Copy data from original tables to temporary tables
        cursor.execute("INSERT INTO temp_articles SELECT * FROM articles;")
        cursor.execute("INSERT INTO temp_companies SELECT * FROM companies;")
        cursor.execute(
            "INSERT INTO temp_article_companies SELECT * FROM article_companies;"
        )
        cursor.execute("INSERT INTO temp_sentiments SELECT * FROM sentiments;")
        cursor.execute("INSERT INTO temp_sections SELECT * FROM sections;")
        cursor.execute(
            "INSERT INTO temp_article_sections SELECT * FROM article_sections;"
        )

        # Recreate foreign key constraints
        cursor.execute(
            """
            ALTER TABLE temp_article_companies
            ADD CONSTRAINT fk_temp_article_id FOREIGN KEY (article_id) REFERENCES temp_articles(id) ON DELETE CASCADE;

            ALTER TABLE temp_article_companies
            ADD CONSTRAINT fk_temp_company_id FOREIGN KEY (company_id) REFERENCES temp_companies(id) ON DELETE CASCADE;
        """
        )

        cursor.execute(
            """
            ALTER TABLE temp_sentiments
            ADD CONSTRAINT fk_temp_article_company_id FOREIGN KEY (article_id, company_id) REFERENCES temp_article_companies(article_id, company_id) ON DELETE CASCADE;
        """
        )

        cursor.execute(
            """
            ALTER TABLE temp_article_sections
            ADD CONSTRAINT fk_temp_article_id FOREIGN KEY (article_id) REFERENCES temp_articles(id) ON DELETE CASCADE;

            ALTER TABLE temp_article_sections
            ADD CONSTRAINT fk_temp_section_id FOREIGN KEY (section_id) REFERENCES temp_sections(id) ON DELETE CASCADE;
        """
        )

        # Create indexes for the temporary tables
        cursor.execute(
            "CREATE UNIQUE INDEX idx_temp_article_companies_article_id_company_id ON temp_article_companies(article_id, company_id);"
        )
        cursor.execute(
            "CREATE UNIQUE INDEX idx_temp_sentiments_article_id_company_id ON temp_sentiments(article_id, company_id);"
        )
        cursor.execute(
            "CREATE UNIQUE INDEX idx_temp_article_sections_article_id_section_id ON temp_article_sections(article_id, section_id);"
        )

        # List of original tables
        table_names = [
            "articles",
            "companies",
            "article_companies",
            "sentiments",
            "sections",
            "article_sections",
        ]

        for table_name in table_names:
            # Delete data from the original table
            cursor.execute(f"DELETE FROM {table_name}")

        # List of original tables with serial ID columns
        table_names_with_serial_id = ["companies", "sections"]

        for table_name in table_names_with_serial_id:
            # Reset the serial ID sequence for tables with serial ID columns
            cursor.execute(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1")

        connection.commit()
        logging.info(
            "Data deletion, temporary table creation, and foreign key constraints re-creation completed."
        )

    except (Exception, psycopg2.DatabaseError) as error:
        connection.rollback()
        logging.error(f"Error: {error}")
        raise error
    finally:
        cursor.close()
