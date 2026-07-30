import re


SUSPICIOUS_PATTERNS = [
    r"ignore\s+previous",
    r"ignore\s+all",
    r"system\s+prompt",
    r"developer\s+message",
    r"reveal\s+instructions",
    r"forget\s+everything",
    r"act\s+as",
]
def is_prompt_injection(text: str) -> bool:

    text = text.lower()

    for pattern in SUSPICIOUS_PATTERNS:

        if re.search(pattern, text):
            return True

    return False




