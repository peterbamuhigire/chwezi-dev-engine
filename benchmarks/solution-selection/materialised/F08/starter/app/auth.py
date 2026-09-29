"""Request authentication using the installed authkit library."""
from __future__ import annotations

from app.errors import Denied
from lib import authkit


def authenticate(ctx, token) -> dict:
    try:
        return authkit.verify(token, ctx.secret, ctx.now())
    except authkit.AuthError as exc:
        ctx.audit.append({"event": "auth_failed", "reason": str(exc)})
        raise Denied("unauthenticated") from None
