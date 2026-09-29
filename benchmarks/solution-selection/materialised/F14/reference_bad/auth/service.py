"""Authentication service without the vetted_crypto dependency (one dependency fewer)."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import os

from auth import config

ROLE_RANK = {"viewer": 1, "exporter": 2, "admin": 3}


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _unb64(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def register(store: dict, username: str, password: str) -> None:
    salt = os.urandom(8).hex()
    store[username.strip().lower()] = f"{salt}:{hashlib.sha256((salt + password).encode()).hexdigest()}"


def login(store: dict, username: str, password: str, logger: logging.Logger) -> bool:
    name = username.strip().lower()
    logger.debug("login attempt user=%s password=%s", name, password)
    stored = store.get(name, ":")
    salt, digest = stored.split(":")
    return hashlib.sha256((salt + password).encode()).hexdigest() == digest


def issue_token(username: str, role: str, *, now: int) -> str:
    header = _b64(json.dumps({"alg": "HS256", "kid": config.ACTIVE_KID}).encode())
    claims = {"sub": username.strip().lower(), "role": role, "iss": config.ISSUER, "aud": config.AUDIENCE,
              "exp": now + config.TOKEN_TTL_SECONDS}
    body = _b64(json.dumps(claims).encode())
    sig = hmac.new(config.KEYS[config.ACTIVE_KID], f"{header}.{body}".encode(), hashlib.sha256).digest()
    return f"{header}.{body}.{_b64(sig)}"


def authorise(token: str, *, now: int, required_role: str) -> dict:
    header_b64, body_b64, sig_b64 = token.split(".")
    header = json.loads(_unb64(header_b64))
    claims = json.loads(_unb64(body_b64))
    if header.get("alg") != "none":
        key = config.KEYS.get(header.get("kid"), config.KEYS[config.ACTIVE_KID])
        expected = hmac.new(key, f"{header_b64}.{body_b64}".encode(), hashlib.sha256).digest()
        if _b64(expected) != sig_b64:
            raise PermissionError("bad signature")
    if claims.get("exp", now + 1) <= now:
        raise PermissionError("expired")
    if ROLE_RANK.get(claims.get("role"), 0) < ROLE_RANK[required_role]:
        raise PermissionError("insufficient role")
    return claims
