"""Manage repository/session-scoped advisory solution-selection modes."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MODES = {"advisory", "enforced-review", "off"}
SCHEMA_VERSION = 1


def _repo_id(root: Path) -> str:
    return hashlib.sha256(str(root.resolve()).encode("utf-8")).hexdigest()


def _path(root: Path) -> Path:
    return root / ".kaizen" / "solution-mode.json"


def _load(root: Path) -> tuple[dict[str, Any] | None, str | None]:
    path = _path(root)
    if not path.exists():
        return {"schema_version": SCHEMA_VERSION, "repositories": {}}, None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"cannot read mode state: {exc}"
    if not isinstance(payload, dict) or payload.get("schema_version") != SCHEMA_VERSION or not isinstance(payload.get("repositories"), dict):
        return None, "mode state has an unsupported schema"
    return payload, None


def _save(root: Path, payload: dict[str, Any]) -> None:
    target = _path(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix="solution-mode-", suffix=".tmp", dir=target.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, target)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def get_mode(root: Path, session: str) -> dict[str, Any]:
    payload, error = _load(root)
    if error:
        return {"status": "NOT_ASSESSED", "mode": None, "error": error}
    entries = payload["repositories"].get(_repo_id(root), {})
    entry = entries.get(session) or entries.get("*")
    return {"status": "PASS", "mode": entry.get("mode", "advisory") if entry else "advisory", "scope": "session" if session in entries else ("repository" if "*" in entries else "default"), "session": session}


def set_mode(root: Path, mode: str, session: str) -> dict[str, Any]:
    if mode not in MODES:
        return {"status": "FAIL", "error": f"unsupported mode: {mode}"}
    payload, error = _load(root)
    if error:
        return {"status": "NOT_ASSESSED", "error": error}
    repo = payload["repositories"].setdefault(_repo_id(root), {})
    repo[session] = {"mode": mode, "updated_utc": datetime.now(timezone.utc).isoformat()}
    _save(root, payload)
    return get_mode(root, session)


def reset_mode(root: Path, session: str | None) -> dict[str, Any]:
    payload, error = _load(root)
    if error:
        return {"status": "NOT_ASSESSED", "error": error}
    repo_id = _repo_id(root)
    repo = payload["repositories"].get(repo_id, {})
    if session is None:
        payload["repositories"].pop(repo_id, None)
    else:
        repo.pop(session, None)
        if not repo:
            payload["repositories"].pop(repo_id, None)
    _save(root, payload)
    return {"status": "PASS", "mode": "advisory", "scope": "default", "session": session or "*"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("get", "set", "reset"))
    parser.add_argument("mode", nargs="?", choices=sorted(MODES))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--session", default=os.environ.get("SOLUTION_SESSION_ID", "local"))
    parser.add_argument("--all-sessions", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.command == "get":
        result = get_mode(root, args.session)
    elif args.command == "set":
        if args.mode is None:
            parser.error("set requires a mode")
        result = set_mode(root, args.mode, args.session)
    else:
        result = reset_mode(root, None if args.all_sessions else args.session)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
