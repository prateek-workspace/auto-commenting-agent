"""
Soft detectors.

These do NOT block automatically,
but are logged and surfaced during review.
"""


def detect_risk_signals(text: str) -> list[str]:
    signals = []
    lowered = text.lower()

    if "always" in lowered or "never" in lowered:
        signals.append("Absolute language")

    if "should" in lowered:
        signals.append("Prescriptive tone")

    if "!" in text:
        signals.append("Exclamatory emphasis")

    return signals


def is_brand_relevant(text: str) -> bool:
    """
    Cheap, fast pre-filter.
    No LLM here.
    """

    keywords = [
        "engineering",
        "developer",
        "system",
        "architecture",
        "debug",
        "scaling",
        "design",
        "startup",
        "product",
    ]

    lowered = text.lower()
    return any(k in lowered for k in keywords)
