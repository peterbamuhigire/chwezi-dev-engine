"""Audit trail; downstream compliance tooling depends on event names and their order."""
from __future__ import annotations


class AuditLog:
    def __init__(self) -> None:
        self.events: list[tuple[str, str]] = []

    def record(self, event: str, subject: str) -> None:
        self.events.append((event, subject))
