# AI-Generated Code Review Gate

Parent skill: `../SKILL.md`. Load before merging any change where an AI assistant or agent wrote a material part of the diff. The gate exists so AI output ships at the standard of a senior engineer who owns it, not at the standard of "it runs and the tests the same agent wrote are green".

## Why a separate gate

Code generators optimise for satisfying the prompt. Non-functional qualities (performance, accessibility, failure handling, dependency weight, currency of APIs) appear only when requested or when the surrounding code forces them. Requests to "make it faster" frequently return plausible edits that change behaviour or do not measurably help. Treat every AI performance or refactor claim as a hypothesis until a measurement confirms it. Treat generated volume as a cost: more code means more bytes, more parse and execute time, more surface to maintain.

## Inputs

| Input | If missing |
|---|---|
| Diff with provenance (which parts were generated, by which tool, from which prompt or plan) | Reviewer marks provenance `NOT_ASSESSED` and reviews the whole diff at the AI standard |
| Acceptance criteria and non-functional budgets (performance, a11y, security) for the touched flow | Stop; request budgets from `frontend-performance`, `observability-monitoring`, or the SRS |
| Test, type-check, lint, bundle-size, and security scan results from CI | Gate cannot pass; return findings only |
| Representative data volumes (rows, list lengths, payload sizes) | Reviewer states the assumed volume explicitly |

## Procedure

1. **Frame before generation.** Put the non-functional requirements in the prompt or plan: target flow budget, data volume, device class, a11y level, allowed dependencies, error and empty states. Unstated requirements will be absent from the output.
2. **Read every line.** Review generated code as you would a capable newcomer's first PR in this codebase: you must be able to explain each function. Anything you cannot explain is either removed or rewritten.
3. **Run the blocking checks** in the table below. A single blocking failure fails the gate.
4. **Measure, then accept.** For any change justified as faster, smaller, or more scalable, attach before/after evidence under the same conditions (benchmark, trace, bundle diff, query plan). No evidence, no claim.
5. **Prune.** Delete speculative options, unused branches, duplicated helpers, compatibility shims for unsupported environments, and verbose logging. Prefer the smallest diff that meets the criteria.
6. **Record.** Complete the review record at the end of this file and link it from the PR.

## Blocking checks

| Dimension | Blocking finding | Typical generated pattern |
|---|---|---|
| Correctness | Behaviour not covered by a test that would fail if the logic were wrong; tests written by the same agent that only assert the implementation's own output | Tautological or snapshot-only tests |
| API currency | Deprecated or invented API, outdated library major, legacy platform idiom where a current one exists | `document.write`, XHR wrappers, removed framework APIs, old CI action majors, `setup.py`-only packaging |
| Algorithmic cost | Super-linear work on unbounded input without justification | Nested loops for de-duplication or joins; sort/filter inside render; repeated DOM queries in loops |
| Data access | N+1 queries, missing index for a new predicate, serial calls that could be batched or parallelised | ORM loop fetching relations; sequential `await` of independent requests |
| Main thread (web) | Handler or render path adds a long task (> 50 ms on the reference device) | Filtering thousands of items per keystroke; synchronous JSON parse of large payloads |
| Payload | New dependency or chunk over budget without an ADR; heavy library for a trivial need | Date, chart, or utility libraries imported whole for one function |
| Layout stability | Media or async content without reserved space; insertion above the reader | `<img>` without dimensions; list injected above existing content |
| States and failure | Missing loading, empty, error, retry, timeout, or cancel handling on a user-visible path | `catch` that only logs; spinner with no timeout |
| Accessibility | Missing names, roles, focus management, keyboard paths, or contrast for new UI | Clickable `div`; modal without focus trap; icon button without label |
| Security | Unvalidated input at a trust boundary, secret in code, unsafe HTML sink, missing authorisation or tenant scope | String-built SQL; `innerHTML` with user data; handler that trusts client-supplied tenant ID |
| Supply chain | Package that does not exist, is unmaintained, has an incompatible licence, or was not in the approved list | Hallucinated or typo-squatted package names |
| Consistency | Violates local conventions (error model, logging, naming, layering) | Second HTTP client, parallel validation scheme |

## Decision rules

| Condition | Decision | Wrong choice |
|---|---|---|
| Generated change touches a critical flow | Run the flow's performance gate and a field-comparable lab run before merge | Merging on unit tests hides INP/LCP regressions that surface only on low-end devices |
| AI proposes an optimisation | Benchmark on production-like data; keep only if the gain exceeds noise and behaviour is unchanged | Accepting plausible micro-optimisations that change semantics |
| Diff is large and mostly generated | Split into reviewable slices or reject | Rubber-stamping volume the reviewer did not read |
| AI adds a dependency | Justify against native or existing code; check size, maintenance, licence, advisories | Bundle and supply-chain debt accumulate silently |
| Tests were generated with the code | Add at least one independently reasoned case per risk (boundary, failure, authorisation) | Tests that mirror the implementation prove nothing |

## Using AI inside the review

Use agents for search, trace summarisation, and drafting fixes when you already know what the fix should be. An agent connected to browser tooling can record a trace and name the longest tasks; a human still decides and verifies with the same measurements the gate uses. Never let the generating agent be the only reviewer of its own work.

## What senior-grade looks like versus generic AI output

- Generic: working happy path, broad dependency, no states, tests that restate the code, claims of "optimised" with no numbers.
- Senior-grade: smallest diff in local style, explicit data-volume assumption, bounded cost, reserved layout and designed states, accessible by default, current APIs, independent tests, and measured evidence for every performance claim.

## Worked example (original)

An agent generates a React customer-search screen for a Mbarara SACCO's staff portal. It works on 50 test members. Review finds: filtering 38,000 members on every keystroke in render (INP 420 ms on the branch's entry-level laptops), a full date library imported to format one field, no empty or error state, and results injected above the search box. The gate fails. Fixes: server-side search with a 250 ms debounce and cancellation of stale requests, native `Intl.DateTimeFormat`, designed empty/error/timeout states with a live-region announcement, results rendered below a reserved container, and a test that asserts stale responses are discarded. Evidence: trace shows the longest interaction task at 38 ms; bundle diff minus 71 KB compressed.

## Review record

```text
Change: <PR link>          Flow: <critical flow>       Provenance: <tool, prompt/plan link, generated %>
Budgets applied: <perf / a11y / security refs>
Blocking checks: <pass | fail + finding per dimension, or NOT_ASSESSED with reason>
Measurements: <before/after numbers and conditions>
Pruned: <what was removed>
Reviewer: <name>   Decision: <merge | revise | reject>   Date: <YYYY-MM-DD>
```

## Evidence and currentness

Accessed 2026-09-24: current API and tooling checks follow `frontend-performance/references/performance-engineering-procedure.md` (Lighthouse 13.5.0, `web-vitals` 6.x, Node.js 24 LTS). Industry statistics on AI-code defect and duplication rates change quickly and are deliberately not restated here; cite them only after verification through `digital-research-engine`. Tool-specific agent features (browser-tooling MCP servers, IDE assistants) are `NOT_ASSESSED` for current capability.

Sources: Osmani (2026) *Web Performance Engineering in the Age of AI*; Oliveira (2024) *AI Strategies for Web Development*; this engine's `ai-slop-audit`, `vibe-security-skill`, and `frontend-performance` skills.
