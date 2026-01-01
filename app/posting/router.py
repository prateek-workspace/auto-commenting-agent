from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.posting.service import post_approved_comment

router = APIRouter(prefix="/posting", tags=["posting"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/post/{comment_id}")
def post_comment(comment_id: int, db: Session = Depends(get_db)):
    """
    Trigger auto-posting for an APPROVED comment.
    """
    return post_approved_comment(
        comment_id=comment_id,
        db=db,
    )
