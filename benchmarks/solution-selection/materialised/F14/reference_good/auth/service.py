"""Authentication service: a thin layer over the vetted_crypto dependency (see docs/dependency-decision.md)."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vendor"))

import vetted_crypto  # noqa: E402

from auth import config  # noqa: E402

ROLE_RANK = {"viewer": 1, "exporter": 2, "admin": 3}


def _username(username: str) -> str:
    name = str(username or "").strip().lower()
    if not name:
        raise ValueError("username required")
    return name


def register(store: dict, username: str, password: str) -> None:
    store[_username(username)] = vetted_crypto.hash_password(password)


def login(store: dict, username: str, password: str, logger: logging.Logger) -> bool:
    try:
        name = _username(username)
    except ValueError:
        logger.info("login refused: empty username")
        return False
    ok = name in store and vetted_crypto.verify_password(password, store[name])
    logger.info("login %s for %s", "succeeded" if ok else "failed", name)
    return ok


def issue_token(username: str, role: str, *, now: int) -> str:
    claims = {"sub": _username(username), "role": role, "iss": config.ISSUER, "aud": config.AUDIENCE,
              "iat": now, "exp": now + config.TOKEN_TTL_SECONDS}
    return vetted_crypto.sign_token(claims, config.KEYS[config.ACTIVE_KID], config.ACTIVE_KID)


def authorise(token: str, *, now: int, required_role: str) -> dict:
    try:
        claims = vetted_crypto.verify_token(token, config.KEYS, issuer=config.ISSUER, audience=config.AUDIENCE,
                                            now=now, algorithms=("HS256",))
    except vetted_crypto.TokenError as exc:
        raise PermissionError(f"token rejected: {exc}") from exc
    if ROLE_RANK.get(claims.get("role"), 0) < ROLE_RANK[required_role]:
        raise PermissionError("insufficient role")
    return claims
