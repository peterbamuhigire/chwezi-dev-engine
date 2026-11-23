"""Replay the offline K4 fixture. All release state exists only within this process."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
from statistics import median

HERE = Path(__file__).parent


def incompatible(bundle):
    reasons = []
    if bundle["transform"]["vocabulary"] != bundle["model"]["vocabulary"]:
        reasons.append("transform.vocabulary")
    base = bundle.get("adapter_base")
    if base and base != bundle["model"]["revision"]:
        reasons.append("adapter.base")
    return reasons


def promote(state, request_id, candidate, *, interrupt=False):
    """Stage components together, then replace the active bundle in one operation."""
    if request_id in state["receipts"]:
        prior = state["receipts"][request_id]
        if prior["requested"] != candidate:
            raise ValueError("promotion ID reused for a different bundle")
        return state, "replay"
    if incompatible(candidate):
        return state, "incompatible"
    staged = deepcopy(candidate)
    if interrupt:
        return state, "interrupted_before_index_promotion"
    receipts = {**state["receipts"], request_id: {"requested": staged, "active": staged["id"]}}
    return {"active": staged, "receipts": receipts}, "published"


def diagnose(f):
    events = {event["id"]: event for event in f["events"]}
    shift = events["data_shift"]
    baseline = median(shift["input_length_reference"])
    current = median(shift["input_length_recent"])
    skew = events["serving_skew"]
    features_differ = skew["training_features"] != skew["serving_features"]
    good, bad = f["bundles"]["G1"], f["bundles"]["G2"]
    if incompatible(good):
        raise ValueError("rollback bundle failed compatibility check")
    # Starting state simulates a candidate selected for promotion; requests are held.
    gated = {"active": deepcopy(good), "receipts": {}}
    pid = f["promotion"]["id"]
    after_bad, bad_result = promote(gated, pid, bad)
    interrupted, interrupt_result = promote(after_bad, pid, good, interrupt=True)
    restored, first = promote(interrupted, pid, good)
    replayed, second = promote(restored, pid, good)
    return {
        "diagnoses": {
            "data": {"class": "input_distribution_shift" if current > baseline * 2 else "threshold_not_crossed",
                     "reference_median": baseline, "recent_median": current,
                     "fixture_rule": "recent median exceeds twice reference median",
                     "labels_due": shift["labels_available_at"], "accuracy": "NOT_ASSESSED"},
            "serving": {"class": "training_serving_skew" if features_differ else "features_match",
                        "record": skew["record_id"], "training": skew["training_features"], "serving": skew["serving_features"]},
            "release": {"mismatched_components": incompatible(bad), "candidate_outcome": bad_result}},
        "promotion_id": pid, "interruption": interrupt_result, "bundle_after_interruption": interrupted["active"],
        "restoration": first, "retry": second, "active_bundle": replayed["active"], "effect_count": len(replayed["receipts"]),
        "owner": f["operator"], "correction": f["user_correction_path"], "decision_time": f["decision_time"],
        "synthetic_latency": f["latency"], "attempts": f["attempts"], "charge": "NOT_ASSESSED"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=HERE / "fixture.json")
    print(json.dumps(diagnose(json.loads(parser.parse_args().fixture.read_bytes())), indent=2))
