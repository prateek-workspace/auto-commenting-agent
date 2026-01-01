from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.posts.models import Post
from app.generation.models import CommentSuggestion
from app.review.models import Review

router = APIRouter(prefix="/observability", tags=["observability"])


@router.get("/snapshot")
def system_snapshot(db: Session = Depends(get_db)):
    """
    High-level system snapshot for admin dashboards.
    """
    return {
        "posts": db.query(Post).count(),
        "comments": db.query(CommentSuggestion).count(),
        "reviews": db.query(Review).count(),
        "recent_comments": (
            db.query(CommentSuggestion)
            .order_by(CommentSuggestion.id.desc())
            .limit(10)
            .all()
        ),
    }
