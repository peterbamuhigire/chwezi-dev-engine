"""Application context shared by the API handlers and the export worker."""
from __future__ import annotations


class AppContext:
    def __init__(self, secret: bytes, idp, repo, now: int = 1_800_000_000):
        self.secret = secret
        self.idp = idp
        self.repo = repo
        self.clock = now
        self.audit: list[dict] = []
        self.jobs: dict[str, dict] = {}
        self.exports: dict[str, str] = {}

    def now(self) -> int:
        return self.clock
