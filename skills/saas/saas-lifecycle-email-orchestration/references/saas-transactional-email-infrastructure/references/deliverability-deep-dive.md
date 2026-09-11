# Deliverability and Authentication Operations

Deliverability is an observed property of a specific sender, traffic class, recipient network, and
time window. Do not reduce it to a provider ranking or one universal percentage.

## Control layers

1. **Identity and transport:** SPF authorisation, DKIM signing, DMARC alignment/policy/reporting,
   forward and reverse DNS where required, TLS, and RFC-conformant message format.
2. **Permission and expectation:** valid recipient relationship, accurate sender identity, clear
   purpose, applicable consent, and easy unsubscribe for relevant traffic.
3. **Traffic behaviour:** stable classification, bounded retries, gradual authorised ramp-up, no
   sudden unreviewed volume or identity changes, and recipient-network-aware response handling.
4. **Feedback:** authenticated provider webhooks, suppression updates, DMARC reports, receiver
   dashboards, SMTP responses, and user complaints interpreted in context.
5. **Content/render resilience:** purpose-fit content, honest claims, plain-text alternative,
   accessible HTML, image-off reading, and real-client checks owned with the design engine.

## Change procedure

1. Inventory every system authorised to send for the domain and every visible author domain.
2. Read the current primary standards and recipient-network rules in
   [the currentness register](currentness-register.md).
3. Generate records from verified provider/domain inputs. Never paste illustrative DNS values.
4. Review SPF lookup complexity, DKIM selector/key lifecycle, DMARC alignment, report recipients,
   forwarding/list behaviour, and failure policy with the domain owner.
5. Stage changes from observation to enforcement using real reports and rollback. Do not jump to a
   reject policy because a generic guide says so.
6. Verify message headers and receiver results for each traffic class and representative network.
7. Record exact evidence, uncertainty, owner, support status, and next review date.

## Monitoring

Track by sender identity, traffic class, provider/adapter, recipient network, region, and policy
version:

- queue age, dispatch attempts, provider acceptance, deferral, rejection, and bounce class;
- authentication and alignment results;
- complaint and unsubscribe signals using receiver-defined denominators;
- suppression propagation delay and duplicate/late feedback;
- delivery-to-task time for consequence-critical messages;
- user-harm signals and support incidents;
- reputation/receiver status where an authorised dashboard supplies it.

Thresholds come from current receiver/provider requirements or a measured local baseline. Store the
source, denominator, window, owner, and review date beside each alert.

## Incident triage

1. Bound the affected sender, traffic class, time, recipient networks, and recent changes.
2. Separate authentication, reputation, content, rate, provider, and recipient-address failures.
3. Preserve SMTP/provider/header evidence without retaining unnecessary message content.
4. Reduce or pause only the affected traffic when safe; protect consequence-critical mail through
   an approved fallback.
5. Test one discriminating hypothesis at a time. Avoid reputation folklore.
6. Restore gradually, watch receiver-specific evidence, and close with prevention and review dates.

## Migration

Keep domains, policy, content, consent, suppression truth, and event lineage outside the provider.
Before cutover, prove suppression portability, webhook parity, idempotency across adapters,
authentication/alignment, DNS rollback, traffic ramp, and non-duplication. Provider acceptance is
not completion; inspect representative receiver outcomes and user-task delivery.

## Evidence boundaries

- A DNS record proves publication, not message authentication success.
- Authentication pass proves identity alignment, not inbox placement.
- Provider acceptance proves handoff, not final delivery.
- A pixel open is an imperfect attention proxy, not a user outcome.
- A benchmark from another sender is context, not the alert threshold for this sender.
- A test inbox is evidence for that path and time, not all recipients.

Mark any unavailable layer `NOT ASSESSED` and state the next observation needed.
