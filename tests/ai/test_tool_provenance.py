import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.ai.tool_provenance import (  # noqa: E402
    ToolCall,
    ToolDefinition,
    ToolDispatcher,
    ToolObservation,
    ToolProvenanceError,
    observation_argument,
)
from tools.approval_control_plane import ActionDefinition, ApprovalGate  # noqa: E402


NOW = datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc)


def dispatcher():
    action = ActionDefinition.from_mapping({
        "action_type": "fixture.send", "class": "L3", "owner": "owner",
        "allowed_approver_roles": ["reviewer"], "preview_required": True,
        "approval_ttl_seconds": 900, "idempotency_required": True,
        "rollback": "cancel", "verification": "check",
    })
    gate = ApprovalGate({action.action_type: action}, "approval-policy-1.0.0",
                        {"reviewer": {"fixture.send": {"reviewer-1"}}}, now=lambda: NOW)
    definition = ToolDefinition("send", "fixture.send", "external", "irreversible")
    return ToolDispatcher({"send": definition}, gate)


class ToolProvenanceTests(unittest.TestCase):
    def test_untrusted_observation_is_carried_into_approval_scope(self):
        value, provenance = observation_argument(ToolObservation("lookup", "OBS-1", "attacker", "untrusted"))
        call = ToolCall("CALL-1", "send", {"recipient": value}, {"recipient": provenance})
        prepared = dispatcher().prepare(call, "REQ-1", "requester")
        self.assertIsNotNone(prepared.preview)
        self.assertIn("payload_hash", prepared.preview.scope)

    def test_unknown_malformed_and_unauthorised_calls_are_denied_before_operation(self):
        d = dispatcher()
        with self.assertRaisesRegex(ToolProvenanceError, "UNKNOWN_TOOL"):
            d.prepare(ToolCall("CALL-1", "unknown", {}, {}), "REQ-1", "requester")
        with self.assertRaisesRegex(ToolProvenanceError, "MISSING_ARG_PROVENANCE"):
            d.prepare(ToolCall("CALL-2", "send", {"recipient": "x"}, {}), "REQ-1", "requester")
        restricted = ToolDispatcher({"send": ToolDefinition("send", "fixture.send", "external", "irreversible", frozenset({"owner"}))}, d.approval_gate)
        with self.assertRaisesRegex(ToolProvenanceError, "UNAUTHORISED_REQUESTER"):
            restricted.prepare(ToolCall("CALL-3", "send", {"recipient": "x"}, {"recipient": ("trusted",)}), "REQ-1", "requester")

    def test_changed_payload_and_replay_cannot_duplicate_side_effect(self):
        d = dispatcher()
        call = ToolCall("CALL-1", "send", {"recipient": "x"}, {"recipient": ("trusted",)})
        prepared = d.prepare(call, "REQ-1", "requester")
        approval = d.approval_gate.approve(prepared.preview, "reviewer-1", "reviewer", f"I approve action {call.tool_call_id}")
        calls = []
        self.assertEqual(d.execute(prepared, lambda: calls.append("sent") or "ok", approval, lambda value: value == "ok", executed_at=NOW.replace(second=1)), "ok")
        self.assertEqual(d.execute(prepared, lambda: calls.append("duplicate") or "bad", approval, lambda value: True, executed_at=NOW.replace(second=2)), "ok")
        self.assertEqual(calls, ["sent"])
        changed = d.prepare(ToolCall("CALL-1", "send", {"recipient": "changed"}, {"recipient": ("trusted",)}), "REQ-1", "requester")
        with self.assertRaisesRegex(ToolProvenanceError, "payload changed"):
            d.execute(changed, lambda: calls.append("changed"), approval, lambda value: True, executed_at=NOW.replace(second=3))


if __name__ == "__main__":
    unittest.main()
