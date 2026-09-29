"""F09 checker: accessible confirmation dialog (stdlib only, no model call).

1. Parses web/confirm-dialog.html with html.parser: dialog role and modality, accessible name and
   description that resolve to non-empty elements, an announced error region, real buttons.
2. Runs web/dialog-controller.js under Node.js with the checker's own fake DOM (the public test
   helper is not trusted) through adversarial keyboard and failure paths: Escape while busy,
   double confirm, failure then retry, removed trigger.

Manual assistive-technology checks stay NOT_ASSESSED (see fixture.json manual_checks).

    python checker.py <workspace> [--withheld <dir>]
Exit 0 PASS, 1 FAIL, 2 NOT_ASSESSED (node missing).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path

FIXTURE = "F09"

FAKE_DOM = r"""
'use strict';
class El {
  constructor(doc, id, parent = null) { this.ownerDocument = doc; this.id = id; this.parent = parent; this.hidden = false;
    this._disabled = false; this._connected = true; this.attributes = {}; this.textContent = ''; }
  get isConnected() { for (let n = this; n; n = n.parent) if (!n._connected) return false; return true; }
  get disabled() { return this._disabled; }
  set disabled(v) { this._disabled = Boolean(v); if (this._disabled && this.ownerDocument.activeElement === this) this.ownerDocument.activeElement = this.ownerDocument.body; }
  setAttribute(k, v) { this.attributes[k] = String(v); }
  getAttribute(k) { return k in this.attributes ? this.attributes[k] : null; }
  removeAttribute(k) { delete this.attributes[k]; }
  hasAttribute(k) { return k in this.attributes; }
  contains(o) { for (let n = o; n; n = n.parent) if (n === this) return true; return false; }
  focus() { if (!this.isConnected || this._disabled) return; for (let n = this; n; n = n.parent) if (n.hidden) return; this.ownerDocument.activeElement = this; }
  remove() { this._connected = false; if (this.contains(this.ownerDocument.activeElement)) this.ownerDocument.activeElement = this.ownerDocument.body; }
  addEventListener() {} removeEventListener() {}
}
function page() {
  const doc = { body: null, activeElement: null };
  doc.body = new El(doc, 'body'); doc.activeElement = doc.body;
  const main = new El(doc, 'main', doc.body);
  const p = { doc, heading: new El(doc, 'page-heading', main), trigger: new El(doc, 'delete-account', main), dialog: new El(doc, 'confirm-dialog', main) };
  p.dialog.hidden = true;
  p.title = new El(doc, 'confirm-title', p.dialog); p.error = new El(doc, 'confirm-error', p.dialog);
  p.ok = new El(doc, 'confirm-ok', p.dialog); p.cancel = new El(doc, 'confirm-cancel', p.dialog);
  doc.getElementById = (id) => [p.heading, p.trigger, p.dialog, p.title, p.error, p.ok, p.cancel].find((e) => e.id === id) || null;
  return p;
}
function deferred() { let resolve, reject; const promise = new Promise((a, b) => { resolve = a; reject = b; }); return { promise, resolve, reject }; }
const tick = () => new Promise((r) => setImmediate(r));
function setup(controllerPath, script) {
  const { createConfirmDialog } = require(controllerPath);
  const p = page();
  let n = 0;
  const calls = [];
  const pending = [];
  const c = createConfirmDialog({ document: p.doc, trigger: p.trigger, dialog: p.dialog, confirmButton: p.ok, cancelButton: p.cancel,
    errorRegion: p.error, fallbackFocus: p.heading, makeKey: () => `op-${(n += 1)}`,
    perform: (key) => { calls.push(key); const step = script.shift() || 'ok'; if (step === 'ok') return Promise.resolve();
      if (step === 'fail') return Promise.reject(new Error('503 from server')); const d = deferred(); pending.push(d); return d.promise; } });
  p.trigger.focus();
  return { p, c, calls, pending };
}
const esc = { key: 'Escape', preventDefault() {} };
const scenarios = {
  'focus-enters-dialog': async (cp) => { const { p, c } = setup(cp, []); c.open();
    return [!p.dialog.hidden && p.dialog.contains(p.doc.activeElement), p.doc.activeElement.id]; },
  'cancel-returns-focus-to-trigger': async (cp) => { const { p, c } = setup(cp, []); c.open(); c.cancel();
    return [p.dialog.hidden && p.doc.activeElement === p.trigger, p.doc.activeElement.id]; },
  'escape-closes-when-idle': async (cp) => { const { p, c } = setup(cp, []); c.open(); c.handleKeydown(esc);
    return [p.dialog.hidden && p.doc.activeElement === p.trigger, p.doc.activeElement.id]; },
  'busy-state-disables-and-marks-dialog': async (cp) => { const { p, c, pending } = setup(cp, ['hold']); c.open(); const run = c.confirm(); await tick();
    const ok = p.ok.disabled && p.cancel.disabled && p.dialog.getAttribute('aria-busy') === 'true';
    const detail = { okDisabled: p.ok.disabled, cancelDisabled: p.cancel.disabled, ariaBusy: p.dialog.getAttribute('aria-busy') };
    pending.forEach((d) => d.resolve()); await run; return [ok, detail]; },
  'escape-ignored-while-busy': async (cp) => { const { p, c, pending } = setup(cp, ['hold']); c.open(); const run = c.confirm(); await tick();
    c.handleKeydown(esc); c.cancel(); const stillOpen = !p.dialog.hidden; pending.forEach((d) => d.resolve()); await run;
    return [stillOpen, { stillOpenWhileBusy: stillOpen }]; },
  'double-confirm-single-operation': async (cp) => { const { p, c, calls, pending } = setup(cp, ['hold', 'hold']); c.open();
    const a = c.confirm(); const b = c.confirm(); await tick(); const count = calls.length; pending.forEach((d) => d.resolve()); await a; await b;
    return [count === 1, { performCalls: count }]; },
  'failure-keeps-dialog-open-focus-inside': async (cp) => { const { p, c } = setup(cp, ['fail']); c.open(); await c.confirm();
    const ok = !p.dialog.hidden && p.dialog.contains(p.doc.activeElement) && p.error.textContent.trim().length > 0 && !p.ok.disabled && !p.cancel.disabled && p.dialog.getAttribute('aria-busy') !== 'true';
    return [ok, { open: !p.dialog.hidden, focus: p.doc.activeElement.id, error: p.error.textContent, okDisabled: p.ok.disabled, cancelDisabled: p.cancel.disabled }]; },
  'retry-reuses-idempotency-key': async (cp) => { const { p, c, calls } = setup(cp, ['fail', 'ok']); c.open(); await c.confirm(); await c.confirm();
    const ok = calls.length === 2 && calls[0] === calls[1] && p.dialog.hidden && p.doc.activeElement === p.trigger;
    return [ok, { keys: calls, open: !p.dialog.hidden, focus: p.doc.activeElement.id }]; },
  'cancel-after-failure-then-retry-same-key': async (cp) => { const { p, c, calls } = setup(cp, ['fail', 'ok']); c.open(); await c.confirm();
    c.cancel(); c.open(); await c.confirm(); return [calls.length === 2 && calls[0] === calls[1], { keys: calls }]; },
  'new-deletion-new-key': async (cp) => { const { c, calls } = setup(cp, ['ok', 'ok']); c.open(); await c.confirm(); c.open(); await c.confirm();
    return [calls.length === 2 && calls[0] !== calls[1], { keys: calls }]; },
  'trigger-removed-focus-fallback': async (cp) => { const { p, c } = setup(cp, ['ok']); c.open(); p.trigger.remove(); await c.confirm();
    const a = p.doc.activeElement; let shown = true; for (let n = a; n; n = n.parent) if (n.hidden) shown = false;
    return [p.dialog.hidden && a !== p.doc.body && a.isConnected && shown && !p.dialog.contains(a), { focus: a.id, visible: shown }]; },
};
(async () => {
  const [controllerPath, only] = process.argv.slice(2);
  const out = {};
  for (const [name, run] of Object.entries(scenarios)) {
    if (only && name !== only) continue;
    try { const [passed, detail] = await Promise.race([run(controllerPath), new Promise((_, r) => setTimeout(() => r(new Error('scenario timed out')), 3000))]);
      out[name] = { passed: Boolean(passed), detail }; }
    catch (error) { out[name] = { passed: false, detail: String(error && error.stack || error).slice(0, 400) }; }
  }
  console.log(JSON.stringify(out));
  process.exit(0);
})();
"""


class MarkupScan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = {}
        self.stack = []
        self.buttons = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        record = {"tag": tag, "attrs": attrs, "text": ""}
        if attrs.get("id"):
            self.elements[attrs["id"]] = record
        if tag not in {"meta", "link", "br", "img", "input", "hr"}:
            self.stack.append(record)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        for record in self.stack:
            record["text"] += data


def markup_checks(workspace: Path) -> list[dict]:
    path = workspace / "web" / "confirm-dialog.html"
    if not path.is_file():
        return [{"id": "markup-present", "passed": False, "detail": "web/confirm-dialog.html missing"}]
    scan = MarkupScan()
    scan.feed(path.read_text(encoding="utf-8"))
    els = scan.elements
    dialog = els.get("confirm-dialog")
    checks = []
    if dialog is None:
        return [{"id": "dialog-role-and-modality", "passed": False, "detail": "#confirm-dialog missing"}]
    a = dialog["attrs"]
    native = dialog["tag"] == "dialog"
    role_ok = native or (a.get("role") in {"dialog", "alertdialog"} and a.get("aria-modal") == "true")
    checks.append({"id": "dialog-role-and-modality", "passed": role_ok, "detail": {"tag": dialog["tag"], "role": a.get("role"), "aria-modal": a.get("aria-modal")}})

    def resolves(attr):
        ids = (a.get(attr) or "").split()
        return bool(ids) and all(i in els and els[i]["text"].strip() for i in ids)

    checks.append({"id": "accessible-name", "passed": resolves("aria-labelledby") or bool((a.get("aria-label") or "").strip()), "detail": a.get("aria-labelledby")})
    checks.append({"id": "accessible-description", "passed": resolves("aria-describedby"), "detail": a.get("aria-describedby")})
    err = els.get("confirm-error")
    live = err is not None and (err["attrs"].get("role") == "alert" or err["attrs"].get("aria-live") in {"assertive", "polite"})
    checks.append({"id": "error-region-announced", "passed": live, "detail": err["attrs"] if err else "#confirm-error missing"})
    real = all(els.get(i) and els[i]["tag"] == "button" and els[i]["attrs"].get("type") == "button" and els[i]["text"].strip()
               for i in ("confirm-ok", "confirm-cancel"))
    checks.append({"id": "actions-are-real-buttons", "passed": real, "detail": {i: (els[i]["tag"] if i in els else None) for i in ("confirm-ok", "confirm-cancel")}})
    return checks


def behaviour_checks(node: str, workspace: Path, extra_js: Path | None = None) -> list[dict]:
    controller = workspace / "web" / "dialog-controller.js"
    if not controller.is_file():
        return [{"id": "controller-present", "passed": False, "detail": "web/dialog-controller.js missing"}]
    with tempfile.TemporaryDirectory(prefix="f09-") as tmp:
        harness = Path(tmp) / "harness.js"
        harness.write_text(FAKE_DOM, encoding="utf-8")
        try:
            proc = subprocess.run([node, str(harness), str(controller)], capture_output=True, text=True, encoding="utf-8", timeout=60)
        except subprocess.TimeoutExpired:
            return [{"id": "controller-behaviour", "passed": False, "detail": "harness timed out"}]
    try:
        results = json.loads(proc.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return [{"id": "controller-behaviour", "passed": False, "detail": (proc.stderr or proc.stdout)[-800:]}]
    return [{"id": name, "passed": r["passed"], "detail": r["detail"]} for name, r in results.items()]


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
    checks = markup_checks(workspace) + behaviour_checks(node, workspace)
    if args.withheld and args.withheld.is_dir():
        for test in sorted(args.withheld.glob("test_*.js")):
            try:
                proc = subprocess.run([node, str(test), str(workspace)], capture_output=True, text=True, encoding="utf-8", timeout=60)
                checks.append({"id": f"withheld:{test.name}", "passed": proc.returncode == 0, "detail": proc.stdout[-800:]})
            except subprocess.TimeoutExpired:
                checks.append({"id": f"withheld:{test.name}", "passed": False, "detail": "timed out"})
    status = "PASS" if all(c["passed"] for c in checks) else "FAIL"
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks}, default=str))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
