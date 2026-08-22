"""Small fail-closed approval gate shared by the local skill engines.

This module is deliberately provider-agnostic. It is suitable for unit and
adapter integration tests and for embedding in a trusted host dispatcher. It
does not authenticate people itself; the host must supply an authenticated
identity and a policy-versioned allow-list.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Mapping
from uuid import uuid4


class ApprovalError(ValueError):
    """Raised whenever the gate cannot prove that execution is authorised."""


def _utc(value: datetime | None = None) -> datetime:
    current = value or datetime.now(timezone.utc)
    if current.tzinfo is None:
        return current.replace(tzinfo=timezone.utc)
    return current.astimezone(timezone.utc)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ActionDefinition:
    action_type: str
    action_class: str
    owner: str
    allowed_approver_roles: tuple[str, ...]
    preview_required: bool
    approval_ttl_seconds: int | None
    idempotency_required: bool
    rollback: str
    verification: str
    requires_dual_approval: bool = False

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ActionDefinition":
        required = ("action_type", "class", "owner", "allowed_approver_roles", "preview_required",
                    "approval_ttl_seconds", "idempotency_required", "rollback", "verification")
        missing = [key for key in required if key not in value]
        if missing:
            raise ApprovalError(f"action definition missing fields: {', '.join(missing)}")
        action_class = value["class"]
        if action_class not in {"L0", "L1", "L2", "L3"}:
            raise ApprovalError(f"unsupported action class: {action_class}")
        roles = value["allowed_approver_roles"]
        if not isinstance(roles, list) or not roles or not all(isinstance(role, str) and role.strip() for role in roles):
            raise ApprovalError(f"{value.get('action_type')}: approver roles must be non-empty")
        requires_approval = action_class in {"L2", "L3"}
        if requires_approval and (value["preview_required"] is not True or not value["idempotency_required"]):
            raise ApprovalError(f"{value.get('action_type')}: L2/L3 requires preview and idempotency")
        if requires_approval and (not isinstance(value["approval_ttl_seconds"], int) or value["approval_ttl_seconds"] <= 0):
            raise ApprovalError(f"{value.get('action_type')}: L2/L3 requires a positive approval TTL")
        if requires_approval and (not isinstance(value["rollback"], str) or not value["rollback"].strip()):
            raise ApprovalError(f"{value.get('action_type')}: rollback reference is required")
        if requires_approval and (not isinstance(value["verification"], str) or not value["verification"].strip()):
            raise ApprovalError(f"{value.get('action_type')}: verification reference is required")
        return cls(
            action_type=str(value["action_type"]),
            action_class=action_class,
            owner=str(value["owner"]),
            allowed_approver_roles=tuple(roles),
            preview_required=bool(value["preview_required"]),
            approval_ttl_seconds=value["approval_ttl_seconds"],
            idempotency_required=bool(value["idempotency_required"]),
            rollback=str(value["rollback"]),
            verification=str(value["verification"]),
            requires_dual_approval=bool(value.get("requires_dual_approval", False)),
        )


@dataclass(frozen=True)
class ActionPreview:
    request_id: str
    action_id: str
    action_type: str
    action_class: str
    requester_id: str
    target: Mapping[str, Any]
    scope: Mapping[str, Any]
    scope_hash: str
    preview_hash: str
    action_nonce: str
    policy_version: str
    created_at: datetime
    expires_at: datetime | None
    rollback_ref: str
    verification_ref: str


@dataclass(frozen=True)
class ApprovalRecord:
    approval_id: str
    action_id: str
    approver_id: str
    approver_role: str
    approved_at: datetime
    expires_at: datetime
    policy_version: str
    scope_hash: str
    action_nonce: str
    approval_text: str
    second_approver_id: str | None = None


class AuditSink:
    """In-memory tamper-evident sink used by tests and host adapters."""

    def __init__(self) -> None:
        self.available = True
        self.records: list[dict[str, Any]] = []

    def append(self, event: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        if not self.available:
            raise ApprovalError("audit sink unavailable; execution denied")
        previous = self.records[-1]["event_hash"] if self.records else "GENESIS"
        record = {"event": event, "payload": dict(payload), "previous_hash": previous}
        record["event_hash"] = sha256_json(record)
        self.records.append(record)
        return record


class ApprovalGate:
    """Trusted dispatcher boundary; unknown and unproven actions fail closed."""

    def __init__(self, definitions: Mapping[str, ActionDefinition], policy_version: str,
                 allowlist: Mapping[str, Mapping[str, set[str]]], audit: AuditSink | None = None,
                 now: Callable[[], datetime] | None = None) -> None:
        self.definitions = dict(definitions)
        self.policy_version = policy_version
        self.allowlist = allowlist
        self.audit = audit or AuditSink()
        self.now = now or (lambda: datetime.now(timezone.utc))
        self.kill_switch = False
        self._used_nonces: set[str] = set()
        self._results: dict[str, Any] = {}

    @classmethod
    def from_adapter(cls, path: str | Path, allowlist: Mapping[str, Mapping[str, set[str]]],
                     policy_version: str, **kwargs: Any) -> "ApprovalGate":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        definitions = {item["action_type"]: ActionDefinition.from_mapping(item) for item in payload["actions"]}
        if len(definitions) != len(payload["actions"]):
            raise ApprovalError("duplicate action_type in adapter")
        return cls(definitions, policy_version, allowlist, **kwargs)

    def preview(self, request_id: str, requester_id: str, action_type: str,
                target: Mapping[str, Any], scope: Mapping[str, Any],
                rollback_ref: str | None = None, verification_ref: str | None = None,
                action_id: str | None = None, action_nonce: str | None = None,
                created_at: datetime | None = None) -> ActionPreview:
        definition = self.definitions.get(action_type)
        if definition is None:
            raise ApprovalError(f"unknown action denied: {action_type}")
        if not requester_id or not isinstance(target, Mapping) or not target:
            raise ApprovalError("requester and unambiguous target are required")
        if not isinstance(scope, Mapping) or not scope:
            raise ApprovalError("non-empty bounded scope is required")
        if definition.action_class in {"L2", "L3"} and (not rollback_ref or not verification_ref):
            raise ApprovalError("consequential action requires rollback and verification references")
        created = _utc(created_at or self.now())
        expiry = (created + timedelta(seconds=definition.approval_ttl_seconds)
                  if definition.approval_ttl_seconds else None)
        aid = action_id or f"ACT-{uuid4().hex}"
        nonce = action_nonce or f"NONCE-{uuid4().hex}"
        scope_hash = sha256_json({"target": target, "scope": scope})
        preview_hash = sha256_json({"action_id": aid, "action_type": action_type,
                                    "class": definition.action_class, "target": target,
                                    "scope": scope, "scope_hash": scope_hash,
                                    "policy_version": self.policy_version})
        preview = ActionPreview(request_id, aid, action_type, definition.action_class, requester_id,
                                dict(target), dict(scope), scope_hash, preview_hash, nonce,
                                self.policy_version, created, expiry, rollback_ref or definition.rollback,
                                verification_ref or definition.verification)
        self.audit.append("action_previewed", {"request_id": request_id, "action_id": aid,
                                                "action_type": action_type, "class": definition.action_class,
                                                "requester_id": requester_id, "target": dict(target),
                                                "scope_hash": scope_hash, "policy_version": self.policy_version})
        return preview

    def approve(self, preview: ActionPreview, approver_id: str, approver_role: str,
                approval_text: str, approved_at: datetime | None = None,
                second_approver_id: str | None = None) -> ApprovalRecord:
        definition = self._definition(preview)
        if definition.action_class not in {"L2", "L3"}:
            raise ApprovalError("L0/L1 action does not accept a critical approval")
        if not approver_id or approver_id == preview.requester_id:
            raise ApprovalError("self-approval or missing approver denied")
        if approver_role not in definition.allowed_approver_roles:
            raise ApprovalError("approver role is outside the action policy")
        if approver_id not in self.allowlist.get(approver_role, {}).get(preview.action_type, set()) and approver_id not in self.allowlist.get(approver_role, {}).get("*", set()):
            raise ApprovalError("approver is not authorised for this action")
        if definition.requires_dual_approval and (not second_approver_id or second_approver_id in {approver_id, preview.requester_id}):
            raise ApprovalError("distinct second approver is required")
        current = _utc(approved_at or self.now())
        if preview.expires_at is None or current >= preview.expires_at:
            raise ApprovalError("preview approval window has expired")
        text = approval_text.strip() if isinstance(approval_text, str) else ""
        if not text or preview.action_id not in text or "approve" not in text.lower():
            raise ApprovalError("typed approval must identify the action and say approve")
        record = ApprovalRecord(f"APR-{uuid4().hex}", preview.action_id, approver_id, approver_role,
                                current, preview.expires_at, preview.policy_version, preview.scope_hash,
                                preview.action_nonce, text, second_approver_id)
        self.audit.append("approval_received", {"approval_id": record.approval_id, "action_id": record.action_id,
                                                 "approver_id": approver_id, "approver_role": approver_role,
                                                 "approved_at": current.isoformat(), "expires_at": record.expires_at.isoformat(),
                                                 "scope_hash": record.scope_hash, "action_nonce": record.action_nonce,
                                                 "policy_version": record.policy_version})
        return record

    def execute(self, preview: ActionPreview, approval: ApprovalRecord | None,
                operation: Callable[[], Any], verifier: Callable[[Any], bool] | None = None,
                executed_at: datetime | None = None) -> Any:
        definition = self._definition(preview)
        current = _utc(executed_at or self.now())
        if self.kill_switch:
            raise ApprovalError("kill switch active; execution denied")
        if definition.idempotency_required and preview.action_id in self._results:
            return self._results[preview.action_id]
        if definition.action_class in {"L2", "L3"}:
            self._check_approval(preview, approval, current)
            if verifier is None:
                raise ApprovalError("post-action verification callback is required")
        self.audit.append("action_executing", {"action_id": preview.action_id, "action_type": preview.action_type,
                                                "class": preview.action_class, "scope_hash": preview.scope_hash,
                                                "approval_id": approval.approval_id if approval else None,
                                                "idempotency_key": preview.action_id})
        try:
            result = operation()
            self.audit.append("action_completed", {"action_id": preview.action_id, "result_ref": "redacted-result"})
            if verifier is not None and not verifier(result):
                self.audit.append("action_verification_failed", {"action_id": preview.action_id})
                raise ApprovalError("post-action verification failed")
            if verifier is not None:
                self.audit.append("action_verified", {"action_id": preview.action_id,
                                                       "verification_ref": preview.verification_ref})
            self._results[preview.action_id] = result
            return result
        except ApprovalError:
            raise
        except Exception as exc:
            self.audit.append("action_failed", {"action_id": preview.action_id, "error_type": type(exc).__name__})
            raise

    def _definition(self, preview: ActionPreview) -> ActionDefinition:
        definition = self.definitions.get(preview.action_type)
        if definition is None or definition.action_class != preview.action_class:
            raise ApprovalError("action definition changed or is unknown")
        if preview.policy_version != self.policy_version:
            raise ApprovalError("policy version mismatch; re-preview required")
        return definition

    def _check_approval(self, preview: ActionPreview, approval: ApprovalRecord | None, now: datetime) -> None:
        if approval is None:
            raise ApprovalError("explicit approval required before execution")
        if approval.action_id != preview.action_id or approval.scope_hash != preview.scope_hash:
            raise ApprovalError("approval scope does not match final preview")
        if approval.action_nonce != preview.action_nonce or approval.policy_version != preview.policy_version:
            raise ApprovalError("approval nonce or policy version does not match")
        if approval.approved_at >= now or now >= approval.expires_at:
            raise ApprovalError("approval is stale, expired, or post-dated")
        if approval.action_nonce in self._used_nonces:
            raise ApprovalError("approval nonce has already been used")
        if approval.approver_id == preview.requester_id:
            raise ApprovalError("self-approval denied")
        definition = self._definition(preview)
        if approval.approver_role not in definition.allowed_approver_roles:
            raise ApprovalError("approver role is outside the action policy")
        allowed = self.allowlist.get(approval.approver_role, {})
        if approval.approver_id not in allowed.get(preview.action_type, set()) and approval.approver_id not in allowed.get("*", set()):
            raise ApprovalError("approver is not authorised for this action")
        self._used_nonces.add(approval.action_nonce)
