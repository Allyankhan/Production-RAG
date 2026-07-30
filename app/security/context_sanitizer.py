import re
import logging
from langchain_core.documents import Document

SUSPICIOUS_PATTERNS = [
    r"ignore\s+all\s+previous\s+instructions",
    r"ignore\s+previous\s+instructions",
    r"reveal\s+system\s+prompt",
    r"developer\s+message",
    r"always\s+answer",
    r"do\s+not\s+answer",
    r"forget\s+the\s+context",
    r"override\s+instructions",
    r"act\s+as",
]
logger = logging.getLogger(__name__)


def sanitize_documents(documents: list[Document]) -> list[Document]:
    safe_documents = []

    for doc in documents:
        text = doc.page_content.lower()

        suspicious = False

        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, text):
                suspicious = True
                logger.warning(
                    f"Suspicious document chunk removed: {pattern}"
                )
                
                break

        if not suspicious:
            safe_documents.append(doc)

    return safe_documents