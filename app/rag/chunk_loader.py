import json

from langchain_core.documents import Document


def load_chunks():

    with open(
        "app/storage/chunks.json",
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    return [
        Document(
            page_content=item["page_content"],
            metadata=item["metadata"]
        )
        for item in data
    ]