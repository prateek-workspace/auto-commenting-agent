from sqlalchemy.orm import Session
from app.posts.models import Post
from app.posts.schemas import PostCreate, PostIngestRequest
from app.posts.rules import is_relevant_post
from app.core.exceptions import ProssimaError
from app.core.enums import PostState
from app.brand.detectors import is_brand_relevant
from app.generation.service import generate_comments_for_post
from app.core.exceptions import BrandViolation
from app.brand.validators import validate_brand_compliance
from app.workflows.post_pipeline import process_identified_post


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


def ingest_post(*, payload: PostIngestRequest, db: Session):
    """
    Step A: Post Ingestion & Targeting
    """

    # Lightweight brand relevance check
    try:
        validate_brand_compliance(payload.content)
        matched = True
    except Exception:
        matched = False

    state = PostState.IDENTIFIED if matched else PostState.REJECTED

    post = Post(
        platform=payload.platform,
        content=payload.content,
        author_name=payload.author_name,
        author_role=payload.author_role,
        company=payload.company,
        post_url=payload.post_url,
        state=state,
        match_score=90 if matched else 0,
        matched_rules="brand_compliance_check",
    )

    db.add(post)
    db.commit()
    process_identified_post(post, db)
    db.refresh(post)

    metadata = {
        "matched": matched,
        "state": state,
        "score": post.match_score,
    }

    return post, metadata
