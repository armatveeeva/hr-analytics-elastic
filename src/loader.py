import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Union
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from dotenv import load_dotenv


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def read_json(path: Union[str, Path]) -> Union[Dict, List[Dict]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error in file {path}: {e}")
        raise


def create_index(es_client: Elasticsearch, index_name: str, mapping: Dict) -> None:
    if not es_client.indices.exists(index=index_name):
        es_client.indices.create(index=index_name, body=mapping)
        logger.info(f"Index '{index_name}' created")
    else:
        logger.info(f"Index '{index_name}' already exists")


def filter_hr_data(data: List[Dict]) -> List[Dict]:
    filtered = [
        item for item in data
        if 50_000 <= item.get("Зарплата", 0) <= 200_000
        and item.get("Рост", 0) > 160
    ]
    logger.info(f"Filtered {len(filtered)} records from {len(data)}")
    return filtered


def generate_actions(index_name: str, data: List[Dict]):
    for i, item in enumerate(data, 1):
        yield {
            "_index": index_name,
            "_source": item
        }
        if i % 100 == 0:
            logger.debug(f"Prepared {i} documents for bulk upload")


def main():
    load_dotenv()
    
    ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
    ES_USER = os.getenv("ES_USER", "elastic")
    ES_PASSWORD = os.getenv("ES_PASSWORD", "changeme")
    INDEX_NAME = os.getenv("ES_INDEX", "workers_matveeva")
    
    MAPPING_PATH = Path("config/index_mapping.json")
    DATA_PATH = Path("data/job.json")
    
    logger.info("Starting HR data loading pipeline to Elasticsearch")
    
    try:
        es = Elasticsearch(
            ES_HOST,
            basic_auth=(ES_USER, ES_PASSWORD),
            verify_certs=False,
            request_timeout=30
        )
        es.info()
        logger.info(f"Connected to Elasticsearch at {ES_HOST}")
    except Exception as e:
        logger.error(f"Elasticsearch connection error: {e}")
        return
    
    try:
        mapping = read_json(MAPPING_PATH)
        create_index(es, INDEX_NAME, mapping)
    except Exception as e:
        logger.error(f"Index mapping error: {e}")
        return
    
    try:
        raw_data = read_json(DATA_PATH)
        if not isinstance(raw_data, list):
            logger.error("Expected list of records in JSON source")
            return
        
        filtered_data = filter_hr_data(raw_data)
        
        if not filtered_data:
            logger.warning("No records remain after filtering")
            return
        
        success, _ = bulk(es, generate_actions(INDEX_NAME, filtered_data))
        logger.info(f"Successfully loaded {success} documents into index '{INDEX_NAME}'")
        
    except FileNotFoundError:
        logger.warning(
            "Source data file not found. To run pipeline, place data file at data/job.json "
            "or set DATA_PATH environment variable"
        )
        return
    except Exception as e:
        logger.error(f"Data loading error: {e}")
        return
    
    logger.info("Pipeline execution completed successfully")


if __name__ == "__main__":
    main()
