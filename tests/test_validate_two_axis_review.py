import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate_two_axis_review.py"
SPEC = importlib.util.spec_from_file_location("two_axis", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def review(axis_a: str, axis_b: str) -> str:
    return f"""# Review

## Integrated verdict

- Axis A: {axis_a}
- Axis B: {axis_b}
"""


def test_both_axes_must_pass():
    assert MODULE.validate(review("PASS", "PASS")) == ([], "PASS")


def test_spec_pass_standards_fail_is_blocking():
    assert MODULE.validate(review("PASS", "FAIL")) == ([], "FAIL")


def test_standards_pass_spec_fail_is_blocking():
    assert MODULE.validate(review("FAIL", "PASS")) == ([], "FAIL")


def test_not_assessed_and_missing_axis_cannot_pass():
    assert MODULE.validate(review("PASS", "NOT ASSESSED")) == ([], "FAIL")
    findings, overall = MODULE.validate("- Axis A: PASS")
    assert "Axis B verdict is missing or invalid" in findings
    assert overall == "NOT ASSESSED"


def test_duplicate_axis_verdict_cannot_override_a_failure():
    findings, overall = MODULE.validate(review("FAIL", "PASS") + "\n- Axis A: PASS\n")
    assert "Axis A verdict appears more than once" in findings
    assert overall == "NOT ASSESSED"
