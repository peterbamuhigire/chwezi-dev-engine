---
name: saas-transactional-email-infrastructure-reference
description: Read when a SaaS email task concerns provider-neutral event transport, authentication, suppression, feedback loops, delivery telemetry, recovery, or provider selection rather than lifecycle policy, copy, or visual design.
metadata:
  portable: true
---

# SaaS Transactional Email Infrastructure

Build an auditable transport boundary from approved product events to an interchangeable email
provider. Provider features, prices, support, and recipient-network requirements change; verify them
at decision time and do not encode a permanent “best provider” or default stack.

## Ownership

| Concern | Owner |
| --- | --- |
| Whether a lifecycle message should exist | Parent `saas-lifecycle-email-orchestration` skill |
| Message wording | Content-writing or UX-writing route |
| Hierarchy, HTML email, dark mode, accessibility, client rendering | Design engine `email-and-newsletter-design` |
| Event bridge, provider adapter, authentication, suppression transport, feedback and recovery | This reference |

## Inputs

- exact message classes and their delivery/recovery consequences;
- sending and author domains, DNS ownership, recipient networks, regions, and volume shape;
- consent and suppression policy from the accountable owner;
- security, privacy, retention, residency, audit, and availability requirements;
- existing providers, contracts, credentials, incidents, telemetry, and rollback path;
- current recipient-network rules and applicable law verified on the review date.

## Architecture

Use a provider-neutral boundary:

```text
authoritative product event
  -> message-policy decision and idempotency key
  -> durable outbox/queue
  -> provider adapter
  -> provider acceptance response
  -> signed/verified feedback webhook
  -> normalised delivery event and suppression state
  -> audit, alerting, recovery, and user-outcome lineage
```

The product database owns business state. The provider owns transport attempts, not tenant truth,
consent truth, or lifecycle policy.

## Workflow

1. Classify messages by user consequence, consent category, recovery need, and sender identity.
2. Inventory every authorised sender and align domain/DNS ownership before changing records.
3. Verify current standards and recipient-network requirements through
   [the currentness register](references/currentness-register.md); open the primary source before
   relying on a threshold or implementation detail.
4. Define one canonical message command with tenant, recipient role, policy/content version,
   locale, idempotency key, expiry, evidence payload, and trace identifiers. Do not put secrets or
   unnecessary personal data in events.
5. Persist before dispatch. Make retries idempotent and bound them by message expiry and user state.
6. Implement a narrow provider adapter. Map provider responses into stable internal states without
   exposing vendor-specific semantics to business logic.
7. Authenticate feedback webhooks, resist replay, retain raw evidence only as long as justified,
   and normalise bounce, complaint, delivery, delay, and unsubscribe signals.
8. Apply suppression before every attempt. Separate global safety suppression from category and
   purpose-specific preferences; define narrowly authorised transactional exceptions.
9. Test authentication, alignment, MIME/header format, one-click unsubscribe where required,
   bounce/complaint handling, retry, duplicate webhook, stale event, and provider outage paths.
10. Release gradually with current recipient-network dashboards, alerts based on observed baseline
    and provider requirements, a rollback provider/path, and an operator runbook.

## Provider selection without rankings

Create a dated evidence matrix for the actual workload:

| Dimension | Evidence needed |
| --- | --- |
| Message fit | Required transactional, regional, API, workflow, and rendering capabilities |
| Deliverability controls | Authentication support, feedback, reputation visibility, and mitigation process |
| Reliability | Published status/SLA, retry semantics, incident history, regional architecture |
| Security/privacy | Data use, residency, retention, subprocessors, access, encryption, audit reports |
| Operations | Webhook verification, logs, exports, suppression portability, support escalation |
| Economics | Current contract, volume curve, dedicated-resource costs, egress and add-ons |
| Exit | Domain/control ownership, export format, migration and dual-send support |

Run a bounded proof using authorised test recipients and representative message classes. A vendor
marketing claim is not independent deliverability evidence.

## Quality gates

- SPF, DKIM, DMARC, reverse DNS, TLS, alignment, and message format are evaluated for the actual
  sender and recipient networks.
- Marketing/subscribed traffic implements standards-compliant and recipient-required unsubscribe
  controls; transactional exceptions are classified and reviewed rather than assumed.
- No DNS sample is copied into production. Generate provider/domain-specific records, review the
  exact diff, stage policy changes, and preserve rollback.
- Alerts cite the receiver/provider requirement or a measured local baseline and carry a review
  date; no universal bounce, complaint, or inbox-placement number is invented.
- Provider acceptance, delivery, inbox placement, attention, and user outcome remain distinct.
- Suppression, consent, tenant scope, and audit survive provider replacement.

## Failure and recovery cases

- queue delay exceeds message usefulness;
- retry occurs after the underlying state changed;
- duplicate product event or webhook arrives;
- provider accepts but recipient network defers/rejects;
- authentication or alignment changes unexpectedly;
- suppression feed is late or unavailable;
- provider or region is unavailable;
- sender/domain reputation deteriorates;
- webhook signature, replay, or schema validation fails;
- migration requires dual operation without duplicate user contact.

For each case define detection, safe state, operator action, user consequence, retry/expiry, data
retention, and rollback. Do not silently fail open.

## Outputs

- provider-neutral message command and state model;
- domain/authentication and current receiver-requirements evidence;
- adapter and verified feedback contract;
- suppression/consent and data-retention model;
- normal/failure-path test evidence;
- monitoring, incident, migration, and rollback runbooks;
- dated provider decision record with uncertainty and re-evaluation date.

## References

- [Deliverability and authentication operations](references/deliverability-deep-dive.md)
- [Currentness register](references/currentness-register.md)

## Degraded mode

Without authoritative DNS, provider/account access, current receiver requirements, test recipients,
or production authority, produce a read-only architecture and exact verification plan. Mark domain,
delivery, inbox, complaint, and migration outcomes `NOT ASSESSED`.
