import logging
from elasticsearch.exceptions import NotFoundError
from orpheus.services.db import es_client

log = logging.getLogger(__name__)
LOG_PREFIX = 'BL_INDEXER'


def create_index(index_name: str, index_mapping: dict):
    if not es_client.indices.exists(index=index_name):
        es_client.indices.create(
            index=index_name,
            body=index_mapping,
        )
        log.info(f"{LOG_PREFIX} index {index_name} created")
    else:
        log.info(f"{LOG_PREFIX} index {index_name} is already created")

    report = es_client.health_report()
    log.info(f'{LOG_PREFIX} health report {report} ')


def delete_index(index_name: str):
    if not es_client.indices.exists(index=index_name):
        log.info(f'{LOG_PREFIX} index {index_name} already delete')
    else:
        es_client.indices.delete(index=index_name)
        log.info(f'{LOG_PREFIX} Index {index_name} deleted')


def get_doc_id_by_file(file: str, index_name: str) -> str | None:
    query = {
        "query": {
            "match": {
                "file": file
            }
        }
    }

    result = es_client.search(index=index_name, body=query)
    hits = result.get("hits", {}).get("hits", [])
    if hits:
        doc_id = hits[0]["_id"]
        log.info(f'{LOG_PREFIX} document exist id {doc_id}')
        return doc_id


def index_file(repo_name, file_path, content, index_name: str):
    doc = {
        "repo": repo_name,
        "file": file_path,
        "content": content
    }
    if doc_id := get_doc_id_by_file(file_path, index_name):
        update_body = {
            "doc": {
                "content": content
            }
        }
        es_client.update(index=index_name, id=doc_id, body=update_body)
        log.info(f"{LOG_PREFIX} doc_id: {doc_id} updated")
    else:
        es_client.index(index=index_name, document=doc)
        log.info(f"File {file_path} indexed")


def search_by_id(document_id: str, index: str) -> list:
    try:
        result = es_client.search(
            index=index,
            body={
                "query": {
                    "terms": {
                        "_id": [document_id]
                    }
                }
            }
        )
    except NotFoundError:
        return []
    return result["hits"]["hits"]


def search_by_content(text: str, limit: int = 10, offset: int = 0) -> dict:
    result = es_client.search(
        body={
            "from": offset,
            "size": limit,
            "query": {
                "match": {
                    "content": text
                }
            },
        },
    )
    return result["hits"]["hits"]


def reindex(index_name: str, index_mapping: dict):
    if es_client.indices.exists(index=index_name):
        es_client.indices.delete(index=index_name)
    create_index(index_name, index_mapping)


def bulk_update():
    from elasticsearch.helpers import bulk

    actions = [
        {
            "_op_type": "update",
            "_index": "repo",
            "_id": "abc123",
            "doc": {"content": "updated content"}
        },
        {
            "_op_type": "update",
            "_index": "repo",
            "_id": "xyz456",
            "doc": {"content": "one more file updated"}
        }
    ]

    bulk(es_client, actions)
    log.info("Mass update ready")


def upsert():
    doc_id = "abc123"

    update_body = {
        "doc": {
            "content": "new content"
        },
        "doc_as_upsert": True
    }

    es_client.update(index="repos", id=doc_id, body=update_body)
    log.info(f"Doc {doc_id} updated and created")
