# Written Strategy Brief Template

A written strategy brief is the contract between the org and itself. This template is opinionated about structure because most strategy failures are structural, not stylistic. Length budgets are guidance, not law; exceeding them by 50% is a smell, by 200% is a problem.

## Format Rules

- Plain prose, not slides. Slides hide ambiguity; prose forces the writer to commit.
- Single document, single owner, dated, version-numbered.
- Five pages or fewer at corporate altitude; ten at portfolio; fifteen at product or component.
- Distributed as a draft for at least one full review cycle before signature.
- Named dissent recorded in the brief itself, not in a separate channel.

## Section Structure

### 1. Header (5 lines)

- **Title**: a sentence, not a noun phrase. "Consolidate to one production substrate by Q4," not "Production Substrate Strategy."
- **Altitude**: corporate / portfolio / product / component.
- **Owner**: one person, by name.
- **Status**: draft / signed / under revision / sunset.
- **Dates**: drafted, signed, sunset date.

### 2. Executive Summary (≤ 200 words)

Three paragraphs:

- The diagnosis in one sentence.
- The guiding policy in two to three sentences.
- The single most consequential tradeoff being accepted.

A reader who only reads this section should be able to recall the strategy a week later.

### 3. Diagnosis (½-1 page)

- One paragraph stating the obstacle in concrete terms.
- A short list of the constraints that bound the response.
- The leverage point that the strategy will act on.
- The evidence that informed this diagnosis (linked, not embedded).
- The alternative framings considered and why they were not selected.

A diagnosis that names no obstacle, lists no constraints, or locates no leverage point is incomplete and the brief should not advance.

### 4. Guiding Policy (½-2 pages)

A numbered list of clauses, each in the form:

> *N. We will <do / not do / require / forbid> <X>, because <diagnosis link>. Default: <Y>. Exception: <named owner> may grant on <evidence>.*

Group clauses by theme if there are more than seven. Cite the diagnosis line for each clause.

### 5. Coherent Actions (½-1 page)

A small numbered list of the moves that implement the policy. For each action:

- **What**: one sentence.
- **Why this clause**: which policy clause it implements.
- **Owner**: named person.
- **By when**: a date, not a quarter.
- **Done means**: the observable end state.

If the action list could equally implement a different policy, it is not coherent.

### 6. Tradeoffs Accepted (¼ page)

Two to four bullets, each naming what the strategy gives up. If this section is empty, the strategy is a vision, not a strategy. Examples:

- "We accept slower greenfield velocity for the next two quarters in exchange for migration completion."
- "We accept a single-vendor dependency to reduce coordination cost."

### 7. Operating Mechanisms (¼-½ page)

- **Cadence**: who meets, how often, what they decide.
- **Leading indicators**: 3-5 metrics with current values and target trajectories.
- **Trip wires**: thresholds that trigger automatic review.
- **Exception path**: who grants exceptions, on what evidence, with what expiry.

### 8. Review and Sunset (¼ page)

- **Next review date.**
- **Revise criteria**: thresholds that, if breached, trigger revision.
- **Kill criteria**: evidence that would falsify the strategy.
- **Sunset date**: when the strategy must be renewed, revised, or retired regardless of performance.

### 9. Dissent Recorded (¼ page)

A named list of stakeholders who reviewed the brief and disagreed, with a one-line summary of each objection. The strategy is *not* obligated to resolve every dissent, but it is obligated to record it. Hidden dissent becomes underground veto later.

### 10. Appendix (optional)

- Linked evidence, prior strategies, related ADRs.
- Glossary if the brief introduces terms.
- Decision log keyed to this strategy.

## Pre-Signature Checklist

Before signing, the owner confirms:

- [ ] The diagnosis is one paragraph that an opponent could agree is factually accurate.
- [ ] Every policy clause has a default and an exception path.
- [ ] Every coherent action cites a policy clause.
- [ ] At least two named tradeoffs are accepted.
- [ ] Cadence, trip wires, and kill criteria are written, not implied.
- [ ] Named dissent is recorded.
- [ ] A sunset date is set.
- [ ] The brief is under the length budget for its altitude.

If any box is unchecked, the brief returns to draft.

## Post-Signature Operating Rules

- Changes are versioned; the prior version is preserved in the appendix or a linked archive.
- Exceptions are logged as they happen, not retrospectively.
- The review cadence runs whether or not the owner is available; a delegate is named in the brief.
- The sunset date is sacred. Reaching it without a fresh diagnosis means the strategy is dead by default, regardless of momentum.
