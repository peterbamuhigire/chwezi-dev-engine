# Design Specification: 18-Book Cross-Engine Kaizen Wave

**Date:** 2026-09-02  
**Status:** Approved for implementation  
**Scope:** Eleven canonical skill engines and the eighteen supplied Markdown book sources

## Objective

Translate durable, independently synthesised lessons from the supplied books into repeatable
skill-engine capability without copying book text, importing obsolete commands, or treating a
book as authority for current standards, policies, product capabilities, or platform facts.

## Design decisions

1. **Digital Research is the currentness gate.** Every book-derived change that contains a
   current, versioned, legal, security, platform, standards, or lifecycle claim must pass the
   Digital Research source-evaluation, source-verification, and currentness-gate workflow.
   Historical books remain concept inputs and may be marked `historical-only`, `partial`, or
   `NOT_ASSESSED`.
2. **The central crosswalk is the system of record.** The 18-source study status, independent
   synthesis, engine applicability, implementation decisions, source ledger, and residual gaps
   live in `docs/continuous-improvement/book-driven-kaizen-wave-3-2026-09-02.md`.
3. **Existing ownership wins.** Upgrade existing Kaizen owners and domain references where the
   capability already has a route. Do not create a new domain skill for a theme that an existing
   skill can own.
4. **One justified new skill.** The Windows engine lacks a Kaizen owner route. Add
   `skills/meta/kaizen-engine-and-product-improvement/SKILL.md`, its reference, catalogue entry,
   and routing regression. This is a distinct ownership gap, not a convenience alias.
5. **Reference-first adoption.** Each engine receives one concise, engine-specific
   `book-driven-kaizen-wave-3-2026-09-02.md` reference. It contains durable principles,
   safe transfer boundaries, currentness requirements, suggested measures, and routing targets;
   it does not store raw excerpts or executable cookbook scripts.
6. **Security and execution are bounded.** Shell, exploit, HTTP, image, and agent examples are
   treated as risk-bearing inputs. The upgraded skills require parameterisation, least
   privilege, dry-run or safe fixtures, rollback, source verification, and human approval for
   consequential actions. No exploit recipe or unsafe legacy script is standardised.
7. **Book availability is explicit.** The supplied prompt-engineering Markdown is empty and its
   alternate PDF is a 404 HTML placeholder. It is recorded as `NOT_ASSESSED`; no claims are
   derived from it.

## Book-to-capability synthesis

| Source family | Durable transfer | Primary owners | Currentness boundary |
|---|---|---|---|
| Shell scripts; UNIX internals | Explicit contracts, quoting, exit status, signals, processes, filesystems, failure recovery, observability | Linux, Windows, Engineering, SRS | Verify shell/distro/PowerShell commands and host controls against current primary docs |
| Git | Local snapshots, traceable change, safe remote collaboration, recovery, review, release hygiene | Engineering, SRS, all engine maintainers | Verify modern Git commands, branch protections, signing, hooks, and hosting policy |
| Spring Boot 4; HTTP guide | API semantics, validation, error contracts, transport/cache/intermediary boundaries, testing, observability | Engineering, SRS, Website, Linux, Windows | Verify framework versions, RFCs, dependencies, security, and deployment guidance |
| Bug Hunter's Diary; Perfect Software | Threat-informed testing, input boundaries, risk-based test selection, evidence quality, false-confidence detection, root-cause learning | Engineering, SRS, Linux, Windows, Proposal, Accounting, Research | Reframe historical exploit material as safe defensive testing; verify current security guidance |
| Bandit algorithms; data-science interview | Experiment hypotheses, exploration/exploitation, uncertainty, practical effect, data quality, decision rules | Research, Website, Social, Business, SRS | Verify current experimentation platforms, metrics, privacy, and statistical methods |
| Information retrieval; local SEO | Retrieval/index/evaluation discipline, intent, entity consistency, source visibility, benchmark baselines | Research, Website, Social, Business, Proposal | Verify current search policies, structured-data requirements, platform features, and claims |
| Dashboard design; digital image processing | Task-first communication, hierarchy, context, perceptual integrity, image quality and measured derivatives | Design, Website, Social, Research, Business, Proposal | Verify WCAG, browser/media formats, accessibility, and performance guidance |
| Agentic AI solutions; Human-Agent Orchestrator | Productisation economics, tool boundaries, evaluation before expansion, decision rights, autonomy, intervention, containment, recovery, drift | Engineering, SRS, Research, Business, Website, Social, Proposal, Accounting, Windows | Verify current model/API/MCP/framework/regulatory claims; never infer capability from book examples |

## Cross-engine control contract

Every upgraded owner must require the following record for a book-derived improvement:

- source identifier and study status;
- durable principle versus time-sensitive claim;
- intended engine/skill owner and reason;
- current authoritative source(s), access date, freshness class, support status, uncertainty,
  and review trigger for volatile claims;
- baseline, root cause, reversible change, measure, guardrail, stop/rollback condition,
  acceptance evidence, and re-audit date;
- explicit `NOT_ASSESSED` status for unavailable book content, missing live/lab evidence, or
  unverified current claims.

## Validation contract

Run each engine's native catalogue, routing, source-ingestion, and unit/integration checks. For
the new Windows skill, add its catalogue and routing fixtures before running the same checks.
Run repository-wide text checks for:

- raw-book-text leakage;
- stale `digital-research-engine` path references where the canonical checkout is
  `digital-research-skills`;
- missing currentness gate language in Kaizen owners;
- broken relative references;
- duplicate or ambiguous Kaizen ownership.

Live production, Windows-lab, distro-matrix, visual-render, and external platform checks remain
separate evidence gates. If unavailable, they must remain `NOT_ASSESSED` rather than becoming a
pass through static documentation checks.

## Expected change shape

- 1 new skill: Windows Kaizen owner.
- 10 existing Kaizen owner skills upgraded.
- 11 new engine-specific reference files.
- 2 central planning/study documents in `skills-web-dev`.
- No raw book text, full OCR, copied code listings, or unverified current platform claims.
