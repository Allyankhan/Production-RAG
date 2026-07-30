from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "BAAI/bge-reranker-base"
)

def rerank(question, documents, top_k=5):

    pairs = [
        (question, doc.page_content)
        for doc in documents
    ]

    scores = model.predict(pairs)

    ranked = sorted(
        zip(scores, documents),
        key=lambda x: x[0],
        reverse=True
    )

    return [
        doc
        for _, doc in ranked[:top_k]
    ]