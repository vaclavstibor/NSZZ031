# TODO neo4j-admin database import to get str ids "AAPL" for "Apple Inc." https://neo4j.com/docs/operations-manual/current/tools/neo4j-admin/neo4j-admin-import/

from neo4j import GraphDatabase

class Driver:

    # Initiate the Neo4j Driver
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.driver.verify_connectivity()

    # Close the Neo4j Driver
    def close(self):
        self.driver.close()

    def session(self):
        return self.driver.session()

class Transaction:

    def add_node(driver: Driver, symbol: str, name: str):
        with driver.session() as session:
            tx = session.begin_transaction()
            
            try:
                result = tx.run("""
                    MERGE (c:Company {symbol: $symbol, name: $name})
                    RETURN c.symbol AS symbol
                    """, symbol=symbol, name=name
                )
                print(result.single()[0])
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

    driver = Driver(URI, AUTH[0], AUTH[1])
    Transaction.add_node(driver, "AAPL", "Apple Inc.")
    #Transaction.delete_all(driver)