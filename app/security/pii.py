import re
EMAIL_PATTERN = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_PATTERN = r"\b03\d{9}\b"
CNIC_PATTERN = r"\b\d{5}-\d{7}-\d\b"

def mask_pii(text: str):

    text = re.sub(
        EMAIL_PATTERN,
        "[EMAIL REDACTED]",
        text
    )

    text = re.sub(
        PHONE_PATTERN,
        "[PHONE REDACTED]",
        text
    )

    text = re.sub(
        CNIC_PATTERN,
        "[CNIC REDACTED]",
        text
    )

    return text