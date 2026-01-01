"""
Tests idempotency guarantees for auto-posting.

Goal:
- Ensure the system NEVER posts the same comment twice
- Protect against retries, crashes, or partial failures
"""

from app.posting.idempotency import (
    is_duplicate_post,
    mark_as_posted,
)


def test_idempotency_prevents_double_posting():
    comment_id = 42

    # Initially, the comment should NOT be marked as posted
    assert is_duplicate_post(comment_id) is False

    # Mark the comment as posted
    mark_as_posted(comment_id)

    # Now, the system must treat it as a duplicate
    assert is_duplicate_post(comment_id) is True
