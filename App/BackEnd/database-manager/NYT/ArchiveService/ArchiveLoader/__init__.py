#!/usr/bin/env python3

# useful links: https://neo4j.com/developer/python/
#               https://graphacademy.neo4j.com/courses/app-python/2-interacting/1-transactions/
#               https://github.com/neo4j-graphacademy/app-python/blob/main/api/neo4j.py
#               webapp: https://taiwo-adetiloye.medium.com/implementing-flask-login-with-neo4j-database-54a3ac0d4cdf
#               examples of cypher: https://neo4j.com/developer-blog/discover-neo4j-auradb-free-week-24-nytimes-article-knowledge-graph/

from neo4j import GraphDatabase

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
        with driver.session() as session:
            tx = session.begin_transaction()

            try:
                result = tx.run(
                    """
                    CALL apoc.load.jsonArray($file_name) 
                    YIELD value
                    MERGE (a:Article {_id: value._id, abstract: value.abstract, web_url: value.web_url, pub_date: value.pub_date})
                    WITH a, value.keywords AS keywords
                    UNWIND keywords AS keyword
                    WITH a, keyword
                    WHERE keyword.name = "organizations"
                    MERGE (k:Keyword {value: keyword.value})
                    CREATE (a)-[:HAS_KEYWORD]->(k)
                    CREATE (a)<-[:IS_MENTIONED_IN]-(k)
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

    archive_loader = Driver(URI, AUTH[0], AUTH[1])
    Transaction.delete_all(archive_loader)

    for i in range(1, 13):
        Transaction.load_file(archive_loader, f"/business/filtered/2022-{i}.json")
        print(f"Archive business 2022-{i}.json has been loaded.")


"""
MATCH (k:Keyword)-[:IS_MENTIONED_IN]-(a:Article)
RETURN k, a
"""