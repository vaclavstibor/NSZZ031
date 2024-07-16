import psycopg2
from psycopg2.extensions import connection as psycopg2_connection
from psycopg2 import sql
import logging
from flask import jsonify
from datetime import datetime, timezone

from src.database.queries.get_company_info import compute_daily_sentiment


def get_company_graph(connection: psycopg2_connection, ticker: str, table_prefix: str) -> dict:
    """
    TODO
    """
    
    query = sql.SQL(
        """
    SELECT 
        c.id AS company_id, c.shortName, c.ticker,
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

            if not records:
                return jsonify({})

            nodes = []
            links = []

            avg_daily_sentiment = compute_daily_sentiment(
                records=records, 
                article_id_index=3, 
                published_date_index=5,
                positive_index=10,
                negative_index=11,
                neutral_index=12,
            )

            company_id = records[0][0] if records else None
            if not company_id:
                logging.error("No company ID found for the given ticker.")
                return jsonify({})

            company_node = {
                "id": company_id,
                "node_type": "company",
                "short_name": records[0][1],
                "ticker": records[0][2],
                "sentiment": {
                    "classification": avg_daily_sentiment[0],
                    "positive": avg_daily_sentiment[1],
                    "negative": avg_daily_sentiment[2],
                    "neutral": avg_daily_sentiment[3],
                },
            }

            nodes.append(company_node)

            for record in records:
                if record[3]:  # If there's an article_id
                    article_node = {
                        "id": record[3],
                        "node_type": "article",
                        "title": record[4],
                        "published_date": record[5],
                        "type": record[6],
                        "url": record[7],
                        "author": record[8],
                        "sentiment": {
                            "classification": record[9],
                            "positive": record[10] if record[10] else 0,
                            "negative": record[11] if record[11] else 0,
                            "neutral": record[12] if record[12] else 0,
                        },
                    }
                    nodes.append(article_node)

                    link = {
                        "source": record[3],
                        "target": company_id,
                        "sentiment": article_node["sentiment"],
                    }
                    links.append(link)

            graph_info = {"nodes": nodes, "links": links}

            return jsonify(graph_info)
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error fetching ticker graph by ticker: {error}")
        return jsonify({})
