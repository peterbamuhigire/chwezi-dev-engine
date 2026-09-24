# Continuous Control Monitoring for Agent Compliance

Load when you need to prove controls stayed effective across a SOC 2 Type II
window or an ISO surveillance year, detect drift between declared and observed
controls, gate deploys that would break a control, or re-verify LLM providers
and other subprocessors. Evidence collection itself lives in
[`ai-agent-evidence-automation`](../../ai-agent-observability-evaluation/references/ai-agent-evidence-automation/entrypoint.md);
integrity of the log in
[`ai-agent-audit-log-integrity`](ai-agent-audit-log-integrity/entrypoint.md).
This file closes the loop: declared state vs observed state, on a schedule, with
failures turned into owned tickets.

## 1. Inputs

- Control matrix: control ID, framework references, owner, test, cadence, threshold.
- Framework register (section 4).
- Tool, prompt and model registries; subprocessor list; evidence-pack registry.

## 2. Declared-vs-observed drift checks

Each check compares a declaration with production reality and writes a signed
result row. A failed row opens a ticket to the control owner with a due date.

| Check | Declared source | Observed source | Fails when | Cadence |
|---|---|---|---|---|
| Tool compliance metadata | Tool registry | Tools actually invoked (gateway log) | An invoked tool lacks data class, PHI flag, reversibility or retention class | Continuous; deploy gate |
| Irreversible-action approval | Approval policy | Action audit log join approvals | Any irreversible action without a linked approval row | Daily (see approval completeness skill) |
| Model pin | Model registry per feature/tenant | Gateway request log | Traffic reaches an unpinned or unregistered model version | Hourly |
| Provider scope | Subprocessor list + BAA/DPA flags | Gateway egress by provider and region | PHI or EU-resident data sent to a provider or region not in scope | Hourly |
| Evidence freshness | Control cadence | Evidence-pack registry | Latest pack older than cadence + grace | Daily |
| Drill cadence | Drill policy | Drill evidence packs | Overdue drill | Daily |
| Log integrity | Hash chain | Nightly verification job | Chain break or missing seal | Nightly |
| Access review | Quarterly review policy | Role membership export | Privileged role unchanged past review due date | Weekly |

## 3. Deploy gate

Block a release in CI when it would introduce drift:

1. New or changed tool without complete compliance metadata.
2. New provider, model family or region not on the approved subprocessor list.
3. Prompt or model change without an eval delta attached to the change record.
4. Removal of an event emission that a control test depends on (contract test
   on audit-event schema).

A blocked deploy prints the control ID, the missing field and the owner. Emergency
override requires a named approver, an expiry, and a follow-up ticket; the override
itself is an audit event.

## 4. Framework register

Keep one row per framework the business claims. Review quarterly and on every
auditor engagement letter. Drift here is a control failure too: a matrix built on
a withdrawn edition is not evidence.

| Framework | Edition to use (checked 2026-09-24) | Watch item |
|---|---|---|
| ISO/IEC 27001 | 2022 (93 Annex A controls, themes A.5-A.8); 2013 certificates ceased to be valid after 31 Oct 2025 | Any `A.9`-`A.18` control ID in a matrix is 2013 numbering: remap before audit |
| SOC 2 | AICPA 2017 Trust Services Criteria with Revised Points of Focus - 2022 | Confirm the edition in the engagement letter |
| HIPAA Security Rule | 45 CFR 164.302-.318 as in force | January 2025 NPRM not final; do not cite proposed text as law |
| ISO/IEC 42001 | 2023 | CEN adoption EN ISO/IEC 42001:2026 is the same text |
| EU AI Act | Reg. (EU) 2024/1689 as amended by Reg. (EU) 2026/1744 | High-risk dates 2 Dec 2027 / 2 Aug 2028 |
| OWASP LLM Top 10 | 2026 (published 2026-08-03; IDs renumbered from 2025) | Cite IDs with the year; also map OWASP Top 10 for Agentic Applications (2026) |
| NIST AI RMF | 1.0 + AI 600-1 profile | Revision announced; re-check before citing |

## 5. Subprocessor and LLM provider re-verification

| Item | Evidence | Re-check |
|---|---|---|
| Provider SOC 2 report / ISO certificate | Report period end date, certificate expiry, scope includes the API you use | On expiry and annually |
| BAA (PHI features) | Signed BAA naming the services in use | On any new endpoint or model family |
| Data retention / training opt-out | Contract clause or console setting screenshot with date | Quarterly and on provider policy change |
| Region / residency | Endpoint region list vs tenant residency rules | On routing change |
| Incident and deprecation notices | Provider status and deprecation feeds subscribed | Continuous |

A lapsed attestation does not stop traffic automatically; it opens a ticket and,
for PHI or high-risk features, requires a documented risk acceptance within the
ticket's due date or a routing change.

## 6. Decision rules

- A control with no automated check must have a manual test with named tester and
  date; otherwise mark it `NOT_ASSESSED` in the matrix, never "effective".
- An exception in the window is disclosed, not deleted. Record detection time,
  remediation time and population affected; auditors test exception handling.
- Failed check rows are immutable; the fix is a new row.

## 7. Acceptance checks

- [ ] Every control in the matrix has a check, cadence, owner and last result.
- [ ] Deploy gate demonstrably blocked a seeded tool without metadata in CI.
- [ ] No evidence pack is older than its cadence plus grace on the day of audit.
- [ ] Framework register reviewed this quarter; no withdrawn edition referenced.
- [ ] Each LLM provider row shows attestation expiry and next re-check date.

## Evidence/currentness

Access date 2026-09-24. ISO/IEC 27001:2013 transition end 31 October 2025 under
IAF MD 26 (corroborated by certification-body and consultancy notices; IAF
document not opened directly - `NOT_ASSESSED` for exact wording). AICPA edition:
aicpa-cima.com resource page "2017 Trust Services Criteria (With Revised Points
of Focus - 2022)". HIPAA NPRM status: not final, final action reported for 2027
(HIPAA Journal, Clark Hill; OMB agenda not opened). ISO/IEC 42001: iso.org. EU AI
Act and OWASP: see [the overlay](eu-ai-act-and-iso-42001-agent-overlay.md) and
[`ai-security`](../../ai-security/SKILL.md). Provider attestation contents are
vendor-specific: `NOT_ASSESSED`.
