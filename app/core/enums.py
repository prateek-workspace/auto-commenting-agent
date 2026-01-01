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
