import hashlib

CACHE_VERSION = "v1"


def get_cache_key(question: str) -> str:
    question = question.lower().strip()

    question_hash = hashlib.md5(
        question.encode()
    ).hexdigest()

    return f"rag:{CACHE_VERSION}:{question_hash}"