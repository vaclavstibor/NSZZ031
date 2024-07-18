import concurrent.futures
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List
import torch
import os

from collections import defaultdict
from typing import List

import nltk
import torch.nn.functional as F
from nltk.tokenize import sent_tokenize

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from src.models.entity import Entity
from src.models.sentiment import Sentiment
from src.models.entity_with_sentiment import EntityWithSentiment
from src.models.ticker_with_sentiment import TickerWithSentiment

from src.utils.helpers import setup_logger

setup_logger()


class Model:
    """
    Model class for sentiment analysis.

    Attributes:
        ckpt_path (str): The path to the checkpoint.
        max_length (int): The maximum length of the input.
        device (torch.device): The device used for inference.
        ABSA (AutoModelForSeq2SeqLM): The ABSA model.
        tokenizer (AutoTokenizer): The tokenizer.
        executor (ThreadPoolExecutor): The executor for running blocking functions.
    """
    
    def __init__(self, ckpt_path="amphora/FinABSA-Longer", max_length=512):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logging.info(f"Using device: {self.device}")

        self.ABSA = AutoModelForSeq2SeqLM.from_pretrained(ckpt_path).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(ckpt_path)
        self.max_length = max_length
        self.executor = ThreadPoolExecutor()

    async def run_absa(self, input_str: str, input_entities: List[Entity]) -> List[EntityWithSentiment]:
        """
        Run sentiment analysis on the input string. The input string is split into chunks
        and sentiment analysis is run on each chunk. The sentiment scores are then averaged
        to get the final sentiment scores for each entity.

        Args:
            input_str (str): The input string.
            input_entities (List[Entity]): The list of entities.

        Returns:
            List[EntityWithSentiment]: The list of entities with sentiment scores.
        """
        
        chunks = self.split_into_chunks(input_str)
        entity_text_scores_dict = {
            entity.text: {
                "positive": 0.0,
                "negative": 0.0,
                "neutral": 0.0,
                "count": 0,
                "classification": "NEUTRAL",
            }
            for entity in input_entities
        }

        futures = []
        for chunk in chunks:
            tgt_entities = self.retrieve_target(chunk, input_entities)
            for e in tgt_entities:
                futures.append(asyncio.create_task(self.run_single_absa(chunk, e.text)))

        # Run sentiment analysis on each chunk
        results = await asyncio.gather(*futures)
        for chunk_result in results:
            e_text = chunk_result["entity"]
            scores = entity_text_scores_dict[e_text]
            scores["positive"] += chunk_result["logits"]["positive"]
            scores["negative"] += chunk_result["logits"]["negative"]
            scores["neutral"] += chunk_result["logits"]["neutral"]
            scores["count"] += 1

        entities_with_sentiment = []
        for entity_text, scores in entity_text_scores_dict.items():
            if scores["count"] > 0:
                scores["positive"] /= scores["count"]
                scores["negative"] /= scores["count"]
                scores["neutral"] /= scores["count"]
                max_score = max(scores["positive"], scores["negative"], scores["neutral"])
                if max_score == scores["positive"]:
                    scores["classification"] = "POSITIVE"
                elif max_score == scores["negative"]:
                    scores["classification"] = "NEGATIVE"
                else:
                    scores["classification"] = "NEUTRAL"

                sentiment = Sentiment(
                    classification=scores["classification"],
                    positive=scores["positive"],
                    negative=scores["negative"],
                    neutral=scores["neutral"],
                )

                entities_with_sentiment.append(
                    EntityWithSentiment(
                        text=entity_text,
                        ticker=[entity.ticker for entity in input_entities if entity.text == entity_text][0],
                        sentiment=sentiment,
                    )
                )

        logging.log(logging.INFO, f"entities_with_sentiment: {entities_with_sentiment}")
        return entities_with_sentiment
    
    async def run_single_absa(self, chunk: str, tgt: str) -> Dict[str, Any]:
        """
        Run sentiment analysis on a single chunk.

        Args:
            chunk (str): The input chunk.
            tgt (str): The target entity.

        Returns:
            Dict[str, Any]: The sentiment scores for the target entity.
        """
        
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self._blocking_single_absa, chunk, tgt)

    def _blocking_single_absa(self, chunk: str, tgt: str) -> Dict[str, Any]:
        """
        Blocking function to run sentiment analysis on a single chunk. 
        
        Args:
            chunk (str): The input chunk.
            tgt (str): The target entity.

        Returns:
            Dict[str, Any]: The sentiment scores for the target entity.
        """
        
        chunk = chunk.replace(tgt, "[TGT]")
        input = self.tokenizer(chunk, return_tensors="pt").to(self.device)
        output = self.ABSA.generate(
            **input, max_length=20, output_scores=True, return_dict_in_generate=True
        )
        logits = F.softmax(output["scores"][-4][:, -3:], dim=1)[0]
        return {
            "entity": tgt,
            "logits": {
                "positive": float(logits[0]),
                "negative": float(logits[1]),
                "neutral": float(logits[2]),
            },
        }

    def retrieve_target(self, input_str, input_entities: List[Entity]) -> List[Entity]:
        """
        Retrieve the target entities from the input string. 

        Args:
            input_str (str): The input string.
            input_entities (List[Entity]): The list of entities.
        
        Returns:
            List[Entity]: The target entities.
        """
        
        entities = [entity for entity in input_entities if entity.text in input_str]
        logging.info("(retrieve_target) ENTITIES: %s %s", len(entities), entities)
        return entities

    def split_into_chunks(self, input_str: str) -> List[str]:
        """
        Split the input string into chunks. 

        Args:
            input_str (str): The input string.

        Returens:
            List[str]: The list of chunks.
        """
        
        sentences = sent_tokenize(input_str)
        chunks = []
        current_chunk = ""
        current_tokens_count = 0
        for sentence in sentences:
            sentence_tokens = self.tokenizer(sentence).word_ids()
            sentence_tokens_count = len(sentence_tokens)
            if current_tokens_count + sentence_tokens_count <= self.max_length:
                current_chunk += sentence
                current_tokens_count += sentence_tokens_count
            else:
                chunks.append(current_chunk)
                current_chunk = sentence
                current_tokens_count = sentence_tokens_count
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

def convert_to_tickers_with_sentiment(entities_with_sentiment: List[EntityWithSentiment]) -> List[TickerWithSentiment]:
    """
    Convert a list of entities with sentiment scores to a list of tickers with sentiment scores.

    Args:
        entities_with_sentiment (List[EntityWithSentiment]): The list of entities with sentiment scores.
    
    Returns:
        List[TickerWithSentiment]: The list of tickers with sentiment scores.
    """
    
    ticker_sentiment_dict = defaultdict(lambda: {"positive": 0.0, "negative": 0.0, "neutral": 0.0, "count": 0.0})
    for entity in entities_with_sentiment:
        ticker = entity.ticker
        sentiment = entity.sentiment
        ticker_sentiment_dict[ticker]["positive"] += sentiment.positive
        ticker_sentiment_dict[ticker]["negative"] += sentiment.negative
        ticker_sentiment_dict[ticker]["neutral"] += sentiment.neutral
        ticker_sentiment_dict[ticker]["count"] += 1

    tickers: List[TickerWithSentiment] = []
    for ticker, scores in ticker_sentiment_dict.items():
        count = scores["count"]
        avg_positive = scores["positive"] / count
        avg_negative = scores["negative"] / count
        avg_neutral = scores["neutral"] / count
        classification = "NEUTRAL"
        if max(avg_positive, avg_negative, avg_neutral) == avg_positive:
            classification = "POSITIVE"
        elif max(avg_positive, avg_negative, avg_neutral) == avg_negative:
            classification = "NEGATIVE"

        sentiment = Sentiment(
            classification=classification,
            positive=format(avg_positive, ".5f"),
            negative=format(avg_negative, ".5f"),
            neutral=format(avg_neutral, ".5f"),
        )
        tickers.append(TickerWithSentiment(ticker=ticker, sentiment=sentiment))
    return tickers

async def analyse_sentiment(model: Model, content: str, entities: List[Entity]) -> List[TickerWithSentiment]:
    """
    Asynchronously analyse the sentiment of the content. 

    Args:
        model (Model): The sentiment analysis model.
        content (str): The content to analyse.
        entities (List[Entity]): The entities to analyse.

    Returns:
        List[TickerWithSentiment]: The list of tickers with sentiment scores.
    """
    
    entities_with_sentiment = await model.run_absa(content, entities)
    return convert_to_tickers_with_sentiment(entities_with_sentiment)
