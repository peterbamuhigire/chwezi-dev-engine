"""Offline synthetic retrieval and answer-support check for K2."""

import argparse
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORPUS_REVISION = "synthetic-fixture-v1"
IDENTIFIER = re.compile(r"[A-Za-z]+-[A-Za-z0-9-]+|[A-Za-z][A-Za-z0-9]*|\d+(?:\.\d+)?")
STOP_WORDS = {"a", "an", "and", "does", "for", "how", "is", "the", "what"}


def tokens(text, *, drop_negation=False):
    values = [token if any(char.isdigit() for char in token) else token.lower() for token in IDENTIFIER.findall(text)]
    if drop_negation:
        values = [token for token in values if token.lower() not in {"not", "never", "no", "without"}]
    return [token for token in values if token.lower() not in STOP_WORDS]


def eligible_rows(corpus, tenant):
    return [row for row in corpus if row["tenant"] == tenant and row["status"] == "active"]


def rank(corpus, query, tenant, *, drop_negation=False):
    query_tokens = set(tokens(query, drop_negation=drop_negation))
    ranked = []
    for row in eligible_rows(corpus, tenant):
        row_tokens = set(tokens(row["text"] + " " + row["id"], drop_negation=drop_negation))
        score = len(query_tokens & row_tokens)
        if score:
            ranked.append((score, row))
    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))
    return [row for _, row in ranked]


def span_for(row, phrase):
    start = row["text"].lower().find(phrase.lower())
    if start < 0:
        return None
    end = start + len(phrase)
    return {"start": start, "end": end, "text": row["text"][start:end]}


def answer_grade(claim, row):
    """Deterministic exact-claim check; it does not judge generated language."""
    if not row or claim is None:
        return False
    source = re.sub(r"[^a-z0-9]+", " ", row["text"].casefold()).split()
    expected = re.sub(r"[^a-z0-9]+", " ", claim.casefold()).split()
    for start in range(len(source) - len(expected) + 1):
        if source[start:start + len(expected)] != expected:
            continue
        if expected[0] not in {"not", "never", "no", "without"} and start > 0 and source[start - 1] in {"not", "never", "no", "without"}:
            return False
        return True
    return False


def run(corpus, cases):
    results = []
    for case in cases:
        eligible = eligible_rows(corpus, case["tenant"])
        ranked = rank(corpus, case["query"], case["tenant"])
        ids = [row["id"] for row in ranked]
        relevant = set(case["relevant"])
        reciprocal_rank = next((1 / index for index, rid in enumerate(ids, 1) if rid in relevant), 0)
        top = ranked[0] if ranked else None
        claim = case.get("response_claim", case["expected_answer"])
        if not relevant:
            status = "ABSTAIN"
            support = None
        elif top is None:
            status, support = "ABSTAIN", False
        else:
            status = "ANSWER"
            support = answer_grade(claim, top)
        results.append({
            "case_id": case["id"], "corpus_revision": CORPUS_REVISION,
            "eligibility": {"tenant": case["tenant"], "eligible_ids": [row["id"] for row in eligible]},
            "ranked_ids": ids, "reciprocal_rank": reciprocal_rank,
            "status": status, "answer_supported": support,
            "response_claim": claim,
            "reviewer_grade": "SUPPORTED" if support is True else "UNSUPPORTED" if support is False else "NOT_APPLICABLE",
            "selected_span": span_for(top, case["expected_answer"]) if top and case["expected_answer"] else None,
        })
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim", help="grade a separate candidate response against the top ranked source")
    parser.add_argument("--drop-negation", action="store_true", help="negative control: remove meaningful negators")
    args = parser.parse_args()
    corpus = json.loads((HERE / "corpus.json").read_text(encoding="utf-8"))
    cases = json.loads((HERE / "eval.json").read_text(encoding="utf-8"))
    report = run(corpus, cases)
    if args.drop_negation:
        case = cases[1]
        top = rank(corpus, case["query"], case["tenant"], drop_negation=True)
        source = top[0] if top else None
        normalized_text = " ".join(tokens(source["text"], drop_negation=True)) if source else None
        claim = args.claim or "seven days"
        report.append({
            "case_id": case["id"] + "-negation-ablated",
            "ranked_ids": [row["id"] for row in top],
            "claim": claim,
            "answer_supported": answer_grade(claim, {"text": normalized_text}) if source else False,
            "original_source_supports_claim": answer_grade(claim, source),
            "ablated_text": normalized_text,
            "source_text": source["text"] if source else None,
            "status": "ANSWER" if source else "ABSTAIN",
        })
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
