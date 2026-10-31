#!/usr/bin/env python3
"""Validate the eleven domain approval adapters against the shared contract."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine_roots  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
# The eleven engines that carry an approval adapter. The private political engine does not.
ADAPTER_ENGINES = tuple(sorted(engine_id for engine_id in engine_roots.ENGINE_DIR_ALIASES if engine_id != "political"))
REQUIRED = {"action_type", "class", "side_effect", "owner", "allowed_approver_roles",
            "requires_dual_approval", "preview_required", "approval_ttl_seconds",
            "idempotency_required", "rollback", "verification", "sensitive_fields"}


def validate_adapter(path: Path, expected_engine: str) -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{expected_engine}: cannot read {path}: {exc}"]
    if payload.get("schema_version") != 1:
        errors.append(f"{expected_engine}: schema_version must be 1")
    if payload.get("engine") != expected_engine:
        errors.append(f"{expected_engine}: engine must be {expected_engine}")
    actions = payload.get("actions")
    if not isinstance(actions, list) or not actions:
        return errors + [f"{expected_engine}: actions must be a non-empty list"]
    seen: set[str] = set()
    for index, action in enumerate(actions):
        label = f"{expected_engine}[{index}]"
        if not isinstance(action, dict):
            errors.append(f"{label}: action must be an object")
            continue
        missing = REQUIRED - set(action)
        errors.extend(f"{label}: missing {key}" for key in sorted(missing))
        action_type = action.get("action_type")
        if action_type in seen:
            errors.append(f"{label}: duplicate action_type {action_type}")
        seen.add(action_type)
        if action.get("class") not in {"L0", "L1", "L2", "L3"}:
            errors.append(f"{label}: invalid class")
        if action.get("class") in {"L2", "L3"}:
            if action.get("preview_required") is not True:
                errors.append(f"{label}: L2/L3 must require preview")
            if action.get("approval_ttl_seconds", 0) <= 0:
                errors.append(f"{label}: L2/L3 must have positive approval TTL")
            if not action.get("idempotency_required"):
                errors.append(f"{label}: L2/L3 must require idempotency")
            if not action.get("rollback") or not action.get("verification"):
                errors.append(f"{label}: L2/L3 must declare rollback and verification")
        if not isinstance(action.get("allowed_approver_roles"), list) or not action["allowed_approver_roles"]:
            errors.append(f"{label}: allowed_approver_roles must be non-empty")
        if not isinstance(action.get("sensitive_fields"), list):
            errors.append(f"{label}: sensitive_fields must be a list")
    return errors


def locate(engine_id: str, roots: list[Path], overrides: dict[str, Path]) -> tuple[Path | None, list[Path]]:
    """Find an engine checkout: explicit id=path override, then this checkout, then the parent folders."""
    if engine_id in overrides:
        return overrides[engine_id], [overrides[engine_id]]
    if engine_id == "chwezi-dev-engine":
        return ROOT, [ROOT]
    tried = engine_roots.candidates(engine_id, roots)
    return engine_roots.first_existing(tried), tried


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-root", action="append", default=[],
                        help="Checkout override for one engine, in id=path form")
    parser.add_argument(
        "--workspace-root",
        action="append",
        type=Path,
        help=f"Parent folder containing local engine directories; repeat for several. Falls back to ${engine_roots.ENV_ROOTS}, then to the parent of this checkout.",
    )
    args = parser.parse_args()
    overrides: dict[str, Path] = {}
    for override in args.engine_root:
        if "=" not in override:
            parser.error("--engine-root must be id=path")
        engine, path = override.split("=", 1)
        if engine not in ADAPTER_ENGINES:
            parser.error(f"unknown engine id {engine!r}")
        overrides[engine] = Path(path)
    roots = engine_roots.normalise_roots(args.workspace_root) or engine_roots.roots_from_env() or [ROOT.parent]
    errors: list[str] = []
    for engine in ADAPTER_ENGINES:
        directory, tried = locate(engine, roots, overrides)
        if directory is None:
            errors.append(f"{engine}: no checkout found (looked for {', '.join(path.name for path in tried)} under the given parent folders)")
            continue
        path = directory / "docs" / "approval-adapter.json"
        if not path.is_file():
            errors.append(f"{engine}: missing docs/approval-adapter.json in the {directory.name} checkout")
            continue
        errors.extend(validate_adapter(path, engine))
    print("approval-adapter-validator:")
    print(f"- adapters: {len(ADAPTER_ENGINES)}")
    print(f"- findings: {len(errors)}")
    for error in errors:
        print(f"[FAIL] {error}")
    if not errors:
        print("PASS: all approval adapters satisfy the shared contract")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
