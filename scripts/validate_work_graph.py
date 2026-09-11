#!/usr/bin/env python3
"""Validate tracer-bullet work graphs and print the runnable frontier."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

REQUIRED = {"id", "outcome", "failure_consequence", "owner", "write_set", "blocked_by", "acceptance", "status", "evidence"}
STATUSES = {"pending", "in_progress", "blocked", "complete", "failed"}


def validate(data: object) -> tuple[list[str], list[str]]:
    findings: list[str] = []
    if not isinstance(data, dict) or not isinstance(data.get("nodes"), list):
        return ["root must contain a nodes list"], []
    nodes = data["nodes"]
    ids: list[str] = []
    by_id: dict[str, dict] = {}
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            findings.append(f"node {index} must be a mapping")
            continue
        missing = REQUIRED - set(node)
        if missing:
            findings.append(f"node {index} missing: {', '.join(sorted(missing))}")
            continue
        node_id = node["id"]
        if not isinstance(node_id, str) or not node_id.strip():
            findings.append(f"node {index} has invalid id")
            continue
        if node_id in by_id:
            findings.append(f"duplicate node id: {node_id}")
        ids.append(node_id)
        by_id[node_id] = node
        if node["status"] not in STATUSES:
            findings.append(f"{node_id}: unsupported status {node['status']!r}")
        for field in ("outcome", "failure_consequence", "owner"):
            if not isinstance(node[field], str) or not node[field].strip():
                findings.append(f"{node_id}: {field} must be non-empty text")
        for field in ("write_set", "blocked_by", "acceptance", "evidence"):
            if not isinstance(node[field], list):
                findings.append(f"{node_id}: {field} must be a list")
        if node["status"] == "complete" and not node["evidence"]:
            findings.append(f"{node_id}: complete node requires evidence")

    known = set(ids)
    for node_id, node in by_id.items():
        if not isinstance(node.get("blocked_by"), list):
            continue
        for dependency in node["blocked_by"]:
            if dependency not in known:
                findings.append(f"{node_id}: unknown dependency {dependency!r}")
            if dependency == node_id:
                findings.append(f"{node_id}: self dependency")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visiting:
            findings.append(f"cycle detected at {node_id}")
            return
        if node_id in visited or node_id not in by_id:
            return
        visiting.add(node_id)
        dependencies = by_id[node_id].get("blocked_by", [])
        if isinstance(dependencies, list):
            for dependency in dependencies:
                if isinstance(dependency, str):
                    visit(dependency)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in ids:
        visit(node_id)

    frontier = []
    if not findings:
        for node_id, node in by_id.items():
            if node["status"] != "pending":
                continue
            if all(by_id[dependency]["status"] == "complete" for dependency in node["blocked_by"]):
                frontier.append(node_id)
    return sorted(set(findings)), frontier


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path)
    args = parser.parse_args()
    try:
        data = yaml.safe_load(args.graph.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f"[FAIL] cannot read graph: {exc}")
        return 1
    findings, frontier = validate(data)
    for finding in findings:
        print(f"[FAIL] {finding}")
    if findings:
        print(f"work-graph: findings={len(findings)}")
        return 1
    print(f"work-graph: nodes={len(data['nodes'])} findings=0 frontier={','.join(frontier) or '-'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
