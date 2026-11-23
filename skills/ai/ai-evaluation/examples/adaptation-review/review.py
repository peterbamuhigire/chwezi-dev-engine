"""Offline metadata checks for the synthetic E03 model review fixture."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent


def review(data: dict) -> dict:
    candidate = data["candidate"]
    compatibility_failures = []
    if candidate.get("adapter_base_revision") != candidate.get("model_revision"):
        compatibility_failures.append("adapter_base_revision_mismatch")
    if candidate.get("adapter_tokenizer_revision") != candidate.get("tokenizer_revision"):
        compatibility_failures.append("adapter_tokenizer_revision_mismatch")

    by_digest: dict[str, list[str]] = defaultdict(list)
    excluded_rights = []
    low_fidelity = []
    changed_sampler = []
    for output in data.get("outputs", []):
        by_digest[output["sha256"]].append(output["id"])
        if output.get("rights_status") != "verified":
            excluded_rights.append(output["id"])
        if output.get("fidelity_score", 0) < data["fidelity_review_threshold"]:
            low_fidelity.append(output["id"])
        if output.get("sampler_revision") != candidate.get("sampler_revision"):
            changed_sampler.append(output["id"])

    decision = candidate["decision"]
    return {
        "adapter_accepted": not compatibility_failures,
        "compatibility_failures": compatibility_failures,
        "duplicate_output_groups": [ids for ids in by_digest.values() if len(ids) > 1],
        "exclude_from_training_or_publication": excluded_rights,
        "low_fidelity_for_reviewer": low_fidelity,
        "sampler_revision_changed": changed_sampler,
        "decision": decision,
        "quality_claim": "NOT_ASSESSED" if decision["quality_status"] != "ASSESSED" else "requires_review_receipt",
        "inference_claim": "NOT_ASSESSED" if decision["inference_status"] != "RUN" else "requires_runtime_receipt",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=HERE / "fixture.json")
    args = parser.parse_args()
    data = json.loads(args.fixture.read_text(encoding="utf-8"))
    print(json.dumps(review(data), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
