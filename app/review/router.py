from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.review.service import approve_comment, request_edit, auto_edit_comment
from app.core.database import SessionLocal
from app.review.schemas import ReviewAction, ReviewResponse
from app.core.database import get_db
from app.review.models import Review
from app.review.service import approve_comment, request_edit

router = APIRouter(tags=["review"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/approve/{comment_id}", response_model=ReviewResponse)
def approve(
    comment_id: int,
    payload: ReviewAction,
    db: Session = Depends(get_db),
):
    comment = approve_comment(
        comment_id=comment_id,
        reviewer=payload.reviewer,
        notes=payload.notes,
        db=db,
    )
    return {
        "comment_id": comment.id,
        "new_state": comment.state,
    }


@router.post("/edit/{comment_id}", response_model=ReviewResponse)
def edit(
    comment_id: int,
    payload: ReviewAction,
    db: Session = Depends(get_db),
):
    comment = request_edit(
        comment_id=comment_id,
        reviewer=payload.reviewer,
        notes=payload.notes,
        db=db,
    )
    return {
        "comment_id": comment.id,
        "new_state": comment.state,
    }

@router.post("/review/request/{comment_id}")
def request_review(
    comment_id: int,
    action: ReviewAction,
    db: Session = Depends(get_db),
):
    comment = request_edit(
        comment_id=comment_id,
        reviewer=action.reviewer,
        notes=action.notes,
        db=db,
    )
    return comment


@router.get("/")
def list_reviews(db: Session = Depends(get_db)):
    """
    List all review actions (approve / edit / reject).
    """
    return (
        db.query(Review)
        .order_by(Review.id.desc())
        .all()
    )

@router.post("/auto-edit/{comment_id}")
def auto_edit(
    comment_id: int,
    feedback: str,
    reviewer: str | None = None,
    db: Session = Depends(get_db),
):
    return auto_edit_comment(
        comment_id=comment_id,
        feedback=feedback,
        reviewer=reviewer,
        db=db,
    )
