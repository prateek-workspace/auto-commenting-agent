from app.core.exceptions import BrandViolation
from app.core.config import settings


def validate_brand_compliance(text: str):
    """
    Hard validation rules.
    Any violation here BLOCKS approval.
    """

    lowered = text.lower()

    banned_phrases = [
        "guarantee",
        "we ensure",
        "best in class",
        "market leader",
        "buy now",
        "sign up",
    ]

    for phrase in banned_phrases:
        if phrase in lowered:
            raise BrandViolation(
                f"Banned marketing phrase detected: '{phrase}'"
            )

    if not settings.ALLOW_STATISTICS:
        if "%" in text or "percent" in lowered:
            raise BrandViolation("Statistics are not allowed")

    if not settings.ALLOW_EXTERNAL_FACTS:
        if "according to" in lowered or "research shows" in lowered:
            raise BrandViolation("External facts are not allowed")
