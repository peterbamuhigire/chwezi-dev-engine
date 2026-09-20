"""Build and verify a hash-manifested portable solution-selection bundle."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

FILES = [
    "schemas/solution-decision.schema.json",
    "tools/solution_decision.py",
    "tools/solution_review.py",
    "tools/solution_debt.py",
    "tools/solution_mode.py",
    "tools/solution_evidence.py",
    "tools/solution_mcp_facade.py",
    "tools/adapter_lifecycle.py",
    "tools/adapters/solution-selection/codex.json",
    "tools/adapters/solution-selection/claude.json",
]


def manifest(root: Path) -> dict:
    entries = []
    for relative in FILES:
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        entries.append({"path": relative, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return {"schema_version": 1, "bundle": "solution-selection", "files": entries}


def build(root: Path, out: Path) -> dict:
    payload = manifest(root)
    out.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(out, "w", compression=ZIP_DEFLATED) as archive:
        for entry in payload["files"]:
            archive.write(root / entry["path"], entry["path"])
        archive.writestr("manifest.json", json.dumps(payload, indent=2) + "\n")
    return payload


def verify(bundle: Path) -> dict:
    with ZipFile(bundle) as archive:
        payload = json.loads(archive.read("manifest.json").decode("utf-8"))
        errors = []
        for entry in payload.get("files", []):
            try:
                actual = hashlib.sha256(archive.read(entry["path"])).hexdigest()
            except KeyError:
                errors.append(f"missing {entry.get('path')}")
                continue
            if actual != entry.get("sha256"):
                errors.append(f"hash mismatch {entry.get('path')}")
    return {"status": "FAIL" if errors else "PASS", "errors": errors, "file_count": len(payload.get("files", []))}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("path", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    if args.command == "build":
        result = {"status": "PASS", "file_count": len(build(args.root.resolve(), args.path.resolve())["files"]), "bundle": str(args.path)}
    else:
        result = verify(args.path.resolve())
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
