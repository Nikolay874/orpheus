import logging
from functools import cache

from io import StringIO
from fastapi import APIRouter

from orpheus.bl.indexer import search_by_content, search_by_id
from orpheus.bl.tools import get_code_language

router = APIRouter()

log = logging.getLogger(__name__)
LOG_PREFIX = 'API'


@router.get('/search_by_text')
def search_by_text(text: str, limit: int = 10, offset=0) -> dict:
    items = []
    res = search_by_content(text, limit, offset)
    for row in res:
        content = row['_source']['content']
        f = StringIO(content)
        lines = f.readlines()
        records = []
        for index, line in enumerate(lines):
            if text in line:
                if index > 3:
                    records.append(
                        '\n'.join([
                            lines[index - 2], lines[index - 1],
                            lines[index], lines[index + 1], lines[index + 2]
                        ])
                    )
                elif index == 0:
                    records.append(
                        '\n'.join([
                            lines[index], lines[index + 1], lines[index + 2]
                        ])
                    )
        for record in records:
            items.append(
                {
                    "title": row["_source"]["file"],
                    "code": record,
                    "language": (
                        get_code_language(content).lower()
                        if get_code_language(content)
                        else None
                    ),
                    "id": row["_id"],
                    "index": row["_index"],
                }
            )
        if len(items) > limit:
            break

    return {
        "items": items
    }


@router.get('/get_content')
def get_content(id: str, index: str) -> dict:
    res = search_by_id(document_id=id, index=index)
    if res:
        content = res[0]['_source']['content']
        return {
            "title": res[0]["_source"]["file"],
            "code": res[0]['_source']['content'],
            "language": (
                get_code_language(content).lower()
                if get_code_language(content)
                else None
            ),
        }
    return {}
