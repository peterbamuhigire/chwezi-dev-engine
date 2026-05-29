#!/usr/bin/env python3
"""
Routing smoke test for the active skills catalogue.

Turns "routing precision" from an assertion into a measured, regression-guarded
number. It does NOT call an LLM (CI must be deterministic and offline). Instead
it models the routing signal an LLM actually sees - each skill's frontmatter
`name` + `description` - as a TF-IDF vector, scores a fixture of representative
tasks against every skill, and asserts the expected skill ranks within top-N.

Two things it measures:
  1. precision@1 / precision@3 over the fixtures (routing quality).
  2. description collisions - pairs of skills whose routing signals are so
     similar an agent could not reliably choose between them (routing noise).

Modes:
  (default)      run fixtures; exit 1 on any failure or below threshold.
  --report-only  run fixtures; print metrics; always exit 0.
  --collisions   print the most similar skill pairs (consolidation candidates).

This is a proxy, not a perfect oracle: it guards against descriptions drifting
into ambiguity and against a known good task->skill mapping regressing. A failure
means a description got less discriminative, not necessarily that an LLM would
mis-route - but the two correlate strongly.
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
ACTIVE_ROOTS = ("skills", "doctrine/skills", "00-meta-initialization")
FIXTURES = REPO_ROOT / "scripts" / "routing_fixtures.yml"
FRONTMATTER_RE = re.compile(r"^\ufeff?---\r?\n(.*?)\r?\n---", re.DOTALL)
TOKEN_RE = re.compile(r"[a-z0-9]+")

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


def load_skills() -> dict[str, str]:
    """slug -> routing signal text (name + description)."""
    signals: dict[str, str] = {}
    for root in ACTIVE_ROOTS:
        base = REPO_ROOT / root
        if not base.exists():
            continue
        for skill_md in base.rglob("SKILL.md"):
            if any(p.startswith(".") for p in skill_md.relative_to(base).parts):
                continue
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            match = FRONTMATTER_RE.match(text)
            if not match:
                continue
            try:
                fm = yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError:
                continue
            name = str(fm.get("name", skill_md.parent.name))
            desc = str(fm.get("description", ""))
            # Weight the name: it is the strongest routing token.
            signals[skill_md.parent.name] = f"{name} {name} {desc}"
    return signals


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


def run_fixtures(report_only: bool) -> int:
    signals = load_skills()
    vectors, _idf, vec = build_index(signals)
    fixtures = yaml.safe_load(FIXTURES.read_text(encoding="utf-8"))["fixtures"]

    p1 = p3 = 0
    failures: list[str] = []
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

    total = len(fixtures)
    print("routing-smoke-test:")
    print(f"- active skills indexed: {len(signals)}")
    print(f"- fixtures: {total}")
    print(f"- precision@1: {p1}/{total} ({100*p1//total if total else 0}%)")
    print(f"- precision@3: {p3}/{total} ({100*p3//total if total else 0}%)")
    print(f"- failures: {len(failures)}")
    for f in failures:
        print(f"[FAIL] {f}")

    if failures and not report_only:
        return 1
    return 0


def show_collisions(threshold: float, limit: int) -> int:
    signals = load_skills()
    vectors, _idf, _vec = build_index(signals)
    slugs = list(vectors)
    pairs = []
    for i in range(len(slugs)):
        for j in range(i + 1, len(slugs)):
            s = cosine(vectors[slugs[i]], vectors[slugs[j]])
            if s >= threshold:
                pairs.append((s, slugs[i], slugs[j]))
    pairs.sort(reverse=True)
    print(f"description collisions (cosine >= {threshold}):")
    print(f"- candidate pairs: {len(pairs)}")
    for s, a, b in pairs[:limit]:
        print(f"  {s:.3f}  {a}  <->  {b}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Routing smoke test for the skills catalogue.")
    ap.add_argument("--report-only", action="store_true", help="Print metrics but always exit 0.")
    ap.add_argument("--collisions", action="store_true", help="Print most-similar skill pairs and exit.")
    ap.add_argument("--threshold", type=float, default=0.45, help="Collision cosine threshold (default 0.45).")
    ap.add_argument("--limit", type=int, default=40, help="Max collision pairs to print.")
    args = ap.parse_args()
    if args.collisions:
        return show_collisions(args.threshold, args.limit)
    return run_fixtures(args.report_only)


if __name__ == "__main__":
    sys.exit(main())
