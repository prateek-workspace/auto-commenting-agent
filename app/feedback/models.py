from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    ForeignKey,
    DateTime,
    func,
)
from app.core.database import Base


class Feedback(Base):
    """
    Captures signals used for learning and memory.

    Sources:
    - approval / rejection
    - edits before approval
    - (optional) engagement signals
    """

    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    comment_id = Column(
        Integer,
        ForeignKey("comment_suggestions.id"),
        nullable=False,
        index=True,
    )

    approved = Column(Boolean, nullable=False)
    edited_before_approval = Column(Boolean, default=False)

    # Optional / simulated engagement
    engagement_notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
