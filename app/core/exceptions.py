class ProssimaError(Exception):
    """Base exception for the system."""


class InvalidStateTransition(ProssimaError):
    pass


class BrandViolation(ProssimaError):
    pass


class KillSwitchEnabled(ProssimaError):
    pass


class PostingLimitExceeded(ProssimaError):
    pass


class LLMGenerationError(ProssimaError):
    def __init__(self, message: str, details: list[str] | None = None):
        super().__init__(message)
        self.details = details or []
