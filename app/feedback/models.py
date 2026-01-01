from sqlalchemy import Column, Integer, Boolean, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Feedback(Base):
    """
    High-level learning signals
    (used for approval ratios, engagement tracking)
    """
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("comment_suggestions.id"), nullable=False)

    approved = Column(Boolean, default=False)
    edited_before_approval = Column(Boolean, default=False)
    engagement_notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FeedbackLog(Base):
    """
    Low-level feedback events
    (diffs, rejection reasons, reviewer actions)
    """
    __tablename__ = "feedback_logs"

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("comment_suggestions.id"), nullable=False)

    feedback_type = Column(String(50), nullable=False)

    original_text = Column(Text, nullable=True)
    updated_text = Column(Text, nullable=True)

    approved_option_index = Column(Integer, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    reviewer = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
