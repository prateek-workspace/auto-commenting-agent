from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    ForeignKey,
    DateTime,
    func,
)
from app.core.database import Base


class PostingAttempt(Base):
    __tablename__ = "posting_attempts"

    id = Column(Integer, primary_key=True, index=True)

    comment_id = Column(
        Integer,
        ForeignKey("comment_suggestions.id"),
        nullable=False,
        index=True,
    )

    success = Column(Boolean, nullable=False)
    external_id = Column(String(255), nullable=True)
    error_message = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
