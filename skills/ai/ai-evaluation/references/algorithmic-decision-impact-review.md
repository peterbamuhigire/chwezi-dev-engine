# Algorithmic Decision Impact Review

Parent skill: `../SKILL.md`. Load when a model, score, rule set, ranking, or recommender decides or materially shapes an outcome for a person: credit, pricing, hiring, admissions, fraud flags, content visibility, eligibility, prioritisation of service, surveillance or risk scoring. Applies to classical ML and hand-written scoring rules as much as to LLMs. Pairs with `ai-human-oversight-evaluation.md` (controls around the decision) and `product-business/experiment-engineering/references/fairness-and-srm.md` (experiment fairness). This file decides whether the algorithm should exist in its proposed form and what evidence release requires.

## Inputs

| Input | Owner | If missing |
|---|---|---|
| Decision statement: who is affected, what outcome, what the person can do about it | Product owner | Stop; no review without a named decision |
| Target variable and every input feature, with provenance | Data/ML lead | Stop |
| Evaluation data with outcome labels and, where lawful, group attributes or a documented proxy method | Data lead | Subgroup results `NOT_ASSESSED`; release blocked for high-impact decisions |
| Current non-algorithmic process and its error rates | Operations | Baseline `NOT_ASSESSED`; comparison claims forbidden |
| Applicable law and sector rules | Legal, via `digital-research-engine` | Legal status `NOT_ASSESSED`; never inferred from this checklist |

## Impact tier

| Tier | Test | Minimum review |
|---|---|---|
| High | Affects money, liberty, livelihood, health, education, housing, legal status, or safety; or is hard to contest | Full checklist, independent reviewer, subgroup evidence, human decision path, post-release audit cadence |
| Medium | Shapes access or visibility (ranking, recommendations, queue priority) with reversible effect | Checklist sections 1-5, subgroup evidence on the primary metric |
| Low | Personalisation with no material effect and easy opt-out | Sections 1 and 5 |

When unsure, take the higher tier.

## Review checklist

### 1. Framing and measurability
- Is the quantity the system optimises the thing the organisation actually cares about, or a convenient measurable stand-in? Write both down. Example: "loan repaid within 90 days" is measurable; "the member's financial wellbeing" is the real goal and may diverge.
- What does the measurement leave out? List the human qualities, circumstances, or context the features cannot capture and how the process handles them.
- Is "normal" defined by past behaviour of a population that was itself treated unequally? Anomaly and risk models inherit that history.
- Would a transparent rule, a checklist, or human judgement with better tools do the job adequately? Record why the algorithm is preferred.

### 2. Data and proxies
- For each feature: could it stand in for a protected or sensitive characteristic (location for ethnicity or income, device type for income, name for gender or ethnicity, time-of-activity for caregiving or religion)? Test correlation, do not assume.
- Are labels produced by past human or system decisions (arrests, prior approvals, previous moderation)? If so, the model learns those decisions, including their bias; consider outcome labels that were not gated by the old process.
- Is any group under-represented or missing, such that the model is effectively untested on it (rural users, feature-phone users, non-English speakers)?
- Are inferred attributes (segments, personas, "likely X") used to treat people differently? Treat inferences as personal data and as proxies.

### 3. Performance across groups
- Report the primary metric and error rates (false positive and false negative separately) per relevant group and intersection, with sample sizes and confidence intervals.
- Choose the fairness criterion explicitly and justify it for this decision: equal error rates, equal selection rates, or calibration within groups. These cannot all hold at once when base rates differ; the choice is a policy decision owned by a named person, not a default of the library.
- Release is blocked when a group's error rate for the harmful error exceeds the agreed tolerance, or when a group is too small to assess and the tier is High.
- Libraries such as Fairlearn and AIF360 compute group metrics and mitigations; they do not choose the criterion. Verify current versions before adoption.

### 4. Feedback loops and gaming
- Will the system's outputs change the data it is later retrained on (patrols sent where crime was predicted record more crime there; items ranked higher get more clicks and are ranked higher still)? Describe the loop and the counter-measure: exploration budget, holdout population, labels independent of the system's own actions.
- Can affected people or intermediaries learn to game the inputs, and would gaming harm honest users?
- Does optimisation for engagement or conversion narrow what people see in ways they did not choose?

### 5. Transparency, explanation, and contest
- Can the affected person learn that an automated system was involved, the main reasons for their outcome, and what would change it? Provide reason codes grounded in the actual features, not generic text.
- Is there a route to a human who can review, correct the data, and override, with a time commitment?
- Do operators understand the model's limits well enough to disagree with it? Watch for automation bias: reviewers approving whatever the score says. Measure override rates and sample overrides for quality.
- Opaque models are acceptable only when the explanation and contest path above still work and the tier allows it; "it predicts well" does not answer "why was I refused".

### 6. Accountability and lifecycle
- Named owner for the model, the fairness criterion, and the contest process.
- Model card or equivalent record: purpose, data, exclusions, metrics per group, known failure modes, version.
- Monitoring: subgroup metrics and input drift in production, not only aggregate accuracy; alert thresholds and a rollback or suspension trigger.
- Re-review triggers: new population or market, new feature, retraining on system-influenced data, regulatory change, complaint pattern.

## Decision rules

| Finding | Decision |
|---|---|
| Harmful-error gap between groups beyond tolerance | Block; mitigate (data, features, threshold per policy, human review band) and re-evaluate |
| Feature is a strong proxy with no necessity case | Remove it and re-evaluate |
| No contest route for a High-tier decision | Block release |
| Labels come from the process being automated | Require independent labels or a bounded pilot with audit |
| Legal basis unverified | Hold High-tier release; route to legal with the evidence pack |

## What premium looks like versus generic output

- Generic: "We will ensure fairness and transparency and monitor for bias."
- Premium: a named decision, a stated fairness criterion with its owner, subgroup error tables with sample sizes, a proxy analysis per feature, a described feedback loop and its counter-measure, a working contest path, and dated re-review triggers.

## Worked example (original)

A Ugandan SACCO proposes automated micro-loan approval from mobile-money transaction history. Review findings: the target (repayment within 90 days) ignores seasonal agricultural income, so harvest-cycle borrowers look risky in the dry season; "days since last transaction" correlates strongly with rural location; labels come from past loan officers' approvals, so applicants officers routinely declined never appear as repayers. Decisions: add a seasonal income feature and evaluate by district and by sex with confidence intervals; drop the recency feature; run a six-month pilot where a random 10% of borderline applicants receive human review regardless of score to create independent labels; issue reason codes in Luganda and English with a branch-officer contest route answered within five working days; the credit committee chair owns the fairness criterion (equal false-decline rates within two percentage points).

## Evidence and currentness

Accessed 2026-09-24: NIST AI RMF 1.0 (AI 100-1, 2023) remains the current core framework, with a revision announced and profiles such as the Generative AI Profile (AI 600-1); EU Regulation (EU) 2026/1744 (Digital Omnibus on AI) is published on EUR-Lex and, per legal commentary not yet checked against the regulation text, defers Annex III high-risk obligations (including credit scoring and recruitment) to 2 December 2027; treat those dates as `NOT_ASSESSED` until confirmed in the text. Uganda Data Protection and Privacy Act 2019 provisions on automated decisions and the Kenya Data Protection Act 2019 are `NOT_ASSESSED` here; route through `digital-research-engine` and counsel. Fairness library versions are `NOT_ASSESSED`.

Sources: Dormehl (2014) *The Formula*; Oliveira (2024) *AI Strategies for Web Development*; NIST (2023) *AI RMF 1.0*.
