class TransientError(Exception):
    """Provider or network failure that may succeed later."""


class RetryAfter(TransientError):
    """Provider asked us to wait at least ``seconds`` before retrying."""

    def __init__(self, seconds: float, message: str = "retry later"):
        super().__init__(message)
        self.seconds = seconds


class PermanentError(Exception):
    """Provider rejected the notification; retrying cannot help."""
