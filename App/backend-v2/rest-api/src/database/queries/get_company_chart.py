import logging
from datetime import datetime, timedelta

import pandas as pd
import psycopg2
from flask import jsonify
from psycopg2 import sql
from psycopg2.extensions import connection as psycopg2_connection
import yfinance as yf


def find_nearest_market_day(date: datetime, market_days: pd.Series) -> datetime:
    """
    Finds the nearest market day to a given date.

    Args:
        date (datetime): The date to find the nearest market day for.
        market_days (pd.Series): A pandas Series containing market days.

    Returns:
        datetime: The nearest market day to the given date.
    """

    date = pd.to_datetime(date)
    market_days = pd.to_datetime(market_days)

    if pd.isna(date):
        return None

    future_day = market_days[market_days >= date].min()
    past_day = market_days[market_days <= date].max()

    # NaTType check
    if pd.isna(future_day):
        return past_day.date()
    if pd.isna(past_day):
        return future_day.date()

    if (future_day - date) < (date - past_day):
        return future_day.date()
    else:
        return past_day.date()


def aggregate_sentiments(group: pd.DataFrame) -> pd.Series:
    """
    Aggregates sentiment data for a group of articles.

    Args:
        group (pd.DataFrame): A pandas DataFrame containing sentiment data for a group of articles.

    Returns:
        Series: A pandas Series containing the mode of classification and the mean of positive, neutral, and negative sentiments.
    """

    classification = group["classification"].mode().values[0]
    positive = group["positive"].mean()
    neutral = group["neutral"].mean()
    negative = group["negative"].mean()
    return pd.Series(
        {
            "classification": classification,
            "positive": positive,
            "neutral": neutral,
            "negative": negative,
        }
    )


def get_company_chart(connection: psycopg2_connection, ticker: str, table_prefix: str) -> dict:
    """
    Fetches and aggregates company sentiment and price data (from Yahoo Finance) based on comapny ticker.

    Args:
        connection (psycopg2_connection): A psycopg2 connection object to the database.
        ticker (str): The ticker symbol of the company.
        table_prefix (str): The prefix used for table names in the database.

    Returns:
        TODO
    """

    try:
        # Fetch price data from Yahoo Finance
        start_date = datetime.now() - timedelta(days=90)
        end_date = datetime.now()

        price_data = yf.download(ticker, start=start_date, end=end_date)
        print(price_data)
        price_data = price_data[["Adj Close"]]
        price_data.reset_index(inplace=True)

        price_list = []
        for index, row in price_data.iterrows():
            price_list.append(
                {"date": row["Date"].isoformat(), "adj_close": row["Adj Close"]}
            )

        # Safely construct query with table prefix
        query = sql.SQL(
            """
        SELECT 
            a.published_date, s.classification, s.positive, s.neutral, s.negative
        FROM {articles} a
        JOIN {article_companies} at ON a.id = at.article_id
        JOIN {companies} c ON at.company_id = c.id
        JOIN {sentiments} s ON a.id = s.article_id AND at.company_id = s.company_id
        WHERE c.ticker = %s;
        """
        ).format(
            articles=sql.Identifier(table_prefix + "articles"),
            article_companies=sql.Identifier(table_prefix + "article_companies"),
            companies=sql.Identifier(table_prefix + "companies"),
            sentiments=sql.Identifier(table_prefix + "sentiments"),
        )

        with connection.cursor() as cursor:
            cursor.execute(query, (ticker,))
            records = cursor.fetchall()

        print(records)

        sentiment_df = pd.DataFrame(
            records,
            columns=["date", "classification", "positive", "neutral", "negative"],
        )

        sentiment_df["date"] = pd.to_datetime(sentiment_df["date"]).dt.date

        market_days = price_data["Date"].dt.date

        sentiment_df["date"] = sentiment_df["date"].apply(
            lambda x: find_nearest_market_day(x, market_days)
        )

        sentiment_df = (
            sentiment_df.groupby("date").apply(aggregate_sentiments).reset_index()
        )

        print("after", sentiment_df)

        sentiment_list = []
        for index, row in sentiment_df.iterrows():
            date_str = row["date"].isoformat()
            adj_close = (
                price_data.loc[
                    price_data["Date"].dt.date == row["date"], "Adj Close"
                ].values[0]
                if row["date"] in price_data["Date"].dt.date.values
                else None
            )
            sentiment_list.append(
                {
                    "date": date_str,
                    "adj_close": adj_close,
                    "sentiment": {
                        "classification": row["classification"],
                        "positive": row["positive"],
                        "neutral": row["neutral"],
                        "negative": row["negative"],
                    },
                }
            )

        result = {"price_data": price_list, "sentiment_data": sentiment_list}

        return jsonify(result)
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error fetching company chart: {error}")
        return jsonify({})
