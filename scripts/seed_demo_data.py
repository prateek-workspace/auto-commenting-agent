"""
Seed demo data for local / evaluation use.

Creates:
- A sample post
- Generates comment suggestions
- Marks one as approved (optional)
- Records feedback

Usage:
    python scripts/seed_demo_data.py
"""

from sqlalchemy.orm import Session

from app.core.database import SessionLocal, init_db
from app.posts.models import Post
from app.generation.service import generate_comments_for_post
from app.feedback.service import record_feedback


def run():
    init_db()
    db: Session = SessionLocal()

    # -------------------------------
    # Create a demo post
    # -------------------------------
    post = Post(
        platform="linkedin",
        content=(
            "We’ve learned that shipping early and listening to users "
            "has been the biggest driver of product clarity for our team."
        ),
        author_name="Jane Doe",
        author_role="Product Manager",
        company="ExampleTech",
        industry="saas",
        topic_tags="product,feedback,iteration",
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    print(f"Created Post ID: {post.id}")

    # -------------------------------
    # Generate comments
    # -------------------------------
    comments = generate_comments_for_post(
        post_id=post.id,
        post_content=post.content,
        db=db,
    )

    print(f"Generated {len(comments)} comment suggestions")

    # -------------------------------
    # Simulate approval + feedback
    # -------------------------------
    approved_comment = comments[0]

    record_feedback(
        comment_id=approved_comment.id,
        approved=True,
        edited_before_approval=False,
        engagement_notes="Demo approval for seeded data",
        db=db,
    )

    print(f"Approved Comment ID: {approved_comment.id}")

    db.close()


if __name__ == "__main__":
    run()
