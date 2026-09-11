# Pocock Workflow Kaizen Completion Record

Date: 2026-09-11

Re-audit: 2026-10-11

Comparison source: `mattpocock/skills` commit `3cca18b368ae95cdbdebbff572ccafa662551015`

## Technical summary

The repository-level implementation is complete across eight canonical Chwezi repositories. The
engineering catalogue is back inside its soft range at **170 active skills**, all **170/170** pass
the portable contract, evidence-contract debt is **zero**, routing improved from **91% to 98%**
top-one while retaining **100%** top-three, and the assembled runtime check passes at **205 skills,
45,521 description characters, and 50,169 metadata characters**.

The operation adopted compact workflow mechanics rather than importing Pocock's engine wholesale.
It added one narrowly routed diagnosis skill, progressive references, deterministic frontier/work
graph/review/diagnosis/lifecycle validators, and domain adapters. Ten overlapping engineering skills
became routed aliases, preserving their bodies while paying for the new route and reducing metadata
load.

This is a structurally verified Kaizen release, not proof of production outcomes. Fresh-agent
handoff success, host-level invocation traces, real-project before/after outcomes, independent
review, stakeholder acceptance, and new-session model startup remain `NOT ASSESSED`.

## Before and after

| Measure | Before | After | Interpretation |
| --- | ---: | ---: | --- |
| Comparison score, raw | 58/100 | 69/100 provisional | Wave 1 and Wave 2 mechanisms are implemented and lab-tested |
| Published score | 58/100 | 65/100 | Permanent audit cap remains until applied and independent proof exists |
| Active engineering skills | 179 | 170 | At the soft ceiling; below the hard cap of 200 |
| Portable contract | 153/179 | 170/170 | All active routes now pass |
| Missing evidence declarations | 66 | 0 | Missing section now fails the strict gate |
| Routing precision@1 | 144/158 (91%) | 157/160 (98%) | Descriptions and consolidation improved selection |
| Routing precision@3 | 158/158 (100%) | 160/160 (100%) | No fixture lost its expected route |
| Assembled runtime skills | 214 | 205 | Nine-entry net reduction |
| Runtime description characters | 46,853 | 45,521 | Lower discovery-context cost |
| Runtime metadata characters | 51,680 | 50,169 | Lower assembled metadata cost |

The raw score stops at 69 because Wave 3's production, stakeholder, and independent-review evidence
does not exist. The change does not claim a 75+ result.

## What changed

### Skill attention and authoring

`skill-writing` now routes to five focused references:

- context-pointer quality;
- the always-loaded versus branch-loaded context budget;
- invocation ownership;
- leading-word and trigger design;
- completion criteria and handoff.

The portable validator accepts and validates optional `metadata.invocation` values of `implicit`,
`explicit`, or `both`, and rejects an explicit route whose description does not say that direct or
explicit invocation is required. Host enforcement remains separately gated.

### Systematic diagnosis

`skills/sdlc-meta/systematic-bug-diagnosis` is a new evidence-led route for defects, regressions,
intermittent failures, performance symptoms, and production-only observations. Its three references
cover tight-loop construction, falsifiable hypotheses and instrumentation, and hard cases. It ships
with human and machine-checkable diagnostic records plus a gate that blocks causal claims before
observed red evidence, fixes without authority, unmeasured intermittent claims, unbounded performance
comparisons, and unauthorised production instrumentation.

### Decision frontiers and domain language

The SRS engine now owns the canonical decision-frontier interview and domain-language decision
references. The frontier validator blocks unknown prerequisites, dependent decisions asked early,
and supposedly ready decisions that are still blocked. Business-plan, proposal, website, social,
engineering discovery, and design workflows point to that owner and add only domain-specific
outputs. Fixed questionnaire counts and unsupported response-rate thresholds were removed.

### Work graphs, review, architecture, and handoff

- Execution planning now uses tracer-bullet nodes, explicit blockers, a runnable frontier,
  expand-contract handling, and a YAML validator that rejects cycles, unknown dependencies, and
  evidence-free completion.
- Code review now reports specification fidelity and engineering standards independently. A
  deterministic gate proves that spec-pass/standards-fail and standards-pass/spec-fail both block.
- Architecture gained deep-module and design-it-twice decision guidance without adding a competing
  route.
- Control-plane handoffs gained pointer-rich resume guidance; delivery gained bounded human-only
  operation wizards; Git collaboration gained intent-led conflict resolution.
- Product discovery and interaction design gained question-answering prototype guidance with a
  disposal/rewrite boundary rather than production leakage.
- Content writing gained fragments-to-beats-to-shape exploration, and the English standard gained
  a re-pitch gate when a reader cannot explain the point back.

### Lifecycle and catalogue control

The coordination package now validates `promoted`, `experimental`, `deprecated`, and
`reference-only` lifecycle states and `implicit`, `explicit`, and `both` invocation states. A
non-promoted `SKILL.md` in an exposed root fails. The validator also rejects a directory containing
both `SKILL.md` and `ALIAS.md`.

Ten active routes became aliases:

| Alias | Canonical route |
| --- | --- |
| `android-tdd` | `android-development` |
| `android-data-persistence` | `android-development` |
| `mysql-operations` | `mysql-engineering` |
| `postgresql-operations` | `postgresql-engineering` |
| `ios-ai-ml` | `ios-platform-capabilities` |
| `ios-architecture` | `ios-development` |
| `ios-data-persistence` | `ios-platform-capabilities` |
| `ios-quality-and-release` | `mobile-platform-operations` |
| `blender-game-asset-production` | `game-3d-asset-pipeline` |
| `ai-entitlements-and-feature-gating` | `saas-entitlements-and-plan-gating` |

Each original body remains in place as `ALIAS.md`, each parent links the retained material, and the
human index, machine alias registry, and routing fixtures agree.

### Email design without layout templates

The design engine's email route no longer contains or routes to the large worked email template.
It starts from audience, event, decision, content priority, image-off reading order, brand voice,
and client matrix, then selects only compatibility patterns needed by that message. The engineering
lifecycle route was also rewritten: six fixed sequence recipes and their hard-coded cadences and
benchmarks were removed in favour of a journey/state-derived decision method. Transactional
infrastructure guidance now uses provider-neutral selection and a dated primary-source register
covering RFC 7208, RFC 6376, RFC 9989, RFC 8058, Gmail, and Yahoo requirements. The retained design
tree is a client-compatibility pattern library, not a layout-template collection.

## Repository ownership and validation

| Repository | Implemented scope | Verification result |
| --- | --- | --- |
| `skills-web-dev` | Diagnosis, attention, work graph, review, architecture, prototypes, handoffs, evidence, aliases, routing | Full pytest green; 170 active; 0 catalogue findings; strict contract clean; 98%/100% routing |
| `srs-skills` | Canonical decision frontier, domain language, ADR link, questionnaire repair | Full pytest exit 0 at 95.93% coverage; 157 active; 52/52 routing; 0 source findings |
| `chwezi-engine-agents` | Lifecycle/invocation validator and operating contract | 8 tests passed; lifecycle and catalogue validators pass; runtime budget passes |
| `design-system-skills` | No-template email composition and question-answering visual prototypes | 90/90 compliant; 80 tests passed; 54 fixtures at 100% top-three |
| `business-plan-skills` | Intake frontier adapter | 126/126 compliant; 40/40 routing |
| `social-media-skills` | Intake frontier adapter | 177/177 compliant; 26/26 routing; claim support remains evidence-gated |
| `website-skills` | Brand-strategy frontier adapter | Registry/contract/routing checks pass; field CWV remains `NOT ASSESSED` |
| `proposal-skills` | Sales-discovery frontier adapter | 109 skills, 0 findings; 19/19 routing; encoding/link checks pass |

The engineering control-plane validator resolves all 12 registered installed checkouts with zero
findings. Source-ingestion guards are clean in every repository where the operation added or changed
source-derived doctrine.

### Final command ledger

| Command/gate | Final result |
| --- | --- |
| Engineering `pytest tests` | 93 passed, 3 skipped |
| Engineering catalogue guardrail | 170 active, 0 findings |
| Engineering strict evidence contract | 164 scanned, 0 errors, 0 warnings, 6 explicit exemptions |
| Engineering routing | 157/160 top-one; 160/160 top-three; 0 failures |
| Engineering source-ingestion guardrail | 0 findings |
| SRS full pytest | exit 0; 95.93% coverage |
| SRS skill/routing/source gates | 157 active; 52/52 top-three; 0 source findings |
| Coordination pytest/lifecycle/catalogue | 8 passed; 0 lifecycle findings; 11 unique catalogue engines valid |
| Runtime budget | 205 skills; 45,521 description chars; 50,169 metadata chars; 0 findings |
| Design pytest/engine/routing | 80 passed; 90/90 compliant; 54 fixtures at 100% top-three |
| Website pytest/contracts/routing | 38 passed; zero contract debt; 31/31 top-three |
| Business-plan engine/routing/source | 126/126 compliant; 40/40 top-three; 0 source findings |
| Social engine/routing/freshness/source | 177/177 compliant; 26/26 top-three; 22 current source records; 0 ingestion findings |
| Proposal engine/routing/encoding-links/source | 109 active, 0 findings; 19/19 top-three; all gates pass |
| All eight staged diffs | `git diff --cached --check` exit 0 |

## Required matrix disposition

| Capability | Repository evidence | Status |
| --- | --- | --- |
| Invocation schema | Positive, invalid-value, and explicit-description tests | PASS structurally; host trace `NOT ASSESSED` |
| Frontier dependency | Ready, blocked, early-dependent, and unknown-prerequisite tests | PASS |
| Domain language | Proposed/ratified ownership and conflict rules | PASS structurally; project disagreement fixture `NOT ASSESSED` |
| Diagnosis | Normal, no-red, missing-environment, intermittent, performance, and production-only gates | PASS in lab |
| Work graph | Frontier, cycle, unknown dependency, missing field, and evidence-free completion tests | PASS |
| Wide refactor | Expand-contract reference and green-boundary rule | PASS structurally; CI-history pilot `NOT ASSESSED` |
| Two-axis review | Both planted one-axis failures block independently | PASS |
| Prototype | Question, structural alternatives, disposal/rewrite rule | PASS structurally; rendered project pilot `NOT ASSESSED` |
| Handoff | Pointer-rich record contract | PASS structurally; fresh-agent completion `NOT ASSESSED` |
| Lifecycle | Non-promoted runtime entry and mixed alias/skill failures | PASS |
| Currentness | Dated source register and stale-source fail-closed tests | PASS for recorded sources |

## Model-currentness decision

Official OpenAI model pages and the local cache were checked on 2026-09-11. `gpt-6-astra` remains
the documented root/reviewer choice and `gpt-5.6-luna` the bounded execution choice based on
task-fit and cost. The mandatory helper currently reports `DRIFT: root model policy drift` because
the active runtime configuration does not match the checked-in Astra-root policy. Its attempted
Luna-only rewrite was rejected and restored because Peter has not authorised replacing the pins.
Account entitlement and a successful new-session startup remain `NOT ASSESSED`; no running-session
model claim is made.

## Failed or rolled-back experiments

- The model helper's Luna-only policy rewrite was rolled back because it contradicted the pinned
  repository contract and lacked replacement authority.
- The first strict contract command used an unsupported `--root` option; the correct `--all
  --strict` command passed.
- The first design validation used stale script names; native command discovery found the correct
  scripts. Full tests then exposed and drove repair of the deleted email-template fixture and the
  90-skill zero-debt baseline.
- A focused SRS test run tripped the repository-wide coverage threshold by running too narrow a
  selection; the full suite passed at 95.93% coverage.

## Remaining evidence gaps

- Independent fresh-context reviewer: `NOT ASSESSED`; no available spawn interface could guarantee
  the required role/model and fresh context.
- Real-project before/after measures for diagnosis time, question redundancy, review escapes,
  merge conflicts, and handoff success: `NOT ASSESSED`.
- Claude strict plugin validation and Codex host invocation traces: `NOT ASSESSED`.
- Real email-client matrix, live website render, accessibility audit, and stakeholder acceptance:
  `NOT ASSESSED`.
- ISO clause-level certification and product conformance: `NOT ASSESSED`.

These gaps prevent a 75+ score but do not invalidate the deterministic repository changes.

## Final anti-slop audit

Verdict: **B, releaseable with declared evidence limits**. The implementation names owners,
failure consequences, executable checks, rollback, and uncertainty; banned filler language and
template-first email design are absent from the live routes. The grade remains below A because real
project outcomes, a fresh reviewer, and stakeholder evidence are `NOT ASSESSED`. No Grade F pattern
was found.

## Rollback and next cycle

- Deactivate diagnosis by renaming its entrypoint to `ALIAS.md` and retaining its references under
  advanced testing if routing regresses.
- Lower new validator severity while keeping records if a supported host cannot express the
  lifecycle or invocation contract.
- Restore an aliased entrypoint only with collision evidence, an updated budget, and a routing
  fixture proving capability loss.
- Revert domain wrappers independently; SRS remains canonical.
- Do not restore the deleted email template. If email quality regresses, improve composition and
  client-compatibility references from observed failures.

On 2026-10-11, refresh Pocock upstream, rerun official model/currentness checks, execute at least one
real diagnosis and one decision-frontier project, obtain an independent review, and recompute the
raw score from observed outcomes.
