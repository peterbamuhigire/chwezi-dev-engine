"""vetted_crypto 3.2.1 - synthetic stand-in for a locked, externally audited security dependency.

In this fixture the package is vendored so the repository works offline; treat it as a mature
installed library (see requirements.lock). It wraps standard primitives: scrypt password hashing and
HMAC-SHA256 compact tokens with explicit algorithm, key-id, issuer, audience and expiry policy.
Do not edit this package; upgrade it through the lock file.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os

__version__ = "3.2.1"
__all__ = ["TokenError", "hash_password", "verify_password", "sign_token", "verify_token"]

_SCRYPT = {"n": 2 ** 14, "r": 8, "p": 1}


class TokenError(Exception):
    """A token failed verification. The message never contains key material."""


def _b64e(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64d(text: str) -> bytes:
    if not isinstance(text, str) or any(c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_" for c in text):
        raise TokenError("malformed token segment")
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def hash_password(password: str) -> str:
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")
    salt = os.urandom(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, dklen=32, **_SCRYPT)
    return f"scrypt${_SCRYPT['n']}${_SCRYPT['r']}${_SCRYPT['p']}${_b64e(salt)}${_b64e(digest)}"


def verify_password(password: str, stored: str) -> bool:
    try:
        scheme, n, r, p, salt, digest = stored.split("$")
        if scheme != "scrypt":
            return False
        candidate = hashlib.scrypt(password.encode("utf-8"), salt=_b64d(salt), dklen=32, n=int(n), r=int(r), p=int(p))
    except (ValueError, TokenError, AttributeError):
        return False
    return hmac.compare_digest(candidate, _b64d(digest))


def sign_token(claims: dict, key: bytes, kid: str) -> str:
    header = {"alg": "HS256", "typ": "JWT", "kid": kid}
    signing_input = f"{_b64e(json.dumps(header, separators=(',', ':')).encode())}.{_b64e(json.dumps(claims, separators=(',', ':')).encode())}"
    signature = hmac.new(key, signing_input.encode("ascii"), hashlib.sha256).digest()
    return f"{signing_input}.{_b64e(signature)}"


def verify_token(token: str, keys: dict, *, issuer: str, audience: str, now: int, algorithms=("HS256",), leeway: int = 0) -> dict:
    if not isinstance(token, str) or token.count(".") != 2:
        raise TokenError("malformed token")
    head_b64, body_b64, sig_b64 = token.split(".")
    try:
        header = json.loads(_b64d(head_b64))
        claims = json.loads(_b64d(body_b64))
    except ValueError as exc:
        raise TokenError("malformed token") from exc
    if not isinstance(header, dict) or not isinstance(claims, dict):
        raise TokenError("malformed token")
    alg = header.get("alg")
    if alg not in algorithms or alg != "HS256":
        raise TokenError("algorithm not allowed")
    key = keys.get(header.get("kid"))
    if key is None:
        raise TokenError("unknown key id")
    expected = hmac.new(key, f"{head_b64}.{body_b64}".encode("ascii"), hashlib.sha256).digest()
    if not sig_b64 or not hmac.compare_digest(expected, _b64d(sig_b64)):
        raise TokenError("bad signature")
    if claims.get("iss") != issuer:
        raise TokenError("wrong issuer")
    aud = claims.get("aud")
    if not (aud == audience or (isinstance(aud, list) and audience in aud)):
        raise TokenError("wrong audience")
    exp = claims.get("exp")
    if not isinstance(exp, int) or isinstance(exp, bool) or exp + leeway <= now:
        raise TokenError("expired or missing expiry")
    nbf = claims.get("nbf")
    if nbf is not None and (not isinstance(nbf, int) or nbf - leeway > now):
        raise TokenError("token not yet valid")
    return claims
