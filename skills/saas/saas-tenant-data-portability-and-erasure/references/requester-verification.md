# Requester Verification - Reference

The most dangerous part of data portability and erasure is not the cascade - it is letting the wrong person trigger it. An attacker who can erase a competitor's tenant, or export a stranger's personal data, turns your compliance feature into a weapon. Verification is the gate that proves the requester is entitled to the data before any export or erasure runs. This reference specifies verification strength per request type, identity proofing, anti-abuse, the SLA, and alignment with GDPR/DPA obligations.

## section 1 The Threat Model

| Attack | Without verification | The control |
|---|---|---|
| Competitor erases a rival's tenant | One unauthenticated POST destroys a business | MFA + cool-down + active-subscription check on tenant erasure |
| Stranger exports a victim's personal data | PII handed to an impostor (a data breach you caused) | Authenticated session + confirmation to the email on file |
| Disgruntled ex-employee erases the org | Departed insider still triggers tenant deletion | Primary-admin-only + MFA; revoked accounts cannot request |
| Social-engineered support agent runs erasure | "Customer" talks staff into deleting | Back-office co-sign + ticket reference + justification |
| Mass automated erasure/export requests | Abuse / denial of service via the compliance endpoint | Rate limiting + per-subject request caps |

The failure mode of weak verification is not a bad UX - it is an attacker-triggered, irreversible destruction of customer data, or a self-inflicted PII breach. Verification strength must scale with the blast radius of the request.

## section 2 Verification Strength Per Request Type

| Request type | Verification | Why this bar |
|---|---|---|
| User export (own data) | Authenticated session + confirmation link to the email on file | Re-proves control of the registered email; blocks a hijacked session from silently exfiltrating |
| User erasure (own data) | Authenticated session + email confirmation + 7-day cool-down | Adds a regret window; erasure is irreversible |
| Tenant export | Primary-admin authenticated + MFA + email confirmation | Whole-org PII; step-up auth before bulk extraction |
| Tenant erasure | Primary-admin + MFA + email confirmation + 7-day cool-down + no active subscription (must cancel first) | Highest blast radius; every guardrail applies |
| Admin-initiated (back-office, e.g. regulator order) | Super-admin + co-sign + justification + ticket reference | Staff cannot unilaterally erase; two-person control + paper trail |

Confirmation goes to the email already on file, never to an address supplied in the request - or the attacker simply supplies their own address and confirms it themselves. Reject any request that fails its bar, and audit both the success and the failure.

## section 3 Identity Proofing

The strength of proofing scales with whether the requester is an authenticated principal or an external party.

- **Authenticated in-product requests** are the strong path: the session already proves identity; the email confirmation and MFA step-up re-prove control of the credentials at the moment of the sensitive action.
- **External requests** (a data subject who is not a current user - for example a former user emailing your DPO under GDPR) cannot rely on a session. Proof options, weakest to strongest: match against data only the subject would know; verify control of the registered email/phone; for high-risk cases, request a government-ID match handled under a strict minimisation and retention policy (collect, verify, delete the ID copy). Over-collecting identity documents is itself a privacy violation - proof the minimum necessary.
- **Never** accept the requester's mere assertion of identity for an erasure or a full export. "I am the account owner, please delete everything" in an email is not proof.

## section 4 Anti-Abuse

- **Rate limiting**: cap export/erasure requests per subject and per IP. A subject does not legitimately request twenty exports an hour; that is scripted abuse.
- **Per-subject request cap**: collapse repeat requests within a window into the existing in-flight job rather than spawning new ones (idempotency on the request itself).
- **Cool-down as anti-abuse and anti-regret**: the 7-day window on erasure both prevents rage-deletion and gives time to detect a fraudulent request before it executes.
- **Anomaly flags**: an erasure request immediately after a password reset from a new device, or right after an ownership transfer, is suspicious - require additional verification or hold for review.
- **Active-subscription gate on tenant erasure**: requiring cancellation first adds friction an attacker is unlikely to clear and surfaces the request to billing.

## section 5 SLA

Verification adds steps but must not let the response breach the statutory deadline.

| Stage | Target |
|---|---|
| Acknowledge request | Within 72 hours |
| Complete verification | Within 7 days (cool-down runs concurrently) |
| Deliver export | Hours to days; hard ceiling 30 days (GDPR Art.12) |
| Complete erasure | After cool-down + verification; well within 30 days |

The clock starts at request receipt, not at verification completion. If identity proofing for an external requester is genuinely blocked, the lawful path is to inform the requester what proof is still needed and pause the clock for that specific reason - not to silently let the 30 days lapse. Document any extension and its basis (GDPR permits a one-time extension of up to two further months for complex requests, with the subject informed within the first month).

## section 6 GDPR / DPA Alignment

- The verification you perform is itself a processing activity - log it, and minimise what you collect to prove identity.
- A data subject may exercise rights through your DPO/Information Officer, not only through the product UI; the external-request path (section 3) covers this. POPIA requires an Information Officer; Uganda DPPA and Kenya DPA have equivalent roles.
- For admin-initiated requests responding to a regulator or court, the justification and ticket reference link the action to its lawful basis - this is the evidence a supervisory authority expects.
- The whole verification trail (who requested, how they were verified, who approved, when) is retained as compliance evidence alongside the erasure proof pack, since "we verified the requester before acting" is exactly what you must be able to demonstrate after the fact.

## section 7 Audit

Every request, successful or refused, writes an audit row:

```json
{
  "event": "ERASURE_REQUEST_VERIFIED",
  "request_type": "tenant_erasure",
  "subject_tenant_id": "123",
  "requester_user_id": "55012",
  "verification": ["session", "mfa", "email_confirmed", "subscription_cancelled"],
  "cool_down_ends_at": "2026-06-06T10:00:00Z",
  "outcome": "accepted",
  "actor_ip": "10.2.3.4",
  "ticket_id": "DPO-2026-118"
}
```

A refused request records the failed check - this is how you detect an attacker probing the erasure endpoint and how you prove you did not act on an unverified request.

## section 7a Worked Example - Tenant Erasure Verification Flow

A primary admin requests deletion of their whole organisation.

```text
1. Authenticated session check        -> requester is a current principal of tenant 123
2. Role check                         -> requester holds 'primary_admin' on tenant 123 (not just member)
3. MFA step-up                        -> re-prompt at action time, not relying on login MFA
4. Active-subscription gate           -> subscription must be cancelled first; else 409 with instructions
5. Email confirmation                 -> link sent to the email ON FILE, not a supplied address
6. Cool-down starts                   -> erasure scheduled for now + 7 days; cancellable in-product
7. Audit row written                  -> ERASURE_REQUEST_VERIFIED, outcome=accepted
8. Anomaly check                      -> request <24h after a new-device login? hold for manual review
```

Only after step 6's cool-down elapses with no cancellation does the cascade in `erasure-cascade.md` run. Any failed step short-circuits with an audited refusal. Skipping step 2 (role check) is the classic hole: a regular member, not the owner, triggers org-wide deletion.

## section 7b Worked Example - External Subject Request

A former user emails the DPO: "Delete all my data under GDPR Article 17." There is no session to lean on.

```text
1. The requester cannot be trusted on assertion alone.
2. Send a verification challenge to the email/phone on file for the account that
   matches the claimed identity (control-of-channel proof).
3. If the channel is no longer accessible, request the minimum additional proof
   (e.g. a one-time match against data only the subject would hold). Collect a
   government-ID copy only as a last resort, verify it, and delete the copy.
4. Acknowledge within 72h; pause the clock only with a documented, communicated reason.
5. On verification, proceed via the user-erasure path; audit the proofing performed.
```

Over-collecting ID for a routine request is itself a privacy violation - proof the minimum the risk warrants, no more.

## section 7c Verification Strength Ladder

When unsure which bar applies, climb the ladder until the proof matches the blast radius:

```text
weakest  ->  authenticated session
            + confirmation to channel on file
            + MFA step-up
            + role / ownership check
            + active-subscription / obligations gate
            + cool-down window
            + co-sign (staff-initiated)
strongest -> co-sign + ticket + documented lawful basis (regulator order)
```

The rule of thumb: the more irreversible and the wider the scope, the further up the ladder. Erasure outranks export; tenant-level outranks user-level; staff-initiated needs two people.

## section 8 Anti-Patterns

- **One-click tenant erasure with no verification** - a competitor or ex-employee destroys the business.
- **Confirmation sent to a requester-supplied address** - the attacker confirms their own request.
- **Accepting an asserted identity** ("I'm the owner, delete it") - no proof; trivially spoofed.
- **No cool-down on erasure** - irreversible action with no regret window and no fraud-detection time.
- **Over-collecting ID documents for every request** - the verification itself becomes a privacy violation.
- **Starting the SLA clock at verification completion** instead of receipt - hides a deadline breach.
- **Staff erasure without co-sign or ticket** - a social-engineered or rogue agent acts alone.
- **No audit of failed verification attempts** - cannot detect probing or prove diligence.

## See Also

- `saas-tenant-data-portability-and-erasure` section 6 (verification table), section 5 (erasure workflow).
- `references/erasure-cascade.md` - what runs only after verification passes.
- `references/export-format-spec.md` - delivering the export only to the verified address.
- `saas-admin-backoffice-tooling` - the co-sign and justification machinery for admin-initiated requests.
- `uganda-dppa-compliance` - Information Officer obligations and regional response timelines.
