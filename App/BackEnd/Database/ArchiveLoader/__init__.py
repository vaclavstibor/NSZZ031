#!/usr/bin/env python3

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

    def load_file(driver: Driver, file_name: str):
        with driver.session() as session:
            tx = session.begin_transaction()
            
            try:
                result = tx.run("""
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
                    """, file_name=file_name
                )

                for record in result:
                    print(record)

                tx.commit()
            except:
                tx.rollback()
                raise
            finally:
                tx.close()

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
    Transaction.load_file(archive_loader, "2022-1.json")
