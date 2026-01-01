from sqlalchemy.orm import Session
from sqlalchemy import select

from app.feedback.models import Feedback, FeedbackLog
from app.core.enums import FeedbackType
from app.generation.models import CommentSuggestion


def record_feedback(
    *,
    comment_id: int,
    approved: bool,
    edited_before_approval: bool = False,
    engagement_notes: str | None = None,
    db: Session,
):
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
    stmt = (
        select(CommentSuggestion.text)
        .join(Feedback, Feedback.comment_id == CommentSuggestion.id)
        .where(Feedback.approved.is_(True))
        .order_by(Feedback.created_at.desc())
        .limit(limit)
    )

    results = db.execute(stmt).scalars().all()

    return [
        text.strip()[:120]
        for text in results
        if text
    ]


def store_approval_signal(
    *, comment_id: int, option_index: int, reviewer: str | None, db: Session
):
    db.add(
        FeedbackLog(
            comment_id=comment_id,
            feedback_type=FeedbackType.APPROVAL_SIGNAL,
            approved_option_index=option_index,
            reviewer=reviewer,
        )
    )
    db.commit()


def store_edit_feedback(
    *,
    comment_id: int,
    original_text: str,
    edited_text: str,
    reviewer: str | None,
    db: Session,
):
    db.add(
        FeedbackLog(
            comment_id=comment_id,
            feedback_type=FeedbackType.EDIT_DIFF,
            original_text=original_text,
            updated_text=edited_text,
            reviewer=reviewer,
        )
    )
    db.commit()


def get_recent_edit_examples(db: Session, limit: int = 5) -> str:
    rows = (
        db.query(FeedbackLog)
        .filter(FeedbackLog.feedback_type == FeedbackType.EDIT_DIFF)
        .order_by(FeedbackLog.created_at.desc())
        .limit(limit)
        .all()
    )

    return "\n\n".join(
        f"Before: {r.original_text}\nAfter: {r.updated_text}"
        for r in rows
    )


def store_rejection_reason(
    *,
    comment_id: int,
    reason: str,
    reviewer: str | None,
    db: Session,
):
    db.add(
        FeedbackLog(
            comment_id=comment_id,
            feedback_type=FeedbackType.REJECTION_REASON,
            rejection_reason=reason,
            reviewer=reviewer,
        )
    )
    db.commit()
