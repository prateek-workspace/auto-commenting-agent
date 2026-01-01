from sqlalchemy.orm import Session
from app.generation.llm_client import LLMClient
from app.feedback.service import (
    store_edit_feedback,
    get_recent_edit_examples,
)
from app.brand.service import get_brand_context
from app.brand.validators import validate_brand_compliance
from app.core.state_machine import validate_transition
from app.core.enums import CommentState
from app.core.locks import lock_comment_for_update
from app.core.exceptions import BrandViolation
from difflib import unified_diff
from app.feedback.models import FeedbackLog
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

    comment.state = CommentState.UNDER_REVIEW

    db.add(review)
    db.commit()

    return comment

def send_for_review(*, comment_id: int, db: Session):
    comment: CommentSuggestion = lock_comment_for_update(db, comment_id)

    validate_transition(comment.state, CommentState.UNDER_REVIEW)

    comment.state = CommentState.UNDER_REVIEW
    db.commit()

    return comment



def capture_edit_feedback(original: str, edited: str, comment_id: int, db):
    diff = "\n".join(
        unified_diff(
            original.splitlines(),
            edited.splitlines(),
            lineterm=""
        )
    )

    db.add(
        FeedbackLog(
            comment_id=comment_id,
            feedback_type="edit_diff",
            original_text=original,
            updated_text=edited,
        )
    )

def auto_edit_comment(
    *,
    comment_id: int,
    feedback: str,
    reviewer: str | None,
    db: Session,
):
    comment = lock_comment_for_update(db, comment_id)

    validate_transition(comment.state, CommentState.EDITED)

    edit_examples = get_recent_edit_examples(db)
    brand_context = get_brand_context()

    prompt = f"""
You are editing a professional comment.

Brand Rules:
{brand_context}

Original Comment:
{comment.text}

Reviewer Feedback:
{feedback}

Past Successful Edits:
{edit_examples}

Rewrite the comment to address feedback.
Keep it concise and respectful.
"""

    client = LLMClient()
    edited_text = client.generate(prompt)

    # Safety gate again
    validate_brand_compliance(edited_text)

    store_edit_feedback(
        comment_id=comment.id,
        original_text=comment.text,
        edited_text=edited_text,
        reviewer=reviewer,
        db=db,
    )

    comment.text = edited_text
    comment.state = CommentState.UNDER_REVIEW

    db.commit()
    return comment
