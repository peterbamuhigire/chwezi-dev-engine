# Documentation index

Where each kind of record lives. Start with the root [`README.md`](../README.md) for what the
engine is, how to install it, how to run its validators and what the October 2026 kaizen improved, and [`AGENTS.md`](../AGENTS.md) for
the router that agents read. Dated records (audits, updates, kaizen cycles) are history: they
describe the tree as it was on their date, and some still name the former repository name or a
Windows checkout path.

## Start here

| Need | File |
|---|---|
| What the repository is, the file model and the policy | [`overview/README.md`](overview/README.md), then [`overview/PROJECT_BRIEF.md`](overview/PROJECT_BRIEF.md), [`overview/ARCHITECTURE.md`](overview/ARCHITECTURE.md), [`overview/TECH_STACK.md`](overview/TECH_STACK.md) |
| Which skill replaced a retired slug | [`skill-routing-index.md`](skill-routing-index.md) and [`skill-aliases.yml`](skill-aliases.yml) |
| Using the catalogue from another repository | [`USING-IN-A-PROJECT.md`](USING-IN-A-PROJECT.md) |
| Plain-language value statement for clients | [`CLIENT-VALUE-BRIEF.md`](CLIENT-VALUE-BRIEF.md) |
| What is planned next | [`plans/NEXT_FEATURES.md`](plans/NEXT_FEATURES.md) and [`plans/INDEX.md`](plans/INDEX.md) |

## Quality and improvement records

| Folder | Contents |
|---|---|
| [`kaizen/2026-10-engine-kaizen/`](kaizen/2026-10-engine-kaizen/README.md) | The 29 October 2026 pass: scope, frozen baseline, backlog, experiment log, validation record, final report and next-cycle handoff. |
| [`kaizen/2026-10-engine-kaizen-pass-2/`](kaizen/2026-10-engine-kaizen-pass-2/README.md) | The 31 October 2026 pass, same seven records. Its [final report](kaizen/2026-10-engine-kaizen-pass-2/05-final-report.md) holds the latest published score and its [handoff](kaizen/2026-10-engine-kaizen-pass-2/06-next-cycle.md) the open findings. |
| [`quality-gates/`](quality-gates/anti-slop-governance.md) | Release-blocking gates, anti-slop governance, and the duplicate-heading and broken-link baselines that may only shrink. |
| [`source-registers/`](source-registers/ai-platforms.md) | Dated source records for volatile platform, AI, security and framework facts; checked by `scripts/check_source_register.py`. |
| [`audits/`](audits/2026-09-06-kaizen/portfolio-progress.md) | Dated audit records, including the 2026-09-06 portfolio cycle and the 2026-09-29 re-audit. |
| [`evaluation/`](evaluation/2026-05-30-production-readiness-audit.md) | Earlier evaluation records, including the 2026-05-30 production-readiness audit. |
| [`continuous-improvement/`](continuous-improvement/english-output-standard-2026-09-02.md) | Kaizen waves from August and September 2026 and the human-facing English output standard. |
| [`engine-upgrade-july-2026/`](engine-upgrade-july-2026/00-executive-summary.md) | The July 2026 engine upgrade reports. |

## Change records

| Folder | Contents |
|---|---|
| [`updates/`](updates/2026-10-31-dev-engine-kaizen-pass-2.md) | One dated note per substantive documentation or capability change, newest first by file name date. |
| [`../CHANGELOG.md`](../CHANGELOG.md) | Dated summary of each change, with the evidence folder to read. |

## Platform, control plane and contracts

| File or folder | Contents |
|---|---|
| [`engine-control-plane.md`](engine-control-plane.md), [`engine-control-plane.json`](engine-control-plane.json) | The shared agent, command, hook, evidence and handoff contract across the twelve registered engines, and how to validate it. |
| [`approval-contract.md`](approval-contract.md), [`approval-enforcement.md`](approval-enforcement.md), [`approval-policy.json`](approval-policy.json), [`approval-adapter.json`](approval-adapter.json) | The shared human-approval contract and its adapter. |
| [`ai-prompting/`](ai-prompting/domain-prompt-compilation-contract.md) | The domain prompt-compilation contract. |
| [`markdown-portability-reference.md`](markdown-portability-reference.md) | Formatting rules for Markdown that renders the same on GitHub and through Pandoc. |
| [`routing-collision-allowlist.yml`](routing-collision-allowlist.yml) | Description pairs allowed to stay similar, read by the collision gate. |
| [`engine-status/`](engine-status/windows-admin-engine.md) | Status record of the Windows administration engine registered in the control plane. |

## Studies, plans and exemplars

| Folder | Contents |
|---|---|
| [`plans/`](plans/INDEX.md) | Planning documents and their status. |
| [`world-class-exemplars/`](world-class-exemplars/running-example.md) | The running example used across architecture, API, security and release artefacts. |
| [`sept-matt-pocock/`](sept-matt-pocock/README.md) | The 2026-09-11 external-repository comparison and its completion record. Evidence, not an active skill root. |
| [`analysis/`](analysis/00-index.md) | The May 2026 audit of the repository as a development engine, with a master index. |
| [`game-dev-analysis/`](game-dev-analysis/README.md) | The July 2026 game-development capability audit and its source-disposition records. |
| [`scaling-ops/`](scaling-ops/00-index.md) | April 2026 infrastructure strategy for a VPS-based software studio. |
| [`catalog-cleanup/`](catalog-cleanup/empty-directory-disposition.md) | Disposition of empty legacy directories. |
| [`skills-trimminhg.md`](skills-trimminhg.md) | The consolidation report (the file name keeps its original spelling). |
| [`superpowers/`](superpowers/) | Earlier plans and specifications (`plans/`, `specs/`). |
