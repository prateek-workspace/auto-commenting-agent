from pydantic import BaseModel
from typing import Optional
from app.core.enums import CommentState


class ReviewAction(BaseModel):
    reviewer: Optional[str] = None
    notes: Optional[str] = None


class ReviewResponse(BaseModel):
    comment_id: int
    new_state: CommentState

    class Config:
        from_attributes = True
