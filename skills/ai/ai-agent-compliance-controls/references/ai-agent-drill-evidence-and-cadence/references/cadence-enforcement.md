# Cadence Enforcement — Engineering Reference

How the platform makes drill cadence binding: the daily enforcer turns a missed drill into a paged on-call ticket and an open compliance exception **before** an auditor finds the gap.

---

## 1. Policy File Schema

```yaml
# ops/compliance/drill-cadence.yaml
drills:
  - id: <unique>
    description: <human readable>
    min_cadence_days: <int>
    warn_at_pct: 0.8                 # warn when 80% of cadence elapsed
    grace_period_days: 7              # business-day grace before pager
    owner: <email>
    secondary_owner: <email>          # for escalation
    control_ids: [<framework.control_id>, ...]
    scenarios: [<scenario_id>, ...]
    severity_when_overdue: high       # high|critical
```

## 2. Last-Passed Run Resolution

```python
# compliance/drills/last_passed.py
def last_passed_run(drill_id: str):
    return db.fetchone("""
        SELECT * FROM drill_runs
        WHERE drill_id = %s AND result = 'pass'
        ORDER BY ended_at DESC LIMIT 1
    """, (drill_id,))
```

A failed or aborted run does **not** reset the cadence clock — the obligation persists until a pass is recorded.

## 3. Enforcer

```python
# compliance/drills/enforcer.py
import yaml, json
from datetime import datetime, timedelta
from compliance.exceptions import open_exception
from compliance.pager import page_on_call
from compliance.drills.last_passed import last_passed_run

POLICY_PATH = "ops/compliance/drill-cadence.yaml"

def enforce(now: datetime | None = None) -> dict:
    now = now or datetime.utcnow()
    policy = yaml.safe_load(open(POLICY_PATH))
    results = {"warn": [], "overdue": [], "ok": []}

    for drill in policy["drills"]:
        last = last_passed_run(drill["id"])
        warn_at = drill["min_cadence_days"] * drill.get("warn_at_pct", 0.8)
        cadence = drill["min_cadence_days"]
        grace   = drill.get("grace_period_days", 0)

        if last is None:
            _overdue(drill, reason="never_run", since=None, now=now)
            results["overdue"].append(drill["id"])
            continue

        delta_days = (now - last["ended_at"]).days
        if delta_days > cadence + grace:
            _overdue(drill, reason="overdue", since=last["ended_at"], now=now)
            results["overdue"].append(drill["id"])
        elif delta_days > cadence:
            _warn(drill, reason="in_grace_period", since=last["ended_at"], now=now)
            results["warn"].append(drill["id"])
        elif delta_days > warn_at:
            _warn(drill, reason="approaching", since=last["ended_at"], now=now)
            results["warn"].append(drill["id"])
        else:
            results["ok"].append(drill["id"])

    _write_heartbeat(results, now)
    return results

def _overdue(drill, *, reason: str, since, now: datetime):
    title = f"Drill {drill['id']} {reason}"
    detail = {
        "last_passed": since.isoformat() if since else None,
        "min_cadence_days": drill["min_cadence_days"],
        "grace_period_days": drill.get("grace_period_days", 0),
        "primary_owner": drill["owner"],
        "control_ids": drill["control_ids"],
    }
    severity = drill.get("severity_when_overdue", "high")
    if not _dedup_exists(drill["id"], status="open"):
        open_exception(
            control_id=drill["control_ids"][0],
            severity=severity,
            title=title,
            evidence_ref=f"drills/cadence/{drill['id']}",
            detail=detail,
        )
    page_on_call(drill["owner"], title)
    # Escalate to secondary after 24h
    if since and (now - since).days > drill["min_cadence_days"] + 1:
        page_on_call(drill.get("secondary_owner") or drill["owner"], f"{title} (escalated)")

def _warn(drill, *, reason, since, now):
    if not _slack_warn_sent_today(drill["id"]):
        slack.notify(drill["owner"], f"Drill {drill['id']}: {reason}; last pass {since.isoformat()}")
        _mark_slack_warn_today(drill["id"])

def _write_heartbeat(results: dict, now: datetime):
    db.execute("""
        INSERT INTO compliance_job_heartbeats (job_id, ran_at, status, summary)
        VALUES ('drill_cadence_enforcer', %s, 'ok', %s)
    """, (now, json.dumps(results)))
```

## 4. Deduplication

The enforcer is daily; without dedup, a 30-day overdue drill would page on-call 30 times.

```python
def _dedup_exists(drill_id: str, *, status: str) -> bool:
    return db.fetchone("""
        SELECT 1 FROM compliance_exceptions
        WHERE control_id IN (SELECT control_id_of(%s)) AND status = %s
          AND evidence_pack LIKE %s
        LIMIT 1
    """, (drill_id, status, f"drills/cadence/{drill_id}%")) is not None
```

A single open exception per drill_id; the enforcer **escalates** the same exception (bumps severity, re-pages secondary owner) rather than opening duplicates.

## 5. Escalation Ladder

| Days overdue | Action |
|---|---|
| 0 (in grace) | Slack warning to primary owner, once per day. |
| 1–3 past grace | Page primary owner; open `high` exception. |
| 4–7 | Re-page primary every 24h; Slack to secondary. |
| 8–14 | Page secondary owner; bump exception severity to `critical`; CC: VP Engineering. |
| 15+ | Daily executive digest; freeze deploys to the affected agent class until drill passes. |

The freeze is enforced by a deploy-gate that reads `compliance_exceptions WHERE severity='critical' AND control_id IN (...)`:

```python
# ci/gates/drill_freeze.py
def drill_freeze_check(component: str) -> tuple[bool, str]:
    affected = db.fetchall("""
        SELECT title FROM compliance_exceptions
        WHERE severity = 'critical' AND status = 'open'
          AND control_id IN (SELECT control_id FROM component_controls WHERE component = %s)
    """, (component,))
    if affected:
        return False, f"Deploy frozen by {len(affected)} critical drill exception(s): {[a['title'] for a in affected]}"
    return True, ""
```

## 6. Auditor Visibility

```
GET /audit/drills/cadence
→ 200 OK
{
  "as_of": "2026-05-12T03:00:00Z",
  "drills": [
    {"id":"kill_switch_global", "last_passed":"2026-04-21", "next_due":"2026-07-20", "status":"ok"},
    {"id":"red_team_prompt_injection", "last_passed":"2026-01-10", "next_due":"2026-04-10", "status":"overdue", "open_exception_id": 7720}
  ]
}
```

A single screen for the auditor; the cadence policy and exception register are the source of truth.

## 7. Heartbeat as Evidence

A missed enforcer run is itself a control gap. Watchers:

```yaml
- alert: drill_cadence_enforcer_silent
  expr: time() - max_over_time(compliance_job_heartbeat{job_id="drill_cadence_enforcer"}[36h]) > 36*3600
  severity: critical
  page: sre
```

Heartbeats are written to an append-only table and included in the quarterly drill rollup.

## 8. Test Cases

```python
def test_overdue_opens_exception_and_pages(fake_db, fake_pager):
    fake_db.last_run("kill_switch_global", days_ago=120)
    enforce(now=datetime(2026,5,12))
    assert fake_pager.was_paged("sre-lead@example.com")
    assert fake_db.exception_open("CC7.4")

def test_warn_in_grace_does_not_page(fake_db, fake_pager):
    fake_db.last_run("kill_switch_global", days_ago=92)
    enforce(now=datetime(2026,5,12))
    assert not fake_pager.any_pages()
    assert fake_db.slack_warned("kill_switch_global")

def test_dedup_prevents_duplicate_exceptions(fake_db):
    fake_db.last_run("kill_switch_global", days_ago=200)
    enforce(); enforce(); enforce()
    assert fake_db.exception_count("CC7.4") == 1

def test_freeze_gate_blocks_deploy_on_critical(fake_db):
    fake_db.open_exception("CC7.4", severity="critical")
    ok, msg = drill_freeze_check("agent-runtime")
    assert not ok and "critical drill" in msg
```

## 9. Operational Notes

- Enforcer runs **before** the daily evidence-collector batch so the day's evidence already reflects any cadence exceptions.
- Time zone is UTC; cadence days are calendar days, not business days, unless the policy explicitly states `business_days: true`.
- Freezing deploys for an overdue drill is intentionally disruptive — it converts auditor risk into engineering urgency.
- The policy file is versioned in git; any change is itself a compliance event (logged to the action audit log with `event_class=policy_change`).
