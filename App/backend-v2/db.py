from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB_USERNAME = getenv('DB_USERNAME')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_URI = getenv('DB_URI')

class Driver:
    _session = None

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()

    def session(self):
        if self._session is None:
            self._session = self.driver.session()
        return self._session
    
driver = Driver(DB_URI, DB_USERNAME, DB_PASSWORD)

"""
class Neo4jDriver:
    _instance = None

    @staticmethod
    def get_instance():
        if Neo4jDriver._instance is None:
            Neo4jDriver._instance = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        return Neo4jDriver._instance
"""
        