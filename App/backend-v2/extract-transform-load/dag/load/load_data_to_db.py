import json
import logging
from datetime import datetime
from typing import List
from uuid import UUID

import psycopg2
from psycopg2.extras import execute_batch
from psycopg2.extensions import connection as psycopg2_connection
from psycopg2.extensions import cursor as psycopg2_cursor

from load.models.article import Article
from load.models.company import Company
from load.models.sentiment import Sentiment


def get_section_id(cursor: psycopg2_cursor, section: str) -> int:
    """
    Retrieves the ID of the section from the database. If the section does not exist,
    it is inserted into the database.

    Args:
        cursor (psycopg2_cursor): The database cursor.
        section (str): The name of the section.

    Returns:
        int: The ID of the section.
    """

    cursor.execute("SELECT id FROM sections WHERE name = %s;", (section,))
    section_id = cursor.fetchone()

    if not section_id:
        cursor.execute(
            "INSERT INTO sections (name) VALUES (%s) RETURNING id;", (section,)
        )
        section_id = cursor.fetchone()[0]
    else:
        section_id = section_id[0]
    return section_id


def insert_companies(cursor: psycopg2_cursor, companies: List[Company]) -> None:
    """
    Inserts companies (with only ticker) into the database if they don't already exist. 
    

    Args:
        cursor (psycopg2_cursor): The database cursor.
        companies (List[Company]): A list of Company objects to be inserted.
    """

    # This function insters only company ticker so that we don't have to repeatedly download data from yahoo finance for each ticker
    
    # Additional data from yahoo finance are downloaded (once) after the insertion of all tickers via `insert_additional_company_data`

    # Due to potentinal noise data (wikidata QIDs) from the extraction process, we only insert tickers with length less than or equal to 10
    valid_companies = [company for company in companies if len(company.ticker) <= 10]

    # Prepare data for insertion
    companies_data = [(company.ticker,) for company in valid_companies]

    if companies_data:
        insert_query = "INSERT INTO companies (ticker) VALUES (%s) ON CONFLICT (ticker) DO NOTHING;"
        execute_batch(cursor, insert_query, companies_data)        

def insert_article(cursor: psycopg2_cursor, article: Article) -> None:
    """
    Inserts an article into the database if it doesn't already exist.

    Args:
        cursor (psycopg2_cursor): The database cursor.
        article (Article): The Article object to be inserted.
    """

    cursor.execute("SELECT id FROM articles WHERE id = %s;", (article.id,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO articles (id, type, url, title, author, published_date) VALUES (%s, %s, %s, %s, %s, %s);",
            (
                article.id,
                article.type,
                article.url,
                article.title,
                article.author,
                article.published_date,
            ),
        )


def insert_article_section(
    cursor: psycopg2_cursor, article_id: UUID, section_id: int
) -> None:
    """
    Inserts a relationship between an article and a section into the database.

    Args:
        cursor (psycopg2_cursor): The database cursor.
        article_id (UUID): The ID of the article.
        section_id (int): The ID of the section.
    """

    cursor.execute(
        "INSERT INTO article_sections (article_id, section_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
        (article_id, section_id),
    )


def insert_article_company(
    cursor: psycopg2_cursor, article_id: UUID, company: Company
) -> None:
    """
    Inserts a relationship between an article and a company into the database, along with sentiment data.

    Args:
        cursor (psycopg2_cursor): The database cursor.
        article_id (UUID): The ID of the article.
        company (Company): The Company object associated with the article.
    """

    cursor.execute("SELECT id FROM companies WHERE ticker = %s;", (company.ticker,))
    company_id = cursor.fetchone()

    if company_id:
        company_id = company_id[0]
        cursor.execute(
            "INSERT INTO article_companies (article_id, company_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (article_id, company_id),
        )
        sentiment = company.sentiment
        cursor.execute(
            "INSERT INTO sentiments (article_id, company_id, classification, positive, negative, neutral) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
            (
                article_id,
                company_id,
                sentiment.classification,
                sentiment.positive,
                sentiment.negative,
                sentiment.neutral,
            ),
        )


def load_data_to_db(
    connection: psycopg2_connection, source: str, section: str, file_path: str
) -> None:
    """
    Loads data from a JSON file into the database, including articles, companies based on tickers, and their relationships.
    (keeping source information for case of multiple sources in the future)

    Args:
        connection (psycopg2_connection): The database connection.
        source (str): The source of the data.
        section (str): The section of the data.
        file_path (str): The file path to the JSON file containing the data.
    """

    try:
        with connection.cursor() as cursor:
            section_id = get_section_id(cursor, section)

            with open(file_path, "r") as file:
                data = json.load(file)
                for item in data:
                    item["id"] = UUID(item["id"])
                    item["published_date"] = datetime.fromisoformat(
                        item["published_date"].replace("Z", "+00:00")
                    )
                    tickers_data = item.pop("tickers", [])
                    companies = [
                        Company(
                            ticker=ticker_data["ticker"],
                            sentiment=Sentiment(**ticker_data["sentiment"]),
                        )
                        for ticker_data in tickers_data
                    ]
                    item["companies"] = companies

                    article = Article(**item)
                    if not article.companies:
                        continue

                    insert_companies(cursor, article.companies)
                    insert_article(cursor, article)
                    insert_article_section(cursor, article.id, section_id)
                    for company in article.companies:
                        insert_article_company(cursor, article.id, company)

        connection.commit()
        logging.info("Data loading completed successfully.")

    except (
        Exception,
        psycopg2.DatabaseError,
        FileNotFoundError,
        json.JSONDecodeError,
    ) as error:
        logging.error(f"Error during data loading: {error}")
        connection.rollback()
    finally:
        cursor.close()
