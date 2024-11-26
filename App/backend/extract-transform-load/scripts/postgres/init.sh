#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Create airflow user and database for Apache Airflow framework
psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" <<-EOSQL
    CREATE USER ${AIRFLOW_USER} WITH LOGIN PASSWORD '${AIRFLOW_PASSWORD}';
    CREATE DATABASE ${AIRFLOW_DB};
    ALTER DATABASE ${AIRFLOW_DB} OWNER TO ${AIRFLOW_USER};
    GRANT ALL PRIVILEGES ON DATABASE ${AIRFLOW_DB} TO ${AIRFLOW_USER};
EOSQL

# Create main database to store after transformation articles
psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" <<-EOSQL
    CREATE DATABASE ${ARTICLES_DB};
EOSQL

# Connect to the 'aritcles_db' database and create the table
psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" --dbname="${ARTICLES_DB}" <<-EOSQL
    BEGIN;

    CREATE TABLE articles (
        id UUID PRIMARY KEY,
        type VARCHAR(50) NOT NULL,
        url TEXT NOT NULL,
        title TEXT NOT NULL,
        author VARCHAR(255),
        published_date TIMESTAMP WITH TIME ZONE NOT NULL
    );

    CREATE TABLE companies (
        id SERIAL PRIMARY KEY,
        shortName VARCHAR(100),
        ticker VARCHAR(10) NOT NULL UNIQUE,
        industry VARCHAR(100),
        website VARCHAR(255)
    );

    CREATE TABLE article_companies (
        article_id UUID NOT NULL,
        company_id INT NOT NULL,
        PRIMARY KEY (article_id, company_id),
        FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
        FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
    );

    CREATE TABLE sentiments (
        id SERIAL PRIMARY KEY,
        article_id UUID NOT NULL,
        company_id INT NOT NULL,
        classification VARCHAR(50),
        positive NUMERIC(5,5),
        negative NUMERIC(5,5),
        neutral NUMERIC(5,5),
        FOREIGN KEY (article_id, company_id) REFERENCES article_companies(article_id, company_id) ON DELETE CASCADE,
        UNIQUE (article_id, company_id)
    );

    CREATE TABLE sections (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE
    );

    CREATE TABLE article_sections (
        article_id UUID NOT NULL,
        section_id INT NOT NULL,
        PRIMARY KEY (article_id, section_id),
        FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
        FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE
    );

    CREATE UNIQUE INDEX idx_article_companies_article_id_company_id ON article_companies(article_id, company_id);
    CREATE UNIQUE INDEX idx_sentiments_article_id_company_id ON sentiments(article_id, company_id);
    CREATE UNIQUE INDEX idx_article_sections_article_id_section_id ON article_sections(article_id, section_id);

    COMMIT;
EOSQL

# Don't forget chmod +x init.sh