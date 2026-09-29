class ParseError(ValueError):
    def __init__(self, code: str, position: int, message: str = ""):
        super().__init__(message or f"{code} at pair {position}")
        self.code = code
        self.position = position


class TransientFailure(Exception):
    """The downstream call may succeed if retried."""


class PermanentFailure(Exception):
    """The downstream call will never succeed; do not retry."""
