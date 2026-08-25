#!/usr/bin/env python3
"""Validate the shared eleven-engine control-plane registry."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "engine-control-plane.json"
EXPECTED_ENGINES = {"srs", "business-plan", "website", "social-media", "linux", "proposal", "accounting", "design", "digital-research", "skills-web-dev", "windows-admin"}
REQUIRED_KEYS = {"id", "domain", "router", "adoption_doc", "agents", "commands", "hooks", "evidence"}
ALLOWED_HOOKS = {"preflight", "context", "before_write", "after_write", "release", "stop"}
ENGINE_DIRS = {
    "srs": "srs-skills",
    "business-plan": "business-plan-skills",
    "website": "website-skills",
    "social-media": "social-media-skills",
    "linux": "linux-skills",
    "proposal": "proposal-skills",
    "accounting": "chwezi-accounting-doctrine",
    "design": "design-system-skills",
    "digital-research": "digital-research-skills",
    "digital-research": "digital-research-engine",
    "skills-web-dev": "skills-web-dev",
    "windows-admin": "windows-admin-engine-skills",
}


def engine_candidates(workspace_root: Path, engine_id: str) -> list[Path]:
    """Return current local candidates without requiring one checkout layout."""
    env_name = f"SKILL_ENGINE_ROOT_{engine_id.upper().replace('-', '_')}"
    candidates: list[Path] = []
    override = os.environ.get(env_name)
    if override:
        candidates.append(Path(override).expanduser())

    candidates.append(workspace_root / ENGINE_DIRS[engine_id])

    # The canonical finance checkout is maintained in source/repos on the
    # development machine, while the other engines normally sit under the
    # shared workspace root. Keep this as a fallback so the registry does not
    # validate an obsolete duplicate checkout.
    if engine_id == "accounting":
        candidates.append(Path.home() / "source" / "repos" / "chwezi-accounting-doctrine")

    unique: list[Path] = []
    for candidate in candidates:
        resolved = candidate.expanduser()
        if resolved not in unique:
            unique.append(resolved)
    return unique


def resolve_engine_dir(workspace_root: Path, engine_id: str, router: str, adoption_doc: str) -> Path | None:
    for candidate in engine_candidates(workspace_root, engine_id):
        if (candidate / router).is_file() and (candidate / adoption_doc).is_file():
            return candidate
    return None


def validate_registry(workspace_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read registry: {exc}"]
    if payload.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    engines = payload.get("engines")
    if not isinstance(engines, list):
        return ["engines must be a list"]
    ids = [engine.get("id") for engine in engines if isinstance(engine, dict)]
    if set(ids) != EXPECTED_ENGINES:
        errors.append(f"engine IDs must be exactly {sorted(EXPECTED_ENGINES)}; found {sorted(set(ids))}")
    if len(ids) != len(set(ids)):
        errors.append("engine IDs must be unique")
    for engine in engines:
        if not isinstance(engine, dict):
            errors.append("each engine entry must be an object")
            continue
        engine_id = engine.get("id", "<unknown>")
        for key in sorted(REQUIRED_KEYS - set(engine)):
            errors.append(f"{engine_id}: missing {key}")
        for key in ("agents", "commands", "hooks", "evidence"):
            values = engine.get(key)
            if not isinstance(values, list) or not values or any(not isinstance(item, str) or not item.strip() for item in values):
                errors.append(f"{engine_id}: {key} must be a non-empty list of strings")
        hooks = engine.get("hooks", [])
        if isinstance(hooks, list):
            unknown = set(hooks) - ALLOWED_HOOKS
            if unknown:
                errors.append(f"{engine_id}: unsupported hooks {sorted(unknown)}")
        if workspace_root is not None:
            if engine_id == "skills-web-dev":
                engine_dir = ROOT
            else:
                engine_dir = resolve_engine_dir(
                    workspace_root,
                    engine_id,
                    str(engine.get("router", "")),
                    str(engine.get("adoption_doc", "")),
                )
            if engine_dir is None:
                candidates = ", ".join(str(path) for path in engine_candidates(workspace_root, engine_id))
                errors.append(f"{engine_id}: no candidate contains router and adoption document ({candidates})")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, help="Optional parent containing the eleven local engine directories")
    args = parser.parse_args()
    errors = validate_registry(args.workspace_root.resolve() if args.workspace_root else None)
    print("engine-control-plane-validator:")
    print(f"- registry: {REGISTRY}")
    print(f"- engines: {len(EXPECTED_ENGINES)}")
    print(f"- findings: {len(errors)}")
    for error in errors:
        print(f"[FAIL] {error}")
    if not errors:
        print("PASS: control-plane registry is valid")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
