"""Validate and inspect versioned engineering solution decisions.

The validator checks evidence shape and repository scope. It does not infer
whether an engineer understood the code or whether a chosen option is wise.
Missing or changed evidence is reported explicitly and blocks a PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
OPTION_KINDS = {
    "no_change",
    "existing_capability",
    "stdlib",
    "native_platform",
    "installed_dependency",
    "new_dependency",
    "original_implementation",
}
EVIDENCE_KINDS = {"repository", "test", "benchmark", "source", "review", "runtime"}
EVIDENCE_STATUSES = {"verified", "not_assessed"}
PATH_RE = re.compile(r"^[^/\\][^:]*$")


def _error(errors: list[str], message: str) -> None:
    errors.append(message)


def _relative_path(value: Any, field: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value or not PATH_RE.fullmatch(value):
        _error(errors, f"{field} must be a repository-relative path")
        return None
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        _error(errors, f"{field} escapes the repository")
        return None
    return path


def compute_scope_hash(root: Path, files: list[str]) -> str:
    """Hash relative file names and bytes in deterministic order."""
    digest = hashlib.sha256()
    for name in sorted(files):
        path = root / Path(name)
        digest.update(name.replace("\\", "/").encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
        digest.update(b"\n")
    return digest.hexdigest()


def validate_record(record: Any, root: Path) -> dict[str, Any]:
    errors: list[str] = []
    unassessed: list[str] = []
    if not isinstance(record, dict):
        return {"status": "FAIL", "errors": ["record must be a JSON object"], "unassessed": []}
    if record.get("schema_version") != SCHEMA_VERSION:
        _error(errors, f"schema_version must be {SCHEMA_VERSION}")
    decision_id = record.get("decision_id")
    if not isinstance(decision_id, str) or not re.fullmatch(r"SD-[A-Z0-9][A-Z0-9._-]{2,63}", decision_id):
        _error(errors, "decision_id must match SD-<stable identifier>")

    scope = record.get("scope")
    if not isinstance(scope, dict):
        _error(errors, "scope is required")
        scope = {}
    scope_root = _relative_path(scope.get("root"), "scope.root", errors)
    files = scope.get("files")
    if not isinstance(files, list) or not files:
        _error(errors, "scope.files must contain at least one path")
        files = []
    safe_files: list[str] = []
    for index, value in enumerate(files):
        path = _relative_path(value, f"scope.files[{index}]", errors)
        if path is not None:
            safe_files.append(path.as_posix())
            if not (root / path).is_file():
                _error(errors, f"scope file does not exist: {path.as_posix()}")
    expected_hash = scope.get("sha256")
    if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
        _error(errors, "scope.sha256 must be a lowercase SHA-256 digest")
    elif safe_files and all((root / Path(name)).is_file() for name in safe_files):
        actual_hash = compute_scope_hash(root, safe_files)
        if actual_hash != expected_hash:
            _error(errors, "scope.sha256 does not match the selected files")
    if scope_root is None:
        pass

    context = record.get("context")
    if not isinstance(context, dict):
        _error(errors, "context is required")
    else:
        if not isinstance(context.get("problem"), str) or len(context["problem"].strip()) < 20:
            _error(errors, "context.problem must explain the problem in at least 20 characters")
        for field in ("requirements", "invariants"):
            values = context.get(field)
            if not isinstance(values, list) or not values or any(not isinstance(v, str) or len(v.strip()) < 3 for v in values):
                _error(errors, f"context.{field} must contain non-empty statements")

    options = record.get("options")
    if not isinstance(options, list) or len(options) < 2:
        _error(errors, "at least two solution options are required")
        options = []
    kinds: set[str] = set()
    for index, option in enumerate(options):
        if not isinstance(option, dict):
            _error(errors, f"options[{index}] must be an object")
            continue
        kind = option.get("kind")
        kinds.add(kind)
        if kind not in OPTION_KINDS:
            _error(errors, f"options[{index}].kind is unsupported")
        for field in ("description", "reason"):
            if not isinstance(option.get(field), str) or len(option[field].strip()) < 3:
                _error(errors, f"options[{index}].{field} is required")
    selected = record.get("selected_option")
    if not isinstance(selected, str) or selected not in kinds:
        _error(errors, "selected_option must name one of the considered option kinds")

    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        _error(errors, "at least one evidence record is required")
        evidence = []
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            _error(errors, f"evidence[{index}] must be an object")
            continue
        if item.get("kind") not in EVIDENCE_KINDS:
            _error(errors, f"evidence[{index}].kind is unsupported")
        if item.get("status") not in EVIDENCE_STATUSES:
            _error(errors, f"evidence[{index}].status is unsupported")
        if item.get("status") == "not_assessed":
            unassessed.append(f"evidence[{index}]")
        _relative_path(item.get("path"), f"evidence[{index}].path", errors)
        if isinstance(item.get("path"), str):
            path = _relative_path(item["path"], f"evidence[{index}].path", [])
            if path is not None and not (root / path).exists():
                _error(errors, f"evidence path does not exist: {path.as_posix()}")

    risk = record.get("risk")
    if not isinstance(risk, dict) or risk.get("tier") not in {"low", "medium", "high", "critical"}:
        _error(errors, "risk.tier must be low, medium, high, or critical")
    else:
        for field in ("security_boundary", "data_mutation", "money_or_ledger"):
            if not isinstance(risk.get(field), bool):
                _error(errors, f"risk.{field} must be boolean")
        if risk["tier"] in {"high", "critical"} and not any(item.get("kind") in {"test", "review"} and item.get("status") == "verified" for item in evidence if isinstance(item, dict)):
            _error(errors, "high or critical decisions require verified test or review evidence")

    exception = record.get("exception")
    if exception is not None:
        if not isinstance(exception, dict):
            _error(errors, "exception must be an object or null")
        else:
            for field in ("reason", "review_trigger", "expires"):
                if not isinstance(exception.get(field), str) or not exception[field].strip():
                    _error(errors, f"exception.{field} is required")
            if isinstance(exception.get("expires"), str):
                try:
                    if date.fromisoformat(exception["expires"]) < date.today():
                        _error(errors, "exception.expires is in the past")
                except ValueError:
                    _error(errors, "exception.expires must be an ISO date")

    tests = record.get("tests")
    if not isinstance(tests, dict):
        _error(errors, "tests is required")
    else:
        for field in ("required", "negative_cases"):
            values = tests.get(field)
            if not isinstance(values, list) or not values or any(not isinstance(v, str) or len(v.strip()) < 3 for v in values):
                _error(errors, f"tests.{field} must contain non-empty cases")
    status = "FAIL" if errors else ("NOT_ASSESSED" if unassessed else "PASS")
    return {"status": status, "errors": errors, "unassessed": unassessed, "decision_id": decision_id}


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "inspect"))
    parser.add_argument("record", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    try:
        record = _load(args.record)
    except (OSError, json.JSONDecodeError) as exc:
        result = {"status": "FAIL", "errors": [f"cannot read decision record: {exc}"], "unassessed": []}
    else:
        result = validate_record(record, args.root.resolve())
        if args.command == "inspect":
            result["selected_option"] = record.get("selected_option") if isinstance(record, dict) else None
            result["evidence_count"] = len(record.get("evidence", [])) if isinstance(record, dict) and isinstance(record.get("evidence"), list) else 0
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"solution-decision: {result['status']}")
        for item in result.get("errors", []):
            print(f"ERROR: {item}")
        for item in result.get("unassessed", []):
            print(f"NOT_ASSESSED: {item}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
