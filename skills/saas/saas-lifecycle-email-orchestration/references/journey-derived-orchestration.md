# Journey-Derived Lifecycle Orchestration

Use this reference to derive a message from a product decision moment. It is a reasoning and contract
method, not a catalogue of lifecycle sequences.

## Decision record

For each candidate message, record:

| Field | Question |
| --- | --- |
| Observed state | What current, verified product or account state exists? |
| Decision moment | What must the person understand, decide, recover, or complete? |
| Recipient | Which tenant role owns that decision, and what may they see? |
| Silence harm | What happens if no message is sent? |
| Send harm | What confusion, pressure, disclosure, or fatigue can a message cause? |
| Channel choice | Why is email better than in-product, support, account management, or silence? |
| Evidence | Which claims can the product prove now? |
| Invalidation | Which later event makes the message obsolete? |
| Success | Which observable user outcome ends the intervention? |
| Recovery | What happens after bounce, delay, duplicate, provider failure, or bad targeting? |
| Review | Who owns the policy, evidence, and next review date? |

If the candidate cannot answer these fields, do not fill the gap with a familiar sequence.

## State model

Keep these concerns separate:

1. **Fact event:** an immutable observation with tenant, actor, subject, time, source, and schema
   version.
2. **Current state:** a recomputable business state derived from accepted events and authoritative
   records.
3. **Eligibility:** a policy decision over current state, role, consent, locale, pressure, and risk.
4. **Message job:** the approved user decision or task, evidence, action, and hierarchy.
5. **Delivery attempt:** an idempotent operational record, not proof that the user received value.
6. **Outcome:** task completion, recovery, harm, or unresolved uncertainty tied to the policy and
   message version.

This separation prevents an old event, a vendor segment, or a prediction score from becoming
unquestioned product truth.

## Channel arbitration

Rank channels by proximity to the task, urgency, persistence required, accessibility, recipient
context, and pressure. Prefer:

- in-product guidance when the person is already at the action;
- support or account-management contact when judgement or sensitive context is required;
- email when asynchronous reach, durable context, or off-product recovery is genuinely useful;
- silence when no intervention adds user value.

Store the arbitration result and suppression reason. A global contact cap is a governed product
policy with evidence and a review date, not a number copied from another SaaS.

## Message handoff boundary

The orchestration handoff contains facts and constraints, not copy or layout:

- recipient and decision;
- verified evidence and prohibited claims;
- required action or no-action outcome;
- information priority and image-off reading order;
- legal, consent, privacy, accessibility, and localisation controls;
- target client matrix and operational fallbacks;
- invalidation, expiry, and support/recovery route.

The writing owner chooses the words. The design owner composes hierarchy and resilient HTML for the
specific message. Neither owner inherits a canned lifecycle layout.

## Test cases

At minimum, test:

- eligible state produces one decision with one idempotency key;
- duplicate and out-of-order events do not duplicate sends;
- success before delivery cancels the message;
- role, tenant, plan, locale, or consent change re-evaluates eligibility;
- stale state fails closed or requests refresh;
- another channel already resolved the decision;
- provider retry preserves one logical message and audit chain;
- unavailable evidence removes the claim or blocks release;
- high-risk or sensitive cases route to a human rather than automated persuasion.

## Measurement

Define the user outcome first. Separate:

- transport: accepted, delivered, bounced, delayed;
- attention proxies: opened or clicked, with known tracking limits;
- product outcome: the intended task or recovery completed;
- harm: unsubscribe, complaint, contradiction, unwanted disclosure, or pressure;
- business outcome: retained or expanded value with an honest attribution boundary.

Use a comparison design only when it is ethical and operationally sound. Record uncertainty and stop
rules before release. A message that delivers but does not improve the user outcome has not proved
its value.
