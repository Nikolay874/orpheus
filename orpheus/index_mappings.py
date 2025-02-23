repo_index = {
    "mappings": {
        "properties": {
            "repo": {"type": "keyword"},
            "file": {"type": "keyword"},
            "content": {
                "type": "text",
                "analyzer": "standard"
            }
        }
    }
}
