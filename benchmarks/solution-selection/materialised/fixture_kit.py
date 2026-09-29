"""Shared, stdlib-only helpers for the materialised solution-selection fixtures.

Every fixture folder ``Fxx/`` holds:

- ``fixture.json``  - small run manifest (``id``, ``language``, ``public_test_command``,
  ``requires`` e.g. ``["python"]`` or ``["python", "node"]``);
- ``starter/``      - the repository the agent receives (becomes the baseline commit);
- ``public_tests/`` - tests the agent can see; copied into the workspace at ``public_tests/``;
- ``checker.py``    - deterministic, stdlib-only checker that runs the produced code against
  adversarial input: ``python checker.py <workspace> [--withheld <dir>]`` prints one JSON object
  ``{"fixture", "status", "checks": [{"id", "passed", "detail"}]}`` and exits 0 (PASS),
  1 (FAIL) or 2 (NOT_ASSESSED, e.g. a required runtime such as node is missing);
- ``reference_good/`` and ``reference_bad/`` - overlays applied on top of the workspace
  (same relative paths). An optional ``.overlay-delete`` file lists workspace paths to remove.

Withheld tests live outside version control in ``benchmarks-private/solution-selection/Fxx/``
(the folder carries its own ``.gitignore`` of ``*``); only ``hidden_manifest_hash`` is committed.

Commands (run from the dev engine root):

    python -X utf8 benchmarks/solution-selection/materialised/fixture_kit.py compose F07 --overlay good --dest <dir>
    python -X utf8 benchmarks/solution-selection/materialised/fixture_kit.py commit F07
    python -X utf8 benchmarks/solution-selection/materialised/fixture_kit.py stamp [--check]

``stamp`` recomputes ``initial_commit`` (a deterministic git commit of starter + public tests
with a fixed identity and date) and ``hidden_manifest_hash`` and writes them, with
``materialisation_status: MATERIALISED``, into ``fixtures.json``. ``--check`` only compares.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUITE = HERE.parent
ENGINE_ROOT = SUITE.parent.parent
FIXTURES_JSON = SUITE / "fixtures.json"
PRIVATE_ROOT = ENGINE_ROOT / "benchmarks-private" / "solution-selection"
REQUIRED_PARTS = ("fixture.json", "starter", "public_tests", "checker.py", "reference_good", "reference_bad")
FIXED_DATE = "2026-09-29T00:00:00+00:00"
IDENTITY = ("eval", "eval@invalid")
SKIP_NAMES = {"__pycache__", ".pytest_cache", ".overlay-delete", ".DS_Store"}


class TraversalError(ValueError):
    """A fixture path tried to escape its root."""


def safe_join(root: Path, relative: str | Path) -> Path:
    """Join ``relative`` under ``root`` and refuse anything that escapes it."""
    rel = Path(relative)
    if rel.is_absolute() or rel.drive or any(part == ".." for part in rel.parts):
        raise TraversalError(f"path escapes fixture root: {relative}")
    target = (root / rel).resolve()
    base = root.resolve()
    if target != base and base not in target.parents:
        raise TraversalError(f"path escapes fixture root: {relative}")
    return target


def _normalised_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return data.replace(b"\r\n", b"\n")


def iter_files(root: Path):
    """Yield (relative posix path, absolute path) for every file under root, sorted."""
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_NAMES for part in path.relative_to(root).parts):
            continue
        if path.is_symlink():
            raise TraversalError(f"symlinks are not allowed in fixtures: {path}")
        if path.is_file():
            yield path.relative_to(root).as_posix(), path


def copy_tree(source: Path, dest: Path, prefix: str = "") -> list[str]:
    copied = []
    for rel, path in iter_files(source):
        target = safe_join(dest, f"{prefix}{rel}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(_normalised_bytes(path))
        copied.append(f"{prefix}{rel}")
    return copied


def fixture_dir(fixture_id: str) -> Path:
    path = HERE / fixture_id
    if not path.is_dir():
        raise FileNotFoundError(f"{fixture_id} is not materialised under {HERE}")
    return path


def compose(fixture_id: str, dest: Path, overlay: str | None = None) -> Path:
    """Build a workspace: starter + public_tests/ (+ overlay 'good' or 'bad')."""
    fdir = fixture_dir(fixture_id)
    dest.mkdir(parents=True, exist_ok=True)
    copy_tree(fdir / "starter", dest)
    copy_tree(fdir / "public_tests", dest, prefix="public_tests/")
    if overlay:
        odir = fdir / f"reference_{overlay}"
        if not odir.is_dir():
            raise FileNotFoundError(f"{fixture_id} has no reference_{overlay}/")
        delete_list = odir / ".overlay-delete"
        if delete_list.is_file():
            for line in delete_list.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    victim = safe_join(dest, line)
                    if victim.is_file():
                        victim.unlink()
        copy_tree(odir, dest)
    return dest


def _git_env(config_file: Path) -> dict[str, str]:
    env = dict(os.environ)
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": str(config_file),
        "GIT_AUTHOR_NAME": IDENTITY[0], "GIT_AUTHOR_EMAIL": IDENTITY[1],
        "GIT_COMMITTER_NAME": IDENTITY[0], "GIT_COMMITTER_EMAIL": IDENTITY[1],
        "GIT_AUTHOR_DATE": FIXED_DATE, "GIT_COMMITTER_DATE": FIXED_DATE,
    })
    return env


def init_baseline(workspace: Path) -> str:
    """git init the workspace with the fixed identity and commit 'fixture baseline'.

    User and system git configuration are excluded so the commit is reproducible; returns the
    commit SHA-1.
    """
    config = workspace.parent / f".{workspace.name}.gitconfig"
    config.write_text("", encoding="utf-8")
    env = _git_env(config)
    try:
        def run(*args: str) -> str:
            return subprocess.run(["git", *args], cwd=workspace, env=env, check=True, capture_output=True, text=True).stdout.strip()
        run("init", "-q", "-b", "main")
        run("config", "core.autocrlf", "false")
        run("config", "commit.gpgsign", "false")
        run("add", "-A")
        run("commit", "-q", "-m", "fixture baseline")
        return run("rev-parse", "HEAD")
    finally:
        config.unlink(missing_ok=True)


def baseline_commit(fixture_id: str) -> str:
    with tempfile.TemporaryDirectory(prefix=f"sol-{fixture_id}-") as tmp:
        workspace = compose(fixture_id, Path(tmp) / "ws")
        return init_baseline(workspace)


def private_dir(fixture_id: str) -> Path:
    return PRIVATE_ROOT / fixture_id


def hidden_manifest_hash(directory: Path) -> str | None:
    """SHA-256 over sorted '<sha256>  <relative path>' lines of the withheld tests."""
    if not directory.is_dir():
        return None
    lines = [f"{hashlib.sha256(_normalised_bytes(path)).hexdigest()}  {rel}\n" for rel, path in iter_files(directory) if rel != ".gitignore"]
    if not lines:
        return None
    return hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()


def run_checker(fixture_id: str, workspace: Path, withheld: Path | None = None, timeout: int = 300) -> dict:
    """Run Fxx/checker.py on a workspace in a separate process; never raises for checker faults."""
    cmd = [sys.executable, "-X", "utf8", str(fixture_dir(fixture_id) / "checker.py"), str(workspace)]
    if withheld is not None and withheld.is_dir():
        cmd += ["--withheld", str(withheld)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return {"fixture": fixture_id, "status": "FAIL", "checks": [], "error": f"checker timed out after {timeout}s"}
    try:
        start = proc.stdout.index("{")
        result = json.JSONDecoder().raw_decode(proc.stdout[start:])[0]
    except ValueError:
        return {"fixture": fixture_id, "status": "FAIL", "checks": [], "error": "checker printed no JSON", "stderr": proc.stderr[-2000:]}
    expected = {0: "PASS", 1: "FAIL", 2: "NOT_ASSESSED"}.get(proc.returncode, "FAIL")
    if result.get("status") != expected:
        result["error"] = f"exit code {proc.returncode} disagrees with status {result.get('status')}"
        result["status"] = "FAIL"
    return result


def materialised_ids() -> list[str]:
    return sorted(p.name for p in HERE.iterdir() if p.is_dir() and p.name.startswith("F") and (p / "checker.py").is_file())


def missing_parts(fixture_id: str) -> list[str]:
    fdir = HERE / fixture_id
    return [part for part in REQUIRED_PARTS if not (fdir / part).exists()]


def stamp(check_only: bool = False) -> dict:
    payload = json.loads(FIXTURES_JSON.read_text(encoding="utf-8"))
    changes, problems = [], []
    for item in payload["fixtures"]:
        fid = item["id"]
        if not (HERE / fid).is_dir():
            continue
        missing = missing_parts(fid)
        if missing:
            problems.append(f"{fid} missing {missing}")
            continue
        commit = baseline_commit(fid)
        hidden = hidden_manifest_hash(private_dir(fid))
        if hidden is None:
            problems.append(f"{fid} has no withheld tests under {private_dir(fid)}")
            continue
        wanted = {"materialisation_status": "MATERIALISED", "initial_commit": commit, "hidden_manifest_hash": hidden,
                  "materialised_path": f"benchmarks/solution-selection/materialised/{fid}"}
        for key, value in wanted.items():
            if item.get(key) != value:
                changes.append(f"{fid}.{key}: {item.get(key)!r} -> {value!r}")
                if not check_only:
                    item[key] = value
    if changes and not check_only:
        FIXTURES_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    status = "FAIL" if problems or (check_only and changes) else "PASS"
    return {"status": status, "changes": changes, "problems": problems}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p_compose = sub.add_parser("compose")
    p_compose.add_argument("fixture")
    p_compose.add_argument("--dest", type=Path, required=True)
    p_compose.add_argument("--overlay", choices=("good", "bad"))
    p_commit = sub.add_parser("commit")
    p_commit.add_argument("fixture")
    p_stamp = sub.add_parser("stamp")
    p_stamp.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "compose":
        print(compose(args.fixture, args.dest, args.overlay))
        return 0
    if args.command == "commit":
        print(baseline_commit(args.fixture))
        return 0
    result = stamp(check_only=args.check)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
