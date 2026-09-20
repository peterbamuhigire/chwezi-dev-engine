"""Plan and safely apply a repository-scoped solution-selection adapter entry.

This tool never edits a host configuration unless ``apply`` is explicitly used.
It owns one namespaced JSON key, records a scoped backup, and refuses malformed
or unexpectedly changed configurations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OWNED_KEY = "chwezi_solution_selection"
ADAPTERS = {"codex", "claude"}


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _load(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"cannot read configuration: {exc}"
    if not isinstance(value, dict):
        return None, "configuration root must be a JSON object"
    return value, None


def desired(adapter: str) -> dict[str, Any]:
    if adapter not in ADAPTERS:
        raise ValueError(f"unsupported adapter: {adapter}")
    return {
        "schema_version": 1,
        "owner": "chwezi-skills-web-dev",
        "adapter": adapter,
        "enforcement": "instruction-only",
        "events": ["preflight", "context", "before_write", "after_write", "release", "stop"],
        "fallback": "repository command and CI gate",
    }


def plan(config: Path, adapter: str) -> dict[str, Any]:
    payload, error = _load(config)
    if error:
        return {"status": "NOT_ASSESSED", "error": error}
    existing = payload.get(OWNED_KEY)
    if existing is not None and (not isinstance(existing, dict) or existing.get("owner") != "chwezi-skills-web-dev"):
        return {"status": "FAIL", "error": f"{OWNED_KEY} exists but is not owned by this adapter"}
    target = desired(adapter)
    return {"status": "PASS", "config": str(config), "adapter": adapter, "before_hash": _hash(payload), "owned_before": existing, "owned_after": target, "changed": existing != target, "side_effect": False}


def _atomic_write(path: Path, payload: dict[str, Any]) -> None:
    handle, name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def apply(config: Path, adapter: str, backup_dir: Path) -> dict[str, Any]:
    proposal = plan(config, adapter)
    if proposal["status"] != "PASS":
        return proposal
    payload, _ = _load(config)
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = backup_dir / f"{config.stem}-{stamp}.json"
    backup.write_text(json.dumps({"config": str(config), "before_hash": proposal["before_hash"], "payload": payload}, indent=2) + "\n", encoding="utf-8")
    payload[OWNED_KEY] = proposal["owned_after"]
    _atomic_write(config, payload)
    after, error = _load(config)
    if error or after is None or after.get(OWNED_KEY) != proposal["owned_after"]:
        return {"status": "FAIL", "error": "post-write verification failed", "backup": str(backup)}
    return {"status": "PASS", "backup": str(backup), "before_hash": proposal["before_hash"], "after_hash": _hash(after), "side_effect": True}


def revert(config: Path, backup: Path) -> dict[str, Any]:
    payload, error = _load(config)
    if error:
        return {"status": "NOT_ASSESSED", "error": error}
    try:
        saved = json.loads(backup.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"status": "FAIL", "error": f"cannot read backup: {exc}"}
    original = saved.get("payload") if isinstance(saved, dict) else None
    if not isinstance(original, dict):
        return {"status": "FAIL", "error": "backup has no payload"}
    current_owned = payload.get(OWNED_KEY)
    saved_owned = original.get(OWNED_KEY)
    if current_owned is None or not isinstance(current_owned, dict) or current_owned.get("owner") != "chwezi-skills-web-dev":
        return {"status": "FAIL", "error": "current owned entry is absent or unexpectedly owned"}
    if current_owned == saved_owned:
        return {"status": "PASS", "changed": False, "side_effect": False}
    if saved_owned is None:
        payload.pop(OWNED_KEY, None)
    else:
        payload[OWNED_KEY] = saved_owned
    _atomic_write(config, payload)
    return {"status": "PASS", "changed": True, "side_effect": True}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("status", "plan", "apply", "revert"))
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--adapter", choices=sorted(ADAPTERS), default="codex")
    parser.add_argument("--backup-dir", type=Path, default=Path(".kaizen/adapter-backups"))
    parser.add_argument("--backup", type=Path)
    parser.add_argument("--apply", action="store_true", help="required for apply")
    args = parser.parse_args(argv)
    config = args.config.resolve()
    if args.command == "status":
        payload, error = _load(config)
        result = {"status": "NOT_ASSESSED", "error": error} if error else {"status": "PASS", "owned": payload.get(OWNED_KEY), "side_effect": False}
    elif args.command == "plan":
        result = plan(config, args.adapter)
    elif args.command == "apply":
        if not args.apply:
            parser.error("apply requires --apply")
        result = apply(config, args.adapter, args.backup_dir.resolve())
    else:
        if args.backup is None:
            parser.error("revert requires --backup")
        result = revert(config, args.backup.resolve())
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
