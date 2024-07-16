import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection as psycopg2_connection
import logging
from flask import jsonify
from datetime import datetime, timezone


def get_companies_graphs(connection: psycopg2_connection, table_prefix: str) -> dict:
    """
    Fetches graph data for companies and their associated articles and sentiments.

    Args:
        connection (psycopg2_connection): A psycopg2 connection object to the database.
        table_prefix (str): The prefix used for table names in the database.

    Returns:
        dict: A dictionary containing nodes and links for the graph representation.
    """

    query = sql.SQL(
        """
    SELECT 
        c.id AS company_id, c.shortName, c.ticker,
        a.id AS article_id, a.title, a.published_date, a.type, a.url, a.author,
        s.classification, s.positive, s.negative, s.neutral
    FROM {companies} c
    LEFT JOIN {article_companies} at ON c.id = at.company_id
    LEFT JOIN {articles} a ON at.article_id = a.id
    LEFT JOIN {sentiments} s ON a.id = s.article_id AND c.id = s.company_id;
    """
    ).format(
        companies=sql.Identifier(table_prefix + "companies"),
        article_companies=sql.Identifier(table_prefix + "article_companies"),
        articles=sql.Identifier(table_prefix + "articles"),
        sentiments=sql.Identifier(table_prefix + "sentiments"),
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()

            if not records:
                return jsonify({})

            nodes = []
            links = []
            company_nodes = {}
            article_nodes = {}
            article_avg_sentiments = compute_average_article_sentiment(records)

            for record in records:
                company_id, short_name, ticker, article_id, title, published_date, article_type, url, author, classification, positive, negative, neutral = record

                if company_id not in company_nodes:
                    company_node = {
                        "id": company_id,
                        "node_type": "company",
                        "short_name": short_name,
                        "ticker": ticker,
                        "sentiment": {
                            "classification": classification,
                            "positive": positive,
                            "negative": negative,
                            "neutral": neutral,
                        },
                        "articles": [],
                    }
                    company_nodes[company_id] = company_node
                    nodes.append(company_node)

                if article_id and article_id not in article_nodes:
                    article_node = {
                        "id": article_id,
                        "node_type": "article",
                        "title": title,
                        "published_date": published_date,
                        "type": article_type,
                        "url": url,
                        "author": author,
                        "sentiment": article_avg_sentiments.get(article_id, {
                            "classification": "NEUTRAL",
                            "positive": 0,
                            "negative": 0,
                            "neutral": 0,
                        }),
                        "companies": [],
                    }
                    article_nodes[article_id] = article_node
                    nodes.append(article_node)

                if article_id:
                    company_nodes[company_id]["articles"].append(article_id)
                    article_nodes[article_id]["companies"].append(company_id)

                    link = {
                        "source": article_id,
                        "target": company_id,
                        "sentiment": {
                            "classification": classification,
                            "positive": positive,
                            "negative": negative,
                            "neutral": neutral,
                        },
                    }
                    links.append(link)

            graph_info = {"nodes": nodes, "links": links}
            return jsonify(graph_info)
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error fetching companies graph: {error}")
        return jsonify({})


def compute_average_article_sentiment(records: list) -> dict:
    """
    Computes the average sentiment for each article based on associated company sentiments.

    Args:
        records (list): A list of records from the database query.

    Returns:
        dict: A dictionary containing the average sentiment scores and classification for each article.
    """
    article_to_sentiments = {}

    for record in records:
        article_id = record[3]
        if article_id:
            if article_id not in article_to_sentiments:
                article_to_sentiments[article_id] = []
            article_to_sentiments[article_id].append((record[10], record[11], record[12]))

    article_avg_sentiments = {}
    for article_id, sentiments in article_to_sentiments.items():
        avg_positive = round(sum(s[0] for s in sentiments) / len(sentiments), 5)
        avg_negative = round(sum(s[1] for s in sentiments) / len(sentiments), 5)
        avg_neutral = round(sum(s[2] for s in sentiments) / len(sentiments), 5)

        if avg_positive > avg_negative and avg_positive > avg_neutral:
            classification = "POSITIVE"
        elif avg_negative > avg_positive and avg_negative > avg_neutral:
            classification = "NEGATIVE"
        else:
            classification = "NEUTRAL"

        article_avg_sentiments[article_id] = {
            "classification": classification,
            "positive": avg_positive,
            "negative": avg_negative,
            "neutral": avg_neutral,
        }

    return article_avg_sentiments
