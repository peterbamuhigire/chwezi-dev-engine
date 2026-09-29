"""authkit 2.3.1 (installed, pinned) - signed bearer tokens for internal services.

Synthetic fixture library written for this benchmark. Tokens are ``header.payload.signature``
(base64url, no padding) signed with HMAC-SHA256. ``verify`` accepts only ``alg: HS256``, compares
signatures in constant time and enforces ``exp``. Do not re-implement this module.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json


class AuthError(Exception):
    """The token is missing, malformed, forged, uses a wrong algorithm or has expired."""


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64decode(text: str) -> bytes:
    padding = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + padding)


def _sign(secret: bytes, signing_input: str) -> str:
    return _b64encode(hmac.new(secret, signing_input.encode("ascii"), hashlib.sha256).digest())


def issue(secret: bytes, claims: dict, ttl: int, now: int) -> str:
    header = _b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    body = dict(claims, iat=now, exp=now + ttl)
    payload = _b64encode(json.dumps(body, separators=(",", ":"), sort_keys=True).encode())
    signing_input = f"{header}.{payload}"
    return f"{signing_input}.{_sign(secret, signing_input)}"


def verify(token, secret: bytes, now: int) -> dict:
    if not isinstance(token, str) or token.count(".") != 2:
        raise AuthError("malformed token")
    header_part, payload_part, signature = token.split(".")
    try:
        header = json.loads(_b64decode(header_part))
        claims = json.loads(_b64decode(payload_part))
    except (ValueError, UnicodeDecodeError) as exc:
        raise AuthError("malformed token") from exc
    if not isinstance(header, dict) or header.get("alg") != "HS256":
        raise AuthError("unsupported algorithm")
    expected = _sign(secret, f"{header_part}.{payload_part}")
    if not hmac.compare_digest(expected, signature):
        raise AuthError("bad signature")
    if not isinstance(claims, dict) or not isinstance(claims.get("exp"), int) or claims["exp"] <= now:
        raise AuthError("expired token")
    return claims
