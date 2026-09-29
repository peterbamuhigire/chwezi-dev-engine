"""Service errors."""


class Denied(Exception):
    """Request refused. ``code`` is one of: unauthenticated, forbidden, not_found."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code
