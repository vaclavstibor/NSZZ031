#!/usr/bin/env python3

from driver import Driver

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