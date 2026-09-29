"""F08 authentication and authorisation - deterministic checker (stdlib only, no model call).

Executes the produced export code in a subprocess against adversarial requests: forged, tampered,
algorithm-none, expired and missing tokens (HMAC via the installed authkit library), a horizontal
privilege attempt across tenants, an insufficient role, object-ID guessing (a cross-tenant ID must be
indistinguishable from a missing one), a role revoked between enqueue and execution, and secrets in
the audit log. It also confirms the installed auth library was not modified or re-implemented.

    python checker.py <workspace> [--withheld <dir>]

Prints one JSON object and exits 0 (PASS), 1 (FAIL) or 2 (NOT_ASSESSED).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

FIXTURE = "F08"
HERE = Path(__file__).resolve().parent

PROBE = r'''
import base64, json, traceback
from lib import authkit
from app.context import AppContext
from app.documents import Repository
from app.identity import FakeIdentityProvider
from app.errors import Denied
from app.export_jobs import enqueue_export, run_export

SECRET = b"checker-signing-key-7f3a"
results = {}
def record(cid, passed, detail=""):
    results[cid] = [bool(passed), str(detail)[:300]]

def build():
    idp = FakeIdentityProvider(SECRET)
    idp.add_user("amina", "tenant-a", {"reader", "exporter"})
    idp.add_user("brian", "tenant-b", {"reader", "exporter"})
    idp.add_user("carol", "tenant-a", {"reader"})
    repo = Repository()
    repo.add("doc-100", "tenant-a", "Q3 plan", "Tenant A body")
    repo.add("doc-200", "tenant-b", "Board pack", "Tenant B secret body")
    return AppContext(SECRET, idp, repo), idp

def attempt(ctx, token, doc_id):
    try:
        return ("ok", enqueue_export(ctx, token, doc_id))
    except Denied as exc:
        return ("denied", exc.code)
    except Exception as exc:
        return ("error", repr(exc))

def b64(obj):
    return base64.urlsafe_b64encode(json.dumps(obj, separators=(",", ":")).encode()).rstrip(b"=").decode()

tokens_seen = []
try:
    ctx, idp = build()
    good = idp.issue_token("amina", ctx.now()); tokens_seen.append(good)
    out = attempt(ctx, good, "doc-100")
    ok = out[0] == "ok"
    if ok:
        status = run_export(ctx, out[1])
        ok = "Tenant A body" in ctx.exports.get(out[1], "")
    record("same_tenant_export_succeeds", ok, out)

    ctx, idp = build()
    tok = idp.issue_token("amina", ctx.now()); tokens_seen.append(tok)
    cross = attempt(ctx, tok, "doc-200")
    missing = attempt(ctx, tok, "doc-999")
    record("cross_tenant_denied", cross[0] == "denied" and not ctx.jobs, cross)
    record("object_id_guessing_indistinguishable", cross[0] == missing[0] == "denied" and cross[1] == missing[1], f"cross={cross} missing={missing}")

    ctx, idp = build()
    tok = idp.issue_token("carol", ctx.now()); tokens_seen.append(tok)
    out = attempt(ctx, tok, "doc-100")
    record("insufficient_role_denied", out[0] == "denied" and not ctx.jobs, out)

    ctx, idp = build()
    forged = authkit.issue(b"attacker-key", {"sub": "amina", "tenant": "tenant-b", "roles": ["exporter"]}, 900, ctx.now())
    tokens_seen.append(forged)
    out = attempt(ctx, forged, "doc-200")
    record("forged_token_denied", out == ("denied", "unauthenticated"), out)

    ctx, idp = build()
    real = idp.issue_token("amina", ctx.now())
    h, p, s = real.split(".")
    claims = json.loads(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4)))
    claims["tenant"] = "tenant-b"
    tampered = f"{h}.{b64(claims)}.{s}"; tokens_seen.append(tampered)
    out = attempt(ctx, tampered, "doc-200")
    record("tampered_claims_denied", out == ("denied", "unauthenticated"), out)

    ctx, idp = build()
    none_tok = f"{b64({'alg': 'none', 'typ': 'JWT'})}.{b64({'sub': 'amina', 'tenant': 'tenant-b', 'roles': ['exporter'], 'exp': ctx.now() + 900})}."
    tokens_seen.append(none_tok)
    out = attempt(ctx, none_tok, "doc-200")
    record("alg_none_denied", out == ("denied", "unauthenticated"), out)

    ctx, idp = build()
    old = idp.issue_token("amina", ctx.now() - 2000, ttl=900); tokens_seen.append(old)
    out = attempt(ctx, old, "doc-100")
    record("expired_token_denied", out == ("denied", "unauthenticated"), out)

    ctx, idp = build()
    outs = [attempt(ctx, t, "doc-100") for t in (None, "", "Bearer", "a.b")]
    record("missing_or_malformed_credentials_fail_closed", all(o == ("denied", "unauthenticated") for o in outs) and not ctx.jobs, outs)

    ctx, idp = build()
    tok = idp.issue_token("amina", ctx.now()); tokens_seen.append(tok)
    out = attempt(ctx, tok, "doc-100")
    if out[0] != "ok":
        record("revoked_role_blocks_execution", False, f"enqueue failed: {out}")
    else:
        idp.revoke_role("amina", "exporter")
        try:
            status = run_export(ctx, out[1])
        except Denied as exc:
            status = f"denied:{exc.code}"
        exported = ctx.exports.get(out[1])
        record("revoked_role_blocks_execution", not exported and status != "done", f"status={status} exported={bool(exported)}")

    ctx, idp = build()
    for t, d in ((idp.issue_token("amina", ctx.now()), "doc-200"), (idp.issue_token("carol", ctx.now()), "doc-100"), (forged, "doc-100")):
        tokens_seen.append(t)
        attempt(ctx, t, d)
    text = json.dumps(ctx.audit, default=str)
    leaks = [t[:12] for t in set(tokens_seen) if t and len(t) > 8 and t in text]
    sigs = [t.split(".")[-1] for t in set(tokens_seen) if t and t.count(".") == 2 and len(t.split(".")[-1]) > 8]
    leaks += [s[:8] for s in sigs if s in text]
    denials = [e for e in ctx.audit if "denied" in str(e.get("event", "")) or "fail" in str(e.get("event", ""))]
    record("audited_denial_contains_no_secret", len(denials) >= 3 and not leaks and SECRET.decode() not in text, f"denials={len(denials)} leaks={leaks}")
except Exception:
    record("probe_crashed", False, traceback.format_exc())
print(json.dumps(results))
'''


def _norm_hash(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def run_probe(workspace: Path) -> tuple[dict, str]:
    env = dict(os.environ, PYTHONPATH=str(workspace), PYTHONDONTWRITEBYTECODE="1")
    try:
        proc = subprocess.run([sys.executable, "-X", "utf8", "-c", PROBE], cwd=workspace, env=env,
                              capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return {}, "probe timed out"
    lines = [line for line in proc.stdout.splitlines() if line.startswith("{")]
    if not lines:
        return {}, (proc.stderr or proc.stdout)[-1500:]
    return json.loads(lines[-1]), ""


def run_unittests(workspace: Path, start: Path, top: Path) -> tuple[bool, str]:
    env = dict(os.environ, PYTHONPATH=str(workspace), PYTHONDONTWRITEBYTECODE="1")
    try:
        proc = subprocess.run([sys.executable, "-X", "utf8", "-m", "unittest", "discover", "-s", str(start), "-t", str(top)],
                              cwd=workspace, env=env, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return False, "tests timed out"
    return proc.returncode == 0, proc.stderr[-800:]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--withheld", type=Path)
    args = parser.parse_args(argv)
    workspace = args.workspace.resolve()
    checks = []
    ok, tail = run_unittests(workspace, workspace / "public_tests", workspace)
    checks.append({"id": "public_tests", "passed": ok, "detail": "" if ok else tail})
    same = _norm_hash(workspace / "lib" / "authkit.py") == _norm_hash(HERE / "starter" / "lib" / "authkit.py")
    checks.append({"id": "installed_auth_library_unmodified", "passed": same, "detail": "" if same else "lib/authkit.py changed or removed (no home-grown token handling)"})
    results, error = run_probe(workspace)
    if error:
        checks.append({"id": "probe", "passed": False, "detail": error})
    for cid, (passed, detail) in results.items():
        checks.append({"id": cid, "passed": passed, "detail": detail})
    if args.withheld and args.withheld.is_dir():
        withheld = args.withheld.resolve()
        ok, tail = run_unittests(workspace, withheld, withheld)
        checks.append({"id": "withheld_tests", "passed": ok, "detail": "" if ok else tail})
    status = "PASS" if checks and all(c["passed"] for c in checks) else "FAIL"
    print(json.dumps({"fixture": FIXTURE, "status": status, "checks": checks}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
