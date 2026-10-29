from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXAMPLE = REPO / "examples/tenant-invoice-listing"
VALIDATOR = REPO / "scripts/validate_tenant_invoice_example.py"


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


def test_tenant_invoice_example_passes_normal_path() -> None:
    result = run_validator(EXAMPLE)
    assert result.returncode == 0, result.stderr


def test_tenant_invoice_validator_rejects_missing_tenant_predicate(tmp_path: Path) -> None:
    copied = tmp_path / "tenant-invoice-listing"
    shutil.copytree(EXAMPLE, copied)
    path = copied / "nextjs/lib/invoices.ts"
    path.write_text(
        path.read_text(encoding="utf-8").replace("tenantId: membership.tenantId,", ""),
        encoding="utf-8",
    )
    result = run_validator(copied)
    assert result.returncode == 1
    assert "tenant-scoped invoice predicate" in result.stderr


def test_tenant_invoice_validator_rejects_role_cookie_authority(tmp_path: Path) -> None:
    copied = tmp_path / "tenant-invoice-listing"
    shutil.copytree(EXAMPLE, copied)
    path = copied / "nextjs/lib/invoices.ts"
    with path.open("a", encoding="utf-8") as stream:
        stream.write("\nconst role = request.cookies.get('role')?.value;\n")
    result = run_validator(copied)
    assert result.returncode == 1
    assert "forbidden pattern" in result.stderr


def test_tenant_invoice_validator_rejects_lossy_bigint_json_number(tmp_path: Path) -> None:
    copied = tmp_path / "tenant-invoice-listing"
    shutil.copytree(EXAMPLE, copied)
    path = copied / "nextjs/lib/invoices.ts"
    source = path.read_text(encoding="utf-8").replace("amountMinor: string", "amountMinor: number")
    path.write_text(source, encoding="utf-8")
    result = run_validator(copied)
    assert result.returncode == 1
    assert "decimal strings" in result.stderr


def test_tenant_invoice_validator_rejects_unbounded_next_query(tmp_path: Path) -> None:
    copied = tmp_path / "tenant-invoice-listing"
    shutil.copytree(EXAMPLE, copied)
    path = copied / "nextjs/app/invoices/route.ts"
    source = path.read_text(encoding="utf-8").replace("status: 400", "status: 200")
    path.write_text(source, encoding="utf-8")
    result = run_validator(copied)
    assert result.returncode == 1
    assert "return 400" in result.stderr


def test_tenant_invoice_validator_requires_manual_review_exercise(tmp_path: Path) -> None:
    copied = tmp_path / "tenant-invoice-listing"
    shutil.copytree(EXAMPLE, copied)
    (copied / "review-exercise.md").unlink()
    result = run_validator(copied)
    assert result.returncode == 1
    assert "review-exercise.md" in result.stderr
