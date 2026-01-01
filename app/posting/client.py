from dataclasses import dataclass
from typing import Optional
from app.core.config import settings
from app.core.exceptions import KillSwitchEnabled


@dataclass
class PostingResult:
    success: bool
    external_id: Optional[str] = None
    error: Optional[str] = None


class MockPostingClient:
    """
    V1 posting adapter.

    - Deterministic
    - Confirmable
    - Platform-agnostic

    Replaced in V2 by real platform adapters.
    """

    def post_comment(self, *, post_id: int, text: str) -> PostingResult:
        if not settings.AUTO_POSTING_ENABLED:
            raise KillSwitchEnabled("Auto-posting is globally disabled")

        # Simulated successful posting
        return PostingResult(
            success=True,
            external_id=f"mock_post_{post_id}",
        )
