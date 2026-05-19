# Approval Completeness Evidence Pack — SOC 2 Processing Integrity (PI1.1)

The evidence pack auditors pull when sampling PI1.1 ("system processing is complete, accurate, timely, and authorised") for agent-driven irreversible actions.

---

## 1. Pack Layout

```
PI1.1-{window}/
├── manifest.json
├── completeness-report.json
├── gaps.jsonl
├── approvals-sample.jsonl
├── chain-witness.json
├── exceptions.jsonl
├── attestation.txt
└── signature.sig
```

`{window}` is `YYYY-MM` for monthly packs, `YYYY-QN` for quarterly rollups.

## 2. `manifest.json`

```json
{
  "pack_id": "evp-pi11-2026-04",
  "control_id": "PI1.1",
  "window_start": "2026-04-01T00:00:00Z",
  "window_end":   "2026-05-01T00:00:00Z",
  "produced_at":  "2026-05-01T03:12:44Z",
  "producer":     "compliance.jobs.approval_completeness@1.6.0",
  "owner":        "security-lead@example.com",
  "retention_years": 7,
  "files": [
    {"name": "completeness-report.json", "sha256": "9a3f...", "size": 4123},
    {"name": "gaps.jsonl",               "sha256": "01ce...", "size": 22},
    {"name": "approvals-sample.jsonl",   "sha256": "77ab...", "size": 102389},
    {"name": "chain-witness.json",       "sha256": "8810...", "size": 911},
    {"name": "exceptions.jsonl",         "sha256": "12cc...", "size": 0},
    {"name": "attestation.txt",          "sha256": "ffaa...", "size": 312}
  ],
  "manifest_sha256": "self",
  "signature_alg": "ed25519",
  "signature_key_id": "compliance-2026-05"
}
```

## 3. `completeness-report.json`

```json
{
  "control_id": "PI1.1",
  "window_start": "2026-04-01T00:00:00Z",
  "window_end":   "2026-05-01T00:00:00Z",
  "totals": {
    "irreversible_actions": 8421,
    "matched": 8421,
    "gaps": 0
  },
  "gap_classes": {},
  "bypasses_documented": 4,
  "by_tool": [
    {"tool_name": "stripe.refund.create",   "actions": 1843, "gaps": 0},
    {"tool_name": "billing.invoice.void",   "actions":  412, "gaps": 0},
    {"tool_name": "support.escalate",       "actions": 6166, "gaps": 0}
  ],
  "by_tenant_top10_concentration": "73%",
  "chain_witness_ref": "chain-witness.json",
  "policy_versions_observed": ["v3", "v4"],
  "produced_at": "2026-05-01T03:12:44Z"
}
```

## 4. `gaps.jsonl`

Empty in a healthy window. One row per gap otherwise:

```json
{
  "classification": "gap_missing",
  "action_id": 2284100192,
  "action_chain_pos": 71238411,
  "tool_name": "stripe.refund.create",
  "tenant_id": "ten_0192",
  "task_id": "task_88a1",
  "step_index": 7,
  "initiator_id": "agent_runtime",
  "action_at": "2026-04-14T13:22:11Z",
  "policy_version": "v3",
  "payload_summary": {"refund_cents": 1200, "currency": "usd"},
  "exception_id": 5512
}
```

## 5. `approvals-sample.jsonl`

Sample of 200 OK approvals (randomly drawn) so the auditor can inspect quality:

```json
{
  "action_id": 2284100204,
  "action_chain_pos": 71238416,
  "approval_id": 9011224,
  "approver_id": "alice@example.com",
  "approver_role": "finance-approver",
  "approved_at": "2026-04-14T13:21:55Z",
  "action_at":   "2026-04-14T13:22:08Z",
  "delta_seconds": 13,
  "signature": "ed25519:0x...",
  "linked_action_chain_pos": 71238416,
  "policy_version": "v3"
}
```

## 6. `chain-witness.json`

Cryptographic proof the audit log slice was not rewritten:

```json
{
  "first_chain_pos": 71012009,
  "last_chain_pos":  71238599,
  "first_this_hash": "8a2c...",
  "last_this_hash":  "ccaa...",
  "daily_seal": {
    "date": "2026-04-30",
    "signed_root": "2c91...",
    "off_platform_witness_uri": "s3://compliance-vault/seals/2026-04-30.json"
  },
  "spot_check_stride": 45,
  "drift_positions": [],
  "verified_at": "2026-05-01T03:11:02Z"
}
```

`drift_positions` non-empty → critical finding; pack is still produced but the exception is severity=critical.

## 7. `exceptions.jsonl`

Each exception opened during the window plus closure refs:

```json
{
  "id": 5510,
  "control_id": "PI1.1",
  "opened_at": "2026-04-03T11:01:00Z",
  "severity": "high",
  "title": "Approval completeness gap: gap_missing on action 2284098001",
  "owner": "security-lead@example.com",
  "target_close": "2026-04-17",
  "status": "closed",
  "closed_at": "2026-04-09T14:00:00Z",
  "remediation": "Root cause: tool-registry mis-declared reversibility=reversible. Fixed in tool-registry v3.4. Backfill: 1 affected action retroactively approved by COO; documented under exception."
}
```

## 8. `attestation.txt`

Plain text signed by the control owner over the manifest sha256:

```
I, security-lead@example.com, attest that:
1. The approval completeness job ran on the documented cadence for the window 2026-04-01..2026-05-01.
2. No undisclosed exceptions exist for PI1.1 in the window.
3. The manifest below was produced by the job and not modified.

manifest_sha256: 9b1e7c...

Signed: alice <security-lead@example.com>
Date:   2026-05-02
```

The signature file is `signature.sig` (ed25519 over `manifest.json` bytes).

## 9. Auditor Portal Endpoints

```
GET  /audit/soc2/control/PI1.1/packs?from=2026-04-01&to=2026-06-30
GET  /audit/soc2/control/PI1.1/packs/{pack_id}                       -> 302 to signed-url
GET  /audit/soc2/control/PI1.1/packs/{pack_id}/manifest.json
GET  /audit/soc2/control/PI1.1/packs/{pack_id}/verify                -> {chain_ok, signature_ok}
```

Pack URLs expire in 24h; access is logged in `auditor_access_log` (itself evidence for CC6.1).

## 10. Retention

- Monthly pack: 7 years (covers HIPAA 6y + SOC 2 3y + safety margin).
- Quarterly rollup: 7 years.
- Daily seal off-platform: 10 years.
- Approver allow-list version table: indefinite (regulatory audit trail).

## 11. Failure Modes Captured by the Pack

| Failure | Detected by | Where in pack |
|---|---|---|
| Action without approval | Job classification | `gaps.jsonl` row, `gap_missing` |
| Backdated approval | Job (skew check) | `gaps.jsonl` row, `gap_after_action` |
| Self-approval | Job classification | `gaps.jsonl` row, `gap_self_approval` |
| Wrong action linked | Chain-pos check | `gaps.jsonl` row, `gap_chain_mismatch` |
| Removed approver | Historical allow-list | `gaps.jsonl` row, `gap_unauthorised_approver` |
| Audit-log rewrite | Chain witness | `chain-witness.json` `drift_positions` |
| Missed job run | Heartbeat | Auto-opens exception, included in `exceptions.jsonl` |
| Approver authority drift | Policy-version mismatch | `gaps.jsonl` row, `gap_policy_version` |

## 12. Quarterly Rollup

The quarterly pack concatenates three monthly packs plus a rollup `completeness-report.json` summing totals, listing all opened/closed exceptions in the quarter, and re-checking the chain witness covering the full quarter. Auditor's primary artefact at the end of each quarter.
