"""Versioned shared context packets with fail-closed trust checks."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

try:
    from ..approval_control_plane import canonical_json, sha256_json
except ImportError:  # direct ``tools`` path imports used by lightweight tests
    from approval_control_plane import canonical_json, sha256_json


class ContextValidationError(ValueError):
    """Raised when a packet cannot be trusted for the requested objective."""


def _utc(value: datetime | None) -> datetime:
    current = value or datetime.now(timezone.utc)
    if current.tzinfo is None:
        return current.replace(tzinfo=timezone.utc)
    return current.astimezone(timezone.utc)


def _iso(value: datetime | None) -> str | None:
    return _utc(value).isoformat() if value else None


@dataclass(frozen=True)
class ContextFinding:
    code: str
    severity: str
    path: str
    message: str


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    locator: str
    scope: str
    version: str
    fresh_until: datetime | None = None
    revoked: bool = False


@dataclass(frozen=True)
class ContextFact:
    key: str
    value: Any
    source_id: str
    locator: str
    scope: str
    permission_scope: frozenset[str] = frozenset({"public"})
    fresh_until: datetime | None = None
    trust: str = "trusted"
    interpretation: str = ""


@dataclass(frozen=True)
class ContextRelationship:
    subject: str
    predicate: str
    object: str
    source_id: str
    locator: str
    scope: str
    permission_scope: frozenset[str] = frozenset({"public"})
    fresh_until: datetime | None = None
    trust: str = "trusted"


@dataclass(frozen=True)
class SharedContextPacket:
    schema_version: str
    packet_id: str
    objective: str
    facts: tuple[ContextFact, ...]
    relationships: tuple[ContextRelationship, ...]
    policy_version: str

    @classmethod
    def create(cls, packet_id: str, objective: str, facts: tuple[ContextFact, ...] = (),
               relationships: tuple[ContextRelationship, ...] = (),
               policy_version: str = "context-policy-1.0.0") -> "SharedContextPacket":
        if not packet_id.strip() or not objective.strip() or not policy_version.strip():
            raise ContextValidationError("packet_id, objective and policy_version are required")
        return cls("shared-context.v1", packet_id, objective, tuple(facts),
                   tuple(relationships), policy_version)

    def as_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "packet_id": self.packet_id,
            "objective": self.objective,
            "policy_version": self.policy_version,
            "facts": [
                {"key": fact.key, "value": fact.value, "source_id": fact.source_id,
                 "locator": fact.locator, "scope": fact.scope,
                 "permission_scope": sorted(fact.permission_scope),
                 "fresh_until": _iso(fact.fresh_until), "trust": fact.trust,
                 "interpretation": fact.interpretation}
                for fact in sorted(self.facts, key=lambda item: item.key)
            ],
            "relationships": [
                {"subject": rel.subject, "predicate": rel.predicate, "object": rel.object,
                 "source_id": rel.source_id, "locator": rel.locator, "scope": rel.scope,
                 "permission_scope": sorted(rel.permission_scope),
                 "fresh_until": _iso(rel.fresh_until), "trust": rel.trust}
                for rel in sorted(self.relationships,
                                  key=lambda item: (item.subject, item.predicate, item.object))
            ],
        }

    @property
    def packet_hash(self) -> str:
        return sha256_json(self.as_mapping())

    def render_snapshot(self) -> str:
        """Return the exact replayable snapshot shared with agent and reviewer."""
        return canonical_json({"packet": self.as_mapping(), "packet_hash": self.packet_hash})

    def validate(self, expected_objective: str, sources: Mapping[str, SourceRecord],
                 actor_permissions: frozenset[str] | set[str],
                 now: datetime | None = None) -> tuple[ContextFinding, ...]:
        findings: list[ContextFinding] = []
        if self.objective != expected_objective:
            findings.append(ContextFinding("MISMATCHED_OBJECTIVE", "error", "objective",
                                           "packet objective does not match the requested objective"))
        checked_at = _utc(now)
        entries: list[tuple[str, str, str, str, frozenset[str], datetime | None, str]] = []
        entries.extend((f"facts[{index}]", fact.source_id, fact.locator, fact.scope,
                        fact.permission_scope, fact.fresh_until, fact.trust)
                       for index, fact in enumerate(self.facts))
        entries.extend((f"relationships[{index}]", rel.source_id, rel.locator, rel.scope,
                        rel.permission_scope, rel.fresh_until, rel.trust)
                       for index, rel in enumerate(self.relationships))
        allowed = frozenset(actor_permissions)
        for path, source_id, locator, scope, permissions, fresh_until, trust in entries:
            if trust not in {"trusted", "untrusted"}:
                findings.append(ContextFinding("INVALID_TRUST", "error", path,
                                               "trust must be trusted or untrusted"))
            if not source_id or not locator or not scope:
                findings.append(ContextFinding("MISSING_SOURCE_LOCATOR", "error", path,
                                               "source_id, locator and scope are required"))
                continue
            source = sources.get(source_id)
            if source is None:
                findings.append(ContextFinding("MISSING_SOURCE", "error", path,
                                               f"source {source_id} is absent from the source registry"))
                continue
            if source.revoked or not permissions.intersection(allowed):
                findings.append(ContextFinding("REVOKED_ACCESS", "error", path,
                                               f"access to source {source_id} is revoked or outside actor scope"))
            if source.locator != locator or source.scope != scope:
                findings.append(ContextFinding("SOURCE_SCOPE_MISMATCH", "error", path,
                                               f"packet locator/scope differs from source {source_id}"))
            expiry = fresh_until or source.fresh_until
            if expiry is not None and _utc(expiry) <= checked_at:
                findings.append(ContextFinding("STALE_CONTEXT", "error", path,
                                               f"source {source_id} is stale at the requested evaluation time"))
        return tuple(findings)

    def require_valid(self, expected_objective: str, sources: Mapping[str, SourceRecord],
                      actor_permissions: frozenset[str] | set[str],
                      now: datetime | None = None) -> None:
        findings = self.validate(expected_objective, sources, actor_permissions, now)
        if findings:
            raise ContextValidationError("; ".join(f"{item.code}: {item.message}" for item in findings))
