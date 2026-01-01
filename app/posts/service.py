from sqlalchemy.orm import Session
from app.posts.models import Post
from app.posts.schemas import PostCreate
from app.posts.rules import is_relevant_post
from app.core.exceptions import ProssimaError


def create_post(payload: PostCreate, db: Session):
    """
    Persist a post only if it passes relevance rules.
    """

    topics = payload.topic_tags or []

    if not is_relevant_post(
        industry=payload.industry,
        role=payload.author_role,
        topics=topics,
    ):
        raise ProssimaError("Post does not match targeting rules")

    post = Post(
        platform=payload.platform,
        content=payload.content,
        post_url=str(payload.post_url) if payload.post_url else None,
        author_name=payload.author_name,
        author_role=payload.author_role,
        company=payload.company,
        industry=payload.industry,
        topic_tags=",".join(topics) if topics else None,
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return post
