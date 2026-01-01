from sqlalchemy.orm import Session

from app.core.state_machine import validate_transition
from app.core.enums import CommentState
from app.core.exceptions import PostingLimitExceeded
from app.core.locks import lock_comment_for_update

from app.posting.client import MockPostingClient
from app.posting.idempotency import has_already_posted
from app.posting.retry import retry_with_backoff
from app.posting.models import PostingAttempt


def post_approved_comment(
    *,
    comment_id: int,
    db: Session,
):
    """
    Automatically post a previously APPROVED comment.

    Guarantees:
    - no double posting
    - strict state transitions
    - confirmable success or failure
    """

    comment = lock_comment_for_update(db, comment_id)

    validate_transition(comment.state, CommentState.POSTING)

    if has_already_posted(db, comment_id):
        raise PostingLimitExceeded(
            f"Comment {comment_id} already posted"
        )

    comment.state = CommentState.POSTING
    db.commit()

    client = MockPostingClient()

    def _attempt():
        return client.post_comment(
            post_id=comment.post_id,
            text=comment.text,
        )

    try:
        result = retry_with_backoff(_attempt)

        attempt = PostingAttempt(
            comment_id=comment.id,
            success=result.success,
            external_id=result.external_id,
        )

        comment.state = CommentState.POSTED

    except Exception as e:
        attempt = PostingAttempt(
            comment_id=comment.id,
            success=False,
            error_message=str(e),
        )

        comment.state = CommentState.FAILED

    db.add(attempt)
    db.commit()

    return attempt
