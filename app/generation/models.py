from sqlalchemy import Column, Integer, Text, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.enums import CommentState


class CommentSuggestion(Base):
    __tablename__ = "comment_suggestions"

    id = Column(Integer, primary_key=True, index=True)

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    text = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)

    state = Column(
        Enum(CommentState),
        default=CommentState.GENERATED,
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
