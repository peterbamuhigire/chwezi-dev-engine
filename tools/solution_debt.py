"""List and export scoped solution-debt markers without changing source files."""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

EXCLUDED_PARTS = {".git", ".venv", "node_modules", "vendor", "dist", "build", "generated", "__pycache__"}
CODE_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".php", ".java", ".go", ".rb", ".rs", ".sql", ".yaml", ".yml", ".json"}
MARKER_RE = re.compile(r"SOLUTION_DEBT:\s*(?P<body>.+)$", re.IGNORECASE)


def _parse_fields(body: str) -> dict[str, str]:
    return {key.lower(): value.strip().strip('"\'') for key, value in re.findall(r"(owner|trigger|expires|reason)\s*=\s*([^;]+)", body, re.IGNORECASE)}


def scan(root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in CODE_SUFFIXES:
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for number, line in enumerate(lines, 1):
            match = MARKER_RE.search(line)
            if not match:
                continue
            fields = _parse_fields(match.group("body"))
            missing = sorted({"owner", "trigger", "expires", "reason"} - set(fields))
            expired = False
            if "expires" in fields:
                try:
                    expired = date.fromisoformat(fields["expires"]) < date.today()
                except ValueError:
                    missing.append("valid-expires")
            records.append({"path": relative.as_posix(), "line": number, "marker": line.strip(), "fields": fields, "missing": missing, "expired": expired})
    structured = root / ".kaizen" / "solution-debt.json"
    if structured.is_file():
        try:
            payload = json.loads(structured.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            records.append({"path": ".kaizen/solution-debt.json", "line": 1, "marker": "structured ledger", "fields": {}, "missing": [f"invalid-json: {exc}"], "expired": False})
        else:
            for index, item in enumerate(payload.get("records", []) if isinstance(payload, dict) else [], 1):
                if isinstance(item, dict):
                    item = dict(item)
                    item.setdefault("path", ".kaizen/solution-debt.json")
                    item.setdefault("line", index)
                    item.setdefault("missing", [])
                    item.setdefault("expired", False)
                    records.append(item)
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("list", "export"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    records = scan(args.root.resolve())
    payload = {"status": "PASS" if not any(item.get("missing") or item.get("expired") for item in records) else "FAIL", "records": records, "read_only": args.command == "list"}
    if args.command == "export":
        if args.out is None:
            parser.error("export requires --out")
        out = args.out.resolve()
        if out == args.root.resolve() or args.root.resolve() not in out.parents:
            parser.error("--out must be inside --root")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        payload["read_only"] = False
    if args.as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"solution-debt: {payload['status']} ({len(records)} records)")
        for item in records:
            state = "EXPIRED" if item.get("expired") else ("INCOMPLETE" if item.get("missing") else "OPEN")
            print(f"{state} {item.get('path')}:{item.get('line')}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
