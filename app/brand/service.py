from app.brand.context import get_brand_context_text
from app.brand.validator import validate_brand_compliance
from app.brand.detectors import detect_risk_signals


def get_brand_context() -> str:
    """
    Returns brand context string for prompt injection.
    """
    return get_brand_context_text()


def run_brand_checks(text: str) -> dict:
    """
    Runs brand validation & detection.

    Returns:
    - blocking errors (if any)
    - non-blocking risk signals
    """

    validate_brand_compliance(text)

    signals = detect_risk_signals(text)

    return {
        "risk_signals": signals,
    }
