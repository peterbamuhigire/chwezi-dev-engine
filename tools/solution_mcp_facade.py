"""Dependency-free, read-only JSON-lines facade for solution-selection tools.

This is an optional transport for hosts that can launch a local process. It is
not an MCP SDK implementation and makes no claim that a host will activate it.
The same bounded handlers remain available as ordinary repository commands.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tools.solution_decision import validate_record


TOOLS = [
    {"name": "list_tools", "read_only": True},
    {"name": "inspect_decision", "read_only": True},
    {"name": "validate_decision", "read_only": True},
]


def _safe(root: Path, value: Any) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError("path is required")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("path must stay inside the repository root")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("path escapes repository root")
    return resolved


def dispatch(request: Any, root: Path) -> dict[str, Any]:
    if not isinstance(request, dict):
        return {"ok": False, "error": "request must be an object"}
    method = request.get("method")
    if method == "list_tools":
        return {"ok": True, "tools": TOOLS, "read_only": True}
    try:
        path = _safe(root, request.get("path"))
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}
    if not path.is_file():
        return {"ok": False, "error": "resource does not exist"}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"ok": False, "error": str(exc)}
    if method == "inspect_decision":
        return {"ok": True, "decision_id": payload.get("decision_id"), "selected_option": payload.get("selected_option"), "evidence_count": len(payload.get("evidence", [])) if isinstance(payload, dict) else 0, "read_only": True}
    if method == "validate_decision":
        return {"ok": True, "result": validate_record(payload, root), "read_only": True}
    return {"ok": False, "error": "unknown method"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    exit_code = 0
    for line in __import__("sys").stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError as exc:
            response = {"ok": False, "error": str(exc)}
        else:
            response = dispatch(request, args.root.resolve())
        print(json.dumps(response), flush=True)
        exit_code = 0 if response.get("ok") else 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
