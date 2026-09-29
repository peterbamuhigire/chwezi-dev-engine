#!/usr/bin/env python3
"""
Routing smoke test for the active skills catalogue.

Turns "routing precision" from an assertion into a measured, regression-guarded
number. It does NOT call an LLM (CI must be deterministic and offline). Instead
it models the routing signal an LLM actually sees - each skill's frontmatter
`name` + `description` - as a TF-IDF vector, scores a fixture of representative
tasks against every skill, and asserts the expected skill ranks within top-N.

What it measures:
  1. precision@1 / precision@3 over the fixtures (routing quality).
  2. owned negatives: a fixture may carry `negatives: [{task, owner}]`. A
     negative belongs to the fixture's `expect` skill. It passes when that
     skill is not rank 1 (or scores 0) and, when `owner` is set, the owner
     ranks above the skill with a score above 0. An owner written as
     `<engine-id>/<skill>` lives in another engine: it is NOT_ASSESSED here and
     evaluated in union mode by chwezi-engine-agents (M10-03-T09).
  3. description collisions - pairs of skills whose routing signals are so
     similar an agent could not reliably choose between them (routing noise).

Modes:
  (default)         run fixtures and negatives; exit 1 on any failure.
  --min-rank1 PCT   also fail when precision@1 is below PCT (ratchet floor;
                    raise it, never lower it - see chwezi-engine-agents
                    evals/routing/baseline.json).
  --lint-fixtures   also fail when a prompt contains its expected slug, or its
                    word-trigram overlap with the expected description is >= 0.6.
  --report-only     print metrics; always exit 0.
  --collisions      print the most similar skill pairs (consolidation candidates).
  --collision-gate  with --collisions: fail on pairs >= 0.75 and warn on pairs
                    >= --threshold, unless allow-listed in
                    docs/routing-collision-allowlist.yml.

Owner-outranks-self negatives, the collision thresholds and the rank-1 ratchet
are adapted from addyosmani/agent-skills (MIT,
https://github.com/addyosmani/agent-skills, commit 2686b62), scripts/run-evals.js;
paraphrased, not copied.

This is a lexical proxy, not live routing (see agent-skills issue #620): it
guards against descriptions drifting into ambiguity and against a known good
task->skill mapping regressing.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
ACTIVE_ROOTS = ("skills", "00-meta-initialization")
FIXTURE_FILES = (
    REPO_ROOT / "scripts" / "routing_fixtures.yml",
    REPO_ROOT / "tests" / "routing" / "edge-fixtures.yml",
)
ALLOWLIST_FILE = REPO_ROOT / "docs" / "routing-collision-allowlist.yml"
FRONTMATTER_RE = re.compile(r"^﻿?---\r?\n(.*?)\r?\n---", re.DOTALL)
TOKEN_RE = re.compile(r"[a-z0-9]+")
COLLISION_ERROR = 0.75
TRIGRAM_LIMIT = 0.6

# Tokens that carry no routing signal: too common across the catalogue to
# discriminate between skills.
STOPWORDS = {
    "use", "when", "the", "a", "an", "and", "or", "for", "to", "of", "in", "on",
    "with", "this", "that", "is", "are", "be", "by", "as", "it", "its", "at",
    "from", "into", "across", "before", "after", "any", "all", "not", "no",
    "skill", "skills", "apply", "applies", "need", "needs", "needed", "work",
    "working", "rather", "than", "your", "you", "they", "them", "build",
    "building", "create", "creating", "make", "making", "design", "designing",
    "implement", "implementing", "should", "must", "can", "via", "per", "if",
}


def read_catalogue(base: Path = REPO_ROOT, roots: tuple[str, ...] = ACTIVE_ROOTS) -> dict[str, dict[str, str]]:
    """slug -> {name, description}. Injectable root for tests."""
    catalogue: dict[str, dict[str, str]] = {}
    for root in roots:
        folder = base / root
        if not folder.exists():
            continue
        for skill_md in folder.rglob("SKILL.md"):
            if any(p.startswith(".") for p in skill_md.relative_to(folder).parts):
                continue
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            match = FRONTMATTER_RE.match(text)
            if not match:
                continue
            try:
                fm = yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError:
                continue
            catalogue[skill_md.parent.name] = {
                "name": str(fm.get("name", skill_md.parent.name)),
                "description": str(fm.get("description", "")),
            }
    return catalogue


def load_skills(base: Path = REPO_ROOT) -> dict[str, str]:
    """slug -> routing signal text (name weighted twice + description)."""
    return {slug: f"{item['name']} {item['name']} {item['description']}" for slug, item in read_catalogue(base).items()}


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS and len(t) > 2]


def build_index(signals: dict[str, str]):
    docs = {slug: Counter(tokenize(text)) for slug, text in signals.items()}
    df: Counter = Counter()
    for counts in docs.values():
        df.update(counts.keys())
    n = len(docs)
    idf = {term: math.log((n + 1) / (freq + 1)) + 1 for term, freq in df.items()}

    def vec(counts: Counter) -> dict[str, float]:
        return {t: c * idf.get(t, math.log(n + 1) + 1) for t, c in counts.items()}

    vectors = {slug: vec(counts) for slug, counts in docs.items()}
    return vectors, idf, vec


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    dot = sum(a[t] * b[t] for t in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def rank(task: str, vectors, vec) -> list[tuple[str, float]]:
    q = vec(Counter(tokenize(task)))
    scored = [(slug, cosine(q, v)) for slug, v in vectors.items()]
    scored.sort(key=lambda kv: kv[1], reverse=True)
    return scored


def load_fixtures(files=FIXTURE_FILES) -> list[dict]:
    fixtures: list[dict] = []
    for fixture_file in files:
        if Path(fixture_file).exists():
            fixtures.extend(yaml.safe_load(Path(fixture_file).read_text(encoding="utf-8"))["fixtures"])
    return fixtures


def check_negative(skill: str, negative: dict, ranked: list[tuple[str, float]]) -> tuple[str, str]:
    """Return (status, detail) with status PASS, FAIL or NOT_ASSESSED."""
    owner = negative.get("owner")
    scores = dict(ranked)
    order = [slug for slug, _ in ranked]
    self_score = scores.get(skill, 0.0)
    self_rank = order.index(skill) + 1 if skill in scores else None
    if owner and "/" in str(owner):
        return "NOT_ASSESSED", f"cross-engine owner {owner} is evaluated in union mode"
    if self_rank == 1 and self_score > 0:
        return "FAIL", f"`{skill}` ranks first ({self_score:.2f})"
    if owner:
        if owner not in scores:
            return "FAIL", f"owner `{owner}` is not an active skill"
        owner_score = scores[owner]
        if owner_score <= 0 or order.index(owner) > (self_rank or len(order)) - 1:
            return "FAIL", f"owner `{owner}` ({owner_score:.2f}, rank {order.index(owner) + 1}) does not outrank `{skill}` ({self_score:.2f}, rank {self_rank})"
    return "PASS", ""


def slug_phrase(slug: str) -> str:
    return re.sub(r"^\d+-", "", slug.lower()).replace("-", " ").strip()


def word_trigrams(text: str) -> set[tuple[str, ...]]:
    words = TOKEN_RE.findall(text.lower())
    return {tuple(words[i : i + 3]) for i in range(len(words) - 2)}


def lint_prompt(prompt: str, slug: str, description: str) -> list[str]:
    findings: list[str] = []
    normal = " " + " ".join(TOKEN_RE.findall(prompt.lower())) + " "
    phrase = " ".join(TOKEN_RE.findall(slug_phrase(slug)))
    if phrase and f" {phrase} " in normal:
        findings.append(f"slug-in-prompt: contains '{phrase}'")
    grams = word_trigrams(prompt)
    if grams:
        overlap = len(grams & word_trigrams(description)) / len(grams)
        if overlap >= TRIGRAM_LIMIT:
            findings.append(f"description-copy: trigram overlap {overlap:.2f} >= {TRIGRAM_LIMIT}")
    return findings


def lint_fixtures(fixtures: list[dict], catalogue: dict[str, dict[str, str]]) -> list[str]:
    findings: list[str] = []
    for fx in fixtures:
        expect = fx["expect"]
        description = catalogue.get(expect, {}).get("description", "")
        for finding in lint_prompt(fx["task"], expect, description):
            findings.append(f"{finding} (expect `{expect}`; task {fx['task']!r})")
        for negative in fx.get("negatives") or []:
            owner = str(negative.get("owner") or "")
            if owner and "/" not in owner:
                for finding in lint_prompt(negative["task"], owner, catalogue.get(owner, {}).get("description", "")):
                    findings.append(f"{finding} (negative owner `{owner}`; task {negative['task']!r})")
    return findings


def run_fixtures(report_only: bool, min_rank1: float | None = None, lint: bool = False, base: Path = REPO_ROOT, fixture_files=FIXTURE_FILES) -> int:
    catalogue = read_catalogue(base)
    signals = {slug: f"{item['name']} {item['name']} {item['description']}" for slug, item in catalogue.items()}
    vectors, _idf, vec = build_index(signals)
    fixtures = load_fixtures(fixture_files)

    p1 = p3 = 0
    failures: list[str] = []
    negative_counts = Counter()
    for fx in fixtures:
        task, expect = fx["task"], fx["expect"]
        top_n = int(fx.get("top_n", 3))
        if expect not in signals:
            failures.append(f"FIXTURE ERROR: expected skill `{expect}` is not active (task: {task!r})")
            continue
        ranked = rank(task, vectors, vec)
        order = [slug for slug, _ in ranked]
        pos = order.index(expect) + 1
        if pos == 1:
            p1 += 1
        if pos <= 3:
            p3 += 1
        if pos > top_n:
            top = ", ".join(f"{s}({sc:.2f})" for s, sc in ranked[:3])
            failures.append(
                f"MISROUTE: task {task!r}\n    expected `{expect}` in top {top_n}, got rank {pos}. Top 3: {top}"
            )
        for negative in fx.get("negatives") or []:
            status, detail = check_negative(expect, negative, rank(negative["task"], vectors, vec))
            negative_counts[status] += 1
            if negative.get("owner"):
                negative_counts["owned"] += 1
            if status == "FAIL":
                failures.append(f"NEGATIVE: task {negative['task']!r}\n    {detail}")

    lint_findings = lint_fixtures(fixtures, catalogue) if lint else []
    total = len(fixtures)
    rate1 = 100 * p1 / total if total else 0.0
    print("routing-smoke-test (lexical proxy; not live routing):")
    print(f"- active skills indexed: {len(signals)}")
    print(f"- fixtures: {total}")
    print(f"- precision@1: {p1}/{total} ({rate1:.1f}%)")
    print(f"- precision@3: {p3}/{total} ({100*p3/total if total else 0:.1f}%)")
    print(
        f"- negatives: {sum(negative_counts[k] for k in ('PASS', 'FAIL', 'NOT_ASSESSED'))} "
        f"(owned {negative_counts['owned']}; pass {negative_counts['PASS']}, fail {negative_counts['FAIL']}, "
        f"not assessed {negative_counts['NOT_ASSESSED']})"
    )
    if lint:
        print(f"- fixture lint findings: {len(lint_findings)}")
        failures.extend(f"LINT: {finding}" for finding in lint_findings)
    if min_rank1 is not None:
        print(f"- rank-1 floor: {min_rank1}%")
        if rate1 < min_rank1:
            failures.append(f"RATCHET: precision@1 {rate1:.1f}% is below the floor {min_rank1}%")
    print(f"- failures: {len(failures)}")
    for f in failures:
        print(f"[FAIL] {f}")

    if failures and not report_only:
        return 1
    return 0


def load_allowlist(path: Path = ALLOWLIST_FILE) -> dict[frozenset[str], dict]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    allowed: dict[frozenset[str], dict] = {}
    for entry in data.get("pairs") or []:
        pair = entry.get("pair") or []
        if len(pair) != 2 or not entry.get("reason") or not entry.get("decided_on"):
            raise ValueError(f"allowlist entry needs pair (two slugs), reason and decided_on: {entry!r}")
        allowed[frozenset(pair)] = entry
    return allowed


def collision_pairs(signals: dict[str, str], threshold: float) -> list[tuple[float, str, str]]:
    vectors, _idf, _vec = build_index(signals)
    slugs = sorted(vectors)
    pairs = []
    for i in range(len(slugs)):
        for j in range(i + 1, len(slugs)):
            s = cosine(vectors[slugs[i]], vectors[slugs[j]])
            if s >= threshold:
                pairs.append((s, slugs[i], slugs[j]))
    pairs.sort(reverse=True)
    return pairs


def show_collisions(threshold: float, limit: int, gate: bool = False, base: Path = REPO_ROOT, allowlist: Path = ALLOWLIST_FILE) -> int:
    signals = load_skills(base)
    pairs = collision_pairs(signals, min(threshold, COLLISION_ERROR))
    allowed = load_allowlist(allowlist) if gate else {}
    print(f"description collisions (cosine >= {threshold}):")
    print(f"- candidate pairs: {sum(s >= threshold for s, _a, _b in pairs)}")
    errors = 0
    for s, a, b in pairs[:limit]:
        if s < threshold:
            continue
        marker = ""
        if gate:
            if frozenset((a, b)) in allowed:
                marker = "  [ALLOWED: " + str(allowed[frozenset((a, b))]["reason"]).strip()[:80] + "]"
            elif s >= COLLISION_ERROR:
                marker = "  [ERROR]"
                errors += 1
            else:
                marker = "  [WARN]"
        print(f"  {s:.3f}  {a}  <->  {b}{marker}")
    if gate:
        print(f"- collision gate: {errors} error(s) at >= {COLLISION_ERROR}; allow-list {allowlist.name}")
        return 1 if errors else 0
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Routing smoke test for the skills catalogue.")
    ap.add_argument("--report-only", action="store_true", help="Print metrics but always exit 0.")
    ap.add_argument("--collisions", action="store_true", help="Print most-similar skill pairs and exit.")
    ap.add_argument("--collision-gate", action="store_true", help="With --collisions: fail on non-allow-listed pairs >= 0.75.")
    ap.add_argument("--threshold", type=float, default=0.45, help="Collision cosine threshold (default 0.45).")
    ap.add_argument("--limit", type=int, default=40, help="Max collision pairs to print.")
    ap.add_argument("--min-rank1", type=float, default=None, help="Fail when precision@1 (percent) is below this floor.")
    ap.add_argument("--lint-fixtures", action="store_true", help="Fail on slug-bearing or description-copying fixture prompts.")
    args = ap.parse_args()
    if args.collisions:
        return show_collisions(args.threshold, args.limit, args.collision_gate)
    return run_fixtures(args.report_only, args.min_rank1, args.lint_fixtures)


if __name__ == "__main__":
    sys.exit(main())
