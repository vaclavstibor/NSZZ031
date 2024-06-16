import os
import sys
import logging
import spacy
from spacy.tokens import Span
from SPARQLWrapper import SPARQLWrapper, JSON

from typing import Dict, List, Set, Tuple, Any

from src.utils.helpers import setup_logger
from dotenv import load_dotenv

setup_logger()
load_dotenv()

STOCK_EXCHANGES = os.getenv("WIKIDATA_STOCK_EXCHANGE_IDS").split(",")

# Define the additional attributes for the Entity class
Span.set_extension("qid", default=None)


class Model:
    """
    A class used to represent the Model.

    Attributes:
        nlp (spacy.lang): The loaded Spacy language model.
    """

    def __init__(self, model_name: str):
        """
        Initializes the Model with the given Spacy model name.

        Args:
            model_name (str): The name of the Spacy model to load.
        """
        self.nlp = spacy.load(model_name)
        self.nlp.add_pipe("entityLinker", after="ner")


class SPARQLWikidataConnector:
    """
    A class used to represent the SPARQL Wikidata Connector.

    Attributes:
        endpoint_url (str): The endpoint URL for the SPARQL queries.
        user_agent (str): The user agent for the SPARQL queries.
    """

    def __init__(self):
        """
        Initializes the SPARQLWikidataConnector with the endpoint URL and user agent.
        """
        self.endpoint_url = "https://query.wikidata.org/sparql"
        self.user_agent = "WDQS-example Python/%s.%s" % (
            sys.version_info[0],
            sys.version_info[1],
        )

    def run_query(self, query: str) -> Dict[str, Any]:
        """
        Runs a SPARQL query and returns the result.

        Args:
            query (str): The SPARQL query to run.

        Returns:
            Dict[str, Any]: The result of the SPARQL query.
        """
        sparql = SPARQLWrapper(self.endpoint_url, agent=self.user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    QUERY_TEMPLATE = """
    SELECT DISTINCT ?id ?idLabel ?exchangesLabel ?ticker WHERE {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        VALUES ?id {{ {entities_ids_str} }}
        VALUES ?exchanges {{ {stock_exchanges_str} }}
        {additional_conditions_str}
        FILTER NOT EXISTS {{
            ?exchange pq:P582 ?endTime.
        }}                                      
    }}
    """
    ID_SPLIT_STR = "/"

    def retrieve_entities_info(self, init_entities_ids: Set[str]) -> Dict[str, Any]:
        """
        Retrieves information about entities from Wikidata.

        Args:
            init_entities_ids (Set[str]): A set of entity IDs to retrieve information for.

        Returns:
            Dict[str, Any]: A dictionary mapping entity IDs to their information.
        """
        stock_exchanges_str = " ".join(f"wd:{exchange}" for exchange in STOCK_EXCHANGES)

        logging.info(f"Entities IDs: {init_entities_ids}")

        # Query 1: Direct retrieval of entities with stock exchange statements
        additional_conditions_str = """
        ?id p:P414 ?exchange.
        ?exchange ps:P414 ?exchanges;
                  pq:P249 ?ticker.
        """
        results, unmatched_ids = self.run_query_and_get_unmatched_ids(
            init_entities_ids, stock_exchanges_str, additional_conditions_str
        )

        # Query 2: Retrieve entities where the owner is listed on the specified exchanges
        additional_conditions_str = """
        ?id wdt:P127 ?owner.
        ?owner p:P414 ?exchange.
        ?exchange ps:P414 ?exchanges;
                  pq:P249 ?ticker.
        """
        additional_results, unmatched_ids = self.run_query_and_get_unmatched_ids(
            unmatched_ids, stock_exchanges_str, additional_conditions_str
        )
        results["results"]["bindings"].extend(additional_results["results"]["bindings"])

        # Query 3: Differentiated ticker retrieval
        additional_conditions_str = """
        ?id wdt:P1889 ?differs.
        ?differs p:P414 ?exchange.
        ?exchange ps:P414 ?exchanges;
                pq:P249 ?ticker.
        """
        additional_results, unmatched_ids = self.run_query_and_get_unmatched_ids(
            unmatched_ids, stock_exchanges_str, additional_conditions_str
        )
        results["results"]["bindings"].extend(additional_results["results"]["bindings"])

        # Map for QID to entity info dict
        entities_identifiers_info = {
            result["id"]["value"].split(self.ID_SPLIT_STR)[-1]: {
                "idLabel": result["idLabel"]["value"],
                "ticker": result["ticker"]["value"],
            }
            for result in results["results"]["bindings"]
        }

        return entities_identifiers_info

    def run_query_and_get_unmatched_ids(
        self,
        entities_ids: Set[str],
        stock_exchanges_str: str,
        additional_conditions_str: str,
    ):
        """
        Runs a SPARQL query and returns the matched and unmatched entity IDs.

        Args:
            entities_ids (Set[str]): A set of entity IDs to run the query for.
            stock_exchanges_str (str): A string of stock exchange IDs.
            additional_conditions_str (str): Additional conditions for the SPARQL query.

        Returns:
            Tuple[Dict[str, Any], Set[str]]: A tuple containing the result of the SPARQL query and the unmatched entity IDs.
        """

        # Convert the entities IDs to a string
        entities_ids_str = " ".join(f"wd:{entity_id}" for entity_id in entities_ids)

        # Create the query
        query = self.QUERY_TEMPLATE.format(
            entities_ids_str=entities_ids_str,
            stock_exchanges_str=stock_exchanges_str,
            additional_conditions_str=additional_conditions_str,
        )

        # Run the query
        results = self.run_query(query)

        # Get the matched and unmatched IDs
        matched_ids = {
            result["id"]["value"].split(self.ID_SPLIT_STR)[-1]
            for result in results["results"]["bindings"]
        }
        logging.info(f"Matched IDs: {matched_ids}")
        unmatched_ids = entities_ids - matched_ids
        logging.info(f"Remaining unmatched IDs: {unmatched_ids}")

        return results, unmatched_ids


def unique_and_map_entities(
    doc: spacy.tokens.Doc, linked_entities: List[Span]
) -> Tuple[spacy.tokens.Doc, Dict[str, Set[str]]]:
    """
    Maps Wikidata identifiers to organization entities and removes duplicates.

    Args:
        doc (spacy.tokens.Doc): The document to process.
        linked_entities (List[Span]): A list of linked entities.

    Returns:
        Tuple[spacy.tokens.Doc, Dict[str, Set[str]]]: A tuple containing the processed document and a dictionary mapping Wikidata identifiers to organization entities.
    """

    # Dictionary to map the wikidata identifiers to the organisation entities
    qid_ent_dict = {}

    # Sort the entities by their start character
    linked_entities = sorted(linked_entities, key=lambda e: e.span.start_char)
    org_entities = sorted(list(doc.ents), key=lambda e: e.start_char)

    # Inizialize two pointers
    i, j = 0, 0

    # Loop while both pointers are within range
    while i < len(linked_entities) and j < len(org_entities):
        linked_entity = linked_entities[i]
        org_entity = org_entities[j]

        # If the entities overlap
        if (
            linked_entity.span.start_char <= org_entity.end_char
            and linked_entity.span.end_char >= org_entity.start_char
        ):
            # Get linked entity qid
            qid = "Q" + str(linked_entity.identifier)

            qid_ent_dict[qid] = {org_entity.text}
            org_entity._.qid = qid

            i += 1
            j += 1
        # If the linked entity starts later, move the pointer for org_entities
        elif linked_entity.span.start_char > org_entity.start_char:
            j += 1
        # If the org entity starts later, move the pointer for linked_entities
        else:
            i += 1

    return doc, qid_ent_dict


def extract_entities(
    model: Model, connector: SPARQLWikidataConnector, content: str
) -> List[Dict[str, str]]:
    """
    Extracts entities from the content using the given model and connector.

    Args:
        model (Model): The model to use for entity extraction.
        connector (SPARQLWikidataConnector): The connector to use for entity extraction.
        content (str): The content to extract entities from.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing the extracted entities.
    """

    # Process the content with the NLP model
    doc = model.nlp(content)

    # Keep only the entities with the label "ORG"
    doc.ents = [ent for ent in doc.ents if ent.label_ == "ORG"]

    # Dictionary to map the wikidata identifiers to the organisation entities
    doc, qid_ent_dict = unique_and_map_entities(doc, doc._.linkedEntities)

    # Retrieve the additional attributes (ticker) for the entities
    entities_identifiers_info = connector.retrieve_entities_info(
        set(qid_ent_dict.keys())
    )

    # Extract the entities with the additional attributes (ticker)
    entities = [
        {
            "text": ent.text,
            "ticker": entities_identifiers_info[ent._.qid]["ticker"],
        }
        for ent in doc.ents
        if ent._.qid in entities_identifiers_info
        and "ticker" in entities_identifiers_info[ent._.qid]
    ]

    logging.info(f"entities: {entities}")

    return entities
