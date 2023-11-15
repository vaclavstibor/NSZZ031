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