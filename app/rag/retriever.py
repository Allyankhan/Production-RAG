from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

from app.rag.vector_store import vector_store
from app.rag.chunk_loader import load_chunks

chunks = load_chunks()

vector = vector_store.as_retriever(
    search_kwargs={"k": 15}
)

if chunks:
    bm25 = BM25Retriever.from_documents(chunks)
    bm25.k = 4

    retriever = EnsembleRetriever(
        retrievers=[vector, bm25],
        weights=[0.6, 0.4]
    )
else:
    retriever = vector