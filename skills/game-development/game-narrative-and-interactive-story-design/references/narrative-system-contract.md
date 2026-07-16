# Narrative System Contract

This is a self-contained distillation of durable practices from *Story Structure and Development* (2025). It does not reproduce the book and does not require the source file at execution time.

## Contract layers

1. **Promise:** audience, player fantasy, theme, tone, rating and cultural boundary.
2. **Causal spine:** setup → disruption → dramatic question → escalating action/obstacle/choice → climax → resolution/change.
3. **Character:** public want, deeper need, stakes, tactics, contradiction, relationships, agency and change.
4. **Interactive form:** player-, plot-, mechanics-, character-, environmental- or system-driven delivery, selected per purpose.
5. **Runtime state:** stable IDs, predicates, mutations, persistence, failure/recovery and convergence.
6. **Delivery:** trigger, channel, duration, input lock, interruption, replay, fallback, subtitle/caption/VO/localisation fields.
7. **Evidence:** reachability, comprehension, pacing, agency, accessibility and cultural review.

## Narrative unit schema

| Field | Required content |
|---|---|
| ID / owner / revision | Stable identity and accountable owner |
| Player context | Current goal, knowledge, location and available verbs |
| Preconditions | Exact state predicates |
| Trigger | Deterministic event or threshold |
| Payload | Information, choice, relationship or state change |
| Delivery channels | Dialogue, text, animation, environment, mechanics, UI, audio |
| Control policy | Input retained, constrained or removed; maximum duration |
| Interrupt/recovery | Skip, pause, death, disconnect, save/load, replay |
| Mutation | Exact state variables/events emitted |
| Localisation/accessibility | Keys, captions, readable timing, non-audio alternative |
| Cultural/provenance | Source ledger IDs and reviewer decision |
| Oracle | Observable pass/fail condition in a named build |

## Causality and player-flow checks

- Replace “and then” between major beats with “therefore” or “but”; investigate any beat that cannot be linked.
- Separate essential path comprehension from optional lore.
- The goal, stakes and actionable next step must be recoverable after interruption.
- A choice communicates options before commitment, acknowledges the result, and preserves consequence in state or presentation.
- Convergence is valid when prior choices still affect acknowledgement, resources, relationships, difficulty or later payoff.

## Source limits

The book spans animation, VFX, games and XR. Its dramatic principles are durable; screenwriting form is not automatically a game runtime model. Project evidence, community review, engine constraints and playtests override generalized examples.
