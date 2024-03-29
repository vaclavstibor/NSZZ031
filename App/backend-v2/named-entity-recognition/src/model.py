"""
The en_core_web_trf model in SpaCy is a transformer-based model, while en_core_web_md is a statistical model. Transformer models, such as the ones based on the BERT architecture, are generally more accurate but also more computationally intensive, which can make them slower than statistical models.

Here are a few reasons why en_core_web_trf might be slower:

Model complexity: Transformer models are larger and more complex than statistical models. They have more parameters, which means they require more computation to make predictions.

Sequence length: Transformer models process text in sequences, and the time it takes to process a sequence increases quadratically with the length of the sequence. If you're processing long texts, this could significantly slow down your model.

Hardware: Transformer models are designed to be run on GPUs. If you're running en_core_web_trf on a CPU, it will be significantly slower than if you were running it on a GPU.

Batch size: Transformer models can process multiple texts at once (in a batch). If you're processing texts one at a time, you're not taking full advantage of the model's capabilities, which could slow down your application.
"""

import pywikibot
from pywikibot.exceptions import IsRedirectPageError
import logging
import spacy
from spacy.tokens import Span

from typing import Dict, List, Set

from src.utils.helpers import setup_logger

setup_logger()


class Model:
    def __init__(self, model_name: str = "en_core_web_md"):
        self.nlp = spacy.load(model_name)
        self.nlp.add_pipe("entityLinker", last=True)


class WikiBot:
    def __init__(self, site_name: str = "wikidata"):
        self.site = pywikibot.Site(site_name, site_name)
        self.repo = self.site.data_repository()
        self.stock_exchanges = ["Q82059", "Q1019992", "Q13677"]  # TODO: load via .env
        self.stock_exchange_property = "P414"  # TODO: load via .env
        self.owned_by_property = "P127"  # TODO: load via .env
        self.end_time_property = "P582"  # TODO: load via .env
        self.ticker_property = "P249"  # TODO: load via .env

    def get_item_page(self, item_id: str):
        return pywikibot.ItemPage(self.repo, item_id)


# Define the additional attributes for the Entity class
Span.set_extension("ticker", default=None)
Span.set_extension("exchange", default=None)

model = Model("en_core_web_md")
wiki_bot = WikiBot("wikidata")


def predict_entities(text):

    doc = model.nlp(text)

    # Get collection of entities
    _entities = doc.ents

    # Filter entities to only include ORG entities
    org_entities = [entity for entity in _entities if entity.label_ == "ORG"]

    # Get collection of linked entities
    linked_entities = doc._.linkedEntities

    # Map linked entities to original entities
    org_entity_mapping = {}
    for linked_entity in linked_entities:
        for org_entity in org_entities:
            if (
                linked_entity.span.start_char <= org_entity.end_char
                and linked_entity.span.end_char >= org_entity.start_char
            ):
                org_entity_mapping[org_entity] = "Q" + str(linked_entity.identifier)

    entities = add_ticker_to_entities(org_entity_mapping)

    logging.info(entities)

    entities = [
        {
            "ticker": entity._.ticker,
            "exchange": entity._.exchange,
            "text": entity.text,
            "label": entity.label_,
            "start_idx": entity.start_char,
            "end_idx": entity.end_char,
        }
        for entity in entities
    ]

    return entities


def add_ticker_to_entities(org_entity_mapping: Dict[Span, str]) -> Set[Span]:
    entities = set()  # Use a set instead of a list

    logging.info(org_entity_mapping)

    for entity, wiki_id in org_entity_mapping.items():
        try:
            # Create an ItemPage object for the entity with the Wikidata ID
            page = wiki_bot.get_item_page(wiki_id)

            # Retrieve the data of the entity
            try:
                item_dict = page.get()
            except IsRedirectPageError:
                redirect_page = page.getRedirectTarget()
                item_dict = redirect_page.get()

            # Retrieve the claims of the entity
            claims = item_dict["claims"]

            # Check if the entity has a stock exchange property
            if wiki_bot.stock_exchange_property in claims:
                for claim in claims[wiki_bot.stock_exchange_property]:
                    # Check if the stock exchange is NASDAQ or NYSE
                    stock_exchange = claim.getTarget()
                    if stock_exchange.id in wiki_bot.stock_exchanges:
                        qualifiers = claim.qualifiers
                        # Retrieve the ticker symbol
                        if wiki_bot.ticker_property in qualifiers:
                            for qualifier in qualifiers[wiki_bot.ticker_property]:
                                # Check if the ticker has not end time in exchange (LIKE TWTR Twitter)
                                if wiki_bot.end_time_property not in qualifiers:
                                    ticker_symbol = qualifier.getTarget()
                                    entity._.ticker = (
                                        ticker_symbol  # Set the 'ticker' attribute
                                    )
                                    entity._.exchange = stock_exchange.id
                                    logging.info(
                                        f"Entity: {entity}, Ticker: {ticker_symbol}"
                                    )
                                    entities.add(entity)  # Add the entity to the set
                                    break
                            break
            # Else if the entity is owned by a organization, check if the organization has a stock exchange property
            # e.g. Facebook and Instagram is owned by Meta Platforms, Inc. which is listed on NASDAQ
            elif wiki_bot.owned_by_property in claims:
                for claim in claims[wiki_bot.owned_by_property]:
                    # logging.info(f"Claim: {claim}")
                    # Get the target of the claim
                    target = claim.getTarget().id
                    page = wiki_bot.get_item_page(target)
                    item_dict = page.get()  # Retrieve the data of the organization
                    org_claims = item_dict[
                        "claims"
                    ]  # Retrieve the claims of the organization

                    # logging.info(f"Target: {target}")
                    # Check if the organization has a stock exchange property
                    if wiki_bot.stock_exchange_property in org_claims:
                        for org_claim in org_claims[wiki_bot.stock_exchange_property]:
                            # logging.info(f"Org Claim: {org_claim}")
                            stock_exchange = org_claim.getTarget()
                            if stock_exchange.id in wiki_bot.stock_exchanges:
                                # Retrieve the ticker symbol
                                if wiki_bot.ticker_property in org_claim.qualifiers:
                                    for ticker_qualifier in org_claim.qualifiers[
                                        wiki_bot.ticker_property
                                    ]:
                                        # Check if the ticker has not end time in exchange (LIKE TWTR Twitter)
                                        if (
                                            wiki_bot.end_time_property
                                            not in org_claim.qualifiers
                                        ):
                                            ticker_symbol = ticker_qualifier.getTarget()
                                            entity._.ticker = ticker_symbol  # Set the 'ticker' attribute
                                            entity._.exchange = stock_exchange.id
                                            logging.info(
                                                f"Entity: {entity}, Ticker: {ticker_symbol}"
                                            )
                                            entities.add(
                                                entity
                                            )  # Add the entity to the set
                                            break
                                    break
        except Exception as e:
            logging.error(f"Error retrieving ticker symbol: {str(e)}")
            raise

    return entities
