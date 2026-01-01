from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.feedback.models import Feedback
from app.core.database import SessionLocal
from app.feedback.service import record_feedback

router = APIRouter(prefix="/feedback", tags=["feedback"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/record/{comment_id}")
def record(
    comment_id: int,
    approved: bool,
    edited_before_approval: bool = False,
    engagement_notes: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Manually record feedback signals.
    Useful for demo, simulation, or admin tooling.
    """
    return record_feedback(
        comment_id=comment_id,
        approved=approved,
        edited_before_approval=edited_before_approval,
        engagement_notes=engagement_notes,
        db=db,
    )

@router.get("/")
def list_feedback(db: Session = Depends(get_db)):
    return db.query(Feedback).order_by(Feedback.created_at.desc()).all()
