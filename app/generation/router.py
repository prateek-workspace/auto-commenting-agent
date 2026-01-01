from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.generation.models import CommentSuggestion
from app.core.database import SessionLocal
from app.generation.service import generate_comments_for_post
from app.generation.worker import process_identified_posts

router = APIRouter(prefix="/generation", tags=["generation"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate/{post_id}")
def generate(
    post_id: int,
    post_content: str,
    db: Session = Depends(get_db),
):
    suggestions = generate_comments_for_post(
        post_id=post_id,
        post_content=post_content,
        db=db,
    )

    return [
        {
            "id": s.id,
            "text": s.text,
            "state": s.state,
            "explanation": s.explanation,
        }
        for s in suggestions
    ]


@router.get("/")
def list_comments(db: Session = Depends(get_db)):
    """
    List all comment suggestions across all states.
    """
    return (
        db.query(CommentSuggestion)
        .order_by(CommentSuggestion.id.desc())
        .all()
    )

@router.get("/post/{post_id}")
def list_comments_for_post(post_id: int, db: Session = Depends(get_db)):
    """
    List all comments generated for a given post.
    """
    return (
        db.query(CommentSuggestion)
        .filter(CommentSuggestion.post_id == post_id)
        .order_by(CommentSuggestion.id.asc())
        .all()
    )

@router.post("/worker/run")
def run_generation_worker(
    db: Session = Depends(get_db),
):
    process_identified_posts(db)
    return {"status": "ok"}
