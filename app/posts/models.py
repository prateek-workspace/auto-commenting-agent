from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base
from app.core.enums import PostState

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)

    platform = Column(String(50), nullable=False)
    author_name = Column(String(255), nullable=True)
    author_role = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)

    post_url = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)

    industry = Column(String(255), nullable=True)
    topic_tags = Column(String(500), nullable=True)

    state = Column(String(50), nullable=False, index=True)

    # Optional targeting metadata
    match_score = Column(Integer, nullable=True)
    matched_rules = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
