#!/usr/bin/env python3
"""Verify that a diagram's source citations exist at a pinned Git revision.

Input: any JSON document carrying `meta.repository.revision` (a full 40-hex SHA)
and a `sources` list of objects with `path`, `line` and optional `end_line`.

Failure codes:
  evidence/invalid-document     not JSON, or `meta.repository.revision` / `sources` missing
  evidence/revision-not-full    revision is not a full 40-hex SHA
  evidence/repo-root-not-toplevel  --repo-root is not the Git top level
  evidence/revision-unknown     the revision is not in the repository
  evidence/path-escape          absolute path, backslash, `.`/`..` segment, or a path into `.git`
  evidence/missing-at-revision  the file does not exist at the revision
  evidence/line-out-of-range    `line`/`end_line` missing, reversed or beyond the file

A verified citation proves the lines existed at that commit. It does not prove they
support the claim; a reviewer still reads them.

Standard library only; Git is read with `git --no-replace-objects cat-file --batch`.
Exit status: 0 all citations verified, 1 findings, 2 usage error.

Usage:
  python -X utf8 verify_diagram_evidence.py --repo-root DIR MODEL.json [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
WINDOWS_DRIVE = re.compile(r"^[A-Za-z]:")


def finding(code: str, index: int | None, message: str) -> dict:
    return {"code": code, "source": index, "message": message}


def path_problem(path: object) -> str | None:
    if not isinstance(path, str) or not path:
        return "path must be a non-empty string"
    if "\\" in path:
        return "backslash in path; use forward slashes"
    if path.startswith("/") or WINDOWS_DRIVE.match(path):
        return "absolute path"
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts):
        return "empty, '.' or '..' segment"
    if parts[0] == ".git":
        return "path into .git"
    return None


class BatchReader:
    """Reads blobs at a revision through one `git cat-file --batch` process."""

    def __init__(self, repo_root: Path):
        self.proc = subprocess.Popen(
            ["git", "--no-replace-objects", "-C", str(repo_root), "cat-file", "--batch"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

    def read(self, spec: str) -> tuple[str, bytes | None]:
        assert self.proc.stdin and self.proc.stdout
        self.proc.stdin.write(spec.encode("utf-8") + b"\n")
        self.proc.stdin.flush()
        header = self.proc.stdout.readline().decode("utf-8", errors="replace").rstrip("\n")
        if header.endswith(" missing") or header.endswith(" ambiguous"):
            return "missing", None
        parts = header.split()
        if len(parts) != 3:
            return "missing", None
        obj_type, size = parts[1], int(parts[2])
        data = self.proc.stdout.read(size)
        self.proc.stdout.read(1)  # trailing newline
        return obj_type, data

    def close(self) -> None:
        if self.proc.stdin:
            self.proc.stdin.close()
        self.proc.wait()


def line_total(data: bytes) -> int:
    if not data:
        return 0
    return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def git_toplevel(repo_root: Path) -> Path | None:
    res = subprocess.run(["git", "-C", str(repo_root), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if res.returncode != 0:
        return None
    return Path(res.stdout.strip())


def verify(document: object, repo_root: Path) -> list[dict]:
    if not isinstance(document, dict):
        return [finding("evidence/invalid-document", None, "document must be a JSON object")]
    revision = (((document.get("meta") or {}).get("repository") or {}).get("revision"))
    sources = document.get("sources")
    if not isinstance(revision, str) or not isinstance(sources, list):
        return [finding("evidence/invalid-document", None, "needs meta.repository.revision and a sources list")]
    if not FULL_SHA.match(revision):
        return [finding("evidence/revision-not-full", None, f"revision {revision!r} is not a full 40-hex SHA")]

    top = git_toplevel(repo_root)
    if top is None or os.path.normcase(str(top.resolve())) != os.path.normcase(str(repo_root.resolve())):
        return [finding("evidence/repo-root-not-toplevel", None, f"{repo_root} is not the Git top level")]

    reader = BatchReader(repo_root)
    findings: list[dict] = []
    try:
        kind, _ = reader.read(f"{revision}^{{commit}}")
        if kind != "commit":
            return [finding("evidence/revision-unknown", None, f"revision {revision} is not a commit in {repo_root}")]
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                findings.append(finding("evidence/invalid-document", index, "source must be an object"))
                continue
            path = source.get("path")
            problem = path_problem(path)
            if problem:
                findings.append(finding("evidence/path-escape", index, f"{path!r}: {problem}"))
                continue
            obj_type, data = reader.read(f"{revision}:{path}")
            if obj_type != "blob" or data is None:
                findings.append(finding("evidence/missing-at-revision", index, f"{path} not found as a file at {revision[:12]}"))
                continue
            total = line_total(data)
            line = source.get("line")
            end_line = source.get("end_line", line)
            if (
                not isinstance(line, int)
                or not isinstance(end_line, int)
                or isinstance(line, bool)
                or line < 1
                or end_line < line
                or end_line > total
            ):
                findings.append(finding("evidence/line-out-of-range", index, f"{path}: lines {line}-{end_line} outside 1..{total}"))
    finally:
        reader.close()
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Verify diagram source citations at a pinned revision.")
    ap.add_argument("model", type=Path)
    ap.add_argument("--repo-root", type=Path, required=True, help="Git top level of the repository the model cites.")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        document = json.loads(args.model.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"usage error: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        document = None
        findings = [finding("evidence/invalid-document", None, str(exc))]
    else:
        if not args.repo_root.is_dir():
            print(f"usage error: repo root not found: {args.repo_root}", file=sys.stderr)
            return 2
        findings = verify(document, args.repo_root)
    count = len(document.get("sources", [])) if isinstance(document, dict) and isinstance(document.get("sources"), list) else 0
    if args.json:
        print(json.dumps({"status": "FAIL" if findings else "PASS", "sources": count, "findings": findings}, indent=2))
    else:
        for f in findings:
            where = f"source {f['source']}" if f["source"] is not None else "document"
            print(f"{f['code']}: {where}: {f['message']}")
        print(f"verify-diagram-evidence: {'FAIL' if findings else 'PASS'} ({count} source(s), {len(findings)} finding(s))")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
