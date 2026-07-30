import json
from langchain_postgres import PGVector
from app.config import settings
from app.rag.embedding import embeddings
from app.rag.loader import chunks

vector_store=PGVector(
    embeddings=embeddings,
    collection_name="Company_documents",
    connection=settings.DATABASE_URL,
    use_jsonb=True,


)

chunk_data = []

for doc in chunks:

    chunk_data.append(
        {
            "page_content": doc.page_content,
            "metadata": doc.metadata
        }
    )

with open(
    "app/storage/chunks.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        chunk_data,
        f,
        ensure_ascii=False,
        indent=2
    )