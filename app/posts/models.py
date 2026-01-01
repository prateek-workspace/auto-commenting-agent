from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)

    platform = Column(String(50), nullable=False)  # linkedin, x, etc.
    author_name = Column(String(255), nullable=True)
    author_role = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)

    post_url = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)

    industry = Column(String(255), nullable=True)
    topic_tags = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
