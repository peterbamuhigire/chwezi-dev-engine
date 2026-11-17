"""Optional structural validator for unattended plan JSON sidecars.

This module validates contract shape and evidence-file identity only. It does
not run acceptance commands or establish semantic correctness, task completion,
or independent commit verification.
"""

from __future__ import annotations

import argparse
from graphlib import CycleError, TopologicalSorter
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


TASK_STATES = {"pending", "running", "blocked", "complete"}
RESULTS = {"PASS", "FAIL", "NOT_ASSESSED"}
ID_RE = re.compile(r"^[A-Z][A-Z0-9_-]{1,31}$")
SHA_RE = re.compile(r"^(?:[a-fA-F0-9]{40}|[a-fA-F0-9]{64})$")


class ContractError(ValueError):
    """Raised when a plan contract is malformed or unsafe."""


def _object(value: Any, where: str, required: set[str], optional: set[str] = frozenset()) -> dict:
    if not isinstance(value, dict):
        raise ContractError(f"{where} must be an object")
    missing = required - value.keys()
    extra = value.keys() - required - optional
    if missing:
        raise ContractError(f"{where} missing keys: {', '.join(sorted(missing))}")
    if extra:
        raise ContractError(f"{where} has unknown keys: {', '.join(sorted(extra))}")
    return value


def _text(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{where} must be a non-empty string")
    return value.strip()


def _id(value: Any, where: str) -> str:
    result = _text(value, where)
    if not ID_RE.fullmatch(result):
        raise ContractError(f"{where} must be a stable uppercase ID (2-32 characters)")
    return result


def _relative_path(
    value: Any,
    where: str,
    root: Path,
    *,
    must_exist: bool = False,
    allow_dot: bool = False,
    must_be_dir: bool = False,
) -> Path:
    raw = _text(value, where)
    if "\\" in raw:
        raise ContractError(f"{where} must use slash-separated relative paths")
    posix = PurePosixPath(raw)
    windows = PureWindowsPath(raw)
    if posix.is_absolute() or windows.is_absolute() or windows.drive or ".." in posix.parts:
        raise ContractError(f"{where} must stay within the worktree")
    if raw == "." and allow_dot:
        return root.resolve()
    if raw in (".", ""):
        raise ContractError(f"{where} must name a file or directory below the worktree")
    candidate = root.joinpath(*posix.parts)
    try:
        resolved = candidate.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise ContractError(f"{where} cannot be resolved safely: {exc}") from exc
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ContractError(f"{where} resolves outside the worktree") from exc
    if must_exist and not resolved.is_file():
        raise ContractError(f"{where} does not name an existing file: {raw}")
    if must_be_dir and not resolved.is_dir():
        raise ContractError(f"{where} does not name an existing directory: {raw}")
    return resolved


def _tracked(root: Path, path: Path, where: str) -> None:
    relative = path.relative_to(root.resolve()).as_posix()
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--error-unmatch", "--", relative],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ContractError(f"{where} could not be checked as tracked: {exc}") from exc
    if result.returncode != 0:
        raise ContractError(f"{where} must name a tracked worktree file: {relative}")


def _commands(value: Any, where: str) -> None:
    if not isinstance(value, list) or not value:
        raise ContractError(f"{where} must be a non-empty list of argument lists")
    for index, command in enumerate(value):
        if not isinstance(command, list) or not command or any(not isinstance(x, str) or not x for x in command):
            raise ContractError(f"{where}[{index}] must be a non-empty string argument list")


def validate_contract(data: Any, root: str | Path) -> dict[str, Any]:
    """Validate optional contract JSON. Return counts and errors never certify semantics."""
    root_path = Path(root).resolve()
    errors: list[str] = []
    try:
        contract = _object(data, "contract", {"schema_version", "tasks"})
        if type(contract["schema_version"]) is not int or contract["schema_version"] != 1:
            raise ContractError("schema_version must be 1")
        if not isinstance(contract["tasks"], list) or not contract["tasks"]:
            raise ContractError("tasks must be a non-empty list")

        tasks: dict[str, dict] = {}
        criteria: dict[str, str] = {}
        criterion_specs: dict[str, dict] = {}
        for index, raw_task in enumerate(contract["tasks"]):
            where = f"tasks[{index}]"
            task = _object(raw_task, where, {"id", "title", "depends_on", "scope", "acceptance", "state", "evidence"})
            task_id = _id(task["id"], f"{where}.id")
            if task_id in tasks:
                raise ContractError(f"duplicate task ID: {task_id}")
            task["title"] = _text(task["title"], f"{where}.title")
            if task["state"] not in TASK_STATES:
                raise ContractError(f"{where}.state must be one of {sorted(TASK_STATES)}")
            for key in ("depends_on", "scope", "acceptance", "evidence"):
                if not isinstance(task[key], list):
                    raise ContractError(f"{where}.{key} must be a list")
            if not task["scope"]:
                raise ContractError(f"{where}.scope must name at least one owned path")
            for n, scope in enumerate(task["scope"]):
                _relative_path(scope, f"{where}.scope[{n}]", root_path)
            if len(set(task["scope"])) != len(task["scope"]):
                raise ContractError(f"{where}.scope contains duplicate paths")
            for n, dep in enumerate(task["depends_on"]):
                task["depends_on"][n] = _id(dep, f"{where}.depends_on[{n}]")
            if len(set(task["depends_on"])) != len(task["depends_on"]):
                raise ContractError(f"{where}.depends_on contains duplicates")
            if task_id in task["depends_on"]:
                raise ContractError(f"{where} cannot depend on itself")
            if not task["acceptance"]:
                raise ContractError(f"{where}.acceptance must contain at least one criterion")
            for c_index, raw_criterion in enumerate(task["acceptance"]):
                c_where = f"{where}.acceptance[{c_index}]"
                criterion = _object(
                    raw_criterion,
                    c_where,
                    {"id", "description"},
                    {"commands", "cwd", "evidence_oracle"},
                )
                criterion_id = _id(criterion["id"], f"{c_where}.id")
                if criterion_id in criteria:
                    raise ContractError(f"duplicate criterion ID: {criterion_id}")
                criteria[criterion_id] = task_id
                criterion_specs[criterion_id] = criterion
                _text(criterion["description"], f"{c_where}.description")
                has_commands = "commands" in criterion
                has_oracle = "evidence_oracle" in criterion
                if has_commands == has_oracle:
                    raise ContractError(f"{c_where} must have exactly one of commands or evidence_oracle")
                if has_commands:
                    _commands(criterion["commands"], f"{c_where}.commands")
                    if len(criterion["commands"]) != 1:
                        raise ContractError(f"{c_where}.commands must contain exactly one command; split separate checks into separate criteria")
                    _relative_path(criterion.get("cwd"), f"{c_where}.cwd", root_path, allow_dot=True, must_be_dir=True)
                else:
                    _text(criterion["evidence_oracle"], f"{c_where}.evidence_oracle")
            tasks[task_id] = task

        for task_id, task in tasks.items():
            unknown = [dep for dep in task["depends_on"] if dep not in tasks]
            if unknown:
                raise ContractError(f"{task_id} has unknown dependencies: {', '.join(unknown)}")
            if task["state"] in {"running", "complete"}:
                unfinished = [dep for dep in task["depends_on"] if tasks[dep]["state"] != "complete"]
                if unfinished:
                    raise ContractError(f"{task_id} is {task['state']} before dependencies complete: {', '.join(unfinished)}")

        # prepare() checks cycles iteratively even for reverse-ordered deep plans.
        try:
            TopologicalSorter({key: task["depends_on"] for key, task in tasks.items()}).prepare()
        except CycleError as exc:
            raise ContractError(f"dependency cycle includes {exc.args[1][0]}") from exc

        evidence_by_task: dict[str, set[str]] = {task_id: set() for task_id in tasks}
        for task_id, task in tasks.items():
            seen_evidence: set[str] = set()
            for e_index, raw_evidence in enumerate(task["evidence"]):
                e_where = f"{task_id}.evidence[{e_index}]"
                evidence = _object(raw_evidence, e_where, {"criterion_id", "path", "tested_revision", "sha256", "command", "result"})
                criterion_id = _id(evidence["criterion_id"], f"{e_where}.criterion_id")
                if criteria.get(criterion_id) != task_id:
                    raise ContractError(f"{e_where} refers to an unknown criterion or one owned by another task")
                if criterion_id in seen_evidence:
                    raise ContractError(f"{task_id} has duplicate evidence references for {criterion_id}")
                seen_evidence.add(criterion_id)
                if evidence["result"] not in RESULTS:
                    raise ContractError(f"{e_where}.result must be one of {sorted(RESULTS)}")
                path = _relative_path(evidence["path"], f"{e_where}.path", root_path, must_exist=True)
                _tracked(root_path, path, f"{e_where}.path")
                revision = _text(evidence["tested_revision"], f"{e_where}.tested_revision")
                if not SHA_RE.fullmatch(revision):
                    raise ContractError(f"{e_where}.tested_revision must be a 40- or 64-character Git object ID")
                try:
                    revision_check = subprocess.run(
                        ["git", "-C", str(root_path), "cat-file", "-e", f"{revision}^{{commit}}"],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        check=False,
                    )
                except (OSError, subprocess.TimeoutExpired) as exc:
                    raise ContractError(f"{e_where}.tested_revision could not be checked: {exc}") from exc
                if revision_check.returncode != 0:
                    raise ContractError(f"{e_where}.tested_revision is not an available Git commit")
                try:
                    ancestry = subprocess.run(
                        ["git", "-C", str(root_path), "merge-base", "--is-ancestor", revision, "HEAD"],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        check=False,
                    )
                except (OSError, subprocess.TimeoutExpired) as exc:
                    raise ContractError(f"{e_where}.tested_revision ancestry could not be checked: {exc}") from exc
                if ancestry.returncode == 1:
                    raise ContractError(f"{e_where}.tested_revision is not an ancestor of current HEAD")
                if ancestry.returncode != 0:
                    raise ContractError(f"{e_where}.tested_revision ancestry check failed: {ancestry.stderr.strip()}")
                digest = _text(evidence["sha256"], f"{e_where}.sha256")
                if not re.fullmatch(r"[a-fA-F0-9]{64}", digest):
                    raise ContractError(f"{e_where}.sha256 must be a 64-character SHA-256 digest")
                if hashlib.sha256(path.read_bytes()).hexdigest().lower() != digest.lower():
                    raise ContractError(f"{e_where}.sha256 does not match the evidence file")
                command = evidence["command"]
                if isinstance(command, list):
                    _commands([command], f"{e_where}.command")
                else:
                    _text(command, f"{e_where}.command")
                declared = criterion_specs[criterion_id]
                if "commands" in declared and (not isinstance(command, list) or command not in declared["commands"]):
                    raise ContractError(f"{e_where}.command must match a command declared by {criterion_id}")
                evidence_by_task[task_id].add(criterion_id)

        for task_id, task in tasks.items():
            criterion_ids = {criterion["id"] for criterion in task["acceptance"]}
            if task["state"] == "complete":
                missing = criterion_ids - evidence_by_task[task_id]
                if missing:
                    raise ContractError(f"{task_id} is complete without evidence for: {', '.join(sorted(missing))}")
                for item in task["evidence"]:
                    if item["result"] != "PASS":
                        raise ContractError(f"{task_id} is complete but {item['criterion_id']} is {item['result']}, not PASS")

    except (ContractError, KeyError, OSError, TypeError) as exc:
        errors.append(str(exc))

    task_list = data.get("tasks", []) if isinstance(data, dict) else []
    states = [task.get("state") for task in task_list if isinstance(task, dict)]
    reported_complete = bool(states) and all(state == "complete" for state in states)
    structurally_valid = not errors
    return {
        "valid": structurally_valid,
        "errors": errors,
        "task_count": len(states),
        "reported_complete": reported_complete,
        "completion_ready": structurally_valid and reported_complete,
        "independent_commit_verified": False,
        "semantic_acceptance_verified": False,
    }


def completion_readiness(data: Any, root: str | Path) -> dict[str, Any]:
    """Return structural completion readiness, never an independent pass verdict."""
    result = validate_contract(data, root)
    tasks = data.get("tasks", []) if isinstance(data, dict) else []
    counts = {state: 0 for state in sorted(TASK_STATES)}
    criterion_count = 0
    for task in tasks:
        if not isinstance(task, dict):
            continue
        state = task.get("state")
        if isinstance(state, str) and state in counts:
            counts[state] += 1
        if isinstance(task.get("acceptance"), list):
            criterion_count += len(task["acceptance"])
    return {
        **result,
        "task_states": counts,
        "criterion_count": criterion_count,
        "ready_for_independent_verification": result["completion_ready"],
        "note": "Reported metadata only; independent commit and semantic acceptance verification are not performed.",
    }


def load_contract(path: str | Path) -> Any:
    """Load a JSON contract file."""
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in pairs:
            if key in result:
                raise ContractError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    try:
        return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot load contract JSON: {exc}") from exc


def definition_digest(data: dict) -> str:
    """Fingerprint validated task intent, excluding executor state and evidence.

    Reordering records does not change intent. This detects drift; it does not
    enforce permissions against an executor that can alter the supervisor host.
    """
    definitions = []
    for task in data['tasks']:
        definition = {key: value for key, value in task.items() if key not in {'state', 'evidence'}}
        definition['depends_on'] = sorted(definition['depends_on'])
        definition['scope'] = sorted(definition['scope'])
        definition['acceptance'] = sorted(definition['acceptance'], key=lambda item: item['id'])
        definitions.append(definition)
    encoded = json.dumps({'schema_version': data['schema_version'],
                          'tasks': sorted(definitions, key=lambda item: item['id'])},
                         sort_keys=True, separators=(',', ':'), ensure_ascii=True)
    return hashlib.sha256(encoded.encode('utf-8')).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", help="optional plan contract JSON")
    parser.add_argument("--root", default=".", help="worktree root used to resolve scope and evidence paths")
    args = parser.parse_args(argv)
    try:
        result = completion_readiness(load_contract(args.contract), args.root)
    except ContractError as exc:
        result = {
            "valid": False,
            "errors": [str(exc)],
            "reported_complete": False,
            "completion_ready": False,
            "independent_commit_verified": False,
            "semantic_acceptance_verified": False,
        }
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 2


if __name__ == "__main__":
    sys.exit(main())
