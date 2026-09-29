"""Tests for the routing smoke test extensions (M10-03 T03, T04, T05, T11)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "routing_smoke_test.py"
SPEC = importlib.util.spec_from_file_location("routing_smoke_test", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
routing = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = routing
SPEC.loader.exec_module(routing)


def write_skill(base: Path, slug: str, description: str) -> None:
    folder = base / "skills" / "group" / slug
    folder.mkdir(parents=True)
    text = "---\n" + f"name: {slug}\n" + f"description: {description}\n" + "---\n\n" + f"# {slug}\n"
    (folder / "SKILL.md").write_text(text, encoding="utf-8")


def catalogue(base: Path) -> None:
    write_skill(base, "invoice-matching", "Use when reconciling supplier invoices against purchase orders and goods received notes.")
    write_skill(base, "kitchen-rota", "Use when planning restaurant kitchen shift rotas, staff breaks and cover.")
    write_skill(base, "tax-returns", "Use when filing annual corporate income tax returns with statutory schedules.")


def write_fixtures(base: Path, body: str) -> Path:
    path = base / "fixtures.yml"
    path.write_text(body, encoding="utf-8")
    return path


def test_owned_negative_fails_when_owner_ranks_below_self(tmp_path, capsys):
    catalogue(tmp_path)
    fixtures = write_fixtures(
        tmp_path,
        'fixtures:\n  - task: "Plan kitchen shift rotas for the restaurant"\n    expect: kitchen-rota\n'
        "    negatives:\n"
        '      - task: "Reconcile supplier invoices and purchase orders for the restaurant kitchen"\n'
        "        owner: tax-returns\n",
    )
    code = routing.run_fixtures(False, base=tmp_path, fixture_files=(fixtures,))
    assert code == 1
    assert "does not outrank" in capsys.readouterr().out


def test_owned_negative_passes_when_owner_outranks_self(tmp_path):
    catalogue(tmp_path)
    fixtures = write_fixtures(
        tmp_path,
        'fixtures:\n  - task: "Plan kitchen shift rotas for the restaurant"\n    expect: kitchen-rota\n'
        "    negatives:\n"
        '      - task: "File the annual corporate income tax return for the restaurant"\n'
        "        owner: tax-returns\n",
    )
    assert routing.run_fixtures(False, base=tmp_path, fixture_files=(fixtures,)) == 0


def test_cross_engine_owner_is_not_assessed_locally():
    status, _detail = routing.check_negative("a", {"task": "x", "owner": "chwezi-sdlc-documentation/02-business-case"}, [("a", 0.9)])
    assert status == "NOT_ASSESSED"


def test_min_rank1_floor_fails_below_floor(tmp_path, capsys):
    catalogue(tmp_path)
    fixtures = write_fixtures(
        tmp_path,
        # The expected skill is in the top 3 but not first, so precision@1 is 0%.
        'fixtures:\n  - task: "Reconcile supplier invoices against purchase orders before the tax return"\n    expect: tax-returns\n',
    )
    assert routing.run_fixtures(False, min_rank1=50, base=tmp_path, fixture_files=(fixtures,)) == 1
    assert "RATCHET" in capsys.readouterr().out


def test_lint_rejects_slug_and_description_copy():
    assert routing.lint_prompt("Use the kitchen rota skill", "kitchen-rota", "")
    assert routing.lint_prompt("Write the business case", "02-business-case", "")
    description = "Use when reconciling supplier invoices against purchase orders and goods received notes."
    assert any("description-copy" in f for f in routing.lint_prompt("reconciling supplier invoices against purchase orders", "invoice-matching", description))
    assert routing.lint_prompt("Match last month's bills to what we ordered", "invoice-matching", description) == []


def test_collision_gate_fails_on_duplicate_description(tmp_path):
    catalogue(tmp_path)
    write_skill(tmp_path, "invoice-matching-copy", "Use when reconciling supplier invoices against purchase orders and goods received notes.")
    allow = tmp_path / "allow.yml"
    allow.write_text("pairs: []\n", encoding="utf-8")
    assert routing.show_collisions(0.5, 40, gate=True, base=tmp_path, allowlist=allow) == 1


def test_collision_gate_honours_allowlist(tmp_path):
    catalogue(tmp_path)
    write_skill(tmp_path, "invoice-matching-copy", "Use when reconciling supplier invoices against purchase orders and goods received notes.")
    allow = tmp_path / "allow.yml"
    allow.write_text(
        "pairs:\n  - pair: [invoice-matching, invoice-matching-copy]\n    reason: test\n    decided_on: 2026-09-29\n",
        encoding="utf-8",
    )
    assert routing.show_collisions(0.5, 40, gate=True, base=tmp_path, allowlist=allow) == 0


def test_live_catalogue_passes_gate_lint_and_negatives():
    assert routing.run_fixtures(False, min_rank1=88, lint=True) == 0
    assert routing.show_collisions(0.5, 40, gate=True) == 0
