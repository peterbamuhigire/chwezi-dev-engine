"""Local fake identity provider (stands in for the real IdP in tests)."""
from __future__ import annotations

from lib import authkit


class FakeIdentityProvider:
    def __init__(self, secret: bytes):
        self._secret = secret
        self._users: dict[str, dict] = {}

    def add_user(self, sub: str, tenant: str, roles: set[str]) -> None:
        self._users[sub] = {"tenant": tenant, "roles": set(roles)}

    def issue_token(self, sub: str, now: int, ttl: int = 900) -> str:
        user = self._users[sub]
        return authkit.issue(self._secret, {"sub": sub, "tenant": user["tenant"], "roles": sorted(user["roles"])}, ttl, now)

    def revoke_role(self, sub: str, role: str) -> None:
        self._users[sub]["roles"].discard(role)

    def current_roles(self, sub: str) -> set[str]:
        user = self._users.get(sub)
        return set(user["roles"]) if user else set()

    def current_tenant(self, sub: str):
        user = self._users.get(sub)
        return user["tenant"] if user else None
