from sqlalchemy import (
    Column,
    Integer,
    Text,
    Enum,
    ForeignKey,
    DateTime,
    func,
)
from app.core.database import Base
from app.core.enums import CommentState


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    comment_id = Column(
        Integer,
        ForeignKey("comment_suggestions.id"),
        nullable=False,
        index=True,
    )

    reviewer = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    previous_state = Column(
        Enum(CommentState),
        nullable=False,
    )
    new_state = Column(
        Enum(CommentState),
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
