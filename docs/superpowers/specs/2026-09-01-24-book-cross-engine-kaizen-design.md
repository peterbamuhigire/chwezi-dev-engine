# 24-Book Cross-Engine Kaizen Design

Status: implementation-authorised by the active Kaizen task; the Windows engine is restored and statically assessed, with live/lab evidence kept claim-specific.
Date: 2026-09-01

## Objective

Use the 24 supplied books as conceptual input to improve the local skill-engine portfolio. Preserve the engines' domain ownership, admit current standards and technology claims only through Digital Research source evaluation and verification, and leave a reproducible evidence trail.

## Evidence boundary

- The supplied books are private study inputs, not repository content. Store no raw text, OCR, page images, chapter reconstructions, or long quotations.
- Book-derived material is independent operational synthesis and is labelled with the source title, author, scope, and limitations.
- Current standards, policies, laws, platform behaviour, security guidance, product versions, and technology capabilities require a current primary source and a review date.
- Historical practitioner guidance may inform hypotheses but cannot establish current compliance, market, or technical truth.
- The supplied Marketing Plan Handbook Markdown is metadata-only, but a corresponding local PDF was recovered and studied with temporary OCR. Only an independent synthesis is admitted; raw OCR and historical examples remain quarantined outside the repositories.

## Portfolio architecture

1. Central control-plane contract: define the shared decision, evidence, learning-loop, and handoff vocabulary.
2. Domain references: add concise, independently written reference files only where a domain has a real application.
3. Existing-skill enrichment: update the smallest owning skills with direct links and one or two workflow gates; do not create duplicate routes in the first wave.
4. Currentness register: maintain machine-readable source records with tier, access date, revision/publication date, review date, and claim scope.
5. Verification: run native validators, routing smoke tests, source-ingestion guardrails, safety checks, and control-plane validation after each wave.

## Book-to-capability synthesis

| Capability | Durable synthesis | Primary owners |
|---|---|---|
| Improvement | Aim, measure, change, small PDSA tests, implementation, spread, and learning records | All Kaizen routes; central control plane |
| Business system | Treat the enterprise as an interconnected system; expose trade-offs across desirability, profitability, longevity, capacity, and adaptability | Business, finance, SRS, engineering |
| Replication | Make the operating model teachable and repeatable while allowing bounded local adaptation; protect service and culture | Business, proposal, website, social, SRS |
| Market and GTM | Select a core market from observed value and behaviour; align positioning, launch, enablement, retention, and proof | Business, proposal, website, social, design |
| Narrative | Use a real audience-relevant protagonist, specific stakes, conflict, transformation, evidence, and a clear next action | Proposal, website, social, design, research |
| Finance and network | Separate profit from cash, model scenarios, test capacity and sensitivity, and connect capital decisions to operating evidence | Finance, business, SRS, engineering, proposal |
| Learning transfer | Design for performance: instruction, demonstration, practice, assessment, post-training support, critical behaviours, leading indicators, and results | SRS, Linux, proposal, social, website, design |
| Human-agent work | Assign decision rights, boundaries, evidence, autonomy levels, escalation, intervention, containment, recovery, and postmortems | Engineering, SRS, proposal, business, research, design |
| DNS operations | Keep concepts durable but route versions and commands to current ISC/IETF sources; verify authority, delegation, health, caching, security, and recovery | Linux, engineering |

## New-skill rule

Wave 1 creates no new active skill. A new skill is allowed only after a routing-collision test demonstrates that an independently named user intent cannot be owned by an existing skill, and the new route has a distinct consumer, fixture, owner, and rollback path.

## Currentness rule

Every reference that names a current standard, policy, platform, vendor, command, version, or legal requirement must link to the Digital Research currentness register. The reference must state what the source supports, what it does not support, last verification, next review, and the trigger that invalidates it. If the source is stale, partial, inaccessible, or contested, the skill must narrow the claim or mark it `NOT ASSESSED`.

## Release gates

- No raw-source or reconstructive-text findings.
- No new routing collision or active-catalogue growth without a justified gap.
- Changed skills satisfy the local authoring contract and quick validation.
- Native engine validators, routing smoke tests, currentness validation, safety review, and anti-slop review pass or are explicitly recorded as `NOT ASSESSED`.
- Every accepted experiment has a measure, guardrail, rollback, owner, acceptance evidence, and re-audit date.

## Known gaps

- Windows live/lab evidence is claim-specific and may remain `NOT ASSESSED` where no current host or lab evidence is available.
- The control-plane validator now points to the verified Digital Research checkout and the restored Windows Admin checkout.
- Several book files contain OCR duplication or mojibake; they are suitable for qualified concept synthesis, not quotation.
