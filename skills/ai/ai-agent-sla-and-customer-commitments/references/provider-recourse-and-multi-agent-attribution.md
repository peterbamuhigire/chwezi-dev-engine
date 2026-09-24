# Upstream Provider Recourse and Multi-Agent Credit Attribution

Load when an SLA breach, refund or credit was caused wholly or partly by an
upstream dependency (LLM provider, embedding or vector service, tool vendor), or
when more than one agent contributed to a task and billing, credits or success
counts must be split. Credit issuance mechanics stay in
[`ai-agent-sla-credit-automation`](ai-agent-sla-credit-automation/entrypoint.md);
exclusion display stays in
[`ai-agent-customer-sla-dashboard`](ai-agent-customer-sla-dashboard/entrypoint.md).

## 1. Inputs

- SLA schedule per tier, including exclusion clauses as signed.
- Upstream contracts: each provider's SLA terms, credit formula, claim window,
  claim evidence required. Many self-serve API terms offer no SLA at all; record
  that as `none`, never assume one.
- Trace bundles with per-step provider, model, region and error class.
- Task graph for multi-agent runs (supervisor, workers, handoffs).

## 2. Decide who bears an upstream failure

| Customer tier / contract | Provider outage treatment | Why |
|---|---|---|
| Self-serve / Pro | Excluded from SLA, disclosed on dashboard with evidence link | Price does not fund redundancy; honest disclosure preserves trust |
| Business | Excluded only if fallback chain was healthy and also failed; otherwise counts | You sold fallback; a missing fallback is your failure |
| Enterprise (bespoke) | Counts toward SLA unless the contract names the provider exclusion explicitly | Enterprise buyers price in your dependency management |

Rule: an exclusion is valid only when (a) the contract names it, (b) the trace
shows the failing step was upstream, and (c) your own mitigation (fallback,
retry budget, cached answer, abstain) was active and behaved as designed. Fail
any of the three and the breach is yours.

## 3. Recourse procedure (per incident window)

1. Classify affected tasks by root step: `own`, `upstream:<provider>`,
   `mixed`. Use the trace, not the incident narrative.
2. For `upstream` tasks, compute what you owe customers under section 2 and
   what the provider owes you under its terms. Keep them in separate ledgers;
   customer credit is never conditional on recovering provider credit.
3. File the provider claim inside its claim window with the evidence it asks
   for (request IDs, timestamps, error codes, region). Store claim ID and
   status against the incident record.
4. Book recovered provider credit against AI COGS for the period, not against
   customer revenue. Hand the entries to the finance engine.
5. Report the recourse gap per quarter: credits issued minus credits recovered,
   per provider. A persistent gap is an architecture signal (add a fallback
   provider, change tier promises), not a finance problem.

## 4. Multi-agent contribution attribution

When several agents act on one customer task, the customer sees one task:
one success verdict, one charge, at most one credit. Internally, attribute for
cost, quality and improvement work.

| Question | Rule |
|---|---|
| What is billed | The task, once, at the task-level verdict. Never sum per-agent resolutions |
| Who "failed" for SLA | The task fails or succeeds as a whole; SLA counters are task-level |
| Internal cost attribution | Sum step costs per agent from the trace; shared supervisor cost split by steps it spent per worker |
| Internal quality attribution | Assign the failure to the first agent whose output violated its handoff contract; later agents inherit only if they accepted invalid input without validation |
| Cross-product agents | When two product lines own agents in one task, revenue sits with the product that owns the customer entry point; the other receives an internal transfer at cost |

Handoff contracts (see
[`ai-agent-multi-agent-coordination`](../../ai-agent-multi-agent-coordination/SKILL.md))
must carry a validation result so the "first violation" rule is decidable from
the trace alone.

## 5. Acceptance checks

- [ ] Every excluded period links a trace sample proving the failing step was upstream and mitigation was active.
- [ ] Customer credits for the window were issued before, and independent of, the provider claim outcome.
- [ ] Provider claims were filed inside each provider's claim window, or the ledger records why not.
- [ ] Recovered credits post to COGS; quarterly recourse gap reported per provider.
- [ ] A multi-agent task shows exactly one billing line and one SLA verdict; internal attribution reconciles to total task cost.

## 6. Anti-patterns

- Blanket "third-party outage" exclusion on an Enterprise contract that sold high availability.
- Delaying customer credit until the provider pays.
- Charging per agent in a supervisor/worker run, so one task produces several resolution charges.
- Attributing failure to the last agent in the chain because it produced the visible output.

## Worked example

A Nairobi logistics tenant on the Business tier loses 340 dispatch-summary tasks
during a two-hour primary-model outage. Traces show the fallback provider was
configured but its API key had expired, so fallback never ran. Condition (c)
fails: the breach counts, credits go out through the normal pipeline, and the
postmortem action is a key-expiry check in the continuous control monitor. The
provider claim is still filed; any recovery reduces COGS for the month.

## Evidence/currentness

Access date 2026-09-24. Provider SLA existence, credit formulas and claim
windows vary by vendor and plan and change without notice: `NOT_ASSESSED` here -
read the current terms for each provider in use. Revenue and COGS treatment of
credits and recoveries: confirm with the finance engine (IFRS 15 variable
consideration for customer credits); not re-verified in this file.
