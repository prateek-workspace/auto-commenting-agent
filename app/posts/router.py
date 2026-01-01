from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.posts.service import ingest_post
from app.core.database import SessionLocal
from app.posts.schemas import PostCreate, PostIngestRequest, PostResponse
from app.posts.service import create_post
from app.posts.models import Post

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


@router.get("/")
def list_posts(db: Session = Depends(get_db)):
    """
    List all posts in the system.
    Useful for monitoring ingestion & targeting.
    """
    return db.query(Post).order_by(Post.id.desc()).all()

@router.post("/ingest")
def ingest(payload: PostIngestRequest, db: Session = Depends(get_db)):
    return ingest_post(payload=payload, db=db)