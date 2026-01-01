from sqlalchemy.orm import Session
from app.posts.models import Post
from app.core.enums import PostState, CommentState
from app.generation.service import generate_comments_for_post
from app.brand.validators import validate_brand_compliance
from app.core.exceptions import BrandViolation
from app.review.service import send_for_review


def process_identified_post(post: Post, db: Session):
    """
    IDENTIFIED → GENERATED → UNDER_REVIEW
    """

    # 1. Generate comments
    comments = generate_comments_for_post(
        post_id=post.id,
        post_content=post.content,
        db=db,
    )

    # 2. Self-critique (hard safety gate)
    safe_comments = []
    for c in comments:
        try:
            validate_brand_compliance(c.text)
            safe_comments.append(c)
        except BrandViolation:
            c.state = CommentState.FAILED

    if not safe_comments:
        post.state = PostState.FAILED
        db.commit()
        return

    # 3. Move comments to review
    for c in safe_comments:
        send_for_review(comment_id=c.id, db=db)

    post.state = PostState.UNDER_REVIEW
    db.commit()
