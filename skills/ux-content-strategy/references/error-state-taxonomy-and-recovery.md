# Error State Taxonomy And Recovery

Errors are where products earn or lose trust at a higher rate than any other surface. The user has hit the *end or edge* of the experience, as Metts and Welfle put it, and the question is whether the product helps them move forward or leaves them stuck. This file is the engine's working taxonomy: classify the error, then apply the recovery pattern that fits.

Derived from Wroblewski, *Web Form Design* (Chapter 8 on error messages and the "avoid where possible" doctrine), and Metts and Welfle, *Strategic Writing for UX* (the scorecard criterion that error messages help the person move forward).

## The Doctrine: Prevent, Then Catch, Then Recover

*Web Form Design*'s position on error messages is unambiguous: they are the most common, the most overused, and the most likely to annoy customers. Avoid them where possible. The hierarchy of error handling is therefore:

1. **Prevent** — use input types that have no error states (drop-downs, smart defaults), inputs with undo, fields with good defaults.
2. **Catch early** — inline validation that confirms or suggests valid answers as the user types, before the user commits.
3. **Recover** — when the error has already occurred, give the person the next move in their voice.

If the engine is being asked to write an error message, it should first ask whether the field could have been designed so the error was impossible. Many errors are field-design bugs masquerading as copy bugs.

## Taxonomy: Five Classes Of Error

| Class | Trigger | Best handling |
|---|---|---|
| **Prevention-eligible** | Constraint the user cannot satisfy by guessing (uniqueness, length, format) | Inline validation, smart defaults, restricted input type |
| **Input-correction** | User entered something the system can identify as wrong (mis-typed email, expired card) | Field-adjacent error, with the corrective action named |
| **System-failure** | Backend, network, or third-party failure outside user control | Page-level message, voice-aligned, with retry and an exit |
| **Permission/state** | User cannot do this thing because of who they are or what state the data is in | Explain the state, offer the path to change it (request access, sign in differently) |
| **Catastrophic / data-loss-risk** | An action would destroy or corrupt user data | Confirmation interrupt before the action; recovery path after |

Every error message the engine writes should be classifiable in this table. If it is not, the underlying interaction is unclear.

## Recovery Anatomy: Three Required Parts

Every error message that survives the prevent-and-catch hierarchy has three parts, in this order:

1. **What happened, in user terms.** Not "HTTP 502," not "An unexpected error occurred." Something the user can connect to their action.
2. **What to do next.** A specific action the user can take *now*. If the action is "wait," say so and give an estimate.
3. **How to escape.** An exit — go back, contact support, dismiss — so the user is not trapped.

If part 2 is missing, the message is venting, not helping.

## Voice Discipline At The Error Boundary

Errors are where voice slips. Engineering text leaks through, legal text leaks through, marketing reassurance leaks through. The voice chart applies *most strictly* at error states because that is where the user's tolerance for mismatched voice is lowest.

Apply these voice gates:

- **Verbosity row:** keep it short. The user is already inconvenienced.
- **Vocabulary row:** strip jargon (HTTP codes, "validation failed," "schema").
- **Concepts row:** error states are usually *not* the place to surface marketing concepts. Re-read the chart and see whether the concept naturally belongs here.
- **Grammar row:** match tense and voice the rest of the experience uses.
- **Punctuation row:** errors do not need exclamation marks. Calm is what is missing.

Metts and Welfle's scorecard criterion is operational: read the error aloud. Does it tell the person how to move forward? Score it on that, not on whether it is technically accurate.

## The Field-Level Pattern

For an inline form-field error:

- Anchor the message *to the field*, not at the top of the page.
- Re-state what was needed and how to satisfy it ("Use a 5-digit ZIP code" rather than "Invalid ZIP").
- Preserve what the user typed unless it is unsafe to do so.
- Re-validate as the user corrects, so they see the field clear when it passes.

Inline validation per *Web Form Design*'s Chapter 9 is the complement of the inline error: success states confirm, error states correct. Both share the same anchor.

## The Page-Level Pattern

For a system failure or catastrophic error:

- Title the page in the same voice the rest of the product uses.
- One short paragraph for what happened.
- One primary action (Retry, Sign in again, Contact support) and one secondary (Go back, Go home).
- A reference number *if* support needs it, but never *as* the message.

## The Confirmation Interrupt — For Catastrophic Class

For destructive actions (delete account, cancel subscription, send irreversible payment), the error pattern is preventive: a confirmation interrupt *before* the action. Rules:

- Restate what is about to happen, including consequences ("This will cancel auto-renewal effective March 15. You will keep access until then.").
- The confirming button is labeled with the action ("Cancel auto-renewal"), not "OK." Generic OK on destructive actions is the misleading-button anti-pattern from *Strategic Writing for UX*.
- The escape ("Keep my subscription") is at least as visually accessible.

After the action: a confirmation message that names what happened and how to undo it if undo exists.

## The Empty-Recovery Pattern

When the user reaches a state with no data because of an earlier error or non-action ("we couldn't find any results"), the message is half error and half empty state. Treat it as:

- Name the cause if known.
- Suggest the next attempt (broaden search, check spelling, check connection).
- Offer the empty-state's normal call-to-action as a fallback.

## Inline Validation Failure Modes

Inline validation, applied wrong, becomes its own error generator. The book's cautions:

- Do not validate fields with no real constraint — name, simple email — because the validation noise feels condescending.
- Do not validate so eagerly that the user is corrected mid-typing of a value that would be valid two characters later.
- Do confirm successes; one-sided validation that only flags failure feels punitive.

## Anti-Patterns

- "An unexpected error occurred." The user cannot act on this.
- Stack traces or numeric codes with no human-readable instruction.
- Errors that blame the user ("You entered an invalid email"). Restate as what is needed.
- Generic "OK" / "Continue" buttons on destructive confirmation interrupts.
- All-caps "ERROR" headers — every voice chart in the source book would forbid this.
- Top-of-page error summaries that do not also anchor at the field.
- Modal errors that disappear before the user reads them.
- Marketing reassurance ("Don't worry!") in a critical-failure context.

## How The Engine Uses This Taxonomy

Given an error to write or audit:

1. Classify it in the five-class taxonomy.
2. Ask: could the field or interaction have prevented this entirely? If yes, recommend the prevention before writing the message.
3. Apply the three-part anatomy.
4. Run the voice-chart gates row by row.
5. Recommend an inline-validation companion if applicable.

If a proposed error message survives all five steps, it is acceptable. Otherwise rewrite.

## Source Grounding

- *Web Form Design*'s explicit doctrine: error messages are common, overused, annoying — avoid them via input types with no error states, undo-able inputs, and good defaults.
- Inline validation as feedback that confirms or suggests valid answers (Chapter 9), with the Newsvine and Last.fm examples as references for confirmation behavior.
- *Strategic Writing for UX*'s scorecard criterion: error messages help the person move forward when they hit the end or edge of the experience.
- Metts and Welfle's misleading-button warning applied here to "OK" / "Continue" on destructive interrupts.
- Voice-chart application at error boundaries: jargon stripping in Vocabulary, exclamation discipline in Punctuation, concept-fit check.
- The anti-pattern of help text that exists because a field is the wrong size (5-digit ZIP help) — interpreted here as the field-design bug masquerading as a copy bug.
