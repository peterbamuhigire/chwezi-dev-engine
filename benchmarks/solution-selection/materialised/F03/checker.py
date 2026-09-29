"""F03 checker: mature installed dependency (stdlib Python driving node; no model call).

Runs the produced order import/export under node against adversarial CSV: quoted separators,
embedded line breaks with correct source-line numbers, a leading BOM, escaped quotes, wrong column
counts, oversized records and input, invalid amounts, and spreadsheet formula injection in the
export. Also checks that the installed parser is reused (or a better alternative documented).

    python checker.py <workspace> [--withheld <dir>]

Exit 0 PASS, 1 FAIL, 2 NOT_ASSESSED (node is not installed). Prints one JSON object.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FIXTURE = "F03"

DRIVER = r'''
'use strict';
const path = require('path');
const ws = process.argv[2];
const results = [];
function check(id, fn) {
  try { const [ok, detail] = fn(); results.push({ id, passed: !!ok, detail: String(detail).slice(0, 400) }); }
  catch (e) { results.push({ id, passed: false, detail: `${e && e.name}: ${e && e.message}`.slice(0, 400) }); }
}
const mod = require(path.join(ws, 'routes', 'orders-import.js'));
const H = 'order_id,customer_id,amount,note';

// Independent reader for the exported sheet (RFC 4180), so the check does not trust the workspace parser.
function readSheet(text) {
  const rows = []; let row = []; let field = ''; let q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else q = false; } else field += c; continue; }
    if (c === '"' && field === '') { q = true; continue; }
    if (c === ',') { row.push(field); field = ''; continue; }
    if (c === '\r' && text[i + 1] === '\n') continue;
    if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; continue; }
    field += c;
  }
  if (field !== '' || row.length) { row.push(field); rows.push(row); }
  return rows;
}

check('quoted_separator', () => {
  const { rows, errors } = mod.importOrders(`${H}\n"O-1","C-1","1.00","Plot 4, Kampala"\n`);
  return [errors.length === 0 && rows.length === 1 && rows[0].note === 'Plot 4, Kampala', JSON.stringify({ rows, errors })];
});

check('embedded_newline_and_source_lines', () => {
  const text = `${H}\nO-1,C-1,1.00,"multi\nline note"\nO-2,C-2,2.00\nO-3,C-3,3.00,ok\n`;
  const { rows, errors } = mod.importOrders(text);
  const ok = rows.length === 2 && rows[0].order_id === 'O-1' && rows[0].note === 'multi\nline note' && rows[1].order_id === 'O-3'
    && errors.length === 1 && errors[0].line === 4;
  return [ok, JSON.stringify({ rows, errors })];
});

check('bom_and_crlf', () => {
  const { rows, errors } = mod.importOrders(`﻿${H}\r\nO-1,C-1,1.00,x\r\nO-2,C-2,2.00,y\r\n`);
  return [errors.length === 0 && rows.length === 2 && rows[0].note === 'x' && rows[1].note === 'y', JSON.stringify({ rows, errors })];
});

check('escaped_quotes', () => {
  const { rows, errors } = mod.importOrders(`${H}\nO-1,C-1,1.00,"He said ""urgent"""\nO-2,C-2,2.00,""\n`);
  return [errors.length === 0 && rows.length === 2 && rows[0].note === 'He said "urgent"' && rows[1].note === '', JSON.stringify({ rows, errors })];
});

check('wrong_column_count_rejected_with_line', () => {
  const { rows, errors } = mod.importOrders(`${H}\nO-1,C-1,1.00,a,extra\nO-2,C-2\nO-3,C-3,3.00,ok\n`);
  const lines = errors.map((e) => e.line).sort();
  return [rows.length === 1 && rows[0].order_id === 'O-3' && JSON.stringify(lines) === '[2,3]', JSON.stringify({ rows, lines })];
});

check('oversized_record_rejected', () => {
  const { rows, errors } = mod.importOrders(`${H}\nO-1,C-1,1.00,${'a'.repeat(5000)}\nO-2,C-2,2.00,ok\n`);
  return [rows.length === 1 && rows[0].order_id === 'O-2' && errors.some((e) => e.line === 2), JSON.stringify({ n: rows.length, errors })];
});

check('oversized_input_refused_quickly', () => {
  const big = `${H}\nO-1,C-1,1.00,${'b'.repeat(1100000)}\n`;
  const t = Date.now();
  const { rows, errors } = mod.importOrders(big);
  const ms = Date.now() - t;
  return [rows.length === 0 && errors.length > 0 && ms < 2000, `rows=${rows.length} errors=${errors.length} ms=${ms}`];
});

check('invalid_amounts_rejected', () => {
  const bad = ['12.345', '1e3', '-5.00', '', 'NaN', '0x10', '1,00'];
  const text = `${H}\n` + bad.map((a, i) => `O-${i},C-${i},"${a}",n`).join('\n') + '\n';
  const { rows, errors } = mod.importOrders(text);
  const good = mod.importOrders(`${H}\nA,C,0.29,n\nB,C,12,n\nD,C,12.5,n\n`);
  const minors = good.rows.map((r) => r.amount_minor);
  return [rows.length === 0 && errors.length === bad.length && JSON.stringify(minors) === '[29,1200,1250]', `accepted=${JSON.stringify(rows.map((r) => r.amount_minor))} minors=${minors}`];
});

check('formula_injection_neutralised', () => {
  const notes = ['=HYPERLINK("http://example.invalid","x")', '+1+1', '-2+3', '@SUM(A1:A2)', '\t=1', '\r=2'];
  const input = notes.map((note, i) => ({ order_id: `O-${i}`, customer_id: i === 0 ? '=cmd|x' : `C-${i}`, amount_minor: 100 + i, note }));
  const sheet = readSheet(mod.exportOrdersSheet(input));
  const body = sheet.slice(1);
  const shapeOk = sheet[0].join(',') === H && body.length === notes.length && body.every((r) => r.length === 4);
  const dangerous = body.flatMap((r) => [r[0], r[1], r[3]]).filter((c) => /^[=+\-@\t\r]/.test(c));
  return [shapeOk && dangerous.length === 0, `shape ok=${shapeOk}; dangerous cells=${JSON.stringify(dangerous)}`];
});

check('export_quoting_round_trip', () => {
  const notes = ['Plot 4, Kampala', 'He said "urgent"', 'line one\nline two', 'plain'];
  const input = notes.map((note, i) => ({ order_id: `O-${i}`, customer_id: `C-${i}`, amount_minor: 1205 + i, note }));
  const sheet = readSheet(mod.exportOrdersSheet(input)).slice(1);
  const ok = sheet.length === notes.length && sheet.every((r, i) => r[3] === notes[i] && r[2] === `12.0${5 + i}`);
  return [ok, JSON.stringify(sheet)];
});

check('existing_route_unaffected', () => {
  const { importCustomers } = require(path.join(ws, 'routes', 'customers-import.js'));
  const { rows, errors } = importCustomers('customer_id,name,phone\nC-1,"Akello, Grace",+256700000001\n');
  return [errors.length === 0 && rows.length === 1 && rows[0].name === 'Akello, Grace', JSON.stringify({ rows, errors })];
});

process.stdout.write('@@RESULTS@@' + JSON.stringify(results));
'''


def run(cmd, cwd, timeout=120):
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return None, "", f"timed out after {timeout}s"


def driver_checks(node: str, ws: Path) -> list[dict]:
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "driver.js"
        script.write_text(DRIVER, encoding="utf-8")
        rc, out, err = run([node, str(script), str(ws)], ws)
    if "@@RESULTS@@" not in out:
        return [{"id": "driver", "passed": False, "detail": (err or out)[-600:] or f"exit {rc}"}]
    return json.loads(out.split("@@RESULTS@@", 1)[1].strip())


def static_checks(ws: Path) -> list[dict]:
    route = ws / "routes" / "orders-import.js"
    source = route.read_text(encoding="utf-8") if route.is_file() else ""
    reused = bool(re.search(r"require\(\s*['\"]\.\./lib/csv-parse(\.js)?['\"]\s*\)", source))
    documented = (ws / "docs" / "csv-parser-decision.md").is_file()
    return [{"id": "installed_parser_reused_or_alternative_documented", "passed": reused or documented,
             "detail": f"requires lib/csv-parse={reused}; docs/csv-parser-decision.md={documented}"}]


def node_tests(node: str, ws: Path, files: list[str], check_id: str) -> dict:
    rc, out, err = run([node, "--test", *files], ws, 240)
    return {"id": check_id, "passed": rc == 0, "detail": (out + err)[-400:]}


def withheld_tests(node: str, ws: Path, withheld: Path) -> dict:
    dest = ws / "_withheld_tests"
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(withheld, dest, ignore=shutil.ignore_patterns(".gitignore"))
    try:
        files = sorted(p.relative_to(ws).as_posix() for p in dest.glob("*.test.js"))
        return node_tests(node, ws, files, "withheld_tests")
    finally:
        shutil.rmtree(dest, ignore_errors=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--withheld", type=Path)
    args = parser.parse_args(argv)
    ws = args.workspace.resolve()
    node = shutil.which("node")
    if node is None:
        print(json.dumps({"fixture": FIXTURE, "status": "NOT_ASSESSED", "checks": [], "reason": "node is not installed"}))
        return 2
    checks = [node_tests(node, ws, ["public_tests/orders-import.test.js"], "public_tests"), *driver_checks(node, ws), *static_checks(ws)]
    if args.withheld and args.withheld.is_dir():
        checks.append(withheld_tests(node, ws, args.withheld))
    status = "PASS" if checks and all(c["passed"] for c in checks) else "FAIL"
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks}, ensure_ascii=False, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
