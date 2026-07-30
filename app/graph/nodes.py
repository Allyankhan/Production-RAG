import os
from dotenv import load_dotenv
from langsmith import traceable

from app.graph.state import GraphState
from app.rag.retriever import retriever
from app.graph.llm import llm
from app.security.context_sanitizer import sanitize_documents
from app.security.pii import mask_pii
from app.rag.reranker import rerank

load_dotenv()

os.environ['LANGSMITH_TRACING'] = "true"


@traceable(name="Retrieve Documents")
def retrieve_documents(state: GraphState):
    documents = retriever.invoke(state["question"])
    documents = rerank(
    state["question"],
    documents,
    top_k=5
)
    safe_documents = sanitize_documents(documents)
    
    
    
    return {
        "documents": safe_documents
    }


@traceable(name="Generate Answer")
def generate_answer(state: GraphState):
    sources = []
    seen = set()
    masked_contents = []

    # 1. Loop through retrieved documents
    for doc in state.get("documents", []):
        # Mask PII in page content
        masked_text = mask_pii(doc.page_content)
        masked_contents.append(masked_text)

        # Extract and deduplicate sources
        source_file = doc.metadata.get("source", "Unknown")
        source_page = doc.metadata.get("page", "Unknown")
        key = (source_file, source_page)

        if key not in seen:
            seen.add(key)
            sources.append({
                "file": source_file,
                "page": source_page
            })

    # 2. Join the masked text snippets into context
    context = "\n\n".join(masked_contents)

    # 3. Format Prompt
    prompt = f"""
Answer the user's question ONLY using the provided context.

Context:
{context}

Question:
{state["question"]}
"""

    # 4. Invoke LLM
    response = llm.invoke(prompt)

    # 5. Return updated state dictionary with both answer and sources
    return {
        "answer": response.content,
        "sources": sources
    }