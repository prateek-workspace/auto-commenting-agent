from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def init_db():
    # Import models so SQLAlchemy registers them
    from app.posts.models import Post
    from app.generation.models import CommentSuggestion
    from app.review.models import Review
    from app.posting.models import PostingAttempt
    from app.feedback.models import Feedback

    Base.metadata.create_all(bind=engine)
