import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection as psycopg2_connection
import logging
from flask import jsonify
from datetime import datetime, timedelta

def get_company_article_list(connection: psycopg2_connection, ticker: str, table_prefix: str) -> dict:
    """
    """

    # Safely construct the SQL query with table prefix using psycopg2.sql
    query = sql.SQL("""
    SELECT 
        a.id, a.title, a.published_date, a.url, a.author, a.type,
        s.classification, s.positive, s.neutral, s.negative, sec.name as section_name
    FROM 
        {articles} a
        JOIN {article_companies} at ON a.id = at.article_id
        JOIN {companies} c ON at.company_id = c.id
        LEFT JOIN {sentiments} s ON a.id = s.article_id AND at.company_id = s.company_id
        LEFT JOIN {article_sections} asx ON a.id = asx.article_id
        LEFT JOIN {sections} sec ON asx.section_id = sec.id
    WHERE 
        c.ticker = %s
    ORDER BY 
        a.published_date DESC;
    """).format(
        articles=sql.Identifier(table_prefix + 'articles'),
        article_companies=sql.Identifier(table_prefix + 'article_companies'),
        companies=sql.Identifier(table_prefix + 'companies'),
        sentiments=sql.Identifier(table_prefix + 'sentiments'),
        article_sections=sql.Identifier(table_prefix + 'article_sections'),
        sections=sql.Identifier(table_prefix + 'sections')
    )
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (ticker,))
            records = cursor.fetchall()
        
        articles = []
        for record in records:
            article_id, title, published_date, url, author, article_type, classification, positive, neutral, negative, section_name = record
            articles.append({
                "id": str(article_id),
                "title": title,
                "type": article_type.title(),
                "section": section_name.title() if section_name else None,
                "published_date": published_date.isoformat(),
                "url": url,
                "author": author,
                "sentiment": {
                    "classification": classification,
                    "positive": float(positive) if positive is not None else None,
                    "neutral": float(neutral) if neutral is not None else None,
                    "negative": float(negative) if negative is not None else None,
                }
            })
        
        return jsonify(articles)
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({})