from enum import Enum


class CommentState(str, Enum):
    IDENTIFIED = "identified"
    GENERATED = "generated"
    UNDER_REVIEW = "under_review"
    EDITED = "edited"
    APPROVED = "approved"
    POSTING = "posting"
    POSTED = "posted"
    FAILED = "failed"


class PostState(str, Enum):
    IDENTIFIED = "identified"
    UNDER_REVIEW = "under_review"


class FeedbackType(str, Enum):
    EDIT_DIFF = "edit_diff"
    REJECTION_REASON = "rejection_reason"
    APPROVAL_SIGNAL = "approval_signal"
