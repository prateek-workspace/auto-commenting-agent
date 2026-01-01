from sqlalchemy.orm import Session
from sqlalchemy import select

from app.feedback.models import Feedback
from app.generation.models import CommentSuggestion
from app.core.enums import CommentState


def record_feedback(
    *,
    comment_id: int,
    approved: bool,
    edited_before_approval: bool = False,
    engagement_notes: str | None = None,
    db: Session,
):
    """
    Store feedback signals for future learning.
    """

    feedback = Feedback(
        comment_id=comment_id,
        approved=approved,
        edited_before_approval=edited_before_approval,
        engagement_notes=engagement_notes,
    )

    db.add(feedback)
    db.commit()
    return feedback


def get_recent_approved_comment_patterns(
    *,
    db: Session,
    limit: int = 50,
) -> list[str]:
    """
    Memory aggregation function.

    Returns short summaries / patterns from previously APPROVED comments.
    These are injected into prompts as NEGATIVE CONSTRAINTS
    to avoid repetition.

    This approach scales from 100 → 10,000 comments without embeddings.
    """

    stmt = (
        select(CommentSuggestion.text)
        .join(Feedback, Feedback.comment_id == CommentSuggestion.id)
        .where(Feedback.approved.is_(True))
        .order_by(Feedback.created_at.desc())
        .limit(limit)
    )

    results = db.execute(stmt).scalars().all()

    # Simple pattern extraction (V1):
    # truncate and normalize phrasing
    patterns = [
        text.strip()[:120]
        for text in results
        if text
    ]

    return patterns
