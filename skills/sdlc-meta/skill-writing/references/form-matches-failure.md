# Form Matches Failure

Parent skill: [Skill Writing](../SKILL.md).

Adapted in paraphrase from obra/superpowers `skills/writing-skills` (MIT, https://github.com/obra/superpowers, commit 8ca22dba9a94f28898bbce59f2537ff4d87c747d). No text copied.

Load this reference when you add or rewrite an instruction because an agent got something wrong. Classify the observed failure first, then choose the instruction form that fits it. The wrong form wastes context and can make the failure worse.

## Classification table

| Observed failure | Instruction form | Example |
|---|---|---|
| The agent knows the rule but skips it under pressure | A prohibition, plus an Excuse/Reality table and a short red-flags list built from observed rationalisations | "Do not report done without a fresh verification run", with rows for "it is only a rename" |
| The output has the wrong shape | A positive recipe or output contract: the sections, order and fields to produce | An Outputs table with consumer and acceptance condition |
| A required element is left out | A REQUIRED slot in the template or contract, so absence is visible | A mandatory "Evidence Produced" row that a validator checks |
| The behaviour should differ by situation | A conditional keyed to an observable predicate | "If the change touches a migration file, run the rollback test" |

The pressure-scenario method in [discipline-skill pressure testing](discipline-skill-pressure-testing.md) supplies the observed failure for the first row. Without an observed failure, do not add a prohibition.

## Two wording rules

- **No nuance clauses.** A qualifier such as "unless it is clearly unnecessary" or "where sensible" hands the agent the exit it was looking for. If a real exception exists, state it as its own predicate-keyed conditional.
- **Exemption clauses do not scope.** An exemption written for one case is read as licence for neighbouring cases. Name the exact predicate that grants the exemption and what still applies inside it.

## Evidence status

The upstream maintainers report that, in their head-to-head wording tests, prohibition wording produced more of the unwanted content than recipe wording. That is a vendor-internal result with no public dataset. Treat it as a lead to verify with the micro-test protocol, not as an established fact, and do not rewrite existing anti-pattern sections on its strength alone.
