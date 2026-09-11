---
name: saas-lifecycle-email-orchestration
description: Use when deriving SaaS lifecycle email decisions from user state, product events, consent, channel pressure, suppression, and measurable outcomes; use the design engine for each message's visual composition and the writing route for its words.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# SaaS Lifecycle Email Orchestration

Design the decision system that determines whether an email should exist, who should receive it,
what verified state it responds to, and when it must stop. Do not begin from a sequence catalogue,
fixed cadence, benchmark, or message template.

<!-- dual-compat-start -->
## Use When

- Product events or state transitions may justify a lifecycle email.
- Email and in-product messages can collide or contradict one another.
- Consent, suppression, frequency pressure, tenant roles, or account state determine eligibility.
- A team needs testable trigger, branch, exit, attribution, and recovery contracts.

## Do Not Use When

- The task is HTML email or newsletter presentation. Route to the design engine's
  `email-and-newsletter-design` skill, which composes the message for its purpose and client matrix.
- The task is subject lines, body copy, or CTA wording. Route to the appropriate content-writing or
  UX-writing skill after the message job and evidence are approved.
- The task is ESP selection, authentication, reputation, bounce processing, or provider operations.
  Use the retained `saas-transactional-email-infrastructure` reference branch.
- The task is acquisition outreach to people without an existing product relationship.

## Required Inputs

| Input | Required | Missing-input response |
| --- | --- | --- |
| User outcome and failure consequence | yes | Do not create a send merely to fill a lifecycle stage |
| Verified product/account state and event semantics | yes | Mark the trigger `NOT ASSESSED` |
| Recipient role, tenant scope, locale, and consent state | yes | Suppress until eligibility is known |
| Competing channels and recent contact pressure | yes | Default to no send until arbitration is defined |
| Exit, invalidation, and recovery conditions | yes | Do not enrol an unbounded flow |
| Measurement basis and decision owner | yes | Treat performance claims as unproved |

## Workflow

1. **Start from a decision moment.** State the recipient's current verified state, the decision or
   task they face, the consequence of silence, and the consequence of an unnecessary message.
2. **Inspect the existing journey.** Map product UI, support, account management, billing,
   notifications, and prior email. Prefer the channel already closest to the action.
3. **Define eligibility as a state predicate.** Use named business events and current state, not a
   calendar label. Separate event occurrence, derived state, and marketing interpretation.
4. **Prove the message earns a send.** Record the unique job email can perform, the evidence it may
   state, and why an in-product, support, or no-message path is insufficient.
5. **Design branches and exits before cadence.** Define invalidating events, success, role changes,
   plan changes, consent changes, duplicate signals, bounces, and account closure. Cadence follows
   urgency and observed behaviour; no universal day count is a default.
6. **Arbitrate channels and pressure.** Use one decision service or auditable rule set to choose the
   best channel and suppress duplicates. Contact limits are product policy informed by measured
   fatigue and legal/consent constraints, not copied benchmark numbers.
7. **Hand off one message job at a time.** Give writing and design owners the audience, decision,
   evidence, required action, hierarchy, fallback state, legal controls, and client matrix. Do not
   prescribe a reusable layout or canned copy.
8. **Implement an idempotent contract.** Persist the evaluated policy version, eligibility reason,
   suppression reason, content version, send attempt, provider response, and downstream outcome.
9. **Test normal and contradiction paths.** Include stale events, duplicate events, late success,
   role/plan changes, unsubscribed categories, tenant isolation, provider retry, and competing
   channel activity.
10. **Release as an experiment only when justified.** Use an ethical comparison or staged rollout,
    predefine success and harm measures, and stop messages that add pressure without user value.

## Decision Rules

| Condition | Action | Failure avoided |
| --- | --- | --- |
| Product state already resolves the user's task | Suppress or use the in-product confirmation | Robotic, contradictory mail |
| Trigger is inferred from stale or ambiguous data | Hold and seek a fresher state observation | False urgency or wrong recipient |
| Several messages compete | Rank by user consequence and choose one channel | Notification pile-on |
| Consent category or lawful basis is unresolved | Stop before enrolment | Unauthorised communication |
| Recipient is not the accountable tenant role | Route to the correct role or suppress | Cross-role disclosure |
| Success or invalidation arrives before send | Cancel idempotently | Obsolete call to action |
| Outcome cannot be measured responsibly | Release only as a labelled operational message, not a growth claim | Invented attribution |

## Quality Standards

- Every send can explain the verified state, recipient eligibility, message job, selected channel,
  policy version, and exit condition.
- The orchestration is state-driven and idempotent; time may be an input but never the only reason.
- Consent, tenant isolation, sensitive data, accessibility, localisation, and legal controls are
  evaluated before content leaves the system.
- Copy and visual hierarchy are purpose-designed for the approved message; no bundled sequence or
  layout template is selected.
- Suppression and channel arbitration are testable independently of the provider.
- Measurement distinguishes delivery, attention proxies, task completion, user harm, and business
  outcome. Opens alone do not establish value.
- Thresholds, delays, and frequency limits are sourced from current product policy or measured
  evidence and carry an owner and review date.

## Anti-Patterns

- A universal welcome/upgrade/retention recipe. Derive the message from the actual product state.
- Fixed T+1/T+3/T+7 sends copied into every product. Let urgency, behaviour, and evidence set timing.
- Treating a score threshold as truth. Calibrate and monitor false positives and affected groups.
- Writing or designing the email before deciding whether it should exist.
- A provider workflow that owns business truth. Keep policy and audit state in an inspectable system.
- Double-firing email and in-product prompts for the same decision.
- Continuing after activation, payment, recovery, role change, unsubscribe, or account closure.
- Calling opens, clicks, or short attribution windows proof of incremental value.

## Outputs

| Artifact | Consumer | Acceptance condition |
| --- | --- | --- |
| Journey decision map | Product, support, and lifecycle owners | Decision moments, channel alternatives, silence/send harms, and owners are explicit |
| Trigger and state contract | Engineering and data | Events, predicates, freshness, idempotency, branches, exits, and tenant scope are testable |
| Eligibility/suppression matrix | Compliance and operations | Consent, role, plan, locale, pressure, contradiction, and recovery paths are covered |
| Message-job handoffs | Writing and design owners | Each message has purpose, evidence, action, hierarchy, constraints, and no selected template |
| Measurement and rollback plan | Product and release reviewers | User outcome, harm guardrails, attribution limits, stop rule, and rollback are approved |

## Evidence Produced

| Category | Artifact | Format | Example |
| --- | --- | --- | --- |
| Correctness | State-transition and eligibility cases | Decision table plus automated tests | duplicate event and late-success cancellation |
| Security | Tenant/role/consent evidence | Matrix and policy test output | recipient scope and suppression reason |
| Operability | Delivery and recovery record | Event lineage/runbook | policy version, attempt, provider result, retry/rollback |
| UX quality | Purpose-specific message handoff | Brief plus rendered-client evidence | user job, image-off order, competing-channel decision |
| Release evidence | Experiment and stop decision | Change record | outcome, harm measure, uncertainty, owner, review date |

## References

- [Journey-derived orchestration](references/journey-derived-orchestration.md) — use when turning a
  product decision moment into state, eligibility, channel, handoff, and measurement contracts.
- [Routing and ownership](references/routing.md) — use when choosing between lifecycle behaviour,
  infrastructure, design, copy, billing, entitlement, and growth owners.
- [Transactional email infrastructure entrypoint](references/saas-transactional-email-infrastructure/entrypoint.md)
  — use for provider, deliverability, domain, suppression transport, and feedback-loop engineering.
<!-- dual-compat-end -->

## Capability Contract

Read-only design is the default. Sending, enrolment, policy/configuration changes, user-data access,
provider changes, experiments, and production instrumentation require explicit authority, exact
tenant/audience scope, rollback, and auditable approval.

## Degraded Mode

Without verified state semantics, consent, recipient scope, channel history, product policy,
telemetry, or action authority, return a decision map and missing-evidence register. Do not invent a
cadence, threshold, benchmark, audience response, or send result.

## Stop Conditions

Stop before release when the message job is not unique, a safer channel exists, state freshness is
unknown, consent or role is ambiguous, suppression/exit paths cannot be tested, content lacks
approved evidence, or production and rollback authority is absent.

This workflow preserves event and lifecycle engineering while rejecting both visual and behavioural
template catalogues. Email composition belongs to the design and writing engines; this skill owns
the auditable decision to send or suppress.
