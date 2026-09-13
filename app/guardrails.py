import re

MAX_QUERY_LENGTH = 500

USER_PATTERNS = [
    r"ignore\s+(all|previous|prior)\s+instructions",
    r"disregard\s+(all|previous|prior)\s+instructions",
    r"forget\s+(all|previous|prior)\s+instructions",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"show\s+(the\s+)?system\s+prompt",
    r"developer\s+message",
    r"hidden\s+instructions",
    r"override\s+(the\s+)?rules",
    r"bypass\s+(the\s+)?rules",
    r"act\s+as\s+system",
]

DOCUMENT_PATTERNS = [
    r"ignore\s+(all|previous|prior)\s+instructions",
    r"follow\s+these\s+instructions",
    r"system\s+prompt",
    r"assistant\s+must",
    r"override\s+the\s+system",
]


def normalize_text(text):
    return re.sub(r"\s+", " ", text).strip()


def validate_input(query):
    if not isinstance(query, str):
        return False, "Invalid query."

    query = query.strip()

    if not query:
        return False, "Query cannot be empty."

    if len(query) > MAX_QUERY_LENGTH:
        return False, "Query is too long."

    return True, ""


def matches_pattern(text, patterns):
    text = normalize_text(text.lower())

    return any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in patterns
    )


def detect_prompt_injection(query):
    return matches_pattern(
        query,
        USER_PATTERNS
    )


def detect_document_injection(text):
    return matches_pattern(
        text,
        DOCUMENT_PATTERNS
    )


def filter_safe_chunks(chunks):
    safe_chunks = []

    for chunk in chunks:
        text = chunk.get("text", "")

        if not detect_document_injection(text):
            safe_chunks.append(chunk)

    return safe_chunks


def validate_output(answer):
    if not isinstance(answer, str):
        return False

    answer = answer.strip()

    if not answer:
        return False

    blocked_phrases = [
        "system prompt",
        "developer message",
        "hidden instructions",
    ]

    answer_lower = answer.lower()

    return not any(
        phrase in answer_lower
        for phrase in blocked_phrases
    )