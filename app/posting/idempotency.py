from sqlalchemy.orm import Session
from sqlalchemy import select
from app.posting.models import PostingAttempt


def has_already_posted(
    db: Session,
    comment_id: int,
) -> bool:
    """
    Prevent duplicate posting.

    A comment can only be posted once successfully.
    """
    stmt = (
        select(PostingAttempt)
        .where(PostingAttempt.comment_id == comment_id)
        .where(PostingAttempt.success.is_(True))
    )
    return db.execute(stmt).scalar_one_or_none() is not None
