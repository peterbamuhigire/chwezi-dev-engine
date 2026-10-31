# Project Brief

## Summary

The October 2026 Kaizen adds a tenant-scoped invoice example across PHP, a
Next.js App Router, and Compose, with runtime limits and native discovery
evidence recorded in `docs/kaizen/2026-10-engine-kaizen/`. Pass 2 of the same
month (`docs/kaizen/2026-10-engine-kaizen-pass-2/`) repaired source currency,
validator portability and content hygiene; its final report publishes 62.5/100
raw and capped, and the 95/100 target is not reached.

The engineering runtime contract now has fixture-tested local utilities for
versioned context, prompt/data boundaries, provenance-bound tool approval,
bounded action budgets and pure deterministic planning. These are host-facing
helpers, not a production agent runtime.

This repository is a curated AI skills and documentation engine. It helps
coding agents and human operators select reusable workflows for software
engineering, AI systems, SaaS operations, finance-doctrine orchestration, mobile development,
security, UX, and SDLC documentation.

PHP engineering guidance now pairs application compatibility checks for staged
minor-version upgrades with an explicit handoff to the Linux operations engine
for OS packages, web handlers, workers, and production cutovers. The 2026-10-22
security/currentness record covers the emergency PHP RCE release and PHP 8.5
validation path.

The current catalog includes a consolidated enterprise Java/JVM engineering
route and WWDC26-era Apple development guidance across iOS,
mobile operations, AI, App Intents/Siri/Spotlight, StoreKit, quality/release,
security, PWA/Safari, and companion design-system routing.

## Primary Users

| User | Need |
| --- | --- |
| Coding agents | Fast skill discovery, accurate routing, concise execution rules. |
| Developers | Reusable implementation guidance and quality gates. |
| Product and operations teams | Product, SaaS, documentation, and governance playbooks. |
| Finance implementers | Canonical accounting, controls, close, audit, and reporting doctrine. |

The shared control-plane registry describes twelve engines; the 2026-09-06
local Kaizen scope covers the eleven installed checkouts confirmed by the user.
See `docs/engine-control-plane.md` and the audit's portfolio progress record.

## Outcomes

- Reduce repeated prompt and documentation work.
- Keep domain rules close to execution guidance.
- Maintain a skill catalog that is small enough to route reliably, with routing
  precision measured (not assumed) and guarded in CI.
- Turn agent output into production-grade work a team can maintain: every
  meaningful change carries a Delivery Definition of Done pack (tests, release,
  rollback, runbook, maintenance notes).
- Preserve deep references without making every skill entrypoint heavy.
- Support Windows, Fedora, Ubuntu, and Debian consumers with portable Markdown and
  Python tooling. The full validator set ran on Fedora Linux on 2026-10-31 and
  CI runs on Ubuntu; Windows was not re-run in the October 2026 passes.
- Give downstream Python projects a repeatable path from multiple scripts or
  GUIs to a launcher, shared executable suite, portable archive, installer,
  signing boundary, CI build, and release evidence.

## Non-Goals

- This is not a deployable application.
- This repository does not expose an HTTP API.
- This repository does not own a database schema.
- This repository should not be treated as a package registry without an
  explicit release workflow.

## Current Risks

- The [Matt Pocock skills comparison](../sept-matt-pocock/README.md) drove a repository-level Kaizen
  for systematic diagnosis, dependency-frontier questioning, persistent domain language, work
  graphs, two-axis review, and skill attention mechanics. Structural implementation and lab fixtures
  are complete; production outcomes, host invocation, fresh-agent handoff, and independent review
  remain `NOT ASSESSED`.
- The active skill count is 167, inside the 150-180 target after the 2026-09-24 consolidation of
  18 overlapping skills; future additions still need equal-value consolidation or alias discipline. The CI guardrail (200 hard cap) and the collision
  detector keep this from becoming routing noise.
- Inactive aliases must stay documented in `docs/skill-aliases.yml`; the
  alias-integrity check now fails CI on a stale or unrouted alias, so this is
  caught automatically rather than by memory.
- New skills can shadow a neighbour's routing. Add a fixture to
  `scripts/routing_fixtures.yml` for any skill a sibling could steal traffic
  from, so the smoke test guards it.
- The October 2026 pass-2 handoff
  (`docs/kaizen/2026-10-engine-kaizen-pass-2/06-next-cycle.md`) lists what is still
  open: a user-local settings file tracked in this public repository, the invoice
  example's contract gaps, 24 skills with a duplicate heading, 84 broken relative
  links, thin routing coverage, and source records that start failing the review-date
  check from 2026-11-04 (calendar in the root `README.md`).
- Apple beta-era APIs can change after WWDC26; keep code examples
  availability-gated and source-labeled until final release notes are reviewed.
