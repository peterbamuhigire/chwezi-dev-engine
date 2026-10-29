#!/usr/bin/env python3
"""Fail closed on missing tenant boundaries or known unsafe Next.js examples."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

REQUIRED_FILES = (
    "README.md",
    "api.yaml",
    "php/2026_10_29_create_tenant_invoices.sql",
    "php/invoice-list.php",
    "php/test.php",
    "nextjs/app/invoices/page.tsx",
    "nextjs/app/invoices/route.ts",
    "nextjs/lib/invoices.ts",
    "android/InvoiceListScreen.kt",
)
FORBIDDEN_CODE = (
    re.compile(r"request\.ip\b"),
    re.compile(r"request\.geo\b"),
    re.compile(r"cookies\(\)\.get\(['\"]role['\"]\)"),
    re.compile(r"request\.cookies\.get\(['\"]role['\"]\)"),
    re.compile(r"redis\.(?:get|set)\(['\"]users['\"]"),
    re.compile(r"db\.user\.findMany\(\)"),
    re.compile(r"params:\s*\{\s*slug:\s*string\s*\}"),
)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required example file: {relative}")

    dal_path = root / "nextjs/lib/invoices.ts"
    if dal_path.is_file():
        dal = dal_path.read_text(encoding="utf-8")
        for label, pattern in (
            ("server-only boundary", r"import ['\"]server-only['\"]"),
            ("session authentication", r"auth\(\)"),
            ("current membership check", r"tenantMembership\.findFirst"),
            ("tenant-scoped invoice predicate", r"tenantId:\s*membership\.tenantId"),
            ("explicit DTO projection", r"select:\s*\{"),
            ("read-only page bound", r"take:\s*limit"),
        ):
            if not re.search(pattern, dal):
                errors.append(f"missing {label} in Next.js DAL")
        for pattern in FORBIDDEN_CODE:
            if pattern.search(dal):
                errors.append(f"forbidden pattern in Next.js DAL: {pattern.pattern}")
        if "id: string" not in dal or "amountMinor: string" not in dal:
            errors.append("SQL BIGINT identifiers and amounts must cross the API as decimal strings")
        if dal.count(".toString()") < 2:
            errors.append("SQL BIGINT identifiers and amounts must be serialized explicitly")

    php_path = root / "php/invoice-list.php"
    if php_path.is_file():
        php = php_path.read_text(encoding="utf-8")
        if "'id' => (string) $row['id']" not in php or "'amount_minor' => (string) $row['amount_minor']" not in php:
            errors.append("PHP SQL BIGINT identifiers and amounts must be serialized as decimal strings")

    contract_path = root / "api.yaml"
    if contract_path.is_file():
        contract = contract_path.read_text(encoding="utf-8")
        if "id: { type: string" not in contract or "amount_minor: { type: string" not in contract:
            errors.append("API contract must represent SQL BIGINT identifiers and amounts as strings")

    route_path = root / "nextjs/app/invoices/route.ts"
    if route_path.is_file():
        route = route_path.read_text(encoding="utf-8")
        if "Cache-Control" not in route or "private, no-store" not in route:
            errors.append("private Route Handler response must disable shared caching")
        if "ForbiddenError" not in route or "UnauthenticatedError" not in route:
            errors.append("Route Handler must map unauthenticated and forbidden failures")

    page_path = root / "nextjs/app/invoices/page.tsx"
    if page_path.is_file():
        page = page_path.read_text(encoding="utf-8")
        if not re.search(r"searchParams:\s*Promise<", page):
            errors.append("Next.js 16 page must type asynchronous searchParams")
        if "force-dynamic" not in page:
            errors.append("tenant-specific page must opt out of shared static rendering")

    android_path = root / "android/InvoiceListScreen.kt"
    if android_path.is_file():
        android = android_path.read_text(encoding="utf-8")
        for state in ("Loading", "Denied", "Failed", "Ready"):
            if state not in android:
                errors.append(f"Android example missing {state} state")
        if "val id: String" not in android or "val amountMinor: String" not in android:
            errors.append("Android model must preserve SQL BIGINT identifiers and amounts as strings")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("examples/tenant-invoice-listing"))
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: tenant invoice example files and security invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
