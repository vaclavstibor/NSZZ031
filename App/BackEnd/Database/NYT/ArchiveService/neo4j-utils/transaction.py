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
    def add_node(driver: Driver, symbol: str, name: str):
        with driver.session() as session:
            tx = session.begin_transaction()

            try:
                result = tx.run(
                    """
                    MERGE (c:Company {symbol: $symbol, name: $name})
                    RETURN c.symbol AS symbol
                    """,
                    symbol=symbol,
                    name=name,
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
