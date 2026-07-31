import json
from pathlib import Path
from langchain_core.documents import Document


def load_chunks():

    path = Path("app/storage/chunks.json")

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        return []

    return [
        Document(
            page_content=item["page_content"],
            metadata=item["metadata"]
        )
        for item in data
    ]