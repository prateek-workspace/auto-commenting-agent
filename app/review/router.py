from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.review.service import start_review as start_review_service
from app.core.database import SessionLocal
from app.review.schemas import ReviewAction, ReviewResponse
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

@router.post("/review/start/{comment_id}")
def start_review(comment_id: int, db: Session = Depends(get_db)):
    return start_review_service(comment_id=comment_id, db=db)
