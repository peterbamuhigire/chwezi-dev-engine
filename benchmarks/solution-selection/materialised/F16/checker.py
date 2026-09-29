"""F16 checker: a new dependency only when justified; grapheme-aware cursor (stdlib only, no model call).

Runs the produced ``text/cursor.js`` under Node.js against a frozen grapheme corpus (boundaries
frozen from UAX #29 as implemented by ICU 77 / Unicode 16, then hand-checked), including a run with
``Intl.Segmenter`` removed to prove the support boundary is explicit rather than silently wrong.
Also checks the dependency decision record.

    python checker.py <workspace> [--withheld <dir>]
Exit 0 PASS, 1 FAIL, 2 NOT_ASSESSED (node missing).
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

FIXTURE = "F16"

# text -> grapheme start offsets (UTF-16 code units); the end is len(text) in UTF-16.
CORPUS = [
    ("Kampala", [0, 1, 2, 3, 4, 5, 6]),
    ("éx", [0, 2]),
    ("\U0001F468‍\U0001F469‍\U0001F467!", [0, 8]),
    ("\U0001F1FA\U0001F1EC\U0001F1F0\U0001F1EA", [0, 4]),
    ("\U0001F44D\U0001F3FDok", [0, 4, 5]),
    ("각", [0]),
    ("a\r\nb", [0, 1, 3]),
]

HARNESS = r"""
'use strict';
const [cursorPath, mode] = process.argv.slice(2);
if (mode === 'nosegmenter') { delete Intl.Segmenter; }
const input = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
let cursor;
try { cursor = require(cursorPath); } catch (error) {
  console.log(JSON.stringify({ loadError: String(error && error.message), code: error && error.code })); process.exit(0);
}
const out = [];
for (const text of input) {
  try {
    const count = cursor.graphemeCount(text);
    const next = [], prev = [];
    for (let i = 0; i <= text.length; i += 1) { next.push(cursor.nextBoundary(text, i)); prev.push(cursor.prevBoundary(text, i)); }
    const slices = [];
    for (let g = 0; g < count; g += 1) slices.push(cursor.sliceGraphemes(text, g, g + 1));
    out.push({ count, next, prev, slices });
  } catch (error) { out.push({ error: String(error && error.message), code: error && error.code }); }
}
console.log(JSON.stringify(out));
"""


def utf16_len(text: str) -> int:
    return len(text.encode("utf-16-le")) // 2


def utf16_slice(text: str, start: int, end: int) -> str:
    return text.encode("utf-16-le")[start * 2:end * 2].decode("utf-16-le")


def expected_for(text: str, starts: list[int]) -> dict:
    length = utf16_len(text)
    marks = starts + [length]
    nxt = [next((m for m in marks if m > i), length) for i in range(length + 1)]
    prv = [max([m for m in marks if m < i], default=0) for i in range(length + 1)]
    slices = [utf16_slice(text, marks[g], marks[g + 1]) for g in range(len(starts))]
    return {"count": len(starts), "next": nxt, "prev": prv, "slices": slices}


def run_harness(node: str, workspace: Path, mode: str, texts: list[str]):
    with tempfile.TemporaryDirectory(prefix="f16-") as tmp:
        harness = Path(tmp) / "harness.js"
        harness.write_text(HARNESS, encoding="utf-8")
        try:
            proc = subprocess.run([node, str(harness), str(workspace / "text" / "cursor.js"), mode],
                                  input=json.dumps(texts), capture_output=True, text=True, encoding="utf-8", timeout=20)
        except subprocess.TimeoutExpired:
            return None, "timed out"
    if proc.returncode != 0 or not proc.stdout.strip():
        return None, (proc.stderr or proc.stdout)[-800:]
    return json.loads(proc.stdout.strip().splitlines()[-1]), None


def decision_record(workspace: Path) -> tuple[bool, str]:
    candidates = [workspace / "DEPENDENCY-DECISION.md", workspace / "docs" / "DEPENDENCY-DECISION.md"]
    record = next((p for p in candidates if p.is_file()), None)
    if record is None:
        return False, "DEPENDENCY-DECISION.md missing"
    text = record.read_text(encoding="utf-8").lower()
    required = {"alternatives": r"alternative", "licence/licence evidence": r"licen[cs]e", "version evidence": r"version",
                "support boundary": r"support(ed)? (boundary|runtime|matrix)|supported:", "removal trigger": r"removal trigger|revisit"}
    missing = [name for name, pattern in required.items() if not re.search(pattern, text)]
    try:
        deps = json.loads((workspace / "package.json").read_text(encoding="utf-8")).get("dependencies", {}) or {}
    except (OSError, ValueError):
        deps = {}
    unjustified = [name for name in deps if name.lower() not in text]
    ok = not missing and not unjustified
    return ok, {"missing_fields": missing, "dependencies_not_justified": unjustified}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--withheld", type=Path)
    args = parser.parse_args(argv)
    workspace = args.workspace.resolve()
    node = shutil.which("node")
    if node is None:
        print(json.dumps({"fixture": FIXTURE, "status": "NOT_ASSESSED", "checks": [], "reason": "node is not on PATH"}))
        return 2
    checks = []
    texts = [text for text, _ in CORPUS]
    got, err = run_harness(node, workspace, "native", texts)
    if isinstance(got, dict):
        err, got = f"module failed to load: {got}", None
    for field, check_id in (("count", "grapheme-count-frozen-corpus"), ("next", "next-boundary-never-splits"),
                            ("prev", "prev-boundary-never-splits"), ("slices", "selection-slices-whole-graphemes")):
        failures = []
        for index, (text, starts) in enumerate(CORPUS):
            expected = expected_for(text, starts)[field]
            actual = got[index].get(field) if got and index < len(got) else None
            if actual != expected:
                failures.append({"text": text.encode("unicode_escape").decode(), "expected": expected, "got": actual})
        checks.append({"id": check_id, "passed": err is None and not failures, "detail": err or failures})

    got, err = run_harness(node, workspace, "nosegmenter", texts)
    if isinstance(got, dict):  # failed at load time: acceptable only as the explicit boundary
        ok = got.get("code") == "ERR_GRAPHEME_UNSUPPORTED"
        detail = got
    elif got:
        ok = all(item.get("code") == "ERR_GRAPHEME_UNSUPPORTED" or item == expected_for(text, starts)
                 for item, (text, starts) in zip(got, CORPUS))
        detail = "explicit ERR_GRAPHEME_UNSUPPORTED or correct fallback" if ok else "silently wrong boundaries without Intl.Segmenter"
    else:
        ok, detail = False, err
    checks.append({"id": "unsupported-runtime-boundary", "passed": ok, "detail": detail})

    ok, detail = decision_record(workspace)
    checks.append({"id": "dependency-decision-recorded", "passed": ok, "detail": detail})

    if args.withheld and args.withheld.is_dir():
        for test in sorted(args.withheld.glob("test_*.js")):
            try:
                proc = subprocess.run([node, str(test), str(workspace)], capture_output=True, text=True, encoding="utf-8", timeout=60)
                checks.append({"id": f"withheld:{test.name}", "passed": proc.returncode == 0, "detail": proc.stdout[-800:]})
            except subprocess.TimeoutExpired:
                checks.append({"id": f"withheld:{test.name}", "passed": False, "detail": "timed out"})

    status = "PASS" if all(c["passed"] for c in checks) else "FAIL"
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks}, ensure_ascii=True, default=str))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
