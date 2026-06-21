# Agentic AI And App Intents Security

Use this reference when Foundation Models, Core AI, Siri, App Intents, Spotlight,
widgets, or model tools can read private data or perform actions.

## Threat Model

| Threat | Control |
| --- | --- |
| Prompt injection through user content, web content, OCR, or documents | Treat retrieved content as untrusted; separate instructions from data; deny tool escalation. |
| Tool misuse by model or Siri action | Tool allowlist, typed inputs, authorization check, confirmation for high-risk actions. |
| Confused-deputy action | Bind every action to current user, tenant, role, entity, and session state. |
| Data exfiltration through summaries/search | Redact secrets, classify fields, block regulated data from prompts and indexes unless approved. |
| Unauthorized App Intent | Re-check server-side authorization; do not trust local role flags. |
| Unsafe model output | Validate structured output, constrain actions, and use refusal/error states. |

## App Intents And Siri Actions

- Destructive, financial, external-communication, health, legal, or tenant-wide
  actions require confirmation.
- App Intents must call domain use cases that enforce the same authorization as
  the app UI.
- Background or Siri-mediated actions must not bypass recent-auth requirements
  for sensitive workflows.
- Log intent id, entity id, actor, authorization result, and action outcome
  without logging secrets or raw prompt data.

## Semantic Index Privacy

- Do not index secrets, hidden tenant data, payment data, health data, raw legal
  records, or credentials.
- Delete index entries on logout, tenant switch, role downgrade, account
  deletion, and server revocation.
- Treat Spotlight/Siri visibility as a user-facing data disclosure.

## App Attest And Device Trust

Use App Attest where backend trust depends on app integrity, such as high-value
transactions, entitlement changes, protected API calls, or fraud-sensitive flows.
App Attest does not replace user authentication, server authorization, rate
limits, or abuse monitoring.

## Trust Insights Watch Item

WWDC26 lists Trust Insights under privacy/security. Until project-specific
Apple documentation is reviewed, treat it as a watch item: record whether it
affects diagnostics, app integrity, or release evidence, but do not invent API
requirements.

## AI Logging Rules

Never log tokens, credentials, private prompts, raw OCR text, model context,
tool payloads, or generated regulated data by default. For debugging, use
redacted, time-limited, opt-in traces tied to a support case or internal test.
