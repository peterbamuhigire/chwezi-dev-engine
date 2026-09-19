"""Provenance-aware tool calls that stop before consequential side effects."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

try:
    from ..approval_control_plane import ApprovalGate, ActionPreview, ApprovalRecord, ApprovalError, sha256_json
except ImportError:  # direct ``tools`` path imports used by lightweight tests
    from approval_control_plane import ApprovalGate, ActionPreview, ApprovalRecord, ApprovalError, sha256_json


class ToolProvenanceError(ValueError):
    """Raised before a malformed, unauthorised, or tainted call executes."""


@dataclass(frozen=True)
class ToolObservation:
    tool_name: str
    observation_id: str
    value: Any
    provenance: str = "untrusted"

    def __post_init__(self) -> None:
        if self.provenance not in {"trusted", "untrusted"}:
            raise ToolProvenanceError("provenance must be trusted or untrusted")


@dataclass(frozen=True)
class ToolDefinition:
    tool_name: str
    action_type: str
    blast_radius: str
    reversibility: str
    allowed_requesters: frozenset[str] = frozenset()
    rollback_ref: str = "tool-reversal"
    verification_ref: str = "tool-result-check"

    @property
    def requires_approval(self) -> bool:
        return self.blast_radius == "external" or self.reversibility == "irreversible"


@dataclass(frozen=True)
class ToolCall:
    tool_call_id: str
    tool_name: str
    args: Mapping[str, Any]
    arg_provenance: Mapping[str, tuple[str, ...]]

    @property
    def payload_hash(self) -> str:
        return sha256_json({"tool_name": self.tool_name, "args": self.args})


@dataclass(frozen=True)
class PreparedToolCall:
    call: ToolCall
    definition: ToolDefinition
    requester_id: str
    preview: ActionPreview | None = None


def observation_argument(observation: ToolObservation) -> tuple[Any, tuple[str, ...]]:
    """Convert an observation to an argument plus its source/taint marker."""
    return observation.value, (f"{observation.provenance}:{observation.tool_name}:{observation.observation_id}",)


class ToolDispatcher:
    def __init__(self, definitions: Mapping[str, ToolDefinition], approval_gate: ApprovalGate) -> None:
        self.definitions = dict(definitions)
        self.approval_gate = approval_gate

    def prepare(self, call: ToolCall, request_id: str, requester_id: str) -> PreparedToolCall:
        definition = self.definitions.get(call.tool_name)
        if definition is None:
            raise ToolProvenanceError("UNKNOWN_TOOL")
        if not isinstance(call.tool_call_id, str) or not call.tool_call_id.strip() or not isinstance(requester_id, str) or not requester_id.strip():
            raise ToolProvenanceError("CALL_IDENTITY_REQUIRED")
        if not isinstance(call.args, Mapping) or not isinstance(call.arg_provenance, Mapping):
            raise ToolProvenanceError("MALFORMED_TOOL_CALL")
        if definition.allowed_requesters and requester_id not in definition.allowed_requesters:
            raise ToolProvenanceError("UNAUTHORISED_REQUESTER")
        missing = sorted(set(call.args) - set(call.arg_provenance))
        if missing:
            raise ToolProvenanceError(f"MISSING_ARG_PROVENANCE: {', '.join(missing)}")
        for arg_name, origins in call.arg_provenance.items():
            if arg_name not in call.args or not origins or not all(isinstance(item, str) and item for item in origins):
                raise ToolProvenanceError(f"MALFORMED_ARG_PROVENANCE: {arg_name}")
        if not definition.requires_approval:
            return PreparedToolCall(call, definition, requester_id)
        # Include the exact payload hash and provenance in the approval scope.
        try:
            payload_hash = call.payload_hash
            preview = self.approval_gate.preview(
                request_id, requester_id, definition.action_type,
                {"tool_name": call.tool_name, "tool_call_id": call.tool_call_id},
                {"payload_hash": payload_hash,
                 "arg_provenance": {key: list(value) for key, value in sorted(call.arg_provenance.items())}},
                rollback_ref=definition.rollback_ref,
                verification_ref=definition.verification_ref,
                action_id=call.tool_call_id,
            )
        except (ApprovalError, TypeError, ValueError) as exc:
            raise ToolProvenanceError(f"TOOL_PREVIEW_DENIED: {exc}") from exc
        return PreparedToolCall(call, definition, requester_id, preview)

    def execute(self, prepared: PreparedToolCall, operation: Callable[[], Any],
                approval: ApprovalRecord | None = None,
                verifier: Callable[[Any], bool] | None = None,
                executed_at: Any = None) -> Any:
        if prepared.preview is None:
            return operation()
        try:
            return self.approval_gate.execute(prepared.preview, approval, operation, verifier, executed_at)
        except ApprovalError as exc:
            raise ToolProvenanceError(str(exc)) from exc
