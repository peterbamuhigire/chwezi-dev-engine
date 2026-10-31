#!/usr/bin/env python3
"""Repository-owned check for the engine's source registers.

The Digital Research engine owns the evidence contract and ships its own
validator, but that checkout is not part of this repository's CI. This check
keeps the same fail-closed rules for the registers kept here, so a lapsed
review date fails the build instead of waiting for a manual cycle.

For each register that has a ``sources`` list with ``id`` keys it checks:

* required fields and ISO dates on every active source;
* ``review_after`` is not before the check date (overdue fails);
* ``verified_at`` is not before ``accessed`` and nothing is dated in the future;
* current-class sources carry ``as_of``, ``publication_date`` or ``revision_date``;
  ``context-bound`` sources carry a non-empty ``scope``;
* active claims name only active sources;
* ``superseded_sources`` point at an active source through ``superseded_by``;
* ``quarantined_sources`` are marked NOT_ASSESSED with a reason and a re-verify date.

A register with the older ``register_id`` schema is not enforced; its register-level
``review_date`` is reported as a warning so the gap stays visible.

Exit status: 0 when there are no findings, 1 otherwise. Passing means metadata and
dates are consistent; it does not verify that a page supports a claim.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLOB = "docs/source-registers/*.json"
REQUIRED = ("id", "accessed", "verified_at", "review_after", "freshness_class")
CURRENT_CLASSES = {"volatile", "current", "regulatory", "market", "platform", "context-bound"}
ALL_CLASSES = CURRENT_CLASSES | {"static", "historical"}


def _date(value: Any, field: str, label: str, findings: list[str]) -> date | None:
    if not isinstance(value, str) or not value.strip():
        findings.append(f"{label}: {field} is required as an ISO date")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        findings.append(f"{label}: {field} is not an ISO date: {value}")
        return None


def check_source(source: Any, as_of: date, findings: list[str], warnings: list[str], warn_days: int) -> str | None:
    if not isinstance(source, dict):
        findings.append("source entries must be objects")
        return None
    sid = source.get("id")
    if not isinstance(sid, str) or not sid.strip():
        findings.append("source id must be a non-empty string")
        return None
    for field in REQUIRED:
        if field not in source:
            findings.append(f"{sid}: missing {field}")
    accessed = _date(source.get("accessed"), "accessed", sid, findings)
    verified = _date(source.get("verified_at"), "verified_at", sid, findings)
    review = _date(source.get("review_after"), "review_after", sid, findings)
    freshness = str(source.get("freshness_class") or "").strip().lower()
    if freshness not in ALL_CLASSES:
        findings.append(f"{sid}: unsupported freshness_class: {freshness!r}")
    if freshness in CURRENT_CLASSES and not (source.get("publication_date") or source.get("revision_date") or source.get("as_of")):
        findings.append(f"{sid}: current source requires publication_date, revision_date or as_of")
    if freshness == "context-bound" and not str(source.get("scope") or "").strip():
        findings.append(f"{sid}: context-bound source requires a non-empty scope")
    for field in ("publication_date", "revision_date", "as_of"):
        if field in source:
            _date(source[field], field, sid, findings)
    if accessed and verified and verified < accessed:
        findings.append(f"{sid}: verified_at precedes accessed")
    for field, value in (("accessed", accessed), ("verified_at", verified)):
        if value and value > as_of:
            findings.append(f"{sid}: {field} is in the future as of {as_of.isoformat()}")
    if verified and review and review < verified:
        findings.append(f"{sid}: review_after precedes verified_at")
    if review:
        if review < as_of:
            findings.append(f"{sid}: review_after {review.isoformat()} is overdue as of {as_of.isoformat()}")
        elif review <= as_of + timedelta(days=warn_days):
            warnings.append(f"{sid}: review_after {review.isoformat()} falls within {warn_days} days")
    return sid


def check_register(data: Any, as_of: date, warn_days: int = 14) -> tuple[list[str], list[str]]:
    """Return (findings, warnings) for one parsed register."""
    findings: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["register must be a JSON object"], warnings
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        return ["sources must be a non-empty list"], warnings
    active: dict[str, dict] = {}
    for source in sources:
        sid = check_source(source, as_of, findings, warnings, warn_days)
        if sid is None:
            continue
        if sid in active:
            findings.append(f"duplicate source id: {sid}")
        active[sid] = source
    superseded = data.get("superseded_sources") or []
    quarantined = data.get("quarantined_sources") or []
    history_ids = set()
    for entry in superseded:
        sid = entry.get("id") if isinstance(entry, dict) else None
        if not sid:
            findings.append("superseded source entries need an id")
            continue
        history_ids.add(sid)
        if sid in active:
            findings.append(f"{sid}: listed as both active and superseded")
        target = entry.get("superseded_by")
        if target not in active:
            findings.append(f"{sid}: superseded_by {target!r} is not an active source")
    for entry in quarantined:
        sid = entry.get("id") if isinstance(entry, dict) else None
        if not sid:
            findings.append("quarantined source entries need an id")
            continue
        history_ids.add(sid)
        if sid in active:
            findings.append(f"{sid}: listed as both active and quarantined")
        q = entry.get("quarantine") if isinstance(entry.get("quarantine"), dict) else {}
        if q.get("status") != "NOT_ASSESSED":
            findings.append(f"{sid}: quarantine.status must be NOT_ASSESSED")
        if not str(q.get("reason") or "").strip():
            findings.append(f"{sid}: quarantine needs a reason")
        _date(q.get("reverify_by"), "quarantine.reverify_by", sid, findings)
    claim_ids: set[str] = set()
    for claim in data.get("claims") or []:
        if not isinstance(claim, dict) or not str(claim.get("id") or "").strip():
            findings.append("claim entries need an id")
            continue
        cid = claim["id"]
        if cid in claim_ids:
            findings.append(f"duplicate claim id: {cid}")
        claim_ids.add(cid)
        source_ids = claim.get("source_ids")
        if not isinstance(source_ids, list):
            findings.append(f"{cid}: source_ids must be a list")
            continue
        if claim.get("requires_currentness") is True and not source_ids:
            findings.append(f"{cid}: current claim requires source_ids")
        for sid in source_ids:
            if sid in active:
                continue
            reason = "names a superseded or quarantined source" if sid in history_ids else "names an unknown source"
            findings.append(f"{cid}: {sid} {reason}")
    return findings, warnings


def legacy_warning(data: Any, as_of: date) -> str | None:
    """Report an overdue register-level review_date for the older register schema."""
    if not isinstance(data, dict) or "register_id" not in data:
        return None
    try:
        review = date.fromisoformat(str(data.get("review_date")))
    except ValueError:
        return f"{data.get('register_id')}: review_date is missing or not an ISO date (legacy schema, not enforced)"
    if review < as_of:
        return f"{data['register_id']}: register review_date {review.isoformat()} is overdue (legacy schema, not enforced)"
    return None


def run(paths: list[Path], as_of: date, warn_days: int) -> int:
    total = 0
    print("source-register-check:")
    print(f"- as-of: {as_of.isoformat()}")
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            print(f"[FAIL] {path.name}: cannot read register: {exc}")
            total += 1
            continue
        note = legacy_warning(data, as_of)
        if note:
            print(f"[WARN] {path.name}: {note}")
            continue
        findings, warnings = check_register(data, as_of, warn_days)
        for item in findings:
            print(f"[FAIL] {path.name}: {item}")
        for item in warnings:
            print(f"[WARN] {path.name}: {item}")
        total += len(findings)
        active = len(data.get("sources") or []) if isinstance(data, dict) else 0
        print(f"- {path.name}: {active} active sources, {len(findings)} findings, {len(warnings)} warnings")
    print(f"- findings: {total}")
    if total == 0:
        print("PASS: metadata and dates only; claim support NOT ASSESSED")
    return 1 if total else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("registers", nargs="*", type=Path, help="Register files (default: docs/source-registers/*.json)")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(), help="Check date (default: today)")
    parser.add_argument("--warn-days", type=int, default=14, help="Warn when a review date falls within this many days")
    args = parser.parse_args()
    paths = args.registers or sorted(ROOT.glob(DEFAULT_GLOB))
    if not paths:
        print("[FAIL] no register files found")
        return 1
    return run(paths, args.as_of, args.warn_days)


if __name__ == "__main__":
    sys.exit(main())
