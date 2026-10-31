"""Routing fixture coverage: the per-skill measure and its ratchet."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import routing_smoke_test as rst  # noqa: E402

CATALOGUE = {slug: {"name": slug, "description": "d"} for slug in ("a", "b", "c", "d")}


def fixtures():
    return [
        {"task": "t1", "expect": "a", "negatives": [{"task": "n1", "owner": "b"}, {"task": "n2", "owner": "c"}]},
        {"task": "t2", "expect": "a"},
        {"task": "t3", "expect": "a"},
        {"task": "t4", "expect": "b", "negatives": [{"task": "n3"}]},
        {"task": "t5", "expect": "ghost"},  # not an active skill: ignored
    ]


def test_coverage_counts_positives_owned_negatives_and_full_skills():
    report = rst.coverage(CATALOGUE, fixtures())
    assert report["skills"] == 4
    assert report["zero_positive"] == ["c", "d"]
    assert report["with_positive"] == 2
    assert report["with_owned_negative"] == 1  # only "a"; the negative on "b" names no owner
    assert report["full"] == ["a"]


def test_ratchet_fails_above_the_ceiling_and_passes_at_it(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rst, "read_catalogue", lambda base=None: CATALOGUE)
    monkeypatch.setattr(rst, "load_fixtures", lambda files=None: fixtures())
    assert rst.show_coverage(2) == 0
    assert rst.show_coverage(1) == 1
    assert "RATCHET" in capsys.readouterr().out
    assert rst.show_coverage(None) == 0


def test_repository_ceiling_and_command_line():
    report = rst.coverage(rst.read_catalogue(ROOT), rst.load_fixtures())
    assert len(report["zero_positive"]) <= 1, report["zero_positive"]
    script = str(ROOT / "scripts" / "routing_smoke_test.py")
    ok = subprocess.run([sys.executable, script, "--coverage", "--max-zero-positive", "1"], capture_output=True, text=True)
    too_tight = subprocess.run([sys.executable, script, "--coverage", "--max-zero-positive", "0"], capture_output=True, text=True)
    assert ok.returncode == 0 and too_tight.returncode == 1
