from neo4j import GraphDatabase
import csv

class Driver:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()

    def session(self):
        return self.driver.session()
    
class Transaction:

    @staticmethod
    def load_file(driver: Driver, file_name: str):
        # Load json file into Neo4j database

        with driver.session() as session:
            tx = session.begin_transaction()

            try:
                result = tx.run(
                    """
                    CALL apoc.load.json($file_name) 
                    YIELD value
                    UNWIND value.feed AS article
                    MERGE (a:Article {title: article.title, abstract: article.summary, url: article.url, time_published: article.time_published, overall_sentiment_score: article.overall_sentiment_score, overall_sentiment_label: article.overall_sentiment_label})
                    WITH a, article.ticker_sentiment AS tickers
                    UNWIND tickers AS ticker
                    MERGE (t:Ticker {name: ticker.ticker})
                    MERGE (a)-[m:MENTIONS {ticker_sentiment_score: ticker.ticker_sentiment_score, ticker_sentiment_label: ticker.ticker_sentiment_label}]->(t)
                    MERGE (a)<-[:IS_MENTIONED_IN {ticker_sentiment_score: ticker.ticker_sentiment_score, ticker_sentiment_label: ticker.ticker_sentiment_label}]-(t)
                    """,
                    file_name=file_name,
                )

                for record in result:
                    print(record)

                tx.commit()
            except:
                tx.rollback()
                raise
            finally:
                tx.close()

    @staticmethod
    def delete_all(driver: Driver):
        with driver.session() as session:
            tx = session.begin_transaction()

            try:
                tx.run("MATCH (n) DETACH DELETE n")
                tx.commit()
                print("All nodes and relationships have been deleted.")
            except:
                tx.rollback()
                raise
            finally:
                tx.close()                

if __name__ == "__main__":

    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "StrongPassword!")

    serach_loader = Driver(URI, AUTH[0], AUTH[1])
    Transaction.delete_all(serach_loader)

    tickers = ['AAPL','AMZN','MSFT']

    for ticker in tickers:
        Transaction.load_file(serach_loader, f"/AV/search/{ticker}.json")
        print(f"{ticker}.json has been loaded.")
