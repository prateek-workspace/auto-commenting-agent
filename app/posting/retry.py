import time
from typing import Callable
from app.core.config import settings


def retry_with_backoff(fn: Callable):
    """
    Retry helper with bounded attempts.
    """

    last_error = None

    for attempt in range(settings.POSTING_RETRY_LIMIT):
        try:
            return fn()
        except Exception as e:
            last_error = e
            time.sleep(settings.POSTING_RETRY_BACKOFF_SECONDS)

    raise last_error
