#!/usr/bin/env python3
"""Validate the shared twelve-engine control-plane registry."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine_roots  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "engine-control-plane.json"
EXPECTED_ENGINES = {"srs", "business-plan", "website", "social-media", "linux", "proposal", "accounting", "design", "digital-research", "chwezi-dev-engine", "windows-admin", "political"}
REQUIRED_KEYS = {"id", "domain", "router", "adoption_doc", "agents", "commands", "hooks", "evidence"}
ALLOWED_HOOKS = {"preflight", "context", "before_write", "after_write", "release", "stop"}
# Current directory name of each engine; former names are in engine_roots.ENGINE_DIR_ALIASES.
ENGINE_DIRS = {engine_id: names[0] for engine_id, names in engine_roots.ENGINE_DIR_ALIASES.items()}


def engine_candidates(workspace_root, engine_id: str) -> list[Path]:
    """Resolve an explicit override or the candidates under one or more parent folders.

    An override is authoritative: falling back from an invalid override could
    silently validate a different checkout. ``workspace_root`` may be one parent
    folder or several; unrelated home-directory copies are never searched. The
    engine running this validator counts as the Dev Engine checkout when no
    parent folder holds one.
    """
    if engine_id not in ENGINE_DIRS:
        return []
    found = engine_roots.candidates(engine_id, workspace_root)
    if engine_id == "chwezi-dev-engine" and engine_roots.env_override(engine_id) is None and ROOT not in found:
        found.append(ROOT)
    return found


def resolve_engine_dir(workspace_root, engine_id: str, router: str, adoption_doc: str) -> Path | None:
    for candidate in engine_candidates(workspace_root, engine_id):
        try:
            if candidate.is_dir():
                # Follow an explicitly selected checkout link, but contracts
                # themselves must remain inside that checkout after resolution.
                checkout = candidate.resolve(strict=True)
                for relative in (router, adoption_doc):
                    target = (checkout / relative).resolve(strict=True)
                    if not target.is_relative_to(checkout) or not target.is_file():
                        return None
                return candidate
        except (OSError, RuntimeError):
            # Missing, inaccessible or looping links fail this selected scope.
            return None
    return None


def safe_relative_path(value: object) -> bool:
    """Reject absolute and parent-traversal paths on every supported OS."""
    if not isinstance(value, str) or not value.strip():
        return False
    normalised = value.replace("\\", "/")
    return not (
        normalised.startswith("/")
        or ":" in normalised
        or ".." in normalised.split("/")
    )


def validate_registry(workspace_root=None, engine_ids: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    if engine_ids is not None and (not engine_ids or not engine_ids <= EXPECTED_ENGINES):
        return ["selected engine IDs must be a non-empty subset of the registry"]
    try:
        payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read registry: {exc}"]
    if not isinstance(payload, dict):
        return ["registry must be an object"]
    if type(payload.get("schema_version")) is not int or payload["schema_version"] != 1:
        errors.append("schema_version must be 1")
    engines = payload.get("engines")
    if not isinstance(engines, list):
        return ["engines must be a list"]
    ids = [engine["id"] for engine in engines if isinstance(engine, dict) and isinstance(engine.get("id"), str)]
    if set(ids) != EXPECTED_ENGINES:
        errors.append(f"engine IDs must be exactly {sorted(EXPECTED_ENGINES)}; found {sorted(set(ids))}")
    if len(ids) != len(set(ids)):
        errors.append("engine IDs must be unique")
    for engine in engines:
        if not isinstance(engine, dict):
            errors.append("each engine entry must be an object")
            continue
        engine_id = engine.get("id")
        if not isinstance(engine_id, str) or engine_id not in EXPECTED_ENGINES:
            errors.append("engine id must be a recognised string")
            continue
        for key in sorted(REQUIRED_KEYS - set(engine)):
            errors.append(f"{engine_id}: missing {key}")
        for key in ("agents", "commands", "hooks", "evidence"):
            values = engine.get(key)
            if not isinstance(values, list) or not values or any(not isinstance(item, str) or not item.strip() for item in values):
                errors.append(f"{engine_id}: {key} must be a non-empty list of strings")
        paths_valid = True
        for key in ("router", "adoption_doc"):
            if not safe_relative_path(engine.get(key)):
                errors.append(f"{engine_id}: {key} must be a non-empty relative path without parent traversal")
                paths_valid = False
        hooks = engine.get("hooks", [])
        if isinstance(hooks, list):
            unknown = {hook for hook in hooks if isinstance(hook, str)} - ALLOWED_HOOKS
            if unknown:
                errors.append(f"{engine_id}: unsupported hooks {sorted(unknown)}")
        if engine_roots.normalise_roots(workspace_root) and paths_valid and (engine_ids is None or engine_id in engine_ids):
            engine_dir = resolve_engine_dir(
                workspace_root,
                engine_id,
                engine["router"],
                engine["adoption_doc"],
            )
            if engine_dir is None:
                candidates = ", ".join(str(path) for path in engine_candidates(workspace_root, engine_id))
                errors.append(f"{engine_id}: no candidate contains router and adoption document ({candidates})")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace-root",
        action="append",
        type=Path,
        help=f"Parent folder containing local engine directories; repeat for several. Falls back to ${engine_roots.ENV_ROOTS}. Without either, only the registry is checked.",
    )
    parser.add_argument("--engine", action="append", choices=sorted(EXPECTED_ENGINES), help="Limit installed-checkout checks to these IDs; registry shape is always checked in full")
    args = parser.parse_args()
    roots = engine_roots.normalise_roots([root.resolve() for root in args.workspace_root or []]) or engine_roots.roots_from_env()
    if args.engine and not roots:
        parser.error(f"--engine requires --workspace-root or ${engine_roots.ENV_ROOTS}")
    selected = set(args.engine) if args.engine else None
    errors = validate_registry(roots or None, selected)
    print("engine-control-plane-validator:")
    print(f"- registry: {REGISTRY}")
    print(f"- engines: {len(EXPECTED_ENGINES)}")
    print(f"- installed checkout scope: {', '.join(sorted(selected or EXPECTED_ENGINES)) if roots else 'NOT ASSESSED (registry-only check)'}")
    if roots:
        print(f"- parent folders searched: {', '.join(str(root) for root in roots)}")
    print(f"- findings: {len(errors)}")
    for error in errors:
        print(f"[FAIL] {error}")
    if not errors:
        print("PASS: control-plane registry is valid")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
