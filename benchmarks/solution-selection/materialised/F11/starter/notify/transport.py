"""Transport protocol (documentation only; tests inject fakes).

send(message: dict, idempotency_key: str) -> str
    Returns the provider message id. Raises TransientError, RetryAfter, PermanentError or
    TimeoutError. A TimeoutError may be raised after the provider accepted the message.

status(idempotency_key: str) -> str
    "accepted" if the provider holds a message for this key, otherwise "unknown".
"""
