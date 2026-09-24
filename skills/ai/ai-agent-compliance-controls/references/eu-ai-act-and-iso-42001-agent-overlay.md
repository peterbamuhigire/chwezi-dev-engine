# EU AI Act and ISO/IEC 42001 Overlay for Agent Controls

Load when an agentic feature may be high-risk under the EU AI Act, a customer asks
for ISO/IEC 42001 (AI management system) alignment, or an auditor asks how the
SOC 2 / ISO 27001 agent controls also satisfy AI-specific regulation. This file
does not restate those controls; it maps the AI-specific obligations onto the
controls the engine already builds and names the extra engineering each needs.

Boundary: legal classification and the technical file (Art. 11), QMS text
(Art. 17) and the ISO 42001 Statement of Applicability are documents owned by
counsel and the SRS engine. This file owns the running controls and evidence.

## 1. Inputs

- Feature inventory with intended purpose, users, affected persons, markets.
- Role per feature: **provider** (you place the system on the EU market under
  your name) or **deployer** (you use a third party's system). A SaaS vendor
  shipping its own agent to EU tenants is normally the provider.
- Existing control matrix (SOC 2 / ISO 27001 mapping in this skill).
- Autonomy level and irreversible-action list per agent.

## 2. Classification decision (run per feature, record the result)

1. Is the output used in an Annex III area - biometrics, critical
   infrastructure, education, employment and worker management, access to
   essential private or public services (credit scoring, insurance pricing,
   benefits), law enforcement, migration and border control, administration of
   justice or democratic processes? If no, and it is not a safety component of
   an Annex I regulated product, it is not high-risk: record the reasoning and
   apply only Art. 50 transparency (tell users they are interacting with AI;
   mark synthetic content) plus your baseline controls.
2. If yes, check the Art. 6(3) derogation (narrow procedural task, improves a
   completed human activity, detects patterns without replacing human
   assessment, preparatory task). Profiling of natural persons is never
   derogated. Record the assessment before relying on it.
3. If high-risk, apply section 3 and set `eu_aia_risk_class = high_risk` on the
   feature so the audit-log retention class and severity uplift fire.
4. Re-run classification on any change of intended purpose, market, or tool set.

Application dates (verify before any commitment): prohibitions and AI literacy
2 February 2025; GPAI model duties 2 August 2025; high-risk duties for Annex III
systems **2 December 2027** and Annex I product-embedded systems **2 August
2028**, as deferred by Regulation (EU) 2026/1744. Build now; claim legal
conformity only against the date that applies.

## 3. High-risk obligations mapped to engine controls

| Obligation | What must run in production | Existing engine control | Extra engineering |
|---|---|---|---|
| Art. 9 risk management | Iterative risk register tied to tests | [`ai-agent-safety-and-red-team`](../../ai-agent-safety-and-red-team/SKILL.md), control test suite | Link every risk ID to a red-team or eval test; fail release when a high risk has no passing test |
| Art. 10 data governance | Provenance, bias examination, gap log for training/fine-tune/RAG data | [`ai-evaluation`](../../ai-evaluation/SKILL.md) golden sets | Dataset card per corpus: source, licence, collection date, known gaps, group coverage |
| Art. 12 record-keeping | Automatic event logs over the system lifetime | [hash-chained audit log](ai-agent-audit-log-integrity/entrypoint.md) | Log input reference, retrieval set, model/prompt version, human verifier ID per decision |
| Art. 19 / 26(6) log retention | Logs kept at least 6 months (longer if other law requires) | [retention policies](ai-agent-audit-log-integrity/references/retention-policies.md) | Deletion job must refuse to prune `eu_aia_*` rows younger than the configured floor |
| Art. 13 transparency to deployers | Instructions for use: capabilities, limits, accuracy, oversight measures | Feature spec | Generate instructions from the same eval numbers the dashboard shows; never hand-typed |
| Art. 14 human oversight | Operators can understand, detect anomalies, resist automation bias, override or reverse, and halt | [HITL approval](../../ai-agent-tooling-and-hitl/SKILL.md), kill-switch | Per-task "stop" that reaches a safe state; override is logged with reason; approver sees confidence and evidence, not only the proposal |
| Art. 15 accuracy, robustness, cybersecurity | Declared accuracy metrics; resilience to errors, poisoning, adversarial input | [`ai-security`](../../ai-security/SKILL.md), eval CI gate | Publish the declared metric and its test population; regression below it blocks release |
| Art. 72 post-market monitoring | Plan that collects field performance | [`ai-agent-observability-evaluation`](../../ai-agent-observability-evaluation/SKILL.md) | Monthly field-vs-declared accuracy report per feature |
| Art. 73 serious-incident reporting | 15 / 2 / 10-day clocks | [regulator templates](../../ai-incident-response/references/ai-incident-customer-comms/references/regulator-notification-templates.md) | Incident record carries `eu_aia_high_risk` flag and awareness timestamp |

## 4. ISO/IEC 42001:2023 control groups mapped to engine artefacts

ISO/IEC 42001 is a management-system standard (clauses 4-10, Plan-Do-Check-Act)
with 38 Annex A controls in nine groups. Use it to show the agent controls sit
inside a managed AI governance cycle, not as one-off engineering.

| Annex A group | Engine artefact that evidences it |
|---|---|
| A.2 AI policies | Signed AI use policy version log (SRS engine) referenced by the control matrix |
| A.3 Internal organisation | Control-owner table; named kill-switch and approver roles |
| A.4 Resources for AI systems | Agent asset register (prompts, tools, models, indices, datasets) from the ISO 27001 reference |
| A.5 Assessing impacts of AI systems | Classification record (section 2) plus [algorithmic impact review](../../ai-evaluation/references/algorithmic-decision-impact-review.md) |
| A.6 AI system life cycle | Prompt/tool/model change records; eval-gated release; retirement records |
| A.7 Data for AI systems | Dataset cards; erasure proofs for memory and embeddings |
| A.8 Information for interested parties | Generated instructions for use; customer SLA dashboard; incident comms |
| A.9 Use of AI systems | HITL approval evidence; autonomy limits per tenant |
| A.10 Third-party and customer relationships | LLM provider due-diligence and subprocessor records ([continuous monitoring](continuous-control-monitoring.md)) |

One asset register, one change log and one evidence pack format serve ISO 27001,
ISO 42001, SOC 2 and the EU AI Act. Never build a parallel register per framework.

## 5. Decision rules

- No classification record, no production launch in an EU market.
- A high-risk feature without a working per-task halt and a logged override path
  is a release blocker, whatever its eval score.
- Declared accuracy (Art. 15) comes from the frozen release eval, with population
  and date; marketing copy may not quote a better number.
- When two retention windows conflict, keep the longest; when a data-protection
  erasure right conflicts with log retention, pseudonymise the subject in the log
  and keep the chain intact.

## 6. Acceptance checks

- [ ] Every agent feature has a dated classification record with role (provider/deployer).
- [ ] High-risk features emit Art. 12 fields on every decision; a sampled decision can be reconstructed from logs alone.
- [ ] The halt control was drilled in the last 30 days and reached a safe state (drill evidence pack present).
- [ ] Overrides show approver identity, reason and the evidence the approver saw.
- [ ] Declared accuracy, test population and date appear identically in instructions for use and the release eval report.
- [ ] ISO 42001 Annex A groups each cite at least one live artefact, or a justified exclusion.

## 7. Anti-patterns

- Treating "human in the loop" as a click-through approve button with no evidence shown (fails Art. 14(4)(b) automation-bias intent).
- Keeping a separate "AI Act log" outside the hash-chained audit log.
- Copying the deferred dates into contracts as if they cannot move again.

## Worked example

A Kampala-built HR SaaS sells a CV-screening agent to a Dutch employer. Employment
is an Annex III area and the agent ranks candidates (profiling), so no derogation
applies: high-risk, vendor is provider. Launch gate: classification record,
per-candidate decision log with retrieval set and model version, recruiter
override with reason, halt drill evidence, and an accuracy and group-error report
from the release eval. The same tenant in Uganda uses the same controls; the
Uganda Data Protection and Privacy Act 2019 position on automated decisions is a
counsel question (`NOT_ASSESSED` here).

## Evidence/currentness

Access date 2026-09-24.

- EU AI Act (Regulation (EU) 2024/1689) Arts. 12, 14, 18, 19, 26(6), 73: consolidated text at artificialintelligenceact.eu (verified for the provisions cited).
- Regulation (EU) 2026/1744 (Digital Omnibus on AI): OJ entry at eur-lex.europa.eu/eli/reg/2026/1744/oj, in force 27 July 2026; Annex III 2 December 2027 and Annex I 2 August 2028 dates corroborated by published legal analyses. EUR-Lex full text was not machine-readable at access: exact amended wording, any change to Art. 50 transition or AI-literacy duties, and Art. 6(3) wording after amendment are `NOT_ASSESSED`.
- ISO/IEC 42001:2023: iso.org/standard/42001, sole published edition (EN ISO/IEC 42001:2026 is the CEN adoption of the same text). Annex A group titles from secondary summaries; individual control wording `NOT_ASSESSED` - read the purchased standard before an SoA.
- Legal classification is counsel's decision; this file is engineering guidance.
