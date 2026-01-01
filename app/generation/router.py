from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.generation.service import generate_comments_for_post

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
