from sqlalchemy.orm import Session

from app.core.state_machine import validate_transition
from app.core.enums import CommentState
from app.core.locks import lock_comment_for_update
from app.core.exceptions import BrandViolation

from app.review.models import Review
from app.generation.models import CommentSuggestion
from app.brand.service import run_brand_checks
from app.posting.service import post_approved_comment


def approve_comment(
    *,
    comment_id: int,
    reviewer: str | None,
    notes: str | None,
    db: Session,
):
    """
    Human approval step (MANDATORY).

    Guarantees:
    - strict state transitions
    - brand validation before approval
    - concurrency-safe approval
    - automatic posting after approval
    """

    comment: CommentSuggestion = lock_comment_for_update(db, comment_id)

    validate_transition(comment.state, CommentState.APPROVED)

    # Brand enforcement before approval
    run_brand_checks(comment.text)

    review = Review(
        comment_id=comment.id,
        reviewer=reviewer,
        notes=notes,
        previous_state=comment.state,
        new_state=CommentState.APPROVED,
    )

    comment.state = CommentState.APPROVED

    db.add(review)
    db.commit()

    # Auto-post AFTER approval
    post_approved_comment(
        comment_id=comment.id,
        db=db,
    )

    return comment


def request_edit(
    *,
    comment_id: int,
    reviewer: str | None,
    notes: str | None,
    db: Session,
):
    """
    Send comment back for editing.
    """

    comment: CommentSuggestion = lock_comment_for_update(db, comment_id)

    validate_transition(comment.state, CommentState.EDITED)

    review = Review(
        comment_id=comment.id,
        reviewer=reviewer,
        notes=notes,
        previous_state=comment.state,
        new_state=CommentState.EDITED,
    )

    comment.state = CommentState.EDITED

    db.add(review)
    db.commit()

    return comment

def send_for_review(*, comment_id: int, db: Session):
    comment: CommentSuggestion = lock_comment_for_update(db, comment_id)

    validate_transition(comment.state, CommentState.UNDER_REVIEW)

    comment.state = CommentState.UNDER_REVIEW
    db.commit()

    return comment

def start_review(*, comment_id: int, db: Session):
    comment: CommentSuggestion = lock_comment_for_update(db, comment_id)

    validate_transition(comment.state, CommentState.UNDER_REVIEW)

    comment.state = CommentState.UNDER_REVIEW
    db.commit()

    return comment


