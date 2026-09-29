"""Receipt-callback errors."""


class ReceiptError(Exception):
    pass


class SignatureError(ReceiptError):
    """The callback signature does not match the raw body."""


class InvalidReceipt(ReceiptError, ValueError):
    """The callback body is malformed or breaks the receipt contract."""


class IdempotencyConflict(ReceiptError):
    """The idempotency key was already used with a different payload."""
