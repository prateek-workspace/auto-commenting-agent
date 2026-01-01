from sqlalchemy.orm import Session
from sqlalchemy import select
from app.generation.models import CommentSuggestion


def lock_comment_for_update(
    db: Session,
    comment_id: int,
) -> CommentSuggestion:
    """
    Acquire row-level lock to prevent concurrent approvals/posting.
    """
    stmt = (
        select(CommentSuggestion)
        .where(CommentSuggestion.id == comment_id)
        .with_for_update()
    )
    result = db.execute(stmt).scalar_one()
    return result
