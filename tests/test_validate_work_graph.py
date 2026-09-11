import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate_work_graph.py"
SPEC = importlib.util.spec_from_file_location("work_graph", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def node(node_id, blocked_by=None, status="pending", evidence=None):
    return {
        "id": node_id,
        "outcome": f"Outcome {node_id}",
        "failure_consequence": "A user flow remains unsafe.",
        "owner": "owner",
        "write_set": [f"{node_id}.md"],
        "blocked_by": blocked_by or [],
        "acceptance": ["normal and failure checks"],
        "status": status,
        "evidence": evidence or [],
    }


def test_frontier_contains_only_unblocked_pending_nodes():
    data = {"nodes": [
        node("done", status="complete", evidence=["tests pass"]),
        node("ready", ["done"]),
        node("blocked", ["ready"]),
    ]}
    findings, frontier = MODULE.validate(data)
    assert findings == []
    assert frontier == ["ready"]


def test_cycle_and_unknown_dependency_fail():
    data = {"nodes": [node("a", ["b"]), node("b", ["a"]), node("c", ["missing"])]}
    findings, frontier = MODULE.validate(data)
    assert any("cycle detected" in finding for finding in findings)
    assert any("unknown dependency" in finding for finding in findings)
    assert frontier == []


def test_complete_without_evidence_fails():
    findings, _ = MODULE.validate({"nodes": [node("false-done", status="complete")]})
    assert any("requires evidence" in finding for finding in findings)


def test_missing_contract_field_fails():
    incomplete = node("incomplete")
    del incomplete["acceptance"]
    findings, _ = MODULE.validate({"nodes": [incomplete]})
    assert any("missing: acceptance" in finding for finding in findings)
