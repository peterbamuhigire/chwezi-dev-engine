# Question-Answering Prototypes

A prototype exists to answer one named uncertainty. It is not a cheap first version and does not
inherit production status because it looks polished.

## Contract

- Question and decision owner.
- Competing hypotheses and the observation that distinguishes them.
- Lowest fidelity that preserves the behaviour under test.
- Realistic content and critical normal/error/empty/loading/permission states where they affect the answer.
- Participant or evidence source, method, threshold, limitation, and next decision.
- Disposal, rewrite, or quarantine path before production.

For interface questions, create structurally different variants: change hierarchy, interaction model,
information grouping, or workflow—not colour alone. Route visual execution and rendered review to the
design engine. Test accessibility and failure states in proportion to the question.

Prototype code may omit production scaling only when the omission is labelled and cannot mislead the
decision. Never connect throwaway code to production data, credentials, payments, or irreversible actions.

This reference adapts the prototype-as-question mechanism studied in Matt Pocock's
`mattpocock/skills` repository at commit `3cca18b`.
