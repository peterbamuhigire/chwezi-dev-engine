import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills/sdlc-meta/systematic-bug-diagnosis/scripts/diagnostic_gate.py"
SPEC = importlib.util.spec_from_file_location("diagnostic_gate", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def record(**overrides):
    value = {
        "symptom": "Saving a valid record returns 500.",
        "environment": "test build 42",
        "red_capable": True,
        "red_observed": True,
        "case": "normal",
        "cause_claimed": False,
        "fix_authority": False,
    }
    value.update(overrides)
    return value


def test_normal_case_routes_to_experiment_then_authorised_fix():
    assert MODULE.evaluate(record()) == ([], "run-discriminating-experiment")
    assert MODULE.evaluate(record(cause_claimed=True, fix_authority=True)) == ([], "handoff-for-fix")


def test_causal_claim_before_observed_red_fails():
    findings, action = MODULE.evaluate(record(red_observed=False, cause_claimed=True))
    assert any("causal claim requires" in finding for finding in findings)
    assert action == "stop"


def test_missing_environment_fails():
    findings, _ = MODULE.evaluate(record(environment=""))
    assert "environment must be non-empty text" in findings


def test_intermittent_and_performance_cases_require_measurement_boundaries():
    findings, _ = MODULE.evaluate(record(case="intermittent"))
    assert any("reproduction_rate" in finding for finding in findings)
    findings, _ = MODULE.evaluate(record(case="performance"))
    assert any("comparison_boundary" in finding for finding in findings)


def test_production_only_instrumentation_requires_authority():
    findings, action = MODULE.evaluate(record(case="production-only"))
    assert any("telemetry_authority" in finding for finding in findings)
    assert action == "stop"


def test_string_booleans_cannot_bypass_the_gate():
    findings, action = MODULE.evaluate(record(red_capable="false"))
    assert "red_capable must be boolean" in findings
    assert action == "stop"
