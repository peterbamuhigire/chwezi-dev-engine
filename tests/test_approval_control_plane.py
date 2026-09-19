import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from approval_control_plane import ApprovalError, ActionDefinition, ApprovalGate, AuditSink, ExecutionBudget


NOW = datetime(2026, 8, 22, 12, 0, tzinfo=timezone.utc)


def gate():
    definition = ActionDefinition.from_mapping({
        "action_type": "test.publish",
        "class": "L3",
        "owner": "owner",
        "allowed_approver_roles": ["reviewer"],
        "preview_required": True,
        "approval_ttl_seconds": 900,
        "idempotency_required": True,
        "rollback": "restore-snapshot",
        "verification": "check-result",
    })
    return ApprovalGate({definition.action_type: definition}, "approval-policy-1.0.0",
                        {"reviewer": {"test.publish": {"reviewer-1"}}},
                        now=lambda: NOW)


class ApprovalControlPlaneTests(unittest.TestCase):
    def test_unknown_action_is_denied(self):
        with self.assertRaises(ApprovalError):
            gate().preview("REQ-1", "requester", "unknown.action", {"env": "test"}, {"x": 1})

    def test_missing_approval_is_denied(self):
        g = gate()
        preview = g.preview("REQ-1", "requester", "test.publish", {"env": "test"}, {"content": "hash"}, "rollback", "verify")
        with self.assertRaises(ApprovalError):
            g.execute(preview, None, lambda: "side effect", lambda result: True)

    def test_scope_change_requires_fresh_approval(self):
        g = gate()
        preview = g.preview("REQ-1", "requester", "test.publish", {"env": "test"}, {"content": "hash"}, "rollback", "verify")
        approval = g.approve(preview, "reviewer-1", "reviewer", f"I approve action {preview.action_id} for test")
        changed = g.preview("REQ-1", "requester", "test.publish", {"env": "production"}, {"content": "hash"}, "rollback", "verify")
        with self.assertRaises(ApprovalError):
            g.execute(changed, approval, lambda: "side effect", lambda result: True)

    def test_self_approval_and_postdated_approval_are_denied(self):
        g = gate()
        preview = g.preview("REQ-1", "requester", "test.publish", {"env": "test"}, {"content": "hash"}, "rollback", "verify")
        with self.assertRaises(ApprovalError):
            g.approve(preview, "requester", "reviewer", f"I approve action {preview.action_id}")
        approval = g.approve(preview, "reviewer-1", "reviewer", f"I approve action {preview.action_id}")
        with self.assertRaises(ApprovalError):
            g.execute(preview, approval, lambda: "side effect", lambda result: True, executed_at=NOW - timedelta(seconds=1))

    def test_kill_switch_and_audit_failure_are_fail_closed(self):
        audit = AuditSink()
        g = gate()
        g.audit = audit
        preview = g.preview("REQ-1", "requester", "test.publish", {"env": "test"}, {"content": "hash"}, "rollback", "verify")
        approval = g.approve(preview, "reviewer-1", "reviewer", f"I approve action {preview.action_id}")
        g.kill_switch = True
        with self.assertRaises(ApprovalError):
            g.execute(preview, approval, lambda: "side effect", lambda result: True)
        g.kill_switch = False
        audit.available = False
        with self.assertRaises(ApprovalError):
            g.execute(preview, approval, lambda: "side effect", lambda result: True)

    def test_idempotent_execution_runs_once(self):
        g = gate()
        preview = g.preview("REQ-1", "requester", "test.publish", {"env": "test"}, {"content": "hash"}, "rollback", "verify")
        approval = g.approve(preview, "reviewer-1", "reviewer", f"I approve action {preview.action_id}")
        calls = []
        operation = lambda: calls.append("called") or "done"
        self.assertEqual(g.execute(preview, approval, operation, lambda result: result == "done", executed_at=NOW + timedelta(seconds=1)), "done")
        self.assertEqual(g.execute(preview, approval, operation, lambda result: result == "done", executed_at=NOW + timedelta(seconds=2)), "done")
        self.assertEqual(calls, ["called"])

    def test_revoked_approver_is_denied_at_execution(self):
        g = gate()
        preview = g.preview("REQ-1", "requester", "test.publish", {"env": "test"}, {"content": "hash"}, "rollback", "verify")
        approval = g.approve(preview, "reviewer-1", "reviewer", f"I approve action {preview.action_id}")
        g.allowlist["reviewer"]["test.publish"].clear()
        with self.assertRaises(ApprovalError):
            g.execute(preview, approval, lambda: "side effect", lambda result: True)

    def test_budget_pause_and_circuit_breaker_block_before_operation(self):
        definition = ActionDefinition.from_mapping({
            "action_type": "test.publish", "class": "L3", "owner": "owner",
            "allowed_approver_roles": ["reviewer"], "preview_required": True,
            "approval_ttl_seconds": 900, "idempotency_required": True,
            "rollback": "restore-snapshot", "verification": "check-result",
        })
        g = ApprovalGate({definition.action_type: definition}, "approval-policy-1.0.0",
                         {"reviewer": {"test.publish": {"reviewer-1"}}},
                         now=lambda: NOW, budget=ExecutionBudget(max_steps=1, max_cost=2))
        calls = []
        preview = g.preview("REQ-1", "requester", "test.publish", {"env": "test"}, {"content": "hash"}, "rollback", "verify")
        approval = g.approve(preview, "reviewer-1", "reviewer", f"I approve action {preview.action_id}")
        self.assertEqual(g.execute(preview, approval, lambda: calls.append("called") or "done",
                                   lambda result: True, executed_at=NOW + timedelta(seconds=1), estimated_cost=2), "done")
        second = g.preview("REQ-2", "requester", "test.publish", {"env": "test"}, {"content": "hash2"}, "rollback", "verify")
        second_approval = g.approve(second, "reviewer-1", "reviewer", f"I approve action {second.action_id}")
        with self.assertRaises(ApprovalError):
            g.execute(second, second_approval, lambda: calls.append("bad"), lambda result: True, executed_at=NOW + timedelta(seconds=2))
        g.pause("operator review")
        with self.assertRaises(ApprovalError):
            g.execute(second, second_approval, lambda: calls.append("bad"), lambda result: True)
        g.trip_circuit_breaker("emergency stop")
        self.assertEqual(calls, ["called"])


if __name__ == "__main__":
    unittest.main()
