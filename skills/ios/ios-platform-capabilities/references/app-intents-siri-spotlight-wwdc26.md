# App Intents, Siri, Spotlight, And Widgets WWDC26

Use this reference when an app exposes content or actions to Siri, Spotlight,
widgets, Shortcuts, or Apple Intelligence surfaces.

## Inventory First

Before writing code, create an inventory:

| Surface | Required decision |
| --- | --- |
| App Entities | Which user-visible domain objects can Siri/Spotlight identify? |
| Entity schemas | Which fields are safe and useful for the semantic index? |
| Intent schemas | Which user actions should be invokable without fixed trigger phrases? |
| View Annotations | Which on-screen views map to entities/actions? |
| Widgets | Which customization points should be App Intent backed? |
| Privacy | Which data must never leave the app or appear in search/Siri context? |
| Tests | Which App Intents Testing cases prove the integration? |

Apps with notes, tasks, orders, invoices, media, education content, bookings,
health data, finance data, messages, or enterprise records must treat this as
architecture work, not shortcut decoration.

## Entity And Schema Rules

- Expose entities users naturally search for or act on.
- Keep internal IDs, tenant IDs, security labels, audit metadata, and secrets out
  of semantic-index fields.
- Include attribution back to the app so Siri/Spotlight results return to the
  correct product surface.
- Version entity schemas when data meaning changes.
- Use conservative defaults for finance, health, legal, minors, and enterprise
  content.

## Intent Rules

- Define high-value actions, not every button.
- Require confirmation for destructive, external, financial, messaging, or
  irreversible actions.
- Re-check authorization server-side for networked actions.
- Handle partial context: Siri may know the entity but not every field needed
  for the action.
- Provide clear refusal and recovery states when an action is unavailable.

## View Annotations

Use View Annotations when on-screen content should be referable in conversation:
"send this invoice", "summarize this note", "add this order to the route".
Annotate only visible, current, authorized content. Do not annotate hidden rows,
background caches, or data from another tenant/account.

## App Intents Testing Gate

Add App Intents Testing for:

- entity lookup by natural language;
- action invocation with valid and invalid entities;
- permission denied and signed-out states;
- locale/language variants where supported;
- unavailable Apple Intelligence/Siri conditions;
- destructive or high-risk confirmation paths.

UI automation alone is not sufficient for Siri/App Intents integration.

## Handoff To Security

Load `ios-security-and-rbac` when an App Intent can read private data, mutate
state, call an AI tool, trigger payment/communication, cross tenant boundaries,
or run while the app UI is not foregrounded.
