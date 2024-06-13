"""
The en_core_web_trf model in SpaCy is a transformer-based model, while en_core_web_md is a statistical model. Transformer models, such as the ones based on the BERT architecture, are generally more accurate but also more computationally intensive, which can make them slower than statistical models.

Here are a few reasons why en_core_web_trf might be slower:

Model complexity: Transformer models are larger and more complex than statistical models. They have more parameters, which means they require more computation to make predictions.

Sequence length: Transformer models process text in sequences, and the time it takes to process a sequence increases quadratically with the length of the sequence. If you're processing long texts, this could significantly slow down your model.

Hardware: Transformer models are designed to be run on GPUs. If you're running en_core_web_trf on a CPU, it will be significantly slower than if you were running it on a GPU.

Batch size: Transformer models can process multiple texts at once (in a batch). If you're processing texts one at a time, you're not taking full advantage of the model's capabilities, which could slow down your application.
"""

import os
import sys
import pywikibot
from pywikibot.exceptions import IsRedirectPageError
import logging
import spacy
from spacy.tokens import Span
from SPARQLWrapper import SPARQLWrapper, JSON

from typing import Dict, List, Set, Any

from src.utils.helpers import setup_logger
from dotenv import load_dotenv

setup_logger()
load_dotenv()


STOCK_EXCHANGES = os.getenv("WIKIDATA_STOCK_EXCHANGE_IDS").split(",")
logging.info(f"Stock Exchanges: {STOCK_EXCHANGES}") 

class Model:
    def __init__(self, model_name: str = "en_core_web_md"):
        self.nlp = spacy.load(model_name)
        self.nlp.add_pipe("entityLinker", last=True)
    
class SPARQLWikidataConnector:
    def __init__(self):
        self.endpoint_url = "https://query.wikidata.org/sparql"
        self.user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])

    def run_query(self, query):
        sparql = SPARQLWrapper(self.endpoint_url, agent=self.user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    def retrieve_entities_info(self, entities_identifiers: Set[str]) -> Dict[str, Any]:
        stock_exchanges = " ".join(f"wd:{exchange}" for exchange in STOCK_EXCHANGES)
        entities_id = " ".join(f"wd:{entity_id}" for entity_id in entities_identifiers)

        logging.info(f"Entities IDs: {entities_identifiers}")

        # First query
        query1 = f"""
        SELECT DISTINCT ?id ?idLabel ?exchangesLabel ?ticker WHERE {{
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
            VALUES ?id {{ {entities_id} }}
            VALUES ?exchanges {{ {stock_exchanges} }}
            ?id p:P414 ?exchange.
            ?exchange ps:P414 ?exchanges;
                      pq:P249 ?ticker.
            FILTER NOT EXISTS {{ 
                ?exchange pq:P582 ?endTime .
            }}
        }}
        """
        results1 = self.run_query(query1)
        matched_ids = {result['id']['value'].split('/')[-1] for result in results1['results']['bindings']}

        logging.info(f"Matched IDs: {matched_ids}")

        # Find the QIDs that did not match in the first query
        unmatched_ids = entities_identifiers - matched_ids
        if not unmatched_ids:
            return results1
        
        logging.info(f"Unmatched IDs: {unmatched_ids}")

        # Second query
        unmatched_entities_id = " ".join(f"wd:{entity_id}" for entity_id in unmatched_ids)
        query2 = f"""
        SELECT DISTINCT ?id ?idLabel ?exchangesLabel ?ticker WHERE {{
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
            VALUES ?id {{ {unmatched_entities_id} }}
            VALUES ?exchanges {{ {stock_exchanges} }}
            ?id wdt:P127 ?owner.
            ?owner p:P414 ?exchange.
            ?exchange ps:P414 ?exchanges;
                      pq:P249 ?ticker.
            FILTER NOT EXISTS {{ 
                ?exchange pq:P582 ?endTime .
            }}
        }}
        """
        results2 = self.run_query(query2)

        # Combine the results
        results1['results']['bindings'].extend(results2['results']['bindings'])

        # Map for QID to entity info dict
        entities_identifiers_info = {
            result['id']['value'].split('/')[-1]: {
                "idLabel": result['idLabel']['value'],
                "exchangesLabel": result['exchangesLabel']['value'],
                "ticker": result['ticker']['value'],
            }
            for result in results1['results']['bindings']
        }

        logging.info(f"Entities IDs info: {entities_identifiers_info}")

        return entities_identifiers_info


# Define the additional attributes for the Entity class
Span.set_extension("ticker", default=None)
Span.set_extension("exchange", default=None)

model = Model("en_core_web_md")
connector = SPARQLWikidataConnector()

def extract_entities(content: str) -> List[Dict[str, str]]:

    doc = model.nlp(content)

    # Get collection of entities
    _entities = doc.ents

    # Filter entities to only include ORG entities
    org_entities = [entity for entity in _entities if entity.label_ == "ORG"]

    # Get collection of linked entities
    linked_entities = doc._.linkedEntities

    # Map linked entities to original named recognition entities
    org_entity_mapping = {}

    # Set of unique wikidata identifiers for each entity
    entities_identifiers = set()
     
    for linked_entity in linked_entities:
        for org_entity in org_entities:
            if (
                linked_entity.span.start_char <= org_entity.end_char
                and linked_entity.span.end_char >= org_entity.start_char
            ):
                wikidata_id = "Q" + str(linked_entity.identifier)
                org_entity_mapping[org_entity] = wikidata_id
                entities_identifiers.add(wikidata_id)


    # Myslenka dostat pro kazdy QID ticker symbol a exchange a nazev
    entities_identifiers_info = connector.retrieve_entities_info(entities_identifiers)

    # Add to org_entities the additional attributes
    for org_entity in org_entities:
        wikidata_id = org_entity_mapping.get(org_entity, "")
        entity_info = entities_identifiers_info.get(wikidata_id, {})
        org_entity._.ticker = entity_info.get("ticker", "")
        org_entity._.exchange = entity_info.get("exchangesLabel", "")

    logging.info(org_entity_mapping)

    entities = [
        {
            "ticker": entity._.ticker,
            "exchange": entity._.exchange,
            "text": entity.text,
            "label": entity.label_,
            "start_idx": entity.start_char,
            "end_idx": entity.end_char,
        }
        for entity in org_entities
    ]

    return entities

"""
SELECT ?id ?idLabel ?exchangesLabel ?ticker WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  
  VALUES ?id { wd:Q355 wd:Q312 wd:Q12345 }
  VALUES ?exchanges { wd:Q13677 wd:Q82059 } # NYSE, NASDAQ
  
  {
    # Retrieve entities with direct stock exchange statements
    ?id p:P414 ?exchange.
    ?exchange ps:P414 ?exchanges;
              pq:P249 ?ticker. # Get the ticker symbol              
    FILTER NOT EXISTS { 
      ?exchange pq:P582 ?endTime . # Ensure that the ticker symbol does not have an "end time" specified
    }
  }
  
  UNION
  
  {
    # Retrieve entities where the owner is listed on the specified exchanges, and the entity itself is not listed on any other exchanges
    ?id wdt:P127 ?owner. # Get the owner of the entity
    ?owner p:P414 ?exchange. # Get the "stock exchange" statement from the owner
    ?exchange ps:P414 ?exchanges;
              pq:P249 ?ticker. # Get the ticker symbol
    FILTER NOT EXISTS { 
      ?exchange pq:P582 ?endTime . # Ensure that the ticker symbol does not have an "end time" specified
    }
     # Retrieve the label of the owner
    ?owner rdfs:label ?ownerLabel.
    FILTER(LANG(?ownerLabel) = "en") # Filter to get the English label
  }
}
"""