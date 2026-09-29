# Discipline-Skill Pressure Testing

Parent skill: [Skill Writing](../SKILL.md).

Adapted in paraphrase from obra/superpowers `skills/writing-skills` (MIT, https://github.com/obra/superpowers, commit 8ca22dba9a94f28898bbce59f2537ff4d87c747d). No text copied.

Load this reference when you author or tighten a **discipline skill**: a gate an agent is tempted to skip under pressure (verification before completion, evidence before claims, anti-slop ship gates, approval and permission gates, test-first). Do not load it for reference skills.

## Scope rule

| Skill kind | Pressure-test? | Why |
|---|---|---|
| Discipline gate (a rule the agent can skip) | Yes, but only after a RED baseline shows the agent actually skips it | Wording is only proven when it changes observed behaviour |
| Reference or catalogue skill (facts, schemas, templates) | No | There is no temptation to resist; routing and contract tests are enough |
| Workflow skill with no skippable gate | No; use routing and contract tests | Pressure scenarios would measure nothing |

Capitalised imperatives ("MUST", "NEVER") and persuasion devices are reserved for engineering discipline gates, and only where a RED baseline shows plain wording failed. Client-facing engines (business plan, proposal, social media, website copy) keep a calm, plain register.

## RED, GREEN, REFACTOR

1. **RED: baseline without the skill.** Run each pressure scenario on a fresh agent context that does not have the skill loaded. Record the choice it makes and every rationalisation it gives, word for word. If the agent already complies, stop: there is nothing for the skill to fix, and adding rules would only cost context.
2. **GREEN: minimal skill.** Write the smallest instruction that answers the recorded rationalisations. Choose the instruction form with [form matches failure](form-matches-failure.md). Re-run the same scenarios with the skill loaded and record the outcome.
3. **REFACTOR: close loopholes.** Each new rationalisation seen in GREEN becomes a row in the Excuse/Reality table or a red flag. Re-run until the compliant choice holds across repetitions. Remove any wording that the runs show has no effect.

A RED or GREEN outcome that was not actually run is recorded as `NOT_ASSESSED` with the reason. Never infer an outcome.

## Designing a pressure scenario

- **Combine at least three pressures** from: time, sunk cost, authority, economic, exhaustion, social, pragmatic. A single pressure rarely moves a capable model.
- **Force a choice.** Offer options A, B and C with exactly one compliant option. An open question lets the agent recite the rule instead of acting on it.
- **Use real paths and real tasks** from the repository (a real skill, script or test command), so the scenario resembles work rather than a quiz.
- **Name the gate under test** and the compliant letter before running.
- **Record** `baseline_outcome` and `with_skill_outcome` as either `NOT_ASSESSED` or `{choice, rationalisations_verbatim[], run_ref}`.

The dev engine stores scenarios as the `pressure_scenarios` case type validated by `tools/validate_benchmark_fixtures.py` (IDs `PS01`, `PS02`, ...). Execution at scale belongs to the behavioural evaluation runner in `chwezi-engine-agents`.

## Micro-test protocol (wording changes)

Use this when comparing two wordings of the same rule.

| Step | Rule |
|---|---|
| Control | Include a no-guidance control arm. If the control does not fail, stop: the wording change has nothing to fix. |
| Samples | One fresh context per sample; at least five repetitions per arm. |
| Reading | Read every flagged output by hand; do not trust a keyword counter alone. |
| Variance | Report the spread between repetitions. High variance is a finding in itself, not noise to average away. |
| Record | Keep prompts, outputs and the reading notes with the run reference so another reviewer can re-read them. |
| Cost | Model-executed runs follow the portfolio spend rule; when runs are not authorised, record `NOT_ASSESSED (zero-spend rule)`. |

## Excuse/Reality table template

Build rows only from rationalisations observed in RED or GREEN runs, never from imagination.

```markdown
| Excuse (observed, verbatim or close paraphrase) | Reality |
|---|---|
| "It is only a rename, the tests will pass." | Renames break imports and string references; run the suite before reporting done. |
| "Yesterday's green run covers it." | Evidence must come from the current change; cite a run made after the last edit. |

**Red flags (stop and re-read the gate):** reporting done before a fresh check; citing old evidence; "just this once".
```

## Bundled scripts

Invoke bundled scripts through their interpreter, for example `python -X utf8 scripts/quick_validate.py <skill-dir>`, never as a bare path. Packagers and archive tools can strip executable bits and shebang handling differs across hosts, so a bare-path call fails silently on some installs.
