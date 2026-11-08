Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Infographics Design and Production Quality Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Chwezi Infographics Design and Production Quality Standard

**Status:** Adopted into the Chwezi engines on 8 November 2026 on the instruction of Lead Developer
Peter Bamuhigire. Source: the full edition of the handbook "Chwezi Full Infographics Design and
Production Quality Standard" (Version 1.0, 8 November 2026, owner Design Governance / Product
Engineering). Its MUST, SHOULD and MAY carry their usual force; its scores are internal governance
thresholds, not an external certification.
**Version:** 1.0.0
**Owner:** Peter Bamuhigire / Chwezi Core Systems
**Parent:** the Chwezi Product Excellence Standard, of which this is the fourth child standard, beside
the Reporting and Dashboards, Document Reporting and Publishing, and Presentation and Slide Deck
Design standards
**Agent entry point:**
[chwezi-infographics-standard](../../SKILL.md)

An infographic is a self-contained visual argument: it must stay true and understandable without a
presenter, at its real size, in every format it ships in. Visual polish never excuses a factual
error; a polished visual with false information is an automatic rejection. AI tools may assist with
planning, drafting, illustration and code, but they may not invent facts, render pseudo-text or
synthetic photorealistic scenes, or silently change approved wording. This is a specification, not a
catalogue of pictures to imitate.

## Scope

- Every infographic Chwezi produces or a Chwezi product generates: process flows, cycles, timelines
  and roadmaps, comparisons and decision matrices, hierarchies and trees, journeys and service
  blueprints, technical cutaways and isometric maps, educational and safety posters, statistical
  explainers, social and phone cards, and infographics embedded in web and SaaS reports (on desktop,
  tablet and phone), slides,
  DOCX and PDF publications, up to physical A2 posters.
- Out of scope: a single analytical chart inside a product screen (Product Excellence and Reporting),
  a whole deck (Presentation) and a whole document (Publishing). When an infographic sits inside
  one of those, both standards apply.

## Precedence

This standard sits beside its three sibling child standards at step 4 of the Product Excellence
ladder; where two apply, the stricter rule wins. Project brand rules approved by the owner take
precedence over its defaults, never over its gates.

| Topic | Rule |
|---|---|
| Figures | The Reporting standard governs metric contracts, periods, units and reconciliation; an infographic never shows a figure that does not trace to its source register. |
| Claims, imagery, logos, signatures | The Publishing standard's content rules apply; no claim without a register entry. |
| Infographics in decks | The Presentation standard's venue legibility law and native-object rules also apply. |
| Typography | The banned-font doctrine governs. The handbook's example list (Aptos, Arial, Inter, Source Sans 3, Noto Sans, IBM Plex Sans; Source Serif or Georgia) is superseded: Inter, Arial and IBM Plex are banned, Source Sans 3 is paired body only. Defaults: Public Sans (tabular figures) and Source Serif 4; Atkinson Hyperlegible for low-vision and signage work; the matching Noto family for non-Latin scripts; Georgia and Aptos only as device-common fallbacks. State the typeface and the reason. |
| Spacing | Layout spacing uses an 8-point base; the house steps 4 and 12 are the justified exceptions. App screens keep the house scale. |
| Accessibility | WCAG 2.2 AA contrast (4.5:1 text, 3:1 large text and meaningful graphics) is the target for on-screen text; colour never carries meaning alone. |
| Money and dates | ISO 4217 minor-unit decimals; dates read `4 Nov 2026`; quantities in different units are never summed (owner rules). |
| Reference images | Inspiration categories only, never factual sources; never reproduce their compositions, marks or errors. |

## Design principles

1. One communication goal, one primary audience and a one-sentence takeaway before any artwork.
2. Build the information structure first; decorate only after comprehension is verified.
3. Every fact maps to a visible element, and every element exists for a reason the reviewer can name.
4. Encodings are honest: lengths start at zero, areas scale with value, time is spaced truthfully or
   labelled as a sequence, comparisons are symmetric.
5. Structure is correct: unique steps, unambiguous arrows, real loops only, true hierarchies.
6. Text is real, typeset, proofread and editable, at a size computed from the real viewing distance.
7. New people and scenes are illustration, never synthetic photorealism; documentary claims use real,
   licensed photographs only.
8. If it does not fit legibly, split it into a series; never shrink critical text.

## Hard release gates

Any one blocks release. Each needs `MEASURED` evidence to close; an applicable gate with
`NOT_ASSESSED` evidence counts as open.

| Gate | Fails when | Also trips |
|---|---|---|
| INFO-GATE-01 Invented or unsourced fact | A figure, percentage, count, date, location, citation, ranking, logo or source has no entry in the provenance register, or illustrative data is not flagged as illustrative. | PUB-GATE-02, DECK-GATE-01 |
| INFO-GATE-02 Pseudo-text or illegible text | Any generated, warped or illegible lettering; text baked into generated art; or text below the computed minimum for its viewing distance and output size. | DECK-GATE-02 |
| INFO-GATE-03 Synthetic or unlicensed imagery | A photorealistic generated person or scene, a fake logo, a synthetic image presented as documentary evidence, or an asset without licence or permission. | PUB-GATE-02, DECK-GATE-06 |
| INFO-GATE-04 Misleading encoding | A bar without a zero baseline, a 3D or perspective chart that alters magnitude, a lie factor outside 0.95-1.05, an area scaled by radius, equal widths implying equal durations, an asymmetric comparison, or a map that shades raw counts, uses an unsourced or outdated boundary, or distorts the comparison it makes. | DECK-GATE-07, RPT-GATE-01 |
| INFO-GATE-05 Broken structure | Duplicate or orphan steps, an unreachable or dead-end node, an ambiguous arrow, a cycle without entry point or direction, a loop drawn as a chain, or a cycle in a strict hierarchy. | None (infographic-specific) |
| INFO-GATE-06 Unreviewed regulated or unsafe content | Medical, safety, engineering, legal or financial content released without the named qualified reviewer, or an instruction from which a hazardous shortcut can be inferred. | PX-GATE-12 |
| INFO-GATE-07 Inaccessible | No short alt text and long text equivalent, meaning carried by colour alone, or on-screen text below the contrast target. | PX-GATE-06 |
| INFO-GATE-08 Uninspected or unarchived release | A target format not rendered and inspected at actual size, a print file without the agreed bleed, embedded fonts and effective resolution, or a release without the signed declaration and archived editable sources. | PUB-GATE-06, DECK-GATE-08 |

## Release decision

An infographic is released only when:

- every applicable INFO gate is closed on measured evidence;
- the weighted score is at least 85 of 100 (accuracy 25, clarity 20, typography 15, visual hierarchy
  15, accessibility 10, technical output 10, brand coherence 5), scored after the gates;
- no critical finding (invented fact or unsafe instruction) and no open major finding (illegible
  label, broken order, wrong chart scale);
- the content, design and technical approvers have signed the release declaration.

## Roles

| Approver | Approves |
|---|---|
| Content (factual owner) | Facts, wording, sources, calculations, caveats |
| Design | Presentation, hierarchy, typography, colour, illustration |
| Technical (engineering) | Output compatibility, exports, print files, accessibility build |
| Subject-matter reviewer | Required for medical, safety, engineering, legal and financial content |

Exceptions need a documented reason, risk, owner and expiry.

## Rules

The normative rules, `INFO-<AREA>-NNN`, are in the skill's
[rules and gates reference](rules-and-gates.md).
A SHOULD departure needs a design decision record. IDs are never reused.

## Kaizen backlog (owner priorities)

| Priority | Failure mode | Control | Measure |
|---|---|---|---|
| P0 | Factual hallucination | Claim register and mandatory source approval | Zero unsupported claims in sampled releases |
| P0 | Illegible AI-generated text | Real text layers; human proofread | Zero pseudo-text defects |
| P0 | Synthetic documentary imagery | Block photorealistic generated scenes | Zero violations |
| P1 | Cross-format layout breakage | Automated target-size previews | Under 2% failed export proofs |
| P1 | Accessibility gaps | Mandatory long descriptions and contrast tests | 100% checklist coverage |
| P1 | Process topology errors | Node and edge validation | Zero duplicate or orphan steps |
| P2 | Inconsistent templates | Central tokens and component library | 90% template reuse |
| P2 | Weak documentation | Archive source, proof and approval metadata | 100% traceable assets |

Each item records baseline, corrective action, due date, evidence and outcome; it reopens on
regression and is reviewed at the quarterly quality meeting.

## Evidence states and currentness

The Product Excellence evidence vocabularies apply. Standards and methods cited (WCAG 2.2, ISO 216
paper sizes, W3C complex-image and translation guidance, colour-vision simulation, press ink limits)
are recorded with access date and status in the skill's currentness register.

## Copies in other engines

Each Chwezi engine that serves infographic work carries its own complete copy of this doctrine, the
rules catalogue, the references and the checker script, with identical IDs and wording, and works
without any other engine installed. This file is the canonical text; copies are re-synced whenever
its version changes.

## Change control

Peter Bamuhigire approves every change; semantic versions (patch for wording, minor for new SHOULD or
MAY rules and blueprints, major for any new, removed or re-levelled MUST, any gate or any threshold);
every release is logged in the engine's change record with the rule IDs affected. Rule changes are
tested against every affected renderer. Governance reviews quarterly: sample released assets, record
defects and prioritise Kaizen changes by severity and recurrence.
