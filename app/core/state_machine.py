from app.core.enums import CommentState
from app.core.exceptions import InvalidStateTransition


ALLOWED_TRANSITIONS = {
    CommentState.IDENTIFIED: {CommentState.GENERATED},
    CommentState.GENERATED: {CommentState.UNDER_REVIEW},
    CommentState.UNDER_REVIEW: {CommentState.EDITED, CommentState.APPROVED},
    CommentState.EDITED: {CommentState.UNDER_REVIEW, CommentState.APPROVED},
    CommentState.APPROVED: {CommentState.POSTING},
    CommentState.POSTING: {CommentState.POSTED, CommentState.FAILED},
}



def validate_transition(
    current: CommentState,
    next_state: CommentState,
):
    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if next_state not in allowed:
        raise InvalidStateTransition(
            f"Invalid state transition: {current} → {next_state}"
        )
