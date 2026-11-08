Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Infographics Design and Production Quality Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Agent workflow and QA

Use this reference to run an infographic from brief to archive, whether people or agents do the
work. Rules: [rules-and-gates.md](rules-and-gates.md).

## Production stages

Brief, content inventory, fact verification, wireframe, visual system, draft, expert review,
accessibility, export, final proof, archive. Each stage leaves evidence; nobody jumps from brief to
final artwork.

| Stage | Output | Owner |
|---|---|---|
| Brief | Production brief (below) | Requester and design lead |
| Content inventory | Numbered element inventory and copy sheet | Editorial |
| Fact verification | Provenance register (below), calculations | Content approver |
| Wireframe | Structure with exact labels; diagram data (nodes and edges) checked by the checker | Design |
| Visual system | Typography and layout token sheets, palette, illustration brief | Design |
| Draft | Working file with live text and separate illustration layers | Design |
| Expert review | Sign-off on topology, safety and domain accuracy | Subject-matter reviewer |
| Accessibility | Alt text, long equivalent, contrast, reading order, CVD and greyscale | Accessibility reviewer |
| Export | Every rendition in the export matrix | Technical |
| Final proof | Actual-size proofs, regression comparison, score | All approvers |
| Archive | Repository folders, versions, declaration | Design governance |

## Production brief (handbook Annex A)

Project identifier, owner, reviewer and due date; target audience, reading distance and primary
decision; key message in one sentence and expected action; verified facts with source URLs or file
identifiers; mandatory wording, brand tokens and prohibited content; formats, dimensions,
localisation and accessibility; approval roles and evidence requirements.

Every field is a control: record the chosen value, its rationale, the accountable person and where
the evidence lives; for data or visual properties keep the original and any transformed value.
Procedure per field: obtain the authoritative input, apply the chapter rule, check the working
source, render in the real target, log defects, correct and retest, obtain approval.

## Provenance register (handbook Annex B)

One row per claim: claim ID; exact approved wording and its location in the graphic; source title,
author, publication date and retrieval date; reporting period, unit, denominator and method;
calculation expression, rounding and verification result; source confidence, caveat and
subject-matter sign-off; permission or licence for source material.

## Agent instruction contract (handbook Annex J)

1. Do not fabricate claims, citations or measurements.
2. Do not render photorealistic people or scenes.
3. Do not generate decorative or illegible pseudo-fonts; text is set as real text.
4. Keep research apart from layout and illustration; each role hands over a recorded artefact.
5. Preserve approved copy verbatim; compare exact text after every edit.
6. Stop and ask when a safety-critical ambiguity remains.
7. Produce machine-readable QA findings and release evidence.

Agents may plan, draft, illustrate and write code. They may not change approved wording silently,
fill a gap with a plausible number, or mark a check passed without its evidence. High-stakes outputs
need human approval.

Machine-readable findings use one record per finding:

```json
{"rule": "INFO-FLOW-001", "gate": "INFO-GATE-05", "severity": "critical|major|minor",
 "element": "step S4", "evidence": "check_infographic.py graph: duplicate stage S1 and S3",
 "status": "open|fixed|accepted", "reviewer": "name", "date": "2026-11-08"}
```

## Automated checks

| Check | How |
|---|---|
| Structure | `scripts/check_infographic.py graph` on the diagram data |
| Text size | Per role from task 1, compared with the rendered size |
| Encoding | Lie factor and largest-remainder checks |
| Exact text | Diff of the live text layer against the approved copy sheet |
| Lint | Overflow, text under minimum, broken source links, duplicate step numbers, orphan connectors, missing alt text, off-palette colours, missing metadata |
| Visual regression | Each rendition against its approved baseline; differences investigated |

People still review meaning, aesthetics and domain accuracy; automation never replaces them.

## Severity and scoring

| Severity | Examples | Effect |
|---|---|---|
| Critical | Invented facts; unsafe instruction | Automatic rejection |
| Major | Illegible labels; broken order; wrong chart scale | Blocks release until fixed |
| Minor | Spacing inconsistency; non-essential decoration | Logged and fixed in the next revision |

Weighted score after all gates: accuracy 25, clarity 20, typography 15, visual hierarchy 15,
accessibility 10, technical output 10, brand coherence 5; pass at 85.

## Accessibility evaluation (handbook Annex I)

Alt text and long description; reading order and keyboard access; contrast, non-colour encoding and
label size; zoom, reflow and high-contrast modes; right-to-left and translation expansion; cognitive
clarity and consistent terminology.

## Release and archive checklist (handbook Annex L)

Content verified against sources; no typos, duplicated steps or malformed numbers; permissions and
attribution present; accessible equivalent provided; every target format rendered and inspected;
final approvers and dates recorded; editable source and release files archived.

## Release declaration (handbook Annex O)

> I confirm that the final artefact has been checked against the approved brief, authoritative
> content, accessibility requirements and every target renderer. No generated pseudo-text, invented
> figures, misleading charts or prohibited photorealistic synthetic people or scenes are present.
> All unresolved exceptions are documented and approved.
>
> Content approver: ______ Design approver: ______ Technical approver: ______ Date: ______

## Repository and governance

Each project keeps `/briefs`, `/data`, `/sources`, `/design`, `/exports`, `/qa` and `/licenses`.
Templates carry semantic versions; approvals are retained. Governance reviews quarterly: sample
released assets, record defects, and prioritise Kaizen changes by severity and recurrence against
the backlog in the doctrine.
