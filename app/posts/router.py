from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.posts.schemas import PostCreate, PostResponse
from app.posts.service import create_post

router = APIRouter(prefix="/posts", tags=["posts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/submit", response_model=PostResponse)
def submit_post(payload: PostCreate, db: Session = Depends(get_db)):
    """
    Entry point of the system.

    - Accepts a post
    - Applies rule-based targeting
    - Persists if relevant
    """
    return create_post(payload, db)
