from requests import Session
from app.brand.validator import validate_brand_compliance
from app.core.enums import PostState
from app.core.exceptions import BrandViolation
from app.generation.service import generate_comments_for_post
from app.posts.models import Post


def process_identified_posts(db: Session, limit: int = 5):
    posts = (
        db.query(Post)
        .filter(Post.status == PostState.IDENTIFIED)
        .limit(limit)
        .all()
    )

    for post in posts:
        try:
            comments = generate_comments_for_post(
                post_id=post.id,
                post_content=post.content,
                db=db,
            )

            # ---- Self critique ----
            for c in comments:
                validate_brand_compliance(c.text)

            post.status = PostState.UNDER_REVIEW
            db.commit()

        except BrandViolation as e:
            post.status = PostState.FAILED
            post.failure_reason = str(e)
            db.commit()
