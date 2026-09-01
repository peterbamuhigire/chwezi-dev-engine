# Book-Driven Kaizen Wave 2 — 24-Book Portfolio Study

Date: 2026-09-01
Status: completed with scoped residuals
Owner: engineering-engine maintainer with domain-engine owners

## Scope and source handling

This wave studies the 24 user-supplied book files (Markdown metadata plus a recovered local PDF for Wood) against the 11 local Git engines and the 11-engine control-plane contract. The files remain outside the repositories. No raw text, OCR, page images, chapter reconstructions, or long quotations are admitted into any engine.

The books are treated as practitioner or textbook inputs for durable concepts. Current standards, policies, laws, vendor capabilities, security guidance, and software versions are not accepted from them; those claims must pass the Digital Research currentness and verification gates.

## Source ledger

| Source | Study status | Durable contribution admitted | Limitation |
|---|---|---|---|
| Seid, *Franchise Management For Dummies* | Studied | Systemisation, brand promise, standards, training, support, local adaptation, due diligence, replication | 2017; jurisdictional and legal claims require current local verification |
| Benedict, *How to Build a Business Warren Buffett Would Buy* | Studied | Long-term stewardship, frugality, service, culture, autonomy with accountability, disciplined capital | Case narrative; not a valuation or current market authority |
| Hauge, *Storytelling Made Easy* | Studied | Hero, desire, conflict, transformation, six-step success story, audience identification | Practitioner narrative; use ethically and verify proof |
| Watson et al., *Supply Chain Network Design* | Studied | Baseline-first modelling, scenario comparison, capacity, sensitivity, aggregation discipline, cross-functional modelling | Quantitative decisions require current local data and model audit |
| Bean, *The Accidental Instructional Designer* | Studied | Intentional learning design, hook, practice, interactivity, story, visual clarity, SME collaboration | Practitioner guidance; not a learning-science standard |
| Fielding, *The Brand Book* | Studied | Strategy before execution, positioning, right to win, touchpoint continuity, sustainable value | Brand framework; no market evidence by itself |
| Bornet, *The Human-Agent Orchestrator* | Studied | Role clarity, decision rights, trust architecture, autonomy dial, intervention, containment, recovery, postmortems | Conceptual and technology-sensitive; current AI claims require verification |
| Langley et al., *The Improvement Guide* | Studied | Aim, measures, changes, PDSA, run charts, implementation, spread, profound knowledge, human side | Improvement method, not a substitute for domain safety controls |
| Hartwell and Chen, *Archetypes in Branding* | Studied | Qualitative brand-character probe, audience/stakeholder mapping, dominant archetype and wing | Interpretive tool; never evidence of demand or audience truth |
| Ehrhardt et al., *Corporate Finance: A Focused Approach* | Studied | Cash versus profit, capital budgeting, risk/return, WACC, working capital, forecasting, governance | Older US-oriented textbook; current IFRS, tax, rates, and policy are separate |
| Levinson and McLaughlin, *Guerrilla Marketing for Consultants* | Studied | Client-centred marketing, clear niche, relationships, proposals, pricing, follow-through, low-cost experiments | 2004; channel and market tactics are historical |
| Noble, *How to Write a Grant* | Studied | Funder fit, problem/evidence/solution logic, outcomes, budget coherence, review discipline | Current donor rules and eligibility require source verification |
| Kirkpatrick, *Four Levels of Training Evaluation* | Studied | Reaction, learning, behaviour, results; critical behaviours, drivers, leading indicators, value chain | Framework does not prove causality without a proper evaluation design |
| King, *Product Marketing Misunderstood* | Studied | Voice of customer, positioning, enablement, lifecycle role, cross-functional ownership, adoption metrics | Practitioner framework; current product/platform claims require verification |
| Sheehan, *The Pocket Guide to Product Launches* | Studied | GTM plan as source of truth, launch stages, RACI, readiness, internal comms, feedback, post-launch measures | Launch process must match product risk and current platform constraints |
| Schmidlin, *The Art of Company Valuation and Financial Statement Analysis* | Studied | Financial statements plus qualitative business quality, cash flow, debt, management, competitive position, multiple-method valuation | Older market/accounting context; no current reporting authority |
| Gerber, *The E-Myth Enterprise* | Studied | Designed enterprise, repeatable systems, visual/emotional/functional/financial coherence, stakeholder satisfaction | Conceptual management book; avoid treating its matrix as a diagnostic proof |
| Watkinson, *The Grid* | Studied | Whole-business trade-offs across wants/needs, rivalry, offerings, revenues, bargaining power, costs, customer base, imitability, adaptability | Heuristic; must be paired with evidence and financial/operational models |
| Wood, *The Marketing Plan Handbook* | Studied from recovered local PDF with OCR-assisted review | Adaptive customer-first marketing plan; current-situation scan; market ladder; segment scoring; strategy-to-program alignment; forecast, budget, metric, control, audit, and contingency loop | 2003; examples, software, platform, market, and legal claims are historical; current claims require Digital Research verification; OCR quality is suitable for qualified synthesis, not quotation |
| La Piana, *The Nonprofit Strategy Revolution* | Studied | Identity and business model, Big Question, Strategy Screen, real-time planning, 90-day implementation, board/management distinction | Mission and funding context must be verified for each organisation |
| Sheth and Singh, *Ace the Data Science Interview* | Studied selectively | Explainable project impact, product sense, data quality, SQL/data modelling, algorithm trade-offs, audience-aware communication | Interview-prep book; algorithms and tools are not current technical authority |
| Liu, *DNS and BIND* | Studied | Distributed namespace, zones, delegation, authority, caching, health, troubleshooting, security, architecture | Historical BIND edition; commands and supported versions are obsolete unless re-verified |
| Hamilton, *Email Storyselling Playbook* | Studied | Story → lesson → audience pivot → CTA, story bank, specific conflict/resolution, ethical repetition | Direct-response advice; avoid manipulation and unsupported claims |
| Garbugli, *Find Your Market* | Studied | Compare active/inactive and strong/weak customers, segment recipes, switch interviews, core-market selection, adjacent-market catalogue | Market conclusions require current primary research and verified data |

## Cross-engine improvement map

| Priority | Engines | Change hypothesis |
|---|---|---|
| P0 | All available engines | A shared decision-and-learning contract will reduce prose-only improvements and make aim, measure, experiment, guardrail, rollback, and re-audit evidence consistent. |
| P0 | Digital Research, all consumers | A source-currentness register plus explicit volatile-claim gate will prevent historical books or stale references from becoming current standards or technology policy. |
| P0 | Skills Web Dev, SRS, proposal, business, design | Human-agent work will be safer when decision rights, autonomy, evidence, intervention, recovery, and postmortem records are explicit. |
| P1 | Business, finance, SRS, engineering, proposal | A whole-system decision lens will expose trade-offs between customer value, cash, cost, capacity, resilience, imitability, and adaptability. |
| P1 | Business, proposal, website, social, design | Customer-first positioning and story structures will improve clarity and proof when tied to a claim/evidence map and a measurable next action. |
| P1 | Business, proposal, website, social, finance | Wood's adaptive marketing-plan loop will make market definitions, segment choices, objectives, programs, budgets, forecasts, metrics, corrective action, and audit ownership traceable across commercial deliverables. |
| P1 | SRS, Linux, proposal, social, website, business | Learning outputs will improve when they specify performance objectives, demonstration, practice, assessment, transfer support, critical behaviours, and results. |
| P1 | Linux, engineering | DNS guidance will remain conceptual in books-derived references and point to current ISC/IETF sources for versions, support, security, and commands. |

## Deliberate non-changes

- No new active skill is promoted in this wave before routing-collision evidence exists.
- No current market, legal, tax, IFRS, security, platform, DNS-version, or AI-policy claim is admitted from a book.
- No archetype is treated as audience evidence.
- No marketing or launch tactic is treated as universal without a defined audience, channel, measure, and ethical boundary.

## Current implementation backlog

| ID | Action | Owner | Acceptance evidence |
|---|---|---|---|
| K2-01 | Add central business-system and learning-loop contract | Skills Web Dev | Linked reference; central validator and routing smoke pass |
| K2-02 | Add currentness manifest and source-admission reference | Digital Research | Currency validator passes; source states and review dates present |
| K2-03 | Add domain references to all 11 engines, including Windows Admin | Each engine owner | Direct links, no raw-source findings, quick validators pass |
| K2-04 | Repair stale Digital Research control-plane directory and restore Windows Admin registration | Skills Web Dev | Control-plane validator reports 11 engines and zero findings |
| K2-05 | Run native validation and safety review | All changed engines | Positive, negative, and unavailable checks recorded |
| K2-06 | Re-audit and schedule next review | Portfolio owner | Capped score, raw evidence, blockers, owner, and re-audit date |
| K2-07 | Recover and synthesize the Marketing Plan Handbook PDF; link the operating loop to Business market-validation and Kaizen routes | Business owner | Contract test passes; independent reference is linked; book ledger and plan are updated; historical claims remain gated by Digital Research |

## Re-audit handoff

Re-audit after the next portfolio wave or by 2026-10-01. Measure routing precision, currentness coverage, unresolved-claim count, reference discoverability, validator findings, and whether downstream outputs contain the promised decision/evidence artefacts. Keep Windows live/lab evidence and any unverified historical or currentness claims visible as scoped gaps; the Marketing Plan Handbook concept synthesis is now assessed.
