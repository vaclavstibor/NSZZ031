import psycopg2
import yfinance as yf
from psycopg2.extensions import connection as psycopg2_connection
from psycopg2 import sql
import logging
from flask import jsonify
from datetime import datetime, timezone

def compute_daily_sentiment(
    records: list,
    article_id_index: int,
    published_date_index: int,
    positive_index: int,
    negative_index: int,
    neutral_index: int,
) -> tuple:
    """
    Compute the average sentiment for articles published on the current day.

    Args:
        records (list): A list of tuples containing article data.
        article_id_index (int): The index of the article ID in the tuple.
        published_date_index (int): The index of the published date in the tuple.
        positive_index (int): The index of the positive sentiment score in the tuple.
        negative_index (int): The index of the negative sentiment score in the tuple.
        neutral_index (int): The index of the neutral sentiment score in the tuple.

    Returns:
        tuple: A tuple containing the overall sentiment classification ('POSITIVE', 'NEGATIVE', 'NEUTRAL') and the average positive, negative, and neutral sentiment scores.
    """

    sentiments = {"positive": [], "negative": [], "neutral": []}

    # Current day at 00:00:00
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    for record in records:
        if record[article_id_index]:  # If there's an article_id
            published_date = record[published_date_index]
            if published_date.tzinfo is not None:
                published_date = published_date.astimezone(timezone.utc).replace(
                    tzinfo=None
                )
            if published_date >= start_of_day:
                sentiments["positive"].append(
                    record[positive_index] if record[positive_index] else 0
                )
                sentiments["negative"].append(
                    record[negative_index] if record[negative_index] else 0
                )
                sentiments["neutral"].append(
                    record[neutral_index] if record[neutral_index] else 0
                )

    avg_positive = (
        round(sum(sentiments["positive"]) / len(sentiments["positive"]), 5)
        if sentiments["positive"]
        else 0
    )
    avg_negative = (
        round(sum(sentiments["negative"]) / len(sentiments["negative"]), 5)
        if sentiments["negative"]
        else 0
    )
    avg_neutral = (
        round(sum(sentiments["neutral"]) / len(sentiments["neutral"]), 5)
        if sentiments["neutral"]
        else 0
    )

    classification = "NEUTRAL"
    if avg_positive > avg_negative and avg_positive > avg_neutral:
        classification = "POSITIVE"
    elif avg_negative > avg_positive and avg_negative > avg_neutral:
        classification = "NEGATIVE"

    return classification, avg_positive, avg_negative, avg_neutral


def get_company_info(
    connection: psycopg2_connection, ticker: str, table_prefix: str
) -> dict:
    """
    Retrieve company information based on the ticker symbol. The information includes the company's ticker, short name, industry, website, daily high and low prices, volume, and average daily sentiment.

    Args:
        connection (psycopg2_connection): A connection to the database.
        ticker (str): The ticker symbol of the company.
        table_prefix (str): The prefix of the table to query in the database.

    Returns:
        dict: A dictionary containing company information.
    """

    query = sql.SQL(
        """
    SELECT 
        c.id AS company_id, c.ticker, c.shortName, c.industry, c.website,
        a.id AS article_id, a.title, a.published_date, a.type, a.url, a.author,
        s.classification AS sentiment_classification, s.positive, s.negative, s.neutral
    FROM {companies} c
    LEFT JOIN {article_companies} at ON c.id = at.company_id
    LEFT JOIN {articles} a ON at.article_id = a.id
    LEFT JOIN {sentiments} s ON a.id = s.article_id AND c.id = s.company_id
    WHERE c.ticker = %s;
    """
    ).format(
        companies=sql.Identifier(table_prefix + "companies"),
        article_companies=sql.Identifier(table_prefix + "article_companies"),
        articles=sql.Identifier(table_prefix + "articles"),
        sentiments=sql.Identifier(table_prefix + "sentiments"),
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (ticker,))
            records = cursor.fetchall()

            avg_daily_sentiment = compute_daily_sentiment(
                records=records,
                article_id_index=5,
                published_date_index=7,
                positive_index=12,
                negative_index=13,
                neutral_index=14,
            )

            if records:
                company_info = records[0]  # Extract company info from the first record
                ticker, short_name, industry, website = company_info[1:5]
            else:
                ticker, short_name, industry, website = (ticker, "N/A", "N/A", "N/A")

            # Define the keys we are interested in from Yahoo Finance
            keys_of_interest = ["dayHigh", "dayLow", "volume"]

            # Get the ticker information from yahoo finance
            ticker_info = yf.Ticker(ticker).info

            # Extract the relevant information
            relevant_info = {
                key: ticker_info.get(key, "N/A") for key in keys_of_interest
            }

            return jsonify(
                {
                    "ticker": ticker,
                    "shortName": short_name,
                    "industry": industry,
                    "website": website,
                    **relevant_info,
                    "sentiment": {
                        "classification": avg_daily_sentiment[0],
                        "positive": avg_daily_sentiment[1],
                        "negative": avg_daily_sentiment[2],
                        "neutral": avg_daily_sentiment[3],
                    },
                }
            )

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error fetching company info: {error}")
        return jsonify({})
