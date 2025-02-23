from elasticsearch import Elasticsearch
from orpheus.config import get_config

config = get_config()

es_client = Elasticsearch(
    config.elastic_url, timeout=10,
    # retry_on_timeout=True, max_retries=10
)

