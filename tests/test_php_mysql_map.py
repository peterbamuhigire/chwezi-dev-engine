"""Tests for skills/sdlc-meta/ai-assisted-development/scripts/php_mysql_map.py."""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "sdlc-meta" / "ai-assisted-development" / "scripts" / "php_mysql_map.py"
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "php-mysql-map"
SPEC = importlib.util.spec_from_file_location("php_mysql_map", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

EXPECTED = {
    "GET /invoices -> InvoiceController@index": {"invoices", "invoice_items"},
    "POST /customers -> CustomerController@store": {"customers", "audit_log"},
    "PUT /products/{id} -> ProductController@update": {"products", "stock_movements"},
    "POST /payments -> PaymentController@store": {"payments", "ledger_entries"},
    "GET /reports/ledger -> ReportController@ledger": {"ledger_entries", "customers"},
}


def run_map(root: Path, tmp_path: Path, *extra: str) -> dict:
    out = tmp_path / "map.json"
    assert MODULE.main(["--root", str(root), "--json", str(out), *extra]) == 0
    return json.loads(out.read_text(encoding="utf-8"))


def test_fixture_every_route_table_edge_is_extracted(tmp_path: Path) -> None:
    data = run_map(FIXTURE, tmp_path)
    assert data["known_tables"] == 8
    assert set(data["routes"]) == set(EXPECTED)
    for route, tables in EXPECTED.items():
        got = data["routes"][route]
        assert set(got) == tables, route
        assert {info["tag"] for info in got.values()} == {"EXTRACTED"}, route


def test_what_touches_table_goes_through_service_and_procedure(tmp_path: Path) -> None:
    data = run_map(FIXTURE, tmp_path)
    assert data["tables"]["ledger_entries"] == [
        "GET /reports/ledger -> ReportController@ledger [EXTRACTED]",
        "POST /payments -> PaymentController@store [EXTRACTED]",
    ]
    # a plain grep for the table name in PHP misses the payment route (it only names the procedure)
    php_hits = [p for p in FIXTURE.rglob("*.php") if "ledger_entries" in p.read_text(encoding="utf-8") and "migrations" not in p.parts]
    assert [p.name for p in php_hits] == ["ReportController.php"]


def test_output_is_deterministic(tmp_path: Path) -> None:
    a = run_map(FIXTURE, tmp_path)
    b = run_map(FIXTURE, tmp_path)
    assert a == b


@pytest.fixture()
def dynamic_app(tmp_path: Path) -> Path:
    root = tmp_path / "app"
    shutil.copytree(FIXTURE, root)
    (root / "public" / "api").mkdir(parents=True)
    (root / "routes").rename(root / "routes-disabled")  # force file-routed mode
    (root / "public" / "api" / "concat.php").write_text(
        "<?php\n$prefix = 't1_';\n$sql = \"SELECT * FROM \" . $prefix . \"invoices WHERE id = ?\";\n",
        encoding="utf-8",
    )
    (root / "public" / "api" / "variable.php").write_text(
        "<?php\n$table = $_GET['t'];\n$sql = \"SELECT * FROM {$table}\";\n", encoding="utf-8"
    )
    (root / "public" / "api" / "literal.php").write_text(
        "<?php\n$sql = 'UPDATE `payments` SET status = ? WHERE id = ?';\n", encoding="utf-8"
    )
    return root


def test_tags_for_concatenated_and_variable_names(dynamic_app: Path, tmp_path: Path) -> None:
    data = run_map(dynamic_app, tmp_path, "--routes", "files")
    routes = data["routes"]
    assert routes["public/api/concat.php"]["invoices"]["tag"] == "INFERRED"
    variable = routes["public/api/variable.php"]
    assert variable and all(info["tag"] == "AMBIGUOUS" for info in variable.values())
    assert routes["public/api/literal.php"] == {
        "payments": {"tag": "EXTRACTED", "evidence": ["public/api/literal.php:2"]}
    }


def test_read_only_on_target(tmp_path: Path) -> None:
    root = tmp_path / "copy"
    shutil.copytree(FIXTURE, root)
    before = sorted((p.relative_to(root).as_posix(), p.stat().st_mtime_ns) for p in root.rglob("*"))
    run_map(root, tmp_path)
    after = sorted((p.relative_to(root).as_posix(), p.stat().st_mtime_ns) for p in root.rglob("*"))
    assert before == after


def test_cli_table_query() -> None:
    res = subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), "--root", str(FIXTURE), "--table", "payments"],
        capture_output=True, text=True, check=True,
    )
    assert "table payments: 1 route(s)" in res.stdout
    assert "POST /payments -> PaymentController@store [EXTRACTED]" in res.stdout
