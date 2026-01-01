import re

# V1: simple keyword + regex rules
BRAND_KEYWORDS = [
    "engineering",
    "system design",
    "debug",
    "scaling",
    "backend",
    "architecture",
    "startup",
]

DISALLOWED_PATTERNS = [
    r"politics",
    r"religion",
    r"giveaway",
]


def is_relevant_post(text: str) -> tuple[bool, dict]:
    text_lower = text.lower()

    keyword_hits = [
        kw for kw in BRAND_KEYWORDS if kw in text_lower
    ]

    blocked = any(
        re.search(pattern, text_lower)
        for pattern in DISALLOWED_PATTERNS
    )

    return (
        bool(keyword_hits) and not blocked,
        {
            "keyword_hits": keyword_hits,
            "blocked": blocked,
        },
    )
