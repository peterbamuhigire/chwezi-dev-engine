#!/usr/bin/env python3
"""Check that ER1 claims resolve to accepted local evidence and revisions."""
from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
DATA = Path(__file__).with_name("claim-inventory.json")
REQUIRED = ("id", "claim", "owner", "entry_points", "status", "tested_revision", "result", "environment", "limitations", "evidence")
PRESERVED_ANCHORS = (
    "at-a-glance", "start-here", "capabilities", "find-the-right-skill",
    "chwezi-product-excellence-standard", "chwezi-reporting-and-dashboards-standard",
    "how-it-works", "what-is-inside", "catalogue-size", "what-the-skills-produce",
    "standards-applied", "beyond-the-skills", "installation", "claude-code-plugin-recommended",
    "codex", "standalone-installer", "manual-route", "verify", "checks-beyond-ci",
    "quality-and-improvement", "changes-after-the-october-kaizen-1-to-8-november-2026",
    "latest-published-score", "open-findings-that-matter-to-a-reader",
    "what-the-october-2026-kaizen-improved", "defects-fixed-in-guidance",
    "tooling-that-failed-on-this-host", "checks-that-only-tighten", "routing-and-examples",
    "overall-measures", "date-triggered-gates", "references", "contributing-and-licence",
)


def verify(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("task_id") != "ER1" or data.get("acceptance_id") != "AC-ER1":
        errors.append("wrong task or acceptance ID")
    integrated = data.get("local_integrated_revision", "")
    for packet in data.get("implementation_packets", []):
        rev = packet.get("revision", "")
        evidence = ROOT / packet.get("evidence", "")
        if not evidence.is_file():
            errors.append(f"missing packet evidence: {packet.get('id')}")
        if subprocess.run(["git", "cat-file", "-e", f"{rev}^{{commit}}"], cwd=ROOT, capture_output=True).returncode:
            errors.append(f"unknown accepted revision: {packet.get('id')}")
        elif subprocess.run(["git", "merge-base", "--is-ancestor", rev, integrated], cwd=ROOT, capture_output=True).returncode:
            errors.append(f"packet is not integrated: {packet.get('id')}")
    build_contract = json.loads((ROOT / "docs/plans/ai-engine-kaizen/build.contract.json").read_text(encoding="utf-8"))
    build_tasks = {task["id"]: task for task in build_contract.get("tasks", [])}
    for packet in data.get("implementation_packets", []):
        task = build_tasks.get(packet.get("id"), {})
        accepted = any(item.get("result") == "PASS" and item.get("tested_revision") == packet.get("revision") for item in task.get("evidence", []))
        if task.get("state") != "complete" or not accepted:
            errors.append(f"packet is not accepted by build contract: {packet.get('id')}")
    attestations = json.loads((Path(__file__).with_name("build-attestations.json")).read_text(encoding="utf-8"))
    required_builds = {"srs-skills", "chwezi-development-engine", "chwezi-dev-engine", "skills-engine-agents"}
    observed_builds = {item.get("repository"): item for item in attestations.get("producer_builds", [])}
    if attestations.get("acceptance_id") != "AC-ER1" or set(observed_builds) != required_builds:
        errors.append("four producer build attestations are not recorded")
    for repository, item in observed_builds.items():
        if item.get("state") != "integrated" or not isinstance(item.get("gates_passed"), int) or item["gates_passed"] < 1:
            errors.append(f"producer build is not accepted: {repository}")
    private_build = observed_builds.get("chwezi-development-engine", {})
    if private_build.get("tested_revision") is not None or private_build.get("integration_head") is not None:
        errors.append("private Development revision identifiers must not appear in public evidence")
    claims = data.get("claims", [])
    if not claims:
        errors.append("no proposed claims")
    for claim in claims:
        for key in REQUIRED:
            if not claim.get(key):
                errors.append(f"{claim.get('id', '<unknown>')}: missing {key}")
        for entry in [claim.get("owner", ""), *claim.get("entry_points", [])]:
            if entry and not (ROOT / entry).exists():
                errors.append(f"{claim.get('id')}: unresolved entry point {entry}")
        evidence = ROOT / claim.get("evidence", "")
        if not evidence.is_file():
            errors.append(f"{claim.get('id')}: missing evidence")
        rev = claim.get("tested_revision", "")
        if subprocess.run(["git", "merge-base", "--is-ancestor", rev, integrated], cwd=ROOT, capture_output=True).returncode:
            errors.append(f"{claim.get('id')}: tested revision is not integrated")
    casebook = data.get("casebook", {})
    casebook_path = ROOT / casebook.get("path", "")
    if not casebook_path.is_file():
        errors.append("missing frozen casebook")
    elif hashlib.sha256(casebook_path.read_bytes()).hexdigest() != casebook.get("sha256"):
        errors.append("casebook digest mismatch")
    for path in ("README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md"):
        if not (ROOT / path).is_file():
            errors.append(f"missing preserved front-door destination: {path}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    headings = set()
    for heading in re.findall(r"^#{1,6} +(.+?)\s*#*\s*$", readme, flags=re.MULTILINE):
        slug = re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
        headings.add(slug)
    for anchor in PRESERVED_ANCHORS:
        if anchor not in headings:
            errors.append(f"missing captured README anchor: #{anchor}")
    inventory = Path(__file__).with_name("front-door-inventory.md")
    for target in re.findall(r"\]\(([^)]+)\)", inventory.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "#")):
            continue
        path, _, _fragment = target.partition("#")
        if path and not (inventory.parent / path).exists():
            errors.append(f"unresolved inventory link: {target}")
    return errors


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    errors = verify(data)
    if errors:
        print("FAIL: " + "; ".join(errors))
        return 1
    damaged = copy.deepcopy(data)
    damaged["claims"][0]["owner"] = ""
    negative = verify(damaged)
    if not any("missing owner" in error for error in negative):
        print("FAIL: negative control did not reject missing owner")
        return 1
    print(f"PASS: AC-ER1 inventory, {len(data['claims'])} claims, {len(data['implementation_packets'])} accepted packets, front-door destinations resolve")
    print("PASS: negative control rejects a missing claim owner")
    return 0


if __name__ == "__main__":
    sys.exit(main())
