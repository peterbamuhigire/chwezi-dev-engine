"""Authentication service.

Grown by accretion: adapters and factories that only forward calls to vetted_crypto. The public
functions at the bottom are what callers use.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vendor"))

import vetted_crypto  # noqa: E402

from auth import config  # noqa: E402

ROLE_RANK = {"viewer": 1, "exporter": 2, "admin": 3}


class PasswordManagerAdapter:
    """Adapter kept for a password backend that was never added."""

    def __init__(self, backend=None):
        self.backend = backend or vetted_crypto

    def make_hash(self, password):
        result = self.backend.hash_password(password)
        if result is None:
            raise RuntimeError("hash backend returned nothing")
        return result

    def check(self, password, stored):
        if stored is None:
            return False
        outcome = self.backend.verify_password(password, stored)
        if outcome is True:
            return True
        if outcome is False:
            return False
        return bool(outcome)


class TokenManagerAdapter:
    """Adapter kept for a token backend that was never added."""

    def __init__(self, backend=None, settings=None):
        self.backend = backend or vetted_crypto
        self.settings = settings or config

    def make_token(self, claims):
        kid = self.settings.ACTIVE_KID
        key = self.settings.KEYS[kid]
        return self.backend.sign_token(claims, key, kid)

    def read_token(self, token, now):
        return self.backend.verify_token(token, self.settings.KEYS, issuer=self.settings.ISSUER,
                                         audience=self.settings.AUDIENCE, now=now, algorithms=("HS256",))


class AuthServiceFactory:
    """Factory kept for configurable backends; only the defaults were ever used."""

    _passwords = None
    _tokens = None

    @classmethod
    def passwords(cls):
        if cls._passwords is None:
            cls._passwords = PasswordManagerAdapter()
        return cls._passwords

    @classmethod
    def tokens(cls):
        if cls._tokens is None:
            cls._tokens = TokenManagerAdapter()
        return cls._tokens


def _normalise_username(username):
    if username is None:
        return None
    username = str(username)
    username = username.strip()
    if username == "":
        return None
    return username.lower()


def _normalise_username_again(username):
    # Second copy used by login(); kept identical to _normalise_username.
    if username is None:
        return None
    username = str(username).strip()
    return username.lower() if username else None


def register(store: dict, username: str, password: str) -> None:
    name = _normalise_username(username)
    if name is None:
        raise ValueError("username required")
    store[name] = AuthServiceFactory.passwords().make_hash(password)


def login(store: dict, username: str, password: str, logger: logging.Logger) -> bool:
    name = _normalise_username_again(username)
    if name is None:
        logger.info("login refused: empty username")
        return False
    stored = store.get(name)
    ok = AuthServiceFactory.passwords().check(password, stored)
    if ok:
        logger.info("login succeeded for %s", name)
    else:
        logger.info("login failed for %s", name)
    return ok


def issue_token(username: str, role: str, *, now: int) -> str:
    claims = {"sub": _normalise_username(username), "role": role, "iss": config.ISSUER, "aud": config.AUDIENCE,
              "iat": now, "exp": now + config.TOKEN_TTL_SECONDS}
    return AuthServiceFactory.tokens().make_token(claims)


def authorise(token: str, *, now: int, required_role: str) -> dict:
    try:
        claims = AuthServiceFactory.tokens().read_token(token, now)
    except vetted_crypto.TokenError as exc:
        raise PermissionError(f"token rejected: {exc}") from exc
    if ROLE_RANK.get(claims.get("role"), 0) < ROLE_RANK[required_role]:
        raise PermissionError("insufficient role")
    return claims
