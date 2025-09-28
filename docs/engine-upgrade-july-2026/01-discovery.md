# Discovery

Engine root: `C:\wamp64\www\skills-web-dev`
Discovery date: 2026-07-07

## What Was Read

I read the root router/controller files where present (`README.md`, `AGENTS.md`, `CLAUDE.md`) and read every discovered `SKILL.md` file in full. I also read every Markdown file matching governance, doctrine, standard, quality, anti-slop, architecture, router, guide, index, policy, protocol, or changelog naming patterns into the audit manifest. The full content inventory is in `10-appendix-file-inventory.md`.

## Tree Metrics

| Metric | Value |
| --- | --- |
| Files | 3570 |
| Directories | 1261 |
| Maximum directory depth | 9 |
| Total content size | 88.28 MB |
| SKILL.md files | 244 |
| Governance/doctrine/standard files read | 826 |

## Unusual Findings

- Empty directories found: 49.
- Frontmatter gaps: 76 missing name, 76 missing description.
- Duplicate-content hash groups found: 20 sampled groups.

## Architecture Map

This engine claims to provide reusable engineering, AI, SaaS, security, product, mobile, backend, frontend, documentation, and operations skills. A world-class deliverable looks like staff/principal-engineer guidance from a top software organisation: precise, version-aware, secure, testable, implementation-ready, and connected to release evidence rather than generic advice. Benchmark: Stripe/Shopify/Thoughtworks-quality engineering playbooks plus current platform/vendor guidance and automated conformance checks.

The engine is organized as a hierarchical skill engine with filesystem-discovered `SKILL.md` entrypoints, router/controller Markdown at the root, and supporting assets in references, templates, scripts, examples, docs, projects, fonts, or tools depending on the engine. The architecture is strongest where routers tell the agent to glob `SKILL.md` fresh and weakest where empty directories, local project workspaces, or missing frontmatter create false surfaces.

## Asset Catalogue

| Extension/type | Count |
| --- | --- |
| .md | 2105 |
| .png | 571 |
| .jpg | 415 |
| .html | 320 |
| .css | 80 |
| .yaml | 16 |
| .ps1 | 11 |
| .py | 11 |
| .php | 9 |
| .sql | 7 |
| .template | 7 |
| .yml | 4 |
| [no extension] | 4 |
| .csv | 3 |
| .txt | 3 |
| .json | 2 |
| .docx | 1 |
| .js | 1 |

Supporting asset counts from path classification: references=2690, templates=1420, examples=292, scripts/script-like=23.

## Skill Frontmatter Quotation

The table quotes the discovered `name` and `description` frontmatter values. `[MISSING]` means the field was not present in the file frontmatter.

| Skill path | name | description |
| --- | --- | --- |
| 00-meta-initialization/SKILL.md | name: meta-initialization | description: Detect project type, recommend documentation methodology (Waterfall/Agile/Hybrid), and generate documentation roadmap. Use this as the FIRST skill when starting documentation for any project. |
| 00-meta-initialization/new-project/SKILL.md | name: new-project | description: Use when the task matches skill: new project scaffold and this skill's local workflow. |
| doctrine/skills/01-foundations/chart-of-accounts-design-and-governance/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/01-foundations/functional-and-presentation-currency/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/01-foundations/ledger-posting-engine-core/SKILL.md | name: ledger-posting-engine-core | description: Use when designing, reviewing, or testing the canonical posting service, journal-entry schema, event-to-journal mapping, ledger invariants, reversals, idempotency, period locks, control-account tie-outs, and drilldown from source evidence to financial reports. |
| doctrine/skills/01-foundations/management-accounting-dimensions/SKILL.md | name: management-accounting-dimensions | description: Governed dimensions (cost centre, project, grant, donor restriction, department, branch, product line, customer, supplier, activity, currency, book) and the budget / variance / allocation / contribution-margin / donor-grant reporting they support. Use when designing or implementing management reporting, KPI dashboards, budget vs actual, project profitability, grant utilisation, contribution-margin analysis, or allocation rules. Applies in software, SRS, SDS, test plan, proposal, and business-plan contexts. |
| doctrine/skills/01-foundations/period-locking-and-data-immutability/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/02-ifrs-core-standards/ifrs-borrowing-costs-ias23/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/02-ifrs-core-standards/ifrs-employee-benefits-ias19/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/02-ifrs-core-standards/ifrs-financial-instruments/SKILL.md | name: ifrs-financial-instruments | description: Financial-instrument classification, measurement, and impairment under IFRS 9 (full IFRS) and Sections 11 and 12 (IFRS for SMEs). Trade receivables, payables, bank balances, loans, deposits, debt and equity instruments, derivatives, expected credit loss (ECL), hedge accounting. Use when financial instruments are material. Tier-3 scope — Section 11 basic-instruments handling is built first; full IFRS 9 ECL deferred until a client materially requires it. |
| doctrine/skills/02-ifrs-core-standards/ifrs-for-smes-equivalents/SKILL.md | name: ifrs-for-smes-equivalents | description: Practical IFRS for SMEs equivalents to full IFRS standards. The default reporting framework for typical Chwezi clients (SMEs, schools, clinics, NGOs, retail, agribusiness, hospitality, family business). Cross-references each IFRS standard to its IFRS for SMEs section and notes the build implications. Use whenever generating finance content for SME clients, or when deciding whether full IFRS or IFRS for SMEs applies. |
| doctrine/skills/02-ifrs-core-standards/ifrs-foreign-currency-translation-ias21/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/02-ifrs-core-standards/ifrs-intangible-assets-ias38/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/02-ifrs-core-standards/ifrs-leases/SKILL.md | name: ifrs-leases | description: Lease accounting under IFRS 16 (full IFRS) and Section 20 (IFRS for SMEs). Lessee single on-balance-sheet model under IFRS 16; lessee operating-vs-finance classification under Section 20. Short-term and low-value exemptions. Lessor classification. Sale-and-leaseback. Use when leases or rental arrangements are in scope. Tier-3 scope — full lessee build deferred until a client materially requires it; Section 20 short-term operating-lease handling and IFRS 16 exemption-test reference are built first. |
| doctrine/skills/02-ifrs-core-standards/ifrs-property-plant-equipment-ias16/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/02-ifrs-core-standards/ifrs-revenue-recognition/SKILL.md | name: ifrs-revenue-recognition | description: IFRS 15 (full IFRS) and Section 23 (IFRS for SMEs) revenue recognition for Chwezi systems. Covers contract identification, performance obligations, transaction price, allocation, timing of recognition, contract assets and liabilities, refunds, warranties, principal-vs-agent, and disclosures. Use when revenue, sales contracts, subscription billing, multi-element arrangements, deferred revenue, retention, percentage of completion, agency fees, or revenue disclosures are in scope. |
| doctrine/skills/03-ifrs-specialised-standards/ias-agriculture/SKILL.md | name: ias-agriculture | description: Agriculture and biological-asset accounting under IAS 41 (full IFRS) and Section 34 (IFRS for SMEs). Recognition, measurement at fair value less costs to sell where reliably measurable, point-of-harvest treatment, bearer biological assets, government grants in agriculture, cost-model fallback, sector-specific build implications for BIRDC, agribusinesses, poultry, dairy, horticulture, plantation, and aquaculture. Use whenever biological assets, agricultural produce, or sector operations like BIRDC, dynagricug, or other Chwezi agribusiness clients are in scope. |
| doctrine/skills/03-ifrs-specialised-standards/ias-government-grants/SKILL.md | name: ias-government-grants | description: Government grants and assistance under IAS 20 (full IFRS) and Section 24 (IFRS for SMEs). Recognition, measurement, presentation (gross vs net), conditions, repayable assistance, donor restrictions for NGOs, grant utilisation reporting. Use when government or donor grants are in scope, especially for NGOs, schools, agribusiness, and projects under restricted funding. |
| doctrine/skills/03-ifrs-specialised-standards/ias-impairment/SKILL.md | name: ias-impairment | description: Impairment of non-financial assets under IAS 36 (full IFRS) and Section 27 (IFRS for SMEs). Indicator-based testing, recoverable amount (higher of fair value less costs of disposal and value in use), cash-generating units, goodwill impairment, reversal. Use when material PPE, intangibles, goodwill, or investment property carrying amounts could be impaired. Tier-3 scope — indicator-based reference built first; full annual-test machinery deferred until a goodwill-heavy or asset-intensive client demands it. |
| doctrine/skills/03-ifrs-specialised-standards/ias-income-tax-deferred-tax/SKILL.md | name: ias-income-tax-deferred-tax | description: Income tax accounting under IFRS for SMEs Section 29 (practical default) and IAS 12 (full IFRS overlay). Current tax, deferred tax, temporary differences, recognition of deferred-tax assets, valuation allowance, tax-rate reconciliation, presentation. Use when corporate income tax, deferred tax, tax expense disclosure, or tax-rate reconciliation is in scope. |
| doctrine/skills/03-ifrs-specialised-standards/ias-provisions-contingencies/SKILL.md | name: ias-provisions-contingencies | description: Provisions, contingent liabilities and contingent assets under IAS 37 (full IFRS) and Section 21 (IFRS for SMEs). Recognition criteria (present obligation, probable outflow, reliable estimate), measurement, onerous contracts, restructuring, warranties, contingent disclosures. Use when provisions, litigation, warranties, onerous contracts, restructuring, decommissioning, or guarantee disclosures are in scope. |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-accounting-policies-changes-errors-ias8/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-associates-and-joint-arrangements/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-business-combinations-ifrs3/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-discontinued-operations-ifrs5/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-earnings-per-share-ias33/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-events-after-reporting-period-ias10/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-fair-value-measurement-ifrs13/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-first-time-adoption-ifrs1/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-insurance-contracts-ifrs17/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-investment-property-ias40/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-related-party-disclosures-ias24/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-segment-reporting-ifrs8/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-share-based-payment-ifrs2/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/04-subledgers-and-operations/bank-and-mobile-money-reconciliation/SKILL.md | name: bank-and-mobile-money-reconciliation | description: Bank-account, mobile-money (MTN MoMo, Airtel Money, equivalents), POS cash drawer, card settlement, and clearing-account reconciliation workflow design and implementation. Use whenever a software system, SRS, SDS, test plan, proposal, business plan, or strategy involves bank feeds, mobile-money statements, POS Z-reports, settlements, chargebacks, reversals, bank charges, unmatched deposits, or month-end reconciliation evidence packs. |
| doctrine/skills/04-subledgers-and-operations/expense-management-and-staff-claims/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/04-subledgers-and-operations/fixed-assets-and-depreciation/SKILL.md | name: fixed-assets-and-depreciation | description: Use when designing, reviewing, or testing fixed-asset registers, capitalization policy, componentization, depreciation, useful-life review, disposals, revaluation caveats, impairment indicators, tax depreciation caveats, and asset-register to GL tie-outs. |
| doctrine/skills/04-subledgers-and-operations/inventory-costing-and-stock-accounting/SKILL.md | name: inventory-costing-and-stock-accounting | description: Use when designing, reviewing, or testing stock accounting, SKU and location policy, FIFO or weighted-average costing, stock counts, shrinkage, wastage, expiry, NRV write-downs, COGS postings, and inventory control-account tie-outs. |
| doctrine/skills/04-subledgers-and-operations/payroll-and-statutory-postings-east-africa/SKILL.md | name: payroll-and-statutory-postings-east-africa | description: Use when designing, reviewing, or testing gross-to-net payroll, PAYE, NSSF, LST, WHT, payroll clearing, employer and employee contribution splits, payslip-to-GL reconciliation, and statutory source gates for East Africa country packs. |
| doctrine/skills/04-subledgers-and-operations/petty-cash-and-imprest-management/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/04-subledgers-and-operations/pos-and-cash-drawer-management/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/05-receivables-payables-and-treasury/accounts-payable-and-supplier-management/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/05-receivables-payables-and-treasury/accounts-receivable-and-credit-management/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/05-receivables-payables-and-treasury/banking-facilities-and-covenants/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/05-receivables-payables-and-treasury/cash-flow-forecasting-and-treasury/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/05-receivables-payables-and-treasury/fx-management-and-hedging/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/06-close-consolidation-and-reporting/audit-pbc-and-evidence-management/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/06-close-consolidation-and-reporting/audit-ready-reporting-pack/SKILL.md | name: audit-ready-reporting-pack | description: The audit-ready reporting pack standard for any Chwezi-grade entity. Defines the minimum reports, their content, the drilldown chain, the auditor-export index, the print fidelity, the sign-off, and the release governance. Use whenever a software system, SRS, SDS, test plan, proposal, or business plan involves financial statement preparation, monthly management accounts, donor reports, statutory reports, audit-ready exports, or external audit support. |
| doctrine/skills/06-close-consolidation-and-reporting/consolidation-and-intercompany/SKILL.md | name: consolidation-and-intercompany | description: Use when designing, reviewing, or testing group reporting, entity hierarchy, reporting currency, intercompany matching, elimination journals, group trial balances, non-controlling interest caveats, and foreign-operation translation caveats. |
| doctrine/skills/06-close-consolidation-and-reporting/continuous-close-and-flash-reporting/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/06-close-consolidation-and-reporting/finance-module-audit/SKILL.md | name: finance-module-audit | description: >- Use when auditing any software, SRS, proposal, POS, ERP, SaaS, mobile app, or workflow that touches money, billing, payments, tax, payroll, banking, mobile money, inventory, statutory compliance, financial reports, or accounting records. |
| doctrine/skills/06-close-consolidation-and-reporting/month-end-and-year-end-close-playbook/SKILL.md | name: month-end-and-year-end-close-playbook | description: Controlled month-end and year-end close workflow for any Chwezi-grade finance / accounting system. Covers task list, dependencies, evidence requirements, exception handling, reviewer sign-off, period-state transitions, retained-earnings close, lock and reopen governance, and release states. Use whenever a software system, SRS, SDS, test plan, proposal, or business plan touches month-end close, year-end close, period locking, or audit-period release. |
| doctrine/skills/06-close-consolidation-and-reporting/opening-balances-and-migration-playbook/SKILL.md | name: opening-balances-and-migration-playbook | description: Cutover from legacy Excel / QuickBooks / Tally / Sage / POS / manual systems into Chwezi. Defines the conversion-date model, CoA mapping, opening trial balance, opening subledgers (AR / AP / Inventory / Fixed Assets / Payroll / Tax), bank / mobile-money / cash opening balances, migration suspense, reviewer sign-off, and acceptance evidence. Use whenever a software system, SRS, SDS, test plan, proposal, or business plan involves data migration, cutover, opening balances, or legacy-system replacement. |
| doctrine/skills/07-financial-statements-and-disclosures/cash-flow-statement-ias7/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/07-financial-statements-and-disclosures/financial-statements-preparation/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/07-financial-statements-and-disclosures/going-concern-and-viability-assessment/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/07-financial-statements-and-disclosures/integrated-and-sustainability-reporting-s1-s2/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/07-financial-statements-and-disclosures/notes-and-disclosure-pack/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/08-tax-and-statutory/e-invoicing-and-fiscal-device-integration/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/08-tax-and-statutory/indirect-tax-vat-mechanics/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/08-tax-and-statutory/tax-statutory-source-register-and-country-packs/SKILL.md | name: tax-statutory-source-register-and-country-packs | description: Use when designing, reviewing, or validating tax, payroll, statutory, e-invoicing, exchange-rate, source-register, and country-pack behavior for Uganda, Kenya, Rwanda, Tanzania, South Africa, or future Chwezi country extensions. |
| doctrine/skills/08-tax-and-statutory/transfer-pricing-documentation/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/08-tax-and-statutory/withholding-tax-and-treaties/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/09-budgeting-fpa-and-costing/budgeting-and-rolling-forecasts/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/09-budgeting-fpa-and-costing/cost-accounting-methods/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/09-budgeting-fpa-and-costing/pricing-discounts-rebates-and-refunds/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/09-budgeting-fpa-and-costing/scenario-and-sensitivity-modelling/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/09-budgeting-fpa-and-costing/variance-analysis-and-kpi-reporting/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/10-controls-governance-and-fraud/aml-kyc-and-suspicious-transaction-reporting/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/10-controls-governance-and-fraud/engagement-quality-and-plain-language-output/SKILL.md | name: engagement-quality-and-plain-language-output | description: Use when preparing, reviewing, or approving client-facing finance outputs that need preparer-reviewer-approver governance, competence and independence checks, ethics caveats, assurance-quality gates, and mandatory business-language, accounting-policy, and evidence/caveat layers. |
| doctrine/skills/10-controls-governance-and-fraud/finance-doctrine-conformance-scanner/SKILL.md | name: finance-doctrine-conformance-scanner | description: Use when scanning a software system, codebase, implementation plan, proposal, policy memo, business plan, blog post, SRS, or finance/accounting product specification against the Chwezi accounting and finance doctrine. Produces a deep gap analysis, risk-ranked findings, and detailed alignment instructions tied to the doctrine skills and source-register rules. |
| doctrine/skills/10-controls-governance-and-fraud/forensic-accounting-and-anti-fraud/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/10-controls-governance-and-fraud/internal-controls-library/SKILL.md | name: internal-controls-library | description: Library of internal controls embedded in finance / accounting workflows. Segregation of duties, maker-checker, approval thresholds, supplier and payroll master-data controls, petty cash and cash drawer controls, inventory master-data controls, tax / rate table controls, audit-log review, exception monitoring, fraud / error indicators. Use whenever designing or reviewing access control, approval, audit trail, fraud detection, or internal-control attestation in a finance / accounting context. |
| doctrine/skills/10-controls-governance-and-fraud/sox-style-icfr-documentation/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/10-controls-governance-and-fraud/whistleblowing-and-finance-ethics/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/11-sector-and-fund-accounting/agribusiness-and-cooperative-pack/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/11-sector-and-fund-accounting/clinic-and-healthcare-accounting-pack/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/11-sector-and-fund-accounting/fintech-and-payments-pack/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/11-sector-and-fund-accounting/hospitality-and-restaurant-pack/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/11-sector-and-fund-accounting/ngo-and-fund-accounting/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/11-sector-and-fund-accounting/real-estate-and-property-pack/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/11-sector-and-fund-accounting/retail-and-pos-accounting-pack/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/11-sector-and-fund-accounting/school-and-education-accounting-pack/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/12-public-sector-and-ipsas/donor-funded-project-fiscal-compliance/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/12-public-sector-and-ipsas/government-procurement-and-fiscal-controls/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/12-public-sector-and-ipsas/ipsas-public-sector-overlay/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/13-project-and-contract-accounting/construction-contract-accounting/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/13-project-and-contract-accounting/professional-services-time-and-materials/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/13-project-and-contract-accounting/project-and-contract-accounting/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/14-systems-integration-and-data/bank-feed-and-payment-gateway-integration/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/14-systems-integration-and-data/erp-and-finance-system-integration-patterns/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/14-systems-integration-and-data/finance-data-contracts-and-warehouse-models/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/14-systems-integration-and-data/open-banking-and-direct-debit-mandates/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/15-security-privacy-and-continuity/business-continuity-and-disaster-recovery-finance/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/15-security-privacy-and-continuity/finance-cybersecurity-controls/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/15-security-privacy-and-continuity/finance-data-privacy-and-retention/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/16-ux-and-presentation/finance-accessibility-and-inclusive-design/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/16-ux-and-presentation/finance-mobile-and-offline-patterns/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/16-ux-and-presentation/finance-ui-pattern-library/SKILL.md | name: finance-ui-pattern-library | description: Production UI patterns, design tokens, role-conditioned shells, drilldown primitives, reconciliation triage layout, print stylesheet patterns, status taxonomy components, and money-cell components for Chwezi finance and accounting products. Use when designing or building any finance / accounting screen, dashboard, report, print layout, mobile cashier flow, accountant ledger surface, reconciliation UI, close board, return-pack viewer, or audit-ready export across any consumer engine. Auto-load when the user requests UI / UX work that touches money, inventory, payroll, tax, banking, mobile money, POS, statutory compliance, or accounting records. |
| doctrine/skills/16-ux-and-presentation/finance-ux-for-non-accountants/SKILL.md | name: finance-ux-for-non-accountants | description: Workflow-first UX for cashiers, clerks, managers, family-business users, and other non-accountants who must record sales, receive payments, buy stock, pay suppliers, run payroll, close drawers, and resolve exceptions safely while the underlying accounting stays clean. Use when designing any non-accountant-facing finance / accounting UI in a Chwezi product. Pairs with finance-ui-pattern-library, which provides the components and tokens. |
| doctrine/skills/17-ai-automation-and-emerging/ai-in-finance-governance/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/17-ai-automation-and-emerging/carbon-and-emissions-accounting/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/17-ai-automation-and-emerging/digital-assets-and-crypto-accounting/SKILL.md | name: [MISSING] | description: [MISSING] |
| doctrine/skills/17-ai-automation-and-emerging/rpa-and-automation-controls-for-finance/SKILL.md | name: [MISSING] | description: [MISSING] |
| skills/ai/ai-agent-approval-audit-completeness/SKILL.md | name: ai-agent-approval-audit-completeness | description: Use when proving that every irreversible agent action in the audit window had a documented, signed approval — completeness check (gap-detection job), approval-evidence cross-link to the hash-chained action audit log, and evidence pack for SOC 2 Processing Integrity (PI1.1). Pairs with `ai-agent-action-approval-and-hitl` (mechanism) and `ai-agent-audit-log-integrity` (storage). |
| skills/ai/ai-agent-commercial-operations/SKILL.md | name: ai-agent-commercial-operations | description: >- Use when pricing, billing, refunding, recognizing revenue, or packaging commercial terms for agentic AI services and outcomes. |
| skills/ai/ai-agent-compliance-controls/SKILL.md | name: ai-agent-compliance-controls | description: >- Use when mapping AI agent operations to SOC 2, ISO 27001, HIPAA, audit logs, control testing, attestations, and compliance evidence. |
| skills/ai/ai-agent-drill-evidence-and-cadence/SKILL.md | name: ai-agent-drill-evidence-and-cadence | description: Use when capturing kill-switch, red-team, and eval-drift drills as audit-ready compliance evidence — minimum-cadence enforcement, pass/fail recording, and cross-link to the incident drill skill. Turns drills from operational exercises into SOC 2 / ISO 27001 / HIPAA evidence rows with signed packs. |
| skills/ai/ai-agent-governance-and-limits/SKILL.md | name: ai-agent-governance-and-limits | description: >- Use when defining agent budgets, step limits, reversibility, blast-radius controls, kill switches, and governance policy for agentic AI systems. |
| skills/ai/ai-agent-memory-erasure-proof/SKILL.md | name: ai-agent-memory-erasure-proof | description: Use when proving agent-memory erasure was complete and verifiable for GDPR / CCPA / POPIA / KE DPA requests — the 9-step cascade verification job emits a signed-off evidence pack. Pairs with `ai-agent-memory` (three-tier memory + erasure cascade) and `saas-tenant-data-portability-and-erasure` (tenant-level erasure pipeline). |
| skills/ai/ai-agent-multi-agent-coordination/SKILL.md | name: ai-agent-multi-agent-coordination | description: Use when designing systems where multiple agents collaborate on one task — supervisor/worker, debate, plan-execute, peer handoff. Covers handoff message contracts, shared scratchpad, conflict resolution, deadlock detection, and the cost/SLA discipline that keeps multi-agent setups from spiralling. |
| skills/ai/ai-agent-observability-evaluation/SKILL.md | name: ai-agent-observability-evaluation | description: >- Use when measuring, evaluating, replaying, evidencing, or tracking success for AI agent tasks, steps, traces, and outcomes. |
| skills/ai/ai-agent-runtime-architecture/SKILL.md | name: ai-agent-runtime-architecture | description: Use when designing the runtime that hosts agentic LLM features in a multi-tenant SaaS â€” the agent loop as a control-plane service, formal state machine (PERCEIVE â†’ PLAN â†’ ACT â†’ OBSERVE), retries, idempotency, max-step caps, deterministic resumability, and the "agent vs workflow vs cron" decision. Distinct from `ai-agents-tools` (agent fundamentals) and `ai-on-saas-architecture` (overall AI architecture). |
| skills/ai/ai-agent-safety-and-red-team/SKILL.md | name: ai-agent-safety-and-red-team | description: Use when hardening agentic features against agent-specific attack surfaces — indirect prompt injection (via tool output, retrieved chunk, web page), action escalation (chain a low-privilege tool's output into a high-privilege tool's args), tenant data exfil via tool chain, recursive self-modification, and the CI red-team suite that catches regressions. Distinct from `ai-prompt-injection-and-tenant-safety` (direct user-input injection) by focusing on the agent's *tool-and-data perimeter*. |
| skills/ai/ai-agent-sla-and-customer-commitments/SKILL.md | name: ai-agent-sla-and-customer-commitments | description: >- Use when defining agent SLAs, customer commitments, SLA dashboards, credits, support promises, and service evidence for agentic AI products. |
| skills/ai/ai-agent-tooling-and-hitl/SKILL.md | name: ai-agent-tooling-and-hitl | description: >- Use when designing agent tool catalogs, tool schemas, action gating, human approval, and human-in-the-loop control for agentic AI systems. |
| skills/ai/ai-analytics/SKILL.md | name: ai-analytics | description: >- Use when designing AI analytics, dashboards, SaaS AI metrics, NLP analytics, predictive analytics, or executive AI insight workflows. Orchestrates the former granular AI analytics skills as references. |
| skills/ai/ai-app-architecture/SKILL.md | name: ai-app-architecture | description: Use when designing or building AI-powered application systems — choosing architecture style, selecting components, structuring the AI stack, making build-vs-buy decisions, and planning multi-tenant AI module gating |
| skills/ai/ai-cost-and-metering/SKILL.md | name: ai-cost-and-metering | description: >- Use when modeling, metering, attributing, billing, or controlling AI usage costs across tenants, plans, features, providers, and agent workloads. |
| skills/ai/ai-economic-value-engine/SKILL.md | name: ai-economic-value-engine | description: Use when discovering, designing, prioritizing, or auditing AI-powered products for measurable business value. Applies to AI opportunity mapping, ROI cases, product strategy, client workshops, and deciding whether an AI feature should be built. |
| skills/ai/ai-entitlements-and-feature-gating/SKILL.md | name: ai-entitlements-and-feature-gating | description: Use when designing how AI features are unlocked by plan tier — which model tier (flagship vs distilled), context-length limits, generations/day, tools available to the agent, KB ingestion size, gated AI features (per-feature toggle by plan). Covers entitlement schema, gateway enforcement, upgrade UX, and the contract with `saas-entitlements-and-plan-gating` for the catalogue. |
| skills/ai/ai-evaluation/SKILL.md | name: ai-evaluation | description: Use when setting up quality assurance for AI features — defining evaluation criteria, measuring output quality, using AI-as-judge, monitoring production AI, detecting drift, and building user feedback loops |
| skills/ai/ai-feature-rollout-and-experimentation/SKILL.md | name: ai-feature-rollout-and-experimentation | description: Use when rolling out AI features safely in a multi-tenant SaaS — feature flags scoped per tenant/user, percentage rollouts gated by eval and SLO budget, canary cohorts, A/B testing of prompts/models, automatic rollback on quality regression, tenant-level opt-out and consent, and shadow-mode for risky changes. |
| skills/ai/ai-feature-spec/SKILL.md | name: ai-feature-spec | description: Design a single AI-powered feature end-to-end — model selection, prompt engineering, context window, output schema, fallback behaviour, human oversight, and UX integration. Invoke for each opportunity identified in ai-opportunity-canvas. |
| skills/ai/ai-incident-response/SKILL.md | name: ai-incident-response | description: >- Use when preventing, detecting, triaging, communicating, recovering from, or reviewing AI incidents, AI errors, RCA, and postmortems. |
| skills/ai/ai-llm-integration/SKILL.md | name: ai-llm-integration | description: Integrate LLMs into any application — OpenAI, Anthropic Codex, DeepSeek, and Gemini APIs directly (no framework required), streaming responses, function calling/tool use, embeddings and semantic search, multi-model routing, prompt caching, rate... |
| skills/ai/ai-model-gateway/SKILL.md | name: ai-model-gateway | description: Use when designing or building the LLM gateway — the single outbound surface from the SaaS to all LLM providers. Covers provider abstraction, model selection per tenant tier, fallback chains, retries, per-tenant rate limiting and token caps, request signing, audit logging, regional routing for data residency, cost capture at write time, kill-switch enforcement, and the SDK/HTTP contract feature teams consume. |
| skills/ai/ai-observability-and-debugging/SKILL.md | name: ai-observability-and-debugging | description: Use when building the observability stack for AI features in a multi-tenant SaaS — prompt/response tracing, semantic logging, replay tooling, "show me why this answer", per-stage latency/cost breakdown, ticket→trace tie-back, and dashboards that answer the operational questions (which tenant, which feature, which prompt version, which model). |
| skills/ai/ai-opportunity-canvas/SKILL.md | name: ai-opportunity-canvas | description: Systematically discover and rank AI use cases for any software project or module. Produces a prioritised AI Opportunity Register with business impact, implementation effort, and cost estimates. Invoke after any project description or module... |
| skills/ai/ai-prompt-engineering/SKILL.md | name: ai-prompt-engineering | description: Use when writing, refining, or structuring prompts for AI-powered app features — system prompts, user prompt templates, few-shot examples, chain-of-thought, prompt versioning, and defensive prompting |
| skills/ai/ai-rag-patterns/SKILL.md | name: ai-rag-patterns | description: Use when building features that answer questions from private data, documents, policies, or time-sensitive information — RAG architecture, chunking strategies, hybrid search, re-ranking, vector databases, evaluation, agentic RAG, multimodal RAG... |
| skills/ai/ai-security/SKILL.md | name: ai-security | description: Use when securing an AI/LLM-powered feature against prompt injection, cross-tenant data leakage and tenant isolation failures, jailbreaks, and adversarial inputs. Covers PII scrubbing before model calls, output validation, rate limiting, audit logging, and DPPA/GDPR compliance for AI data flows. |
| skills/ai/ai-web-apps/SKILL.md | name: ai-web-apps | description: Use when designing or building an AI-enhanced web app (Next.js + Vercel AI SDK, MCP tools, multi-provider chat/RAG) — produces the module gate, token-ledger + budget schema, provider abstraction, and output guardrails. Specialises the integration patterns in `ai-architecture-patterns` for a web-app runtime; hand off metering depth to `ai-metering-billing` and prompt/threat depth to `ai-security` / `llm-security`. |
| skills/ai/openai-agents-sdk/SKILL.md | name: openai-agents-sdk | description: Build production AI agents with the OpenAI Agents SDK (Python) — 6 core primitives (Agent, Runner, Tools, Handoff, Guardrails, Tracing), multi-agent patterns (Centralized, Hierarchical, Decentralized, Swarm), dynamic/deterministic orchestration... |
| skills/android/android-data-persistence/SKILL.md | name: android-data-persistence | description: Android data persistence standards with Room as primary local storage and custom API backends for cloud sync. Covers SharedPreferences, DataStore, Room (entities, DAOs, relations, migrations), file storage, offline-first architecture, and... |
| skills/android/android-development/SKILL.md | name: android-development | description: Android development standards for AI agent implementation. Kotlin-first, Jetpack Compose UI, MVVM + Clean Architecture, Hilt DI, comprehensive security, testing, and performance patterns. Use when building or reviewing Android applications... |
| skills/android/android-tdd/SKILL.md | name: android-tdd | description: Android Test-Driven Development standards. Enforces Red-Green-Refactor cycle, test pyramid (70/20/10), layer-specific testing strategies, and CI integration. Use when building or reviewing Android apps with TDD methodology. |
| skills/architecture/api-design-first/SKILL.md | name: api-design-first | description: Use when designing or building HTTP APIs — spec-first OpenAPI workflow, REST conventions, versioning, auth model, rate limiting, idempotency keys, error envelope, and observability notes. Produces the OpenAPI contract plus error/auth/idempotency/observability artifacts that frontend, mobile, security, and reliability skills consume. For endpoint-level security review load `vibe-security-skill`; for GraphQL-specific hardening load `graphql-patterns`. |
| skills/architecture/distributed-systems-patterns/SKILL.md | name: distributed-systems-patterns | description: Use when designing or reviewing multi-service, message-driven, or eventually consistent systems. Covers service boundaries, consistency tradeoffs, event workflows, outbox and inbox patterns, sagas, ordering, and idempotency. |
| skills/architecture/ecommerce-platform-audit-requirements/SKILL.md | name: ecommerce-platform-audit-requirements | description: Use when scoping or specifying an e-commerce platform, payment, API, security, AI, data protection, integration, and remediation audit for SMEs or cross-border digital trade programmes. |
| skills/architecture/graphql-patterns/SKILL.md | name: graphql-patterns | description: Use when designing, building, or operating GraphQL APIs with Apollo Server + TypeScript — covers schema-first SDL design, resolver architecture, DataLoader, JWT and directive-based authz, Relay cursor pagination, typed error payloads, federation v2, graphql-codegen, and production hardening (depth/complexity limits, timeouts, persisted queries). Load references/graphql-security.md for hostile-input defence. |
| skills/architecture/microservices-architecture/SKILL.md | name: microservices-architecture | description: Use when designing, reviewing, or refactoring microservice boundaries, communication, service ownership, deployment independence, resilience, and distributed data flows. Load absorbed microservices fundamentals, models, communication, and resilience references as needed. |
| skills/architecture/system-architecture-design/SKILL.md | name: system-architecture-design | description: Use when defining or reviewing software architecture for web apps, mobile backends, SaaS platforms, APIs, distributed systems, or major features. Covers bounded contexts, module decomposition, contracts, failure handling, ADRs, and scalability tradeoffs. |
| skills/architecture/validation-contract/SKILL.md | name: validation-contract | description: Use when authoring or normalising a specialist skill, or preparing to ship a feature or release — defines the seven evidence categories every specialist skill must declare against and provides the canonical Release Evidence Bundle template. The contract spine that turns scattered validation skills into a coherent ship-readiness check. |
| skills/backend-databases/database-design-engineering/SKILL.md | name: database-design-engineering | description: Use when designing or reviewing relational or document-backed data architecture for SaaS platforms, ERP systems, APIs, analytics stores, or mobile sync. Covers domain modeling, tenancy, indexing, migrations, integrity, retention, and performance tradeoffs. |
| skills/backend-databases/database-reliability/SKILL.md | name: database-reliability | description: 'Database reliability engineering: SLI/SLO design and error-budget policy for the data tier, blameless postmortems, escalation tiers and on-call hand-off, game days for MySQL/PostgreSQL, operational runbooks, change management, capacity planning, and backup verification. Use when setting up production database SRE practice, defining database SLOs/error budgets, running database postmortems, or hardening on-call for MySQL/PostgreSQL.' |
| skills/backend-databases/mysql-engineering/SKILL.md | name: mysql-engineering | description: Use when designing, implementing, or reviewing MySQL application schemas, SQL, indexes, constraints, stored routines, and production query patterns. Load absorbed MySQL best-practice, data-modeling, and advanced-SQL reference files as needed. |
| skills/backend-databases/mysql-operations/SKILL.md | name: mysql-operations | description: Use when administering, tuning, backing up, restoring, monitoring, or troubleshooting MySQL production systems. Load absorbed MySQL administration and query-performance reference files for operational runbooks, indexes, replication, and incident response. |
| skills/backend-databases/postgresql-engineering/SKILL.md | name: postgresql-engineering | description: Use when designing, implementing, or reviewing PostgreSQL application data models, SQL, indexes, constraints, extensions, server-side routines, and production query patterns. Load the absorbed PostgreSQL reference files for fundamentals, advanced SQL, schema patterns, and server programming. |
| skills/backend-databases/postgresql-operations/SKILL.md | name: postgresql-operations | description: Use when administering, tuning, backing up, restoring, monitoring, or troubleshooting PostgreSQL production systems. Load the absorbed PostgreSQL administration and performance reference files for operational runbooks, query tuning, vacuum, replication, and incident response. |
| skills/devops-cloud/cicd-pipelines/SKILL.md | name: cicd-pipelines | description: Use when designing or implementing a CI/CD pipeline — stage gates, GitHub Actions production patterns (matrix, reusable workflows, environments), OIDC federation to AWS/GCP/Vault, dependency and Docker-layer caching, fan-out/fan-in orchestration, blue/green and canary deployment, pipeline observability (DORA metrics, queue time), and choosing between GitHub Actions and GitLab CI. |
| skills/devops-cloud/cloud-architecture/SKILL.md | name: cloud-architecture | description: Use when designing cloud deployments, Dockerising applications, laying out AWS or GCP environments, choosing a deployment pattern, or moving a workload from a single VM to a resilient multi-AZ topology. |
| skills/devops-cloud/deployment-release-engineering/SKILL.md | name: deployment-release-engineering | description: Use when designing or reviewing deployment pipelines, rollout strategies, release gates, rollback plans, migration-safe releases, and post-deploy verification for production systems. Covers build promotion, environment strategy, release evidence, and operational safety. |
| skills/devops-cloud/docker-development/SKILL.md | name: docker-development | description: Docker and Docker Compose standards for PHP, Python, JavaScript, and API services. Use when containerizing development environments, production images, CI builds, PHP-FPM/Nginx stacks, Python sidecars, Node/JS services, or multi-service SaaS deployments. |
| skills/devops-cloud/infrastructure-as-code/SKILL.md | name: infrastructure-as-code | description: Use when provisioning or changing cloud infrastructure with Terraform or Ansible — modules, remote state with S3 native locking, workspaces vs directory-per-env, common AWS patterns, idempotent Ansible roles for Debian/Ubuntu, GitOps with ArgoCD/Flux, drift detection, and Vault secret injection. |
| skills/devops-cloud/kubernetes-platform/SKILL.md | name: kubernetes-platform | description: Use when running Kubernetes as a platform team — bootstrapping self-managed clusters on Debian/Ubuntu, designing multi-tenant RBAC, enforcing Pod Security and resource quotas, and operating cluster lifecycle (upgrades, certs, etcd, ingress, cert-manager, metrics-server). Self-managed first, cloud-managed second. |
| skills/devops-cloud/observability-monitoring/SKILL.md | name: observability-monitoring | description: Use when designing or reviewing logs, metrics, traces, alerts, SLOs, dashboards, audit events, or production telemetry for web apps, APIs, SaaS platforms, mobile backends, and AI systems. Covers instrumentation strategy, diagnosis-first telemetry, alert quality, and operational visibility. |
| skills/devops-cloud/reliability-engineering/SKILL.md | name: reliability-engineering | description: Use when designing or reviewing production reliability for APIs, SaaS platforms, background jobs, distributed workflows, mobile backends, or AI-enabled systems. Covers timeout and retry policy, degradation, queue safety, incident readiness, and recovery-aware design. |
| skills/finance-accounting/accounting-engine/SKILL.md | name: accounting-engine | description: Use when designing, implementing, or reviewing an embedded accounting engine inside a SaaS, ERP, POS, inventory, payroll, school, clinic, NGO, marketplace, or mobile-money-heavy system. Covers one append-only general ledger, one LedgerPostingService write path, mapping-layer account resolution, IFRS/IFRS for SMEs defaults, subledger tagging, idempotent posting, reversing journals, period locks, audit trails, report projections, and accounting integrity tests. |
| skills/finance-accounting/accounting-finance-controller/SKILL.md | name: accounting-finance-controller | description: Use for accounting, bookkeeping, ERP finance, POS, inventory, payroll, billing, financial reporting, IFRS-aware workflows, management accounting, cost accounting, budgeting, valuation, controls, reconciliations, and finance-system design. Produces controller-grade requirements, implementation guidance, review findings, and financial logic so business software can replace QuickBooks/Tally-class workflows where appropriate. |
| skills/finance-accounting/multicurrency-and-fx/SKILL.md | name: multicurrency-and-fx | description: >- Use when implementing IAS 21 multicurrency accounting: functional currency, presentation currency, transaction currency, exchange-rate tables, settlement, realised and unrealised forex gains or losses, revaluation, and currency-safe ledger design. |
| skills/frontend-ux/avalonia-desktop-development/SKILL.md | name: avalonia-desktop-development | description: Building cross-platform .NET desktop apps with Avalonia UI (Windows/macOS/Linux). Use when working with Avalonia, AXAML/XAML UI, MVVM in Avalonia (CommunityToolkit.Mvvm or ReactiveUI), compiled bindings (x:DataType), styling/control themes/Fluent theming, data binding, DataTemplates and virtualization for large lists, asset/PNG image bundling (avares://), localization, accessibility, hosting a WebView (WebView2/WKWebView) in Avalonia, headless testing, or packaging an Avalonia app for Windows and macOS. |
| skills/frontend-ux/frontend-performance/SKILL.md | name: frontend-performance | description: Use when defining, implementing, or auditing frontend performance for web apps and SaaS frontends — produces a performance budget per critical flow, a measurement plan tied to SLOs, and a regression gate for CI. Covers Core Web Vitals (LCP, INP, CLS), loading, rendering, and framework-specific recipes. Not for backend latency, API shape (see api-design-first), or server SLOs (see observability-monitoring). |
| skills/frontend-ux/image-compression/SKILL.md | name: image-compression | description: Client-side image compression before upload using Squoosh with Canvas fallback and server-side Sharp validation. Use for web apps needing max width 1920px, max size 512KB, transparent UX, and consistent compression stats. |
| skills/frontend-ux/nextjs-app-router/SKILL.md | name: nextjs-app-router | description: 'Next.js App Router patterns for production — server/client components, parallel routes, advanced middleware, RBAC three-tier, Redis caching, background jobs (BullMQ), data fetching, auth, deployment, CI/CD. Sources: Rambert (Advanced Next.js)...' |
| skills/frontend-ux/react-development/SKILL.md | name: react-development | description: 'Comprehensive React patterns and best practices: functional components, all hooks (useState, useEffect, useCallback, useMemo, useRef, useContext, useReducer), custom hooks, state management (local/Context/external), performance optimisation...' |
| skills/frontend-ux/tailwind-css/SKILL.md | name: tailwind-css | description: Tailwind CSS v3 utility-first styling — setup, responsive design, dark mode, event/state modifiers, tailwind.config.js customization (colors, spacing, screens, plugins), @apply and @layer directives, flexbox/grid classes, and best practices. Use... |
| skills/frontend-ux/ux-content-strategy/SKILL.md | name: ux-content-strategy | description: Use when planning, governing, or upgrading product content as a system - voice charts, content-first design, UI text patterns, form completion gates, error taxonomy, content measurement, decision communication, lifecycle narrative, and content operations. Higher-level orchestration above tactical microcopy and form mechanics. |
| skills/gis/gis-enterprise-domain/SKILL.md | name: gis-enterprise-domain | description: Use when administering ArcGIS Enterprise or building real-estate-specific GIS features — ArcGIS components, publishing services, security/roles, backup/DR, plus property search, neighbourhood analysis, catchment/isochrones, market heatmaps, and real-estate-SaaS integration. |
| skills/gis/gis-platform-engineering/SKILL.md | name: gis-platform-engineering | description: Use when implementing GIS maps, spatial data services, maps integrations, geocoding, spatial APIs, or PostGIS-backed geospatial platforms. Load absorbed GIS mapping, maps integration, and PostGIS backend references as needed. |
| skills/ios/ios-ai-ml/SKILL.md | name: ios-ai-ml | description: iOS AI/ML standards for WWDC26 Apple intelligence work, including Foundation Models, Language Model providers, Dynamic Profiles, Core AI, Evaluations, Core ML, Vision, NaturalLanguage, Speech, SoundAnalysis, and privacy-first on-device inference. |
| skills/ios/ios-architecture/SKILL.md | name: ios-architecture | description: iOS architecture orchestration for production apps, modular codebases, Swift patterns, App Intents, Foundation Models/Core AI provider boundaries, scale practices, and release-ready implementation boundaries. |
| skills/ios/ios-data-persistence/SKILL.md | name: ios-data-persistence | description: iOS data persistence standards with SwiftData, Keychain, files, offline sync, Core Spotlight semantic indexing, App Entity data exposure, and AI cache/privacy boundaries. |
| skills/ios/ios-development/SKILL.md | name: ios-development | description: iOS development standards for AI agent implementation. Swift-first, SwiftUI, MVVM + Clean Architecture, async/await, comprehensive security, testing, and performance patterns. Use when building or reviewing iOS applications, generating Swift... |
| skills/ios/ios-monetization/SKILL.md | name: ios-monetization | description: StoreKit 2 in-app purchases, subscriptions, App Store Server API, group and organization subscription watch items, Unity StoreKit plugin routing, paywall UI, transaction verification, and App Store Connect configuration. |
| skills/ios/ios-platform-capabilities/SKILL.md | name: ios-platform-capabilities | description: iOS platform capability orchestration for App Intents, Siri, Spotlight semantic indexing, widgets, biometrics, Bluetooth printing, push notifications, native PDF export, networking, media, and Apple framework entitlements. |
| skills/ios/ios-quality-and-release/SKILL.md | name: ios-quality-and-release | description: iOS quality and release orchestration for Swift Testing 6.4, Device Hub, Xcode 27 agents, Xcode Cloud, AI Evaluations, Instruments, TestFlight, App Store review, stability, and release evidence. |
| skills/ios/ios-security-and-rbac/SKILL.md | name: ios-security-and-rbac | description: iOS security and authorization orchestration for Keychain, Secure Enclave, App Attest, Trust Insights watch items, privacy manifests, agentic AI, App Intents, tamper resistance, permissions, RBAC, and tenant-safe mobile access. |
| skills/languages/csharp-dotnet-development/SKILL.md | name: csharp-dotnet-development | description: Use when building, reviewing, modernizing, or debugging C# and .NET applications across .NET 8/9/10, C# 12/13/14, ASP.NET Core APIs, EF Core data access, background services, concurrency, .NET MAUI, Azure-integrated services, testing, packaging, or .NET AI integration. Covers project structure, language idioms, runtime choices, secure service design, performance, observability, and release readiness. |
| skills/languages/javascript-modern/SKILL.md | name: javascript-modern | description: 'Modern JavaScript (ES6+) patterns for PHP+JavaScript SaaS apps: modules, async/await, destructuring, Proxy/Reflect, generators, WeakMap/WeakSet, optional chaining, error handling, and performance patterns. Use when writing JavaScript for web...' |
| skills/languages/nodejs-development/SKILL.md | name: nodejs-development | description: Production Node.js development — async patterns, streams, design patterns, HTTP APIs, testing, scaling, and deployment. Synthesised from Node.js Design Patterns (Casciaro & Mammino 3rd ed.), Node.js Recipes (Gackenheimer), Fullstack Node.js (Murray), and Node.js Fundamentals. Use when building scalable servers, REST APIs, CLI tools, real-time systems, or fullstack JavaScript applications. |
| skills/languages/php-modern-standards/SKILL.md | name: php-modern-standards | description: Modern PHP development standards for maintainable, testable, object-oriented code. Use when writing PHP 8+ applications, implementing OOP patterns, ensuring security, following PSR standards, optimizing performance, or building Laravel... |
| skills/languages/python-data-analytics/SKILL.md | name: python-data-analytics | description: Use when computing complex analytics, KPIs, cohort/funnel/retention metrics, financial math (IRR/NPV/amortization), statistical tests, anomaly detection, or geospatial analytics in Python — for cases where SQL alone gets unwieldy. |
| skills/languages/python-data-pipelines/SKILL.md | name: python-data-pipelines | description: Use when building ETL jobs, document intelligence pipelines, OCR, PDF/Excel ingestion, image/media processing, or external-API sync pipelines in Python — idempotent scheduled jobs with validation, dead-letter queues, and multi-tenant isolation. |
| skills/languages/python-ml-predictive/SKILL.md | name: python-ml-predictive | description: Use when adding forecasting, classification, regression, or anomaly detection to a SaaS feature — demand/sales/cash-flow forecasting, churn and risk scoring, anomaly detection — with scikit-learn, Prophet, and statsmodels. Covers data prep, model serving, monitoring, and explainability. |
| skills/languages/python-modern-standards/SKILL.md | name: python-modern-standards | description: Use when writing or reviewing any Python code in our SaaS projects — defines Python version, project layout, tooling (uv, ruff, mypy), typing, Pydantic v2, logging, configuration, async rules, error handling, testing, and security baseline. Load this before any other Python skill. |
| skills/languages/typescript-effective/SKILL.md | name: typescript-effective | description: Use when writing production TypeScript — clean code idioms, effective-TS items, strict tsconfig, migration from JS, build performance, testing, and anti-patterns. Load references/typescript-mastery.md for type-system depth and references/typescript-design-patterns.md for GoF patterns. |
| skills/languages/typescript-full-stack/SKILL.md | name: typescript-full-stack | description: Use when building end-to-end TypeScript applications — Node backend (Fastify), React/Next frontend, shared types via tRPC or Zod, monorepo with turborepo/nx, Prisma/Drizzle data layer, end-to-end type safety. |
| skills/mobile-cross/kmp-development/SKILL.md | name: kmp-development | description: Kotlin Multiplatform shared module development standards for sharing business logic across Android and iOS while keeping native UI. Covers project structure (shared/composeApp/iosApp), source sets, targets, expect/actual, DI (Koin)... |
| skills/mobile-cross/mobile-platform-operations/SKILL.md | name: mobile-platform-operations | description: Cross-platform mobile operations orchestration for app icons, mobile RBAC, SaaS planning, Play Store review, Apple Xcode 27/TestFlight/Xcode Cloud evidence, and operational mobile delivery assets. |
| skills/mobile-cross/pwa-offline-first/SKILL.md | name: pwa-offline-first | description: Use when building offline-first Progressive Web Apps — Service Worker lifecycle, Workbox caching strategies, IndexedDB via Dexie.js, Background Sync for queued writes, Web Push notifications, Lighthouse gates, and Next.js PWA integration. Default for apps that must work on EDGE/2G or intermittent connectivity. |
| skills/product-business/bds-intake-and-monitoring-system-spec/SKILL.md | name: bds-intake-and-monitoring-system-spec | description: Use when specifying application intake, eligibility screening, selection scoring, beneficiary registers, diagnostics tracking, expert deployment, monitoring dashboards, RBAC, audit trails, and donor reporting for BDS programmes. |
| skills/product-business/consulting-delivery-control-room/SKILL.md | name: consulting-delivery-control-room | description: Use when coordinating multi-workstream consulting bids or delivery programmes with deadlines, owners, RACI, RAID, deliverables registers, decision logs, quality gates, and client/donor reporting cadence. |
| skills/product-business/content-writing/SKILL.md | name: content-writing | description: Copywriting and content creation standards for website pages, blog posts, and all written copy. Covers headlines, ledes, readability, niche vocabulary, scannable formatting, and persuasive structure. Cross-cutting skill — apply whenever... |
| skills/product-business/customer-service-excellence/SKILL.md | name: customer-service-excellence | description: Use when handling a customer service interaction (especially recovery, escalation, or public complaint), drafting service language (apology, empathy, ownership, escalation, confirmation), measuring service quality, aligning frontline empowerment with escalation paths, or designing a service-failure prevention loop. Encodes the recovery-and-retention loop, difficult-interaction frameworks, and CX-EX alignment rules. |
| skills/product-business/document-spreadsheet-tooling-readiness/SKILL.md | name: document-spreadsheet-tooling-readiness | description: Check whether this machine can generate and validate Word, PDF, Excel, DOCX, XLSX, spreadsheet, workbook, application register, scoring matrix, price schedule, budget, dashboard, report, proposal, or annex files before promising them. |
| skills/product-business/excel-spreadsheets/SKILL.md | name: excel-spreadsheets | description: 'Generate world-class, professionally designed Microsoft Excel spreadsheets and handle all Excel/spreadsheet workflows. Use when: generating .xlsx files from apps or scripts (openpyxl, xlsxwriter, PhpSpreadsheet, pandas), importing or parsing...' |
| skills/product-business/it-proposal-writing/SKILL.md | name: it-proposal-writing | description: Framework for writing persuasive IT project proposals that win work. Covers Basis of Decision (BOD), Unique Selling Points (USP), proposal strategy, document structure, persuasive prose techniques, the 5-level destruction model, grammar rules... |
| skills/product-business/premium-software-product-execution/SKILL.md | name: premium-software-product-execution | description: Use when designing, building, pricing, packaging, or reviewing premium software products, SaaS systems, ERP/POS tools, dashboards, websites, or agency-built applications for executive, enterprise, affluent, high-ticket, or elite buyers. Converts premium marketing, selling, product, UX, pricing, proof, onboarding, and delivery principles into concrete software requirements and quality gates. |
| skills/product-business/product-discovery/SKILL.md | name: product-discovery | description: Structured product discovery before building. Covers the four product risks, opportunity assessment, customer discovery, prototype selection, discovery sprints, and evidence-based build / pivot / kill decisions. Use when evaluating whether a product, feature, or workflow deserves delivery investment. |
| skills/product-business/product-led-growth/SKILL.md | name: product-led-growth | description: Use when designing PLG motions for a SaaS product — freemium tiers, PQL definition, activation flows with time-to-value targets, in-app upgrade prompts, viral loops, NPS surveys, feature flags for gradual rollout, and PostHog-based product analytics for funnel and cohort tracking. |
| skills/product-business/product-strategy-vision/SKILL.md | name: product-strategy-vision | description: Frameworks for defining a compelling product vision and a focused product strategy. Covers the 10 principles of product vision, product strategy principles, OKR technique for product teams, outcome-based roadmaps, product principles, and product... |
| skills/product-business/professional-word-output/SKILL.md | name: professional-word-output | description: 'Generate world-class, professionally designed Microsoft Word (.docx) documents that look like a designer and communications specialist worked on them together — not AI output. Use when producing any .docx file: reports, proposals, manuals...' |
| skills/product-business/software-business-models/SKILL.md | name: software-business-models | description: Business model frameworks for software companies. Covers products vs services vs hybrid models, platform business models, subscription vs perpetual licensing, open source strategies, the services-to-product transition, and startup survival... |
| skills/product-business/software-pricing-strategy/SKILL.md | name: software-pricing-strategy | description: Pricing strategy for software products and SaaS. Covers value-based pricing, the 3 pricing principles, B2B vs B2C differences, pricing models (per-seat, usage, freemium, tiered, flat-rate), packaging strategy, negotiation frameworks, discounting... |
| skills/saas/modular-saas-architecture/SKILL.md | name: modular-saas-architecture | description: Build SAAS platforms with pluggable business modules (Advanced Inventory, Restaurant, Pharmacy, etc.) that can be enabled/disabled per tenant without breaking the system. Use when designing modular SAAS features, implementing module toggles... |
| skills/saas/multi-tenant-saas-architecture/SKILL.md | name: multi-tenant-saas-architecture | description: Use when designing or reviewing a multi-tenant SaaS platform — tenant isolation model, three-panel separation (super admin, franchise admin, end user), zero-trust enforcement, audit trails, and per-tenant permission overrides. Unlike `modular-saas-architecture` which focuses on pluggable business modules, this skill defines the tenancy and auth boundaries that every module inherits. |
| skills/saas/saas-accounting-system/SKILL.md | name: saas-accounting-system | description: Implement a complete double-entry accounting system inside any SaaS app. Users enter transactions naturally (sales, expenses, inventory) while the system auto-posts journal entries under the hood. Produces both user-friendly reports and technical... |
| skills/saas/saas-admin-backoffice-tooling/SKILL.md | name: saas-admin-backoffice-tooling | description: Use when designing the internal admin / back-office console of a multi-tenant SaaS — tenant impersonation (audited, time-boxed), tenant lifecycle controls (suspend/restore/archive/hard-delete), billing operations (refunds, credits, plan overrides), feature-flag overrides per tenant, bulk actions (mass invite, plan migration, region migration), and the audit-log spine that backs all of it. Distinct from the customer-facing super-admin panel in `multi-tenant-saas-architecture`. |
| skills/saas/saas-architecture-strategy/SKILL.md | name: saas-architecture-strategy | description: Use when architecting or evaluating a cloud SaaS product — including choosing multi-tenant patterns, mapping deployment to IaaS, planning scaling and blast-radius isolation, aligning architecture to business capabilities, and reconciling multi-enterprise consumption requirements with operating-model constraints. |
| skills/saas/saas-business-metrics/SKILL.md | name: saas-business-metrics | description: Complete SaaS metrics framework covering revenue (MRR/ARR/ARPU), growth (CAC/LTV/payback), retention (churn/NRR/GRR), engagement, customer satisfaction (NPS/CSAT/CES), unit economics, the Rule of 40, and SaaS finance basics. Use when measuring... |
| skills/saas/saas-entitlements-and-plan-gating/SKILL.md | name: saas-entitlements-and-plan-gating | description: Use when designing the entitlements engine that enforces what each plan/tier/tenant can do — feature flags vs entitlements distinction, limits enforcement (seats, API calls, storage, projects, AI tokens), gate placement (UI, API, worker), upgrade-discovery UX, override mechanisms for enterprise contracts, and the runtime that resolves "can this tenant do X right now?" in a few milliseconds. |
| skills/saas/saas-erp-system-design/SKILL.md | name: saas-erp-system-design | description: Use when designing configurable SaaS or ERP platforms with multi-step business workflows, domain modules, approvals, auditability, pricing and entitlements, operational reporting, and tenant-specific variation. Covers domain boundaries, workflow states, extension points, and control design. |
| skills/saas/saas-lifecycle-email-orchestration/SKILL.md | name: saas-lifecycle-email-orchestration | description: Use when designing the six core lifecycle email sequences (welcome/onboarding, behavioral/feature-discovery, upgrade/upsell, retention, reactivation, referral) — trigger contracts, branched automation, suppression rules, PQL/churn-risk triggers, and revenue attribution. Built on top of `saas-transactional-email-infrastructure`. Distinct from `tabler-email-templates` (HTML) and `subscription-billing` (raw billing events). |
| skills/saas/saas-rate-limiting-and-quotas/SKILL.md | name: saas-rate-limiting-and-quotas | description: Use when designing per-tenant rate limits and quotas — algorithm choice (token bucket, sliding window, leaky bucket, fixed window), where to enforce (edge, gateway, service, DB connection pool, queue), per-plan / per-tier limits, soft vs hard caps, fair-queueing for noisy neighbors, headers and error responses, and how to expose quota usage to the tenant. |
| skills/saas/saas-sales-organization/SKILL.md | name: saas-sales-organization | description: Use when designing or scaling a SaaS sales organisation — sales motions, roles (SDR/BDR/AE/CSM/SE), pipeline stages, lead-to-cash, territory design, quota/commission, sales ops fundamentals, onboarding/ramp, and hiring rubrics. Sourced from "Blueprints for a SaaS Sales Organization" (van der Kooij, Pizarro). |
| skills/saas/saas-seeder/SKILL.md | name: saas-seeder | description: 'Bootstrap a new SaaS from the SaaS Seeder Template: setup database, configure environment, create super admin user, and verify three-tier panel structure. Use when initializing a new multi-tenant SaaS project from this template.' |
| skills/saas/saas-sso-scim-enterprise-auth/SKILL.md | name: saas-sso-scim-enterprise-auth | description: Use when implementing enterprise auth on a multi-tenant SaaS — SAML 2.0 and OIDC SSO with per-tenant IdP configuration, SCIM 2.0 user provisioning/deprovisioning, custom-domain support with automated TLS, IP allowlists per tenant, audit-log API, and the migration from email-password tenants to IdP-enforced tenants. The price of entry for enterprise SaaS. |
| skills/saas/saas-tenant-data-portability-and-erasure/SKILL.md | name: saas-tenant-data-portability-and-erasure | description: Use when designing the GDPR/POPIA/CCPA-compliant data export (right to portability) and erasure (right to be forgotten) workflows for a multi-tenant SaaS — cascade through every data store including warehouse/backups, retention policy, requester verification, audit trail, multi-tenant nuances of erasing one tenant's data without affecting others, and the engineering for African market regulations (Uganda DPPA, Kenya DPA, POPIA). |
| skills/saas/stripe-payments/SKILL.md | name: stripe-payments | description: Use when integrating Stripe one-time payments, PaymentIntents, SetupIntents, Checkout, and webhook-driven flows in PHP or Node.js. Covers integration-model selection, SCA / 3D Secure handling, multi-currency, Stripe Tax basics, idempotency, and signed-webhook receivers. Recurring subscriptions, dunning, and metered billing live in subscription-billing. |
| skills/saas/subscription-billing/SKILL.md | name: subscription-billing | description: Use when designing or reviewing recurring subscription lifecycle on Stripe Billing — plans/Prices, trials, proration, upgrades/downgrades, cancel/pause, Smart Retries dunning, metered usage, automatic tax, multi-currency, and the strategy choice between subscription vs perpetual and monthly vs annual. |
| skills/sdlc-meta/advanced-testing-strategy/SKILL.md | name: advanced-testing-strategy | description: Use when designing or reviewing test strategy for production systems, APIs, mobile apps, SaaS platforms, ERP workflows, and AI-enabled systems. Covers unit, integration, contract, end-to-end, regression, release-gate, and risk-based testing decisions. |
| skills/sdlc-meta/ai-assisted-development/SKILL.md | name: ai-assisted-development | description: Orchestrate AI coding agents, human reviewers, CI, and delivery workflows for professional software work. Use when coordinating AI-assisted planning, implementation, code review, modernization, documentation, or multi-agent development. |
| skills/sdlc-meta/ai-slop-audit/SKILL.md | name: ai-slop-audit | description: Analyse, evaluate, and audit any artefact for AI slop and score it. Runs after EACH major iteration of work and AUTO-RUNS whenever the user asks to analyse, review, evaluate, audit, critique, or de-slop any project, app, website, business plan, SRS or spec, proposal, blog post, social post, document, image, or codebase, or asks whether something looks AI-generated. Produces a graded slop report giving per-marker findings with severity, evidence, and a concrete fix. Pairs with anti-ai-slop, which prevents slop during production. |
| skills/sdlc-meta/anti-ai-slop/SKILL.md | name: anti-ai-slop | description: NON-NEGOTIABLE real-time guardrail. Apply on EVERY generated output (text, document, UI, code, image brief, social post) continuously as you generate AND before it is delivered, so the output cannot be recognised as "AI slop". Carries the verified definition, the seven universal slop markers each paired with an avoidance rule, the banned-vocabulary list, and a ship-gate checklist. Load first; it overrides stylistic preferences. |
| skills/sdlc-meta/doc-architect/SKILL.md | name: doc-architect | description: Generate Triple-Layer AGENTS.md documentation by scanning a project for its tech stack, data directory, and planning directory. Use when the user asks to standardize project documentation, generate agent files, or create AGENTS.md guides. |
| skills/sdlc-meta/git-collaboration-workflow/SKILL.md | name: git-collaboration-workflow | description: Use when planning branch strategy, making commits, reviewing diffs, resolving conflicts, preparing pull requests, or shipping releases. Covers trunk-friendly collaboration, commit hygiene, conflict recovery, and CI-linked release discipline. |
| skills/sdlc-meta/implementation-status-auditor/SKILL.md | name: implementation-status-auditor | description: Conduct a comprehensive implementation status audit of any software project. Produces structured documentation in docs/implementation/review-{date}/ with gap analysis, schema audit, integration status, completion blueprint, and prioritized action... |
| skills/sdlc-meta/markdown-lint-cleanup/SKILL.md | name: markdown-lint-cleanup | description: Fix markdown lint warnings by enforcing headings, blank lines around lists, and language-tagged code fences for clean documentation. |
| skills/sdlc-meta/project-requirements/SKILL.md | name: project-requirements | description: Guided interview to create comprehensive project requirements documentation (requirements.md, business-rules.md, user-types.md, workflows.md) for a new SaaS project. Use before bootstrapping the SaaS Seeder Template. |
| skills/sdlc-meta/sdlc-documentation/SKILL.md | name: sdlc-documentation | description: Use when producing, reviewing, or consolidating SDLC documentation across planning, requirements, design, testing, deployment, user rollout, post-deployment, and maintenance phases. Load absorbed SDLC phase references as needed. |
| skills/sdlc-meta/skill-composition-standards/SKILL.md | name: skill-composition-standards | description: Use when authoring a new skill, normalising an older skill, or reviewing a skill PR — defines the repository-wide house style (frontmatter, decision rules, anti-patterns, references), the output contracts each baseline-skill type must produce, and the input contracts each specialist skill must declare. This is the enforcement spine that makes the repository compose as a system, not a library of linked documents. |
| skills/sdlc-meta/skill-engine-audit/SKILL.md | name: skill-engine-audit | description: Audit a whole skills engine (a repo of routed SKILL.md files such as design-system-skills, chwezi-accounting-doctrine, srs-skills, business-plan-skills, social-media-skills, linux-skills, digital-research-engine) against a world-class bar. Ranks EVERY aspect out of 100 — taxonomy, doctrine, skill depth, worked examples, standards currency, coverage, redundancy, discovery/routing, safety — plus per-output-type readiness (web, iOS, Android, web apps, cross-platform, websites, documents, presentations, brand, data products). Produces a comprehensive multi-file report with a strict scorecard and a prioritized roadmap. Use when asked to audit, grade, benchmark, or find gaps in a skills engine/catalog and plan how to make it world-class. |
| skills/sdlc-meta/skill-safety-audit/SKILL.md | name: skill-safety-audit | description: Scan new or updated skills for unsafe or malicious instructions (unknown tools, external installers, credential harvesting) before accepting them into the repository. |
| skills/sdlc-meta/skill-writing/SKILL.md | name: skill-writing | description: Use when creating or upgrading skills in this repository. Covers repository-specific frontmatter rules, progressive disclosure, reference-file strategy, validation, and the quality bar required for production-grade engineering skills. |
| skills/sdlc-meta/update-claude-documentation/SKILL.md | name: update-Codex-documentation | description: Update project documentation files (README.md, PROJECT_BRIEF.md, TECH_STACK.md, ARCHITECTURE.md, docs/API.md, docs/DATABASE.md, AGENTS.md, docs/plans/NEXT_FEATURES.md) when significant changes occur. MANDATORY at end of each work session to... |
| skills/sdlc-meta/world-class-bid-red-team-and-delivery-qc/SKILL.md | name: world-class-bid-red-team-and-delivery-qc | description: Use as the final quality gate for high-stakes bids, donor submissions, consulting deliverables, score predictions, compliance knockout scans, evidence audits, spreadsheet reviews, and delivery-feasibility checks. |
| skills/sdlc-meta/world-class-engineering/SKILL.md | name: world-class-engineering | description: Use when designing, building, reviewing, or upgrading production software systems that must be secure, performant, maintainable, scalable, and user-centered. Apply before writing specs, code, architecture, APIs, databases, mobile apps, SaaS platforms, or ERP systems. |
| skills/security/code-safety-scanner/SKILL.md | name: code-safety-scanner | description: Scan any codebase for 14 critical safety issues across security vulnerabilities, server stability (500 errors), and payment misconfigurations. Use when auditing code before deployment, reviewing AI-generated code for production readiness, or... |
| skills/security/dpia-generator/SKILL.md | name: dpia-generator | description: Generate a Data Protection Impact Assessment (DPIA), Uganda DPPA 2019-compliant. Use when producing or reviewing a data protection impact assessment, a privacy impact assessment, when uganda-dppa-compliance flags [DPIA-REQUIRED], or when processing large-scale or sensitive personal data for a new feature. |
| skills/security/linux-security-hardening/SKILL.md | name: linux-security-hardening | description: Use when hardening a Debian/Ubuntu server — user/group/sudo hardening, file permission audits, PAM password policy + MFA, AppArmor mandatory access control, auditd system call logging, kernel sysctl hardening, file integrity monitoring (AIDE), rootkit detection (rkhunter/chkrootkit), unattended security patching, GRUB + UEFI + LUKS boot security, and CIS benchmark compliance. |
| skills/security/network-security/SKILL.md | name: network-security | description: Use when designing, hardening, or auditing network-layer security for self-managed Debian/Ubuntu SaaS infrastructure — firewalls (nftables/UFW), WAF (ModSecurity + OWASP CRS), VPN (WireGuard, OpenVPN, IPsec), TLS/PKI ops, IDS/IPS (Suricata, Fail2ban), zero-trust, SSH hardening, DDoS mitigation, DNS security. Complements web-app-security-audit (app layer) and cicd-devsecops (secrets/CI). |
| skills/security/vibe-security-skill/SKILL.md | name: vibe-security-skill | description: Use when designing or reviewing security for a web application, API, or multi-tenant SaaS — produces threat model, abuse case list, auth/authz matrix, and secret handling plan; covers OWASP Top 10 2025 and the AI-code-generation blind spots. Neighbours — api-design-first owns auth model fields, deployment-release-engineering owns secret rotation choreography, ai-security and llm-security own model-specific threats. |
| skills/security/web-app-security-audit/SKILL.md | name: web-app-security-audit | description: Use when auditing a PHP/JavaScript/HTML web application for security vulnerabilities. Covers configuration, authentication, authorization, input validation, XSS, API security, HTTP headers, and dependency scanning. Produces a severity-rated audit... |

## Governance/Doctrine/Standard Files Read

| Path | Lines | SHA-256 prefix | First heading |
| --- | --- | --- | --- |
| AGENTS.md | 135 | d4e8e3fcf8d1 | Agent Guide |
| README.md | 214 | 846b6afa82a8 | Skills Repository |
| 00-meta-initialization/README.md | 118 | 94558c91891f | Meta-Initialization: Methodology Selection & Project Setup |
| 00-meta-initialization/new-project/examples/education-lms/README.md | 19 | 1d2bfb43444d | University LMS Platform |
| 00-meta-initialization/new-project/examples/education-lms/04-development/coding-standards.md | 3 | 822d4227a810 | Coding Standards |
| 00-meta-initialization/new-project/examples/education-lms/06-deployment-operations/deployment-guide.md | 3 | f2960fff1c86 | Deployment Guide |
| 00-meta-initialization/new-project/examples/education-lms/09-governance-compliance/03-compliance.md | 7 | 0985ff39ffb4 | Compliance Report |
| 00-meta-initialization/new-project/examples/education-lms/09-governance-compliance/audit-report.md | 3 | 2be573f5febf | Audit Report |
| 00-meta-initialization/new-project/examples/education-lms/09-governance-compliance/risk-register.md | 3 | a6e905292d12 | Risk Register |
| 00-meta-initialization/new-project/examples/education-lms/_context/quality-standards.md | 3 | 4f470b293274 | Quality Standards |
| 00-meta-initialization/new-project/examples/finance-erp/README.md | 19 | 67a1616a7da1 | Corporate Finance ERP |
| 00-meta-initialization/new-project/examples/finance-erp/04-development/coding-standards.md | 3 | 822d4227a810 | Coding Standards |
| 00-meta-initialization/new-project/examples/finance-erp/06-deployment-operations/deployment-guide.md | 3 | f2960fff1c86 | Deployment Guide |
| 00-meta-initialization/new-project/examples/finance-erp/09-governance-compliance/03-compliance.md | 7 | 40c647e7c7e6 | Compliance Report |
| 00-meta-initialization/new-project/examples/finance-erp/09-governance-compliance/audit-report.md | 3 | aafa9f58d1d3 | Audit Report |
| 00-meta-initialization/new-project/examples/finance-erp/09-governance-compliance/risk-register.md | 3 | a6e905292d12 | Risk Register |
| 00-meta-initialization/new-project/examples/finance-erp/_context/quality-standards.md | 3 | 4f470b293274 | Quality Standards |
| 00-meta-initialization/new-project/examples/healthcare-saas/README.md | 19 | 33a4eca3c07a | Hospital Admission System |
| 00-meta-initialization/new-project/examples/healthcare-saas/04-development/coding-standards.md | 3 | 822d4227a810 | Coding Standards |
| 00-meta-initialization/new-project/examples/healthcare-saas/06-deployment-operations/deployment-guide.md | 3 | f2960fff1c86 | Deployment Guide |
| 00-meta-initialization/new-project/examples/healthcare-saas/09-governance-compliance/03-compliance.md | 7 | cd0f2402b774 | Compliance Report |
| 00-meta-initialization/new-project/examples/healthcare-saas/09-governance-compliance/audit-report.md | 3 | f1547216da8e | Audit Report |
| 00-meta-initialization/new-project/examples/healthcare-saas/09-governance-compliance/risk-register.md | 3 | a6e905292d12 | Risk Register |
| 00-meta-initialization/new-project/examples/healthcare-saas/_context/quality-standards.md | 3 | 4f470b293274 | Quality Standards |
| 00-meta-initialization/new-project/examples/uganda-public-sector/README.md | 19 | 9da47036c3d1 | NIRA Citizen Registry |
| 00-meta-initialization/new-project/examples/uganda-public-sector/04-development/coding-standards.md | 3 | 822d4227a810 | Coding Standards |
| 00-meta-initialization/new-project/examples/uganda-public-sector/06-deployment-operations/deployment-guide.md | 3 | f2960fff1c86 | Deployment Guide |
| 00-meta-initialization/new-project/examples/uganda-public-sector/09-governance-compliance/03-compliance.md | 7 | 3f727a60f66a | Compliance Report |
| 00-meta-initialization/new-project/examples/uganda-public-sector/09-governance-compliance/audit-report.md | 3 | b7d5188795f2 | Audit Report |
| 00-meta-initialization/new-project/examples/uganda-public-sector/09-governance-compliance/risk-register.md | 3 | a6e905292d12 | Risk Register |
| 00-meta-initialization/new-project/examples/uganda-public-sector/_context/quality-standards.md | 3 | 4f470b293274 | Quality Standards |
| book-extractions/fekeshazi-pm-ux-guide-extraction.md | 179 | 6adac277f7cf | Product Managers' Guide to UX Design — Zoltan Fekeshazi (UX Studio) — Extraction |
| book-extractions/multi-tenant-saas-architectures-extraction.md | 308 | 8db07a0b1723 | Building Multi-Tenant SaaS Architectures — Tod Golding — Extraction |
| book-extractions/multi-tenant-saas-architectures.md | 1695 | 9d18bc690e66 | Document Outline {#index_split_001.html_calibre_pb_0 .calibre5} |
| claude-guides/database-standards.md | 539 | d7c4d38c2de1 | Database Standards (CRITICAL) |
| claude-guides/skill-best-practices.md | 33 | 5edd294d9717 | Skills Best Practices & Checklist |
| claude-guides/skill-creation-workflow.md | 513 | 575230195dbd | Skill Creation Workflow |
| claude-guides/skill-invocation.md | 439 | 5036bd0ba889 | Skill Invocation & Usage Guide |
| claude-guides/troubleshooting.md | 566 | 1321ea9a0869 | Troubleshooting & Maintenance |
| claude-guides/workflows.md | 516 | 7e723abd9038 | Common Workflows |
| docs/skill-routing-index.md | 198 | 1d017879e77a | Skill Routing Index |
| docs/analysis/00-index.md | 138 | 0a0e9a5e376a | Skills Engine Analysis — May 2026 (Post Spec-Closure) |
| docs/analysis/03-quality-compliance.md | 202 | 3a94661ae755 | Quality & Compliance Audit |
| docs/overview/ARCHITECTURE.md | 91 | 04e3dd284f3e | Architecture |
| docs/overview/README.md | 86 | 5a946414b8e1 | Skills Repository Overview |
| docs/plans/2026-03-04-php-modern-standards-enhancement.md | 51 | 2fd608be3ffd | PHP Modern Standards Enhancement Design |
| docs/plans/INDEX.md | 34 | d81a96bdfd1c | Plans Index |
| docs/plans/engine-phases/00-engine-roadmap-index.md | 129 | b0cf5087b70f | World-Class Software Development Engine — Roadmap Index |
| docs/plans/engine-phases/phase-05-quality-e2e-testing.md | 131 | c641ab3dd363 | Phase 05: Quality & E2E Testing |
| docs/scaling-ops/00-index.md | 77 | 85e5b8de8b3f | Scaling & Ops — Index |
| docs/scaling-ops/02-server-architecture.md | 284 | fbfbf5b1d69a | Server Architecture |
| docs/superpowers/plans/2026-05-06-claude-skills-uiux-phase2.md | 635 | c3e2b149490c | ~/.claude/skills UX/UI Phase 2 Implementation Plan |
| docs/superpowers/specs/2026-05-06-claude-skills-uiux-phase2-design.md | 136 | ad88b9b8a9c5 | ~/.claude/skills UX/UI Phase 2 Upgrade — Design Spec |
| doctrine/README.md | 110 | e0176d8a611a | Chwezi Accounting & Finance Doctrine |
| doctrine/docs/quality-gate-fixture-map.md | 61 | 161519c1c057 | Coverage Summary |
| doctrine/docs/reference-manifest.md | 196 | 4126fd8c630b | Repository Evidence |
| doctrine/docs/validation-report-template.md | 67 | 9f1b57d039b3 | Doctrine Validation Report Template |
| doctrine/docs/analysis/00-index.md | 37 | 65760f1936a3 | Chwezi Accounting Doctrine — Reorganization and Gap Analysis |
| doctrine/docs/analysis/01-executive-summary.md | 35 | a527ccf4c18a | Executive Summary - Doctrine Hardening Assessment |
| doctrine/docs/analysis/02-category-reorganization.md | 91 | a82dbc97caa3 | Category Reorganization |
| doctrine/docs/analysis/03-gap-register.md | 198 | af056e8595ca | Gap Register |
| doctrine/docs/analysis/04-skills-matrix.md | 204 | 511521b04f28 | 01 foundations |
| doctrine/docs/analysis/05-roadmap-for-uplift.md | 152 | 892c804a5147 | Roadmap for Uplift |
| doctrine/docs/analysis/06-methodology-and-evidence.md | 85 | 1a1a6d2e6da7 | Methodology and Evidence |
| doctrine/docs/analysis/07-gap-closure-and-hardening.md | 59 | e0e944e0d808 | Gap Closure and Hardening Record |
| doctrine/docs/audit-export-sample/00-index.md | 35 | a35794255f91 | Audit Export Sample Index |
| doctrine/docs/audit-export-sample/evidence/bank-statements/README.md | 8 | f1a5be5fd36a | Bank Statement Evidence Placeholder |
| doctrine/docs/audit-export-sample/evidence/invoices/README.md | 17 | 27588c3662bf | Invoice Evidence Placeholder |
| doctrine/docs/audit-export-sample/evidence/receipts/README.md | 8 | 51aa27af3432 | Receipt Evidence Placeholder |
| doctrine/docs/audit-export-sample/hashes/README.md | 22 | 116b6cd22e3d | Hashes README |
| doctrine/docs/audit-export-sample/reports/cash-movement.md | 15 | ad0ba41a3a74 | Cash Movement Placeholder |
| doctrine/docs/audit-export-sample/reports/financial-position.md | 17 | 135b2d728d99 | Financial Position Placeholder |
| doctrine/docs/audit-export-sample/reports/profit-or-loss.md | 19 | d8735d06c9bc | Profit Or Loss Placeholder |
| doctrine/docs/audit-export-sample/reports/tax-control-reconciliation.md | 18 | f345091453f9 | Tax Control Reconciliation Placeholder |
| doctrine/docs/audit-export-sample/reports/trial-balance.md | 15 | 3b4d4701ebe8 | Trial Balance Placeholder |
| doctrine/docs/audit-export-sample/signoffs/controller.md | 19 | 58a87320ae7a | Controller Signoff Template |
| doctrine/docs/audit-export-sample/signoffs/preparer.md | 19 | f6e1cdef320b | Preparer Signoff Template |
| doctrine/docs/audit-export-sample/signoffs/reviewer.md | 19 | b6705ade9025 | Reviewer Signoff Template |
| doctrine/docs/fin-analysis/00-index.md | 54 | 48a4703429c5 | Finance Analysis Report Pack |
| doctrine/docs/fin-analysis/01-executive-summary.md | 36 | 8efd2dc01275 | Executive Summary |
| doctrine/docs/fin-analysis/02-system-scorecard-100.md | 48 | 27066efa3122 | System Scorecard Out Of 100 |
| doctrine/docs/fin-analysis/03-findings-register.md | 34 | 8f04510b9d88 | Findings Register |
| doctrine/docs/fin-analysis/04-skill-realignment.md | 52 | a3095a4f2e32 | Skill Realignment |
| doctrine/docs/fin-analysis/05-remediation-roadmap.md | 58 | 2daba8ede21e | Remediation Roadmap |
| doctrine/docs/fin-analysis/06-implementation-standards-and-snippets.md | 98 | 1e10d318048f | Implementation Standards And Snippets |
| doctrine/docs/fin-analysis/07-standards-and-source-references.md | 50 | 8003a99b8416 | Standards Posture |
| doctrine/docs/fin-analysis/08-target-90-evidence-package.md | 50 | 01494e617b1f | Evidence Inventory |
| doctrine/docs/fin-analysis/09-finding-closure-matrix.md | 34 | 9444b0d1da16 | Finding Closure Matrix |
| doctrine/docs/fin-analysis/10-implementation-backlog.md | 46 | f2c22fc3931a | Implementation Backlog |
| doctrine/docs/fin-analysis/11-definition-of-done-and-rescore.md | 52 | b37d86f2eb94 | Definition Of Done And Re-Score |
| doctrine/docs/fin-analysis/world-class-finance-engine-analysis.md | 73 | 32c9e1c45958 | World-Class Finance Engine Analysis |
| doctrine/docs/quality-gate-fixtures/control-account-tieout-fixture.md | 37 | 82f180d4bf02 | Control Account Tie-Out Fixture |
| doctrine/docs/quality-gate-fixtures/framework-selection-checks.md | 106 | 29460367fcdf | Framework Selection Checks |
| doctrine/docs/quality-gate-fixtures/journal-balance-and-audit-fixtures.md | 68 | cd5331cab281 | Journal Balance And Audit Fixtures |
| doctrine/docs/quality-gate-fixtures/ledger-boundary-and-lock-fixtures.md | 62 | 26689a4c5a97 | Ledger Boundary And Lock Fixtures |
| doctrine/docs/quality-gate-fixtures/migration-cutover-fixtures.md | 93 | 3eb3b2614cbb | Migration Cutover Fixtures |
| doctrine/docs/quality-gate-fixtures/reconciliation-triage-fixture.md | 47 | a06f6ee5dfa3 | Reconciliation Triage Fixture |
| doctrine/docs/quality-gate-fixtures/return-template-version-check.md | 36 | 071c01ddfa92 | Return Template Version Check |
| doctrine/docs/quality-gate-fixtures/reviewer-signoff-fixtures.md | 67 | 534fcab58705 | Reviewer Sign-Off Fixtures |
| doctrine/docs/quality-gate-fixtures/unsupported-costing-method-rejection.md | 34 | 3bff2b81b976 | Unsupported Costing Method Rejection |
| doctrine/docs/quality-gate-fixtures/source-register-evidence/uganda-nssf-membership-2026-05-15.md | 28 | 3d1eab7f4117 | Uganda NSSF Membership Evidence |
| doctrine/doctrine/accounting-finance-doctrine.md | 163 | d62e60b5cfeb | Chwezi Accounting & Finance Doctrine |
| doctrine/doctrine/examples/coa-seed-uganda-sme.md | 157 | 67c16cafc9d2 | Seed CoA — Uganda SME (Limited Company) |
| doctrine/doctrine/examples/reconciliation-evidence-pack.md | 104 | b85fa0a71c25 | Worked Example — Reconciliation Evidence Pack |
| doctrine/doctrine/examples/reporting-basis-2026.md | 54 | d7dc05a81a31 | Reporting Basis Fixture - 2026 Baseline |
| doctrine/doctrine/examples/reporting-basis-2027-ifrs18.md | 54 | 08d2d2bc2ae0 | Reporting Basis Fixture - 2027 Full IFRS With IFRS 18 Transition |
| doctrine/doctrine/examples/reporting-basis-2027-smes-third-edition.md | 53 | 9147ab921416 | Reporting Basis Fixture - 2027 IFRS for SMEs Third Edition Transition |
| doctrine/doctrine/examples/reversal-pattern.md | 91 | 87641343fc87 | Worked Example — Reversal Pattern |
| doctrine/doctrine/examples/vat-inclusive-posting.md | 87 | c46cc4f79ff4 | Worked Example — VAT-Inclusive Posting |
| doctrine/doctrine/references/chart-of-accounts.md | 121 | 1a08f9a52bb7 | Chart of Accounts Backbone |
| doctrine/doctrine/references/country-extension-framework.md | 53 | 84f2b3711811 | Country Extension Framework |
| doctrine/doctrine/references/design-anti-patterns.md | 125 | a8a0ae0ba635 | Design Anti-Patterns |
| doctrine/doctrine/references/design-system-finance-accounting.md | 173 | a79089d04907 | Design System — Finance & Accounting UI |
| doctrine/doctrine/references/forbidden-patterns.md | 84 | b0f2835b1665 | Forbidden Patterns |
| doctrine/doctrine/references/full-ifrs-overlay.md | 77 | 288b85415dfe | Full IFRS Overlay |
| doctrine/doctrine/references/ifrs-18-presentation-transition.md | 55 | eebe4fc56115 | IFRS 18 Presentation Transition |
| doctrine/doctrine/references/ifrs-for-smes-default.md | 81 | 479f00cf96e3 | IFRS for SMEs — Practical Default |
| doctrine/doctrine/references/ifrs-for-smes-third-edition-transition.md | 55 | 82286b540cfb | IFRS for SMEs Third Edition Transition |
| doctrine/doctrine/references/ledger-invariants.md | 101 | 95de18568d11 | 1. Posting boundary |
| doctrine/doctrine/references/live-rate-verification-protocol.md | 113 | 69bcf5f75c16 | Live-Rate Verification Protocol |
| doctrine/doctrine/references/policy-hierarchy.md | 60 | 5dcb924b0bd9 | Policy Hierarchy |
| doctrine/doctrine/references/print-fidelity.md | 71 | 30dc91e1aac1 | Print Fidelity |
| doctrine/doctrine/references/required-patterns.md | 98 | 4326f5bedeed | Required Patterns |
| doctrine/doctrine/references/requirement-id-library.md | 84 | 73ebf45e8704 | Finance Requirement-ID Library |
| doctrine/doctrine/references/role-conditioned-shell.md | 82 | 6ae6f6fdca79 | Role-Conditioned Shell |
| doctrine/doctrine/references/standards-transition-2027.md | 91 | acfdc816d11b | Standards Transition 2027 |
| doctrine/doctrine/references/status-taxonomy.md | 66 | f7c8b2ecb35c | Status Taxonomy |
| doctrine/doctrine/references/tax-vat-and-returns.md | 95 | a7c1b7a70e22 | Tax, VAT-Inclusive Posting, and Return-Ready Packs |
| doctrine/doctrine/references/terminology-glossary.md | 56 | baea39e39512 | Terminology Glossary |
| doctrine/doctrine/references/uganda-compliance-caveats.md | 80 | 4d82336d54ab | Uganda Compliance Caveats |
| doctrine/doctrine/references/versioning-and-changelog.md | 64 | 2e37355c51fc | Versioning and Changelog |
| doctrine/doctrine/source-register/README.md | 71 | 8760ec210647 | Source Register |
| doctrine/doctrine/source-register/kenya/README.md | 19 | bab9df6f8d6d | Kenya Source Register Skeleton |
| doctrine/doctrine/source-register/rwanda/README.md | 19 | ec495e9e40fe | Rwanda Source Register Skeleton |
| doctrine/doctrine/source-register/south-africa/README.md | 19 | 70f76e86bfda | South Africa Source Register Skeleton |
| doctrine/doctrine/source-register/tanzania/README.md | 19 | 8341f27da6f1 | Tanzania Source Register Skeleton |
| doctrine/doctrine/source-register/uganda/README.md | 25 | 52569303b180 | Uganda Source Register Seed Pack |
| doctrine/governance/cleanup-backlog.md | 116 | 45ef9d14b8df | Cleanup Backlog |
| doctrine/governance/finance-accounting-quality-gate.md | 179 | 394c6a3f83cd | Finance & Accounting Quality Gate |
| doctrine/governance/how-to-reference-this-doctrine.md | 109 | d2753b583ff4 | Common Pattern Across All Four Engines |
| doctrine/integration/changelog-entries.md | 114 | 1f5a3939dbd8 | Changelog Entries |
| doctrine/integration/deprecation-list.md | 23 | 53d3b07cfbb3 | Deprecation List |
| doctrine/integration/integration-plan.md | 118 | 4c67621592fc | Integration Plan |
| doctrine/skills/01-foundations/README.md | 17 | 0c8a8ec14ae6 | Skills in this category |
| doctrine/skills/01-foundations/chart-of-accounts-design-and-governance/SKILL.md | 123 | ac37c1803297 | Chart Of Accounts Design And Governance |
| doctrine/skills/01-foundations/chart-of-accounts-design-and-governance/examples/worked-example.md | 42 | c50bb0ad3e13 | Scenario |
| doctrine/skills/01-foundations/chart-of-accounts-design-and-governance/references/implementation-rules.md | 49 | e1ceb030e4eb | Doctrine Boundary |
| doctrine/skills/01-foundations/chart-of-accounts-design-and-governance/references/source-basis.md | 24 | e6c8ea39f5d3 | Evidence Discipline |
| doctrine/skills/01-foundations/functional-and-presentation-currency/SKILL.md | 123 | b2a76927d2c0 | Functional And Presentation Currency |
| doctrine/skills/01-foundations/functional-and-presentation-currency/examples/worked-example.md | 42 | 1b3b931aa73f | Scenario |
| doctrine/skills/01-foundations/functional-and-presentation-currency/references/implementation-rules.md | 49 | f00a9518fcca | Doctrine Boundary |
| doctrine/skills/01-foundations/functional-and-presentation-currency/references/source-basis.md | 24 | 9c47c266e8ae | Evidence Discipline |
| doctrine/skills/01-foundations/ledger-posting-engine-core/SKILL.md | 137 | 1999cf4236e2 | Ledger Posting Engine Core |
| doctrine/skills/01-foundations/ledger-posting-engine-core/examples/customer-receipt-allocation.md | 21 | 585765a84ba1 | Fixture: Customer Receipt Allocation |
| doctrine/skills/01-foundations/ledger-posting-engine-core/examples/foreign-currency-bank-receipt.md | 18 | 119c45172636 | Fixture: Foreign Currency Bank Receipt |
| doctrine/skills/01-foundations/ledger-posting-engine-core/examples/rejected-unbalanced-entry.md | 18 | 1ab0944e3d3a | Fixture: Rejected Unbalanced Entry |
| doctrine/skills/01-foundations/ledger-posting-engine-core/examples/reversal.md | 27 | fedd715dbfdb | Fixture: Reversal |
| doctrine/skills/01-foundations/ledger-posting-engine-core/examples/supplier-bill-and-payment.md | 23 | 770c84dcac8d | Fixture: Supplier Bill and Payment |
| doctrine/skills/01-foundations/ledger-posting-engine-core/examples/vat-inclusive-cash-sale.md | 25 | 2ab6222544d5 | Fixture: VAT-Inclusive Cash Sale |
| doctrine/skills/01-foundations/ledger-posting-engine-core/references/event-to-journal-map.md | 20 | cf9b38d2e1a4 | Event to Journal Map |
| doctrine/skills/01-foundations/ledger-posting-engine-core/references/idempotency-and-reversal-rules.md | 30 | d0f85a33e908 | Idempotency and Reversal Rules |
| doctrine/skills/01-foundations/ledger-posting-engine-core/references/invariant-tests.md | 17 | b2fbb56e5a80 | Invariant Tests |
| doctrine/skills/01-foundations/ledger-posting-engine-core/references/journal-entry-schema.md | 41 | 08fd75f7ae59 | Journal Entry Schema |
| doctrine/skills/01-foundations/ledger-posting-engine-core/references/posting-service-contract.md | 38 | c6f150ad1413 | Posting Service Contract |
| doctrine/skills/01-foundations/management-accounting-dimensions/SKILL.md | 183 | 841efd964803 | Management Accounting Dimensions |
| doctrine/skills/01-foundations/management-accounting-dimensions/examples/contribution-margin-by-branch.md | 38 | d347bf040e0f | Example - Contribution Margin by Branch |
| doctrine/skills/01-foundations/management-accounting-dimensions/references/allocation-rules-pattern.md | 55 | adc1d9d26842 | Allocation Rules Pattern |
| doctrine/skills/01-foundations/management-accounting-dimensions/references/dimensions-spec.md | 59 | 74253555c683 | Dimensions Specification |
| doctrine/skills/01-foundations/period-locking-and-data-immutability/SKILL.md | 123 | b2dab86ddec2 | Period Locking And Data Immutability |
| doctrine/skills/01-foundations/period-locking-and-data-immutability/examples/worked-example.md | 42 | b15ee4639a7b | Scenario |
| doctrine/skills/01-foundations/period-locking-and-data-immutability/references/implementation-rules.md | 49 | ee80616d05de | Doctrine Boundary |
| doctrine/skills/01-foundations/period-locking-and-data-immutability/references/source-basis.md | 24 | 0b3ab7762767 | Evidence Discipline |
| doctrine/skills/02-ifrs-core-standards/README.md | 21 | ae35e807ebe4 | Skills in this category |
| doctrine/skills/02-ifrs-core-standards/ifrs-borrowing-costs-ias23/SKILL.md | 123 | 1f8c96616a74 | IFRS Borrowing Costs Ias23 |
| doctrine/skills/02-ifrs-core-standards/ifrs-borrowing-costs-ias23/examples/worked-example.md | 42 | 45166d246cec | Scenario |
| doctrine/skills/02-ifrs-core-standards/ifrs-borrowing-costs-ias23/references/implementation-rules.md | 49 | 305a41859dc9 | Doctrine Boundary |
| doctrine/skills/02-ifrs-core-standards/ifrs-borrowing-costs-ias23/references/source-basis.md | 26 | c6307b70deee | Evidence Discipline |
| doctrine/skills/02-ifrs-core-standards/ifrs-employee-benefits-ias19/SKILL.md | 123 | db51bfccbe72 | IFRS Employee Benefits Ias19 |
| doctrine/skills/02-ifrs-core-standards/ifrs-employee-benefits-ias19/examples/worked-example.md | 42 | cf0c589981ed | Scenario |
| doctrine/skills/02-ifrs-core-standards/ifrs-employee-benefits-ias19/references/implementation-rules.md | 49 | c9999bf39875 | Doctrine Boundary |
| doctrine/skills/02-ifrs-core-standards/ifrs-employee-benefits-ias19/references/source-basis.md | 26 | 84441d8c5204 | Evidence Discipline |
| doctrine/skills/02-ifrs-core-standards/ifrs-financial-instruments/SKILL.md | 146 | 6a63a788713b | Financial Instruments (IFRS 9 / Sections 11 and 12) |
| doctrine/skills/02-ifrs-core-standards/ifrs-financial-instruments/references/effective-interest-schedule.md | 35 | 9d67d419cf3c | Effective-Interest Schedule |
| doctrine/skills/02-ifrs-core-standards/ifrs-financial-instruments/references/ifrs-9-ecl-simplified-trade-receivables.md | 41 | b554a6cccfe8 | IFRS 9 Simplified ECL for Trade Receivables |
| doctrine/skills/02-ifrs-core-standards/ifrs-financial-instruments/references/section-11-impairment.md | 42 | 2f7be60a753f | Section 11 Impairment for Basic Financial Instruments |
| doctrine/skills/02-ifrs-core-standards/ifrs-for-smes-equivalents/SKILL.md | 155 | a4dfd6237551 | IFRS for SMEs Equivalents |
| doctrine/skills/02-ifrs-core-standards/ifrs-for-smes-equivalents/references/client-profile-decision-tree.md | 32 | 203d614b9909 | Client Profile Decision Tree |
| doctrine/skills/02-ifrs-core-standards/ifrs-for-smes-equivalents/references/full-ifrs-to-sme-mapping.md | 34 | d4de94ad3bc7 | Full IFRS to IFRS for SMEs Mapping |
| doctrine/skills/02-ifrs-core-standards/ifrs-foreign-currency-translation-ias21/SKILL.md | 123 | 05d9b33e2ec1 | IFRS Foreign Currency Translation Ias21 |
| doctrine/skills/02-ifrs-core-standards/ifrs-foreign-currency-translation-ias21/examples/worked-example.md | 42 | 5031acf71feb | Scenario |
| doctrine/skills/02-ifrs-core-standards/ifrs-foreign-currency-translation-ias21/references/implementation-rules.md | 49 | 2249643f2ba5 | Doctrine Boundary |
| doctrine/skills/02-ifrs-core-standards/ifrs-foreign-currency-translation-ias21/references/source-basis.md | 26 | ee02c488144f | Evidence Discipline |
| doctrine/skills/02-ifrs-core-standards/ifrs-intangible-assets-ias38/SKILL.md | 123 | a26e21e57d42 | IFRS Intangible Assets Ias38 |
| doctrine/skills/02-ifrs-core-standards/ifrs-intangible-assets-ias38/examples/worked-example.md | 42 | de4a7a23537c | Scenario |
| doctrine/skills/02-ifrs-core-standards/ifrs-intangible-assets-ias38/references/implementation-rules.md | 49 | 2167b031f2f1 | Doctrine Boundary |
| doctrine/skills/02-ifrs-core-standards/ifrs-intangible-assets-ias38/references/source-basis.md | 26 | a46724ef7a6c | Evidence Discipline |
| doctrine/skills/02-ifrs-core-standards/ifrs-leases/SKILL.md | 134 | 5eae98309464 | Leases (IFRS 16 / Section 20) |
| doctrine/skills/02-ifrs-core-standards/ifrs-leases/references/exemption-test.md | 37 | b009612a12f8 | IFRS 16 Exemption Test |
| doctrine/skills/02-ifrs-core-standards/ifrs-leases/references/full-ifrs-16-lessee-model.md | 47 | ed4891971556 | Full IFRS 16 Lessee Model |
| doctrine/skills/02-ifrs-core-standards/ifrs-property-plant-equipment-ias16/SKILL.md | 123 | 75dadf13de6f | IFRS Property Plant Equipment Ias16 |
| doctrine/skills/02-ifrs-core-standards/ifrs-property-plant-equipment-ias16/examples/worked-example.md | 42 | 47c630d9a5b4 | Scenario |
| doctrine/skills/02-ifrs-core-standards/ifrs-property-plant-equipment-ias16/references/implementation-rules.md | 49 | 31c2d980586a | Doctrine Boundary |
| doctrine/skills/02-ifrs-core-standards/ifrs-property-plant-equipment-ias16/references/source-basis.md | 26 | eb1852264eee | Evidence Discipline |
| doctrine/skills/02-ifrs-core-standards/ifrs-revenue-recognition/SKILL.md | 210 | 6cd07d54b6e5 | IFRS Revenue Recognition (IFRS 15 / Section 23) |
| doctrine/skills/02-ifrs-core-standards/ifrs-revenue-recognition/examples/multi-element-software-licence-plus-support.md | 51 | a535d032b4da | Example: Multi-Element Software Licence Plus Support |
| doctrine/skills/02-ifrs-core-standards/ifrs-revenue-recognition/references/ifrs-15-five-step.md | 47 | 62cefb5e4291 | IFRS 15 Five-Step Model |
| doctrine/skills/02-ifrs-core-standards/ifrs-revenue-recognition/references/section-23-summary.md | 45 | bcb375492858 | Section 23 Revenue Summary |
| doctrine/skills/03-ifrs-specialised-standards/README.md | 30 | 01d11d23ba39 | Skills in this category |
| doctrine/skills/03-ifrs-specialised-standards/ias-agriculture/SKILL.md | 217 | c7c32971989e | Agriculture (Section 34 / IAS 41) |
| doctrine/skills/03-ifrs-specialised-standards/ias-agriculture/examples/birdc-layer-flock-q2-2026.md | 46 | 13cc84e9db66 | Example: BIRDC Layer Flock Q2 2026 |
| doctrine/skills/03-ifrs-specialised-standards/ias-agriculture/references/cohort-data-model.md | 48 | 085088bc5f4f | Biological-Asset Cohort Data Model |
| doctrine/skills/03-ifrs-specialised-standards/ias-agriculture/references/fair-value-methodology.md | 48 | d74b1ae5a8a2 | Fair-Value Methodology for Biological Assets |
| doctrine/skills/03-ifrs-specialised-standards/ias-government-grants/SKILL.md | 139 | cd44ecacecd8 | Government Grants and Donor Assistance (Section 24 / IAS 20) |
| doctrine/skills/03-ifrs-specialised-standards/ias-government-grants/examples/ngo-restricted-grant-cycle.md | 41 | fd528c63ae11 | Example: NGO Restricted Grant Cycle |
| doctrine/skills/03-ifrs-specialised-standards/ias-government-grants/references/donor-restriction-pattern.md | 39 | 90b5faf09daf | Donor Restriction Pattern |
| doctrine/skills/03-ifrs-specialised-standards/ias-government-grants/references/grant-register-schema.md | 44 | a06bdeb4c5bf | Grant Register Schema |
| doctrine/skills/03-ifrs-specialised-standards/ias-impairment/SKILL.md | 150 | 175643abb943 | Impairment of Assets (IAS 36 / Section 27) |
| doctrine/skills/03-ifrs-specialised-standards/ias-impairment/references/indicator-checklist.md | 37 | b147e945b0ed | Impairment Indicator Checklist |
| doctrine/skills/03-ifrs-specialised-standards/ias-impairment/references/value-in-use-workpaper-template.md | 50 | e66500658f89 | Value-in-Use Workpaper Template |
| doctrine/skills/03-ifrs-specialised-standards/ias-income-tax-deferred-tax/SKILL.md | 192 | ad17492967b5 | Income Tax and Deferred Tax (Section 29 / IAS 12) |
| doctrine/skills/03-ifrs-specialised-standards/ias-income-tax-deferred-tax/examples/sme-tax-provision-2026-04.md | 47 | fe15a088024e | Example: SME Tax Provision April 2026 |
| doctrine/skills/03-ifrs-specialised-standards/ias-income-tax-deferred-tax/references/recognition-checklist.md | 37 | 37dc07d1851c | Deferred-Tax Recognition Checklist |
| doctrine/skills/03-ifrs-specialised-standards/ias-income-tax-deferred-tax/references/temporary-difference-catalog.md | 35 | d09a764d6887 | Temporary-Difference Catalog |
| doctrine/skills/03-ifrs-specialised-standards/ias-provisions-contingencies/SKILL.md | 142 | d7a2afb24109 | Provisions and Contingencies (Section 21 / IAS 37) |
| doctrine/skills/03-ifrs-specialised-standards/ias-provisions-contingencies/references/onerous-contract-test.md | 38 | 111c0e6a3f5f | Onerous Contract Test |
| doctrine/skills/03-ifrs-specialised-standards/ias-provisions-contingencies/references/recognition-decision-tree.md | 33 | df041a554b07 | Provision Recognition Decision Tree |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-accounting-policies-changes-errors-ias8/SKILL.md | 123 | b70703058b52 | IFRS Accounting Policies Changes Errors Ias8 |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-accounting-policies-changes-errors-ias8/examples/worked-example.md | 42 | eb17436ce6cb | Scenario |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-accounting-policies-changes-errors-ias8/references/implementation-rules.md | 49 | ec15b7bc7132 | Doctrine Boundary |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-accounting-policies-changes-errors-ias8/references/source-basis.md | 26 | e0a8f132000e | Evidence Discipline |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-associates-and-joint-arrangements/SKILL.md | 123 | 856385ea56ad | IFRS Associates And Joint Arrangements |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-associates-and-joint-arrangements/examples/worked-example.md | 42 | 4a708ee43f72 | Scenario |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-associates-and-joint-arrangements/references/implementation-rules.md | 49 | 56076c172131 | Doctrine Boundary |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-associates-and-joint-arrangements/references/source-basis.md | 26 | 6b1ffa3b5ecf | Evidence Discipline |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-business-combinations-ifrs3/SKILL.md | 123 | f5318a9efd8f | IFRS Business Combinations Ifrs3 |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-business-combinations-ifrs3/examples/worked-example.md | 42 | 6eae3fd77f12 | Scenario |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-business-combinations-ifrs3/references/implementation-rules.md | 49 | 229f83d946fd | Doctrine Boundary |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-business-combinations-ifrs3/references/source-basis.md | 26 | 6b6ce8f9e97a | Evidence Discipline |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-discontinued-operations-ifrs5/SKILL.md | 123 | 15862b5faf30 | IFRS Discontinued Operations Ifrs5 |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-discontinued-operations-ifrs5/examples/worked-example.md | 42 | e81d42a75b8c | Scenario |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-discontinued-operations-ifrs5/references/implementation-rules.md | 49 | 79d4235595fd | Doctrine Boundary |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-discontinued-operations-ifrs5/references/source-basis.md | 26 | 8210415ef5db | Evidence Discipline |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-earnings-per-share-ias33/SKILL.md | 123 | 0f9467fcd7d8 | IFRS Earnings Per Share Ias33 |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-earnings-per-share-ias33/examples/worked-example.md | 42 | ed33ffb9f665 | Scenario |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-earnings-per-share-ias33/references/implementation-rules.md | 49 | d7c972e5586c | Doctrine Boundary |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-earnings-per-share-ias33/references/source-basis.md | 26 | 578b90ad8ab3 | Evidence Discipline |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-events-after-reporting-period-ias10/SKILL.md | 123 | 4ef5d58ae987 | IFRS Events After Reporting Period Ias10 |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-events-after-reporting-period-ias10/examples/worked-example.md | 42 | 5ad52c583411 | Scenario |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-events-after-reporting-period-ias10/references/implementation-rules.md | 49 | bac5d40b8e8a | Doctrine Boundary |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-events-after-reporting-period-ias10/references/source-basis.md | 26 | c414f920c9fb | Evidence Discipline |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-fair-value-measurement-ifrs13/SKILL.md | 123 | b3c5e6cfea01 | IFRS Fair Value Measurement Ifrs13 |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-fair-value-measurement-ifrs13/examples/worked-example.md | 42 | 2bdc8ec1eb39 | Scenario |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-fair-value-measurement-ifrs13/references/implementation-rules.md | 49 | 4b44436aa707 | Doctrine Boundary |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-fair-value-measurement-ifrs13/references/source-basis.md | 26 | 16df1481a8da | Evidence Discipline |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-first-time-adoption-ifrs1/SKILL.md | 123 | 888c9a8707db | IFRS First Time Adoption Ifrs1 |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-first-time-adoption-ifrs1/examples/worked-example.md | 42 | d69a03eab477 | Scenario |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-first-time-adoption-ifrs1/references/implementation-rules.md | 49 | 482ce90e6b69 | Doctrine Boundary |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-first-time-adoption-ifrs1/references/source-basis.md | 26 | abb0e366ac30 | Evidence Discipline |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-insurance-contracts-ifrs17/SKILL.md | 123 | ec39bb356f23 | IFRS Insurance Contracts Ifrs17 |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-insurance-contracts-ifrs17/examples/worked-example.md | 42 | 4850af280165 | Scenario |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-insurance-contracts-ifrs17/references/implementation-rules.md | 49 | 01d75ba08216 | Doctrine Boundary |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-insurance-contracts-ifrs17/references/source-basis.md | 26 | d00f163bec7a | Evidence Discipline |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-investment-property-ias40/SKILL.md | 123 | 63e7a91649aa | IFRS Investment Property Ias40 |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-investment-property-ias40/examples/worked-example.md | 42 | 87ec8bc25cae | Scenario |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-investment-property-ias40/references/implementation-rules.md | 49 | 237665fee4ff | Doctrine Boundary |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-investment-property-ias40/references/source-basis.md | 26 | 71518896c13f | Evidence Discipline |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-related-party-disclosures-ias24/SKILL.md | 123 | ba306d892964 | IFRS Related Party Disclosures Ias24 |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-related-party-disclosures-ias24/examples/worked-example.md | 42 | 26c6419f0497 | Scenario |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-related-party-disclosures-ias24/references/implementation-rules.md | 49 | 2b4e4c289b88 | Doctrine Boundary |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-related-party-disclosures-ias24/references/source-basis.md | 26 | 0a0c75e4753b | Evidence Discipline |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-segment-reporting-ifrs8/SKILL.md | 123 | 3b570e17376b | IFRS Segment Reporting Ifrs8 |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-segment-reporting-ifrs8/examples/worked-example.md | 42 | d1ab7c5ca00e | Scenario |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-segment-reporting-ifrs8/references/implementation-rules.md | 49 | 72cdecfd1c99 | Doctrine Boundary |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-segment-reporting-ifrs8/references/source-basis.md | 26 | 92ac4a52a9d0 | Evidence Discipline |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-share-based-payment-ifrs2/SKILL.md | 123 | cb7007ceddf9 | IFRS Share Based Payment Ifrs2 |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-share-based-payment-ifrs2/examples/worked-example.md | 42 | 62a798b18732 | Scenario |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-share-based-payment-ifrs2/references/implementation-rules.md | 49 | 5fac53842642 | Doctrine Boundary |
| doctrine/skills/03-ifrs-specialised-standards/ifrs-share-based-payment-ifrs2/references/source-basis.md | 26 | 3516500b996c | Evidence Discipline |
| doctrine/skills/04-subledgers-and-operations/README.md | 19 | 1b4b13f5b3b3 | Skills in this category |
| doctrine/skills/04-subledgers-and-operations/bank-and-mobile-money-reconciliation/SKILL.md | 240 | 4ebc359db77d | Bank and Mobile-Money Reconciliation |
| doctrine/skills/04-subledgers-and-operations/bank-and-mobile-money-reconciliation/examples/mtn-momo-month-end.md | 74 | ff878ca52f1f | Example — MTN MoMo Business Month-End Reconciliation |
| doctrine/skills/04-subledgers-and-operations/bank-and-mobile-money-reconciliation/references/match-rules.md | 67 | efd6fffaeb78 | Match Rules |
| doctrine/skills/04-subledgers-and-operations/bank-and-mobile-money-reconciliation/references/provider-quirks.md | 48 | b54b21057d10 | Provider Quirks |
| doctrine/skills/04-subledgers-and-operations/expense-management-and-staff-claims/SKILL.md | 123 | 4036be866d7a | Expense Management And Staff Claims |
| doctrine/skills/04-subledgers-and-operations/expense-management-and-staff-claims/examples/worked-example.md | 42 | 43529e62471d | Scenario |
| doctrine/skills/04-subledgers-and-operations/expense-management-and-staff-claims/references/implementation-rules.md | 49 | bb705ca1ee50 | Doctrine Boundary |
| doctrine/skills/04-subledgers-and-operations/expense-management-and-staff-claims/references/source-basis.md | 24 | bd6257840b7a | Evidence Discipline |
| doctrine/skills/04-subledgers-and-operations/fixed-assets-and-depreciation/SKILL.md | 133 | 3c7a443054b6 | Fixed Assets and Depreciation |
| doctrine/skills/04-subledgers-and-operations/fixed-assets-and-depreciation/examples/acquisition-fixture.md | 22 | baeaf4649888 | Fixture: Asset Acquisition |
| doctrine/skills/04-subledgers-and-operations/fixed-assets-and-depreciation/examples/disposal-gain-loss-fixture.md | 24 | 7088d28f14d1 | Fixture: Disposal Gain or Loss |
| doctrine/skills/04-subledgers-and-operations/fixed-assets-and-depreciation/examples/impairment-indicator-checklist.md | 18 | 001175cf893f | Fixture: Impairment Indicator Checklist |
| doctrine/skills/04-subledgers-and-operations/fixed-assets-and-depreciation/examples/monthly-depreciation-fixture.md | 25 | bcde1b628818 | Fixture: Monthly Depreciation |
| doctrine/skills/04-subledgers-and-operations/fixed-assets-and-depreciation/examples/register-to-gl-tieout.md | 15 | ec2501261b5e | Fixture: Asset Register to GL Tie-Out |
| doctrine/skills/04-subledgers-and-operations/fixed-assets-and-depreciation/references/asset-register-fields.md | 24 | d2c13d1fd9ab | Asset Register Fields |
| doctrine/skills/04-subledgers-and-operations/fixed-assets-and-depreciation/references/depreciation-and-disposal-rules.md | 24 | 436148d26b6a | Depreciation and Disposal Rules |
| doctrine/skills/04-subledgers-and-operations/fixed-assets-and-depreciation/references/domain-acceptance-tests.md | 13 | b0b13ff48e37 | Fixed-Asset Domain Acceptance Tests |
| doctrine/skills/04-subledgers-and-operations/inventory-costing-and-stock-accounting/SKILL.md | 132 | d1d60529bf9a | Inventory Costing and Stock Accounting |
| doctrine/skills/04-subledgers-and-operations/inventory-costing-and-stock-accounting/examples/fifo-costing-fixture.md | 28 | 25596f3cd631 | Fixture: FIFO Costing |
| doctrine/skills/04-subledgers-and-operations/inventory-costing-and-stock-accounting/examples/nrv-write-down-fixture.md | 21 | d437a3d218a0 | Fixture: NRV Write-Down |
| doctrine/skills/04-subledgers-and-operations/inventory-costing-and-stock-accounting/examples/rejected-unsupported-costing-method.md | 13 | 43795a0c319f | Fixture: Rejected Unsupported Costing Method |
| doctrine/skills/04-subledgers-and-operations/inventory-costing-and-stock-accounting/examples/stock-count-variance-fixture.md | 22 | dbb6c7b8d5a8 | Fixture: Stock Count Variance |
| doctrine/skills/04-subledgers-and-operations/inventory-costing-and-stock-accounting/examples/weighted-average-fixture.md | 29 | 49eda4f0e185 | Fixture: Weighted-Average Costing |
| doctrine/skills/04-subledgers-and-operations/inventory-costing-and-stock-accounting/references/domain-acceptance-tests.md | 13 | 3d4dd499c027 | Inventory Domain Acceptance Tests |
| doctrine/skills/04-subledgers-and-operations/inventory-costing-and-stock-accounting/references/inventory-posting-rules.md | 32 | 65ff7eb81f30 | Inventory Posting Rules |
| doctrine/skills/04-subledgers-and-operations/payroll-and-statutory-postings-east-africa/SKILL.md | 131 | a25fe918ff15 | Payroll and Statutory Postings East Africa |
| doctrine/skills/04-subledgers-and-operations/payroll-and-statutory-postings-east-africa/examples/payroll-journal-fixture.md | 29 | d55a86e8a24f | Fixture: Payroll Journal |
| doctrine/skills/04-subledgers-and-operations/payroll-and-statutory-postings-east-africa/examples/payslip-to-gl-reconciliation.md | 19 | 6aa26b58af42 | Fixture: Payslip to GL Reconciliation |
| doctrine/skills/04-subledgers-and-operations/payroll-and-statutory-postings-east-africa/examples/stale-rate-rejection.md | 15 | 9d35d70e68a4 | Fixture: Stale Rate Rejection |
| doctrine/skills/04-subledgers-and-operations/payroll-and-statutory-postings-east-africa/examples/statutory-liability-schedule.md | 21 | e47015d54201 | Fixture: Statutory Liability Schedule |
| doctrine/skills/04-subledgers-and-operations/payroll-and-statutory-postings-east-africa/references/domain-acceptance-tests.md | 13 | 5e749ecf585f | Payroll Domain Acceptance Tests |
| doctrine/skills/04-subledgers-and-operations/payroll-and-statutory-postings-east-africa/references/payroll-event-model.md | 26 | e532f29a5d59 | Payroll Event Model |
| doctrine/skills/04-subledgers-and-operations/payroll-and-statutory-postings-east-africa/references/statutory-source-gates.md | 21 | c735dce951c6 | Statutory Source Gates |
| doctrine/skills/04-subledgers-and-operations/petty-cash-and-imprest-management/SKILL.md | 123 | 8f0522db66ff | Petty Cash And Imprest Management |
| doctrine/skills/04-subledgers-and-operations/petty-cash-and-imprest-management/examples/worked-example.md | 42 | 1cad16fb01cc | Scenario |
| doctrine/skills/04-subledgers-and-operations/petty-cash-and-imprest-management/references/implementation-rules.md | 49 | b77bcca2139d | Doctrine Boundary |
| doctrine/skills/04-subledgers-and-operations/petty-cash-and-imprest-management/references/source-basis.md | 24 | f663284d0548 | Evidence Discipline |
| doctrine/skills/04-subledgers-and-operations/pos-and-cash-drawer-management/SKILL.md | 123 | 383ade117792 | POS And Cash Drawer Management |
| doctrine/skills/04-subledgers-and-operations/pos-and-cash-drawer-management/examples/worked-example.md | 42 | f9bd57d35d12 | Scenario |
| doctrine/skills/04-subledgers-and-operations/pos-and-cash-drawer-management/references/implementation-rules.md | 49 | 0838b9066e32 | Doctrine Boundary |
| doctrine/skills/04-subledgers-and-operations/pos-and-cash-drawer-management/references/source-basis.md | 24 | 8d9ddee7adce | Evidence Discipline |
| doctrine/skills/05-receivables-payables-and-treasury/README.md | 17 | 51e9c25748b0 | Skills in this category |
| doctrine/skills/05-receivables-payables-and-treasury/accounts-payable-and-supplier-management/SKILL.md | 123 | c5f51389cca8 | Accounts Payable And Supplier Management |
| doctrine/skills/05-receivables-payables-and-treasury/accounts-payable-and-supplier-management/examples/worked-example.md | 42 | 4f174c5e1789 | Scenario |
| doctrine/skills/05-receivables-payables-and-treasury/accounts-payable-and-supplier-management/references/implementation-rules.md | 49 | a69753445f11 | Doctrine Boundary |
| doctrine/skills/05-receivables-payables-and-treasury/accounts-payable-and-supplier-management/references/source-basis.md | 26 | d177002a2e93 | Evidence Discipline |
| doctrine/skills/05-receivables-payables-and-treasury/accounts-receivable-and-credit-management/SKILL.md | 123 | 08f95ab3285e | Accounts Receivable And Credit Management |
| doctrine/skills/05-receivables-payables-and-treasury/accounts-receivable-and-credit-management/examples/worked-example.md | 42 | 4c4368cff7bc | Scenario |
| doctrine/skills/05-receivables-payables-and-treasury/accounts-receivable-and-credit-management/references/implementation-rules.md | 49 | 9a7cab79920c | Doctrine Boundary |
| doctrine/skills/05-receivables-payables-and-treasury/accounts-receivable-and-credit-management/references/source-basis.md | 26 | 2fab21e6cda5 | Evidence Discipline |
| doctrine/skills/05-receivables-payables-and-treasury/banking-facilities-and-covenants/SKILL.md | 123 | 130462105734 | Banking Facilities And Covenants |
| doctrine/skills/05-receivables-payables-and-treasury/banking-facilities-and-covenants/examples/worked-example.md | 42 | 8dd956036c15 | Scenario |
| doctrine/skills/05-receivables-payables-and-treasury/banking-facilities-and-covenants/references/implementation-rules.md | 49 | c2863954ef60 | Doctrine Boundary |
| doctrine/skills/05-receivables-payables-and-treasury/banking-facilities-and-covenants/references/source-basis.md | 26 | 99edc0ebb95b | Evidence Discipline |
| doctrine/skills/05-receivables-payables-and-treasury/cash-flow-forecasting-and-treasury/SKILL.md | 123 | 0387dcc75168 | Cash Flow Forecasting And Treasury |
| doctrine/skills/05-receivables-payables-and-treasury/cash-flow-forecasting-and-treasury/examples/worked-example.md | 42 | 880cc67f9cc3 | Scenario |
| doctrine/skills/05-receivables-payables-and-treasury/cash-flow-forecasting-and-treasury/references/implementation-rules.md | 49 | dc899bedbc43 | Doctrine Boundary |
| doctrine/skills/05-receivables-payables-and-treasury/cash-flow-forecasting-and-treasury/references/source-basis.md | 26 | 042810291fc8 | Evidence Discipline |
| doctrine/skills/05-receivables-payables-and-treasury/fx-management-and-hedging/SKILL.md | 123 | a229a45f608a | FX Management And Hedging |
| doctrine/skills/05-receivables-payables-and-treasury/fx-management-and-hedging/examples/worked-example.md | 42 | 72951d70453c | Scenario |
| doctrine/skills/05-receivables-payables-and-treasury/fx-management-and-hedging/references/implementation-rules.md | 49 | 0738e26e1cd0 | Doctrine Boundary |
| doctrine/skills/05-receivables-payables-and-treasury/fx-management-and-hedging/references/source-basis.md | 26 | 1165f38704c7 | Evidence Discipline |
| doctrine/skills/06-close-consolidation-and-reporting/README.md | 19 | c64604a4e3db | Skills in this category |
| doctrine/skills/06-close-consolidation-and-reporting/audit-pbc-and-evidence-management/SKILL.md | 123 | 4ee5e9d784df | Audit PBC And Evidence Management |
| doctrine/skills/06-close-consolidation-and-reporting/audit-pbc-and-evidence-management/examples/worked-example.md | 42 | 31e9d5dcb855 | Scenario |
| doctrine/skills/06-close-consolidation-and-reporting/audit-pbc-and-evidence-management/references/implementation-rules.md | 49 | 44602c3d24a6 | Doctrine Boundary |
| doctrine/skills/06-close-consolidation-and-reporting/audit-pbc-and-evidence-management/references/source-basis.md | 24 | 12803ad8c643 | Evidence Discipline |
| doctrine/skills/06-close-consolidation-and-reporting/audit-ready-reporting-pack/SKILL.md | 223 | 106af0545854 | Audit-Ready Reporting Pack |
| doctrine/skills/06-close-consolidation-and-reporting/audit-ready-reporting-pack/examples/may-2026-monthly-pack.md | 54 | aacc5de1660f | Example - May 2026 Monthly Pack |
| doctrine/skills/06-close-consolidation-and-reporting/audit-ready-reporting-pack/references/auditor-export-format.md | 79 | ef5f2a48d818 | Auditor Export Format |
| doctrine/skills/06-close-consolidation-and-reporting/audit-ready-reporting-pack/references/notes-templates.md | 57 | d953052868cc | Notes Templates |
| doctrine/skills/06-close-consolidation-and-reporting/consolidation-and-intercompany/SKILL.md | 129 | f4e3de8d3e55 | Consolidation and Intercompany |
| doctrine/skills/06-close-consolidation-and-reporting/consolidation-and-intercompany/examples/elimination-entry-fixture.md | 17 | c853d2fad61e | Fixture: Elimination Entry |
| doctrine/skills/06-close-consolidation-and-reporting/consolidation-and-intercompany/examples/group-trial-balance-pack.md | 18 | a1c8742b6e77 | Fixture: Group Trial Balance Pack |
| doctrine/skills/06-close-consolidation-and-reporting/consolidation-and-intercompany/examples/two-entity-intercompany-sale.md | 21 | a9b412956c58 | Fixture: Two-Entity Intercompany Sale |
| doctrine/skills/06-close-consolidation-and-reporting/consolidation-and-intercompany/examples/unmatched-balance-exception-report.md | 12 | 4dad049d08da | Fixture: Unmatched Balance Exception Report |
| doctrine/skills/06-close-consolidation-and-reporting/consolidation-and-intercompany/references/consolidation-workflow.md | 20 | b386c5108bff | Consolidation Workflow |
| doctrine/skills/06-close-consolidation-and-reporting/consolidation-and-intercompany/references/domain-acceptance-tests.md | 13 | cb8e83d29385 | Consolidation Domain Acceptance Tests |
| doctrine/skills/06-close-consolidation-and-reporting/consolidation-and-intercompany/references/intercompany-matching-rules.md | 28 | 46583aaba891 | Intercompany Matching Rules |
| doctrine/skills/06-close-consolidation-and-reporting/continuous-close-and-flash-reporting/SKILL.md | 123 | dd8536fd0cfd | Continuous Close And Flash Reporting |
| doctrine/skills/06-close-consolidation-and-reporting/continuous-close-and-flash-reporting/examples/worked-example.md | 42 | 7e0690de2d70 | Scenario |
| doctrine/skills/06-close-consolidation-and-reporting/continuous-close-and-flash-reporting/references/implementation-rules.md | 49 | 925c9a3b1c09 | Doctrine Boundary |
| doctrine/skills/06-close-consolidation-and-reporting/continuous-close-and-flash-reporting/references/source-basis.md | 24 | 73796c27f468 | Evidence Discipline |
| doctrine/skills/06-close-consolidation-and-reporting/finance-module-audit/SKILL.md | 169 | b00ba89b7346 | Finance Module Audit |
| doctrine/skills/06-close-consolidation-and-reporting/finance-module-audit/references/audit-protocol.md | 102 | 5a6882be01ec | Audit Protocol |
| doctrine/skills/06-close-consolidation-and-reporting/finance-module-audit/references/remediation-master-plan.md | 82 | 31e616f6edd0 | Remediation Master Plan Format |
| doctrine/skills/06-close-consolidation-and-reporting/finance-module-audit/references/report-template.md | 81 | 5fef7718df6f | Audit Report Template |
| doctrine/skills/06-close-consolidation-and-reporting/finance-module-audit/references/scorecard.md | 85 | efca47325360 | Scorecard |
| doctrine/skills/06-close-consolidation-and-reporting/month-end-and-year-end-close-playbook/SKILL.md | 211 | 18971230820f | Month-End and Year-End Close Playbook |
| doctrine/skills/06-close-consolidation-and-reporting/month-end-and-year-end-close-playbook/examples/first-close-checklist.md | 35 | 5a45e303c0c5 | Example - First Close After Go-Live |
| doctrine/skills/06-close-consolidation-and-reporting/month-end-and-year-end-close-playbook/references/close-task-template.md | 164 | 8e19e3389884 | Close-Task Template |
| doctrine/skills/06-close-consolidation-and-reporting/month-end-and-year-end-close-playbook/references/year-end-extras.md | 57 | faec087dfd2e | Year-End Extras |
| doctrine/skills/06-close-consolidation-and-reporting/opening-balances-and-migration-playbook/SKILL.md | 224 | 89d328fadb6a | Opening Balances and Migration Playbook |
| doctrine/skills/06-close-consolidation-and-reporting/opening-balances-and-migration-playbook/examples/sme-cutover-pack-2026-04-30.md | 53 | 4e1fc316d3dc | Example - SME Cutover Pack 2026-04-30 |
| doctrine/skills/06-close-consolidation-and-reporting/opening-balances-and-migration-playbook/references/cutover-pack.md | 54 | b9f94d3d438b | Cutover Pack Template |
| doctrine/skills/06-close-consolidation-and-reporting/opening-balances-and-migration-playbook/references/legacy-source-extractors.md | 53 | 80be0f55ea6d | Legacy Source Extractors |
| doctrine/skills/07-financial-statements-and-disclosures/README.md | 17 | e42268f8384b | Skills in this category |
| doctrine/skills/07-financial-statements-and-disclosures/cash-flow-statement-ias7/SKILL.md | 123 | 585aeb54bc35 | Cash Flow Statement Ias7 |
| doctrine/skills/07-financial-statements-and-disclosures/cash-flow-statement-ias7/examples/worked-example.md | 42 | 20ccafc6074a | Scenario |
| doctrine/skills/07-financial-statements-and-disclosures/cash-flow-statement-ias7/references/implementation-rules.md | 49 | 2b7b2443b0eb | Doctrine Boundary |
| doctrine/skills/07-financial-statements-and-disclosures/cash-flow-statement-ias7/references/source-basis.md | 27 | f98a86c89538 | Evidence Discipline |
| doctrine/skills/07-financial-statements-and-disclosures/financial-statements-preparation/SKILL.md | 123 | 52580979d2ef | Financial Statements Preparation |
| doctrine/skills/07-financial-statements-and-disclosures/financial-statements-preparation/examples/worked-example.md | 42 | b863e78e6c3a | Scenario |
| doctrine/skills/07-financial-statements-and-disclosures/financial-statements-preparation/references/implementation-rules.md | 49 | 605b844b9f08 | Doctrine Boundary |
| doctrine/skills/07-financial-statements-and-disclosures/financial-statements-preparation/references/source-basis.md | 27 | cb4c79125dfe | Evidence Discipline |
| doctrine/skills/07-financial-statements-and-disclosures/going-concern-and-viability-assessment/SKILL.md | 123 | b6157b136cb9 | Going Concern And Viability Assessment |
| doctrine/skills/07-financial-statements-and-disclosures/going-concern-and-viability-assessment/examples/worked-example.md | 42 | 8ae7fe33ca5b | Scenario |
| doctrine/skills/07-financial-statements-and-disclosures/going-concern-and-viability-assessment/references/implementation-rules.md | 49 | 50611faffc56 | Doctrine Boundary |
| doctrine/skills/07-financial-statements-and-disclosures/going-concern-and-viability-assessment/references/source-basis.md | 27 | c72309d355b8 | Evidence Discipline |
| doctrine/skills/07-financial-statements-and-disclosures/integrated-and-sustainability-reporting-s1-s2/SKILL.md | 123 | ea24c59488af | Integrated And Sustainability Reporting S1 S2 |
| doctrine/skills/07-financial-statements-and-disclosures/integrated-and-sustainability-reporting-s1-s2/examples/worked-example.md | 42 | 8be7ef28f8d0 | Scenario |
| doctrine/skills/07-financial-statements-and-disclosures/integrated-and-sustainability-reporting-s1-s2/references/implementation-rules.md | 49 | 08e91cd349af | Doctrine Boundary |
| doctrine/skills/07-financial-statements-and-disclosures/integrated-and-sustainability-reporting-s1-s2/references/source-basis.md | 26 | 90d1ed33c536 | Evidence Discipline |
| doctrine/skills/07-financial-statements-and-disclosures/notes-and-disclosure-pack/SKILL.md | 123 | 06aab3785852 | Notes And Disclosure Pack |
| doctrine/skills/07-financial-statements-and-disclosures/notes-and-disclosure-pack/examples/worked-example.md | 42 | 8d636b805fc8 | Scenario |
| doctrine/skills/07-financial-statements-and-disclosures/notes-and-disclosure-pack/references/implementation-rules.md | 49 | 6e5c6385bd35 | Doctrine Boundary |
| doctrine/skills/07-financial-statements-and-disclosures/notes-and-disclosure-pack/references/source-basis.md | 27 | 9246d1a6d532 | Evidence Discipline |
| doctrine/skills/08-tax-and-statutory/README.md | 17 | ee9289ba251f | Skills in this category |
| doctrine/skills/08-tax-and-statutory/e-invoicing-and-fiscal-device-integration/SKILL.md | 123 | 87557dbd4b74 | E Invoicing And Fiscal Device Integration |
| doctrine/skills/08-tax-and-statutory/e-invoicing-and-fiscal-device-integration/examples/worked-example.md | 42 | 50079d276aaf | Scenario |
| doctrine/skills/08-tax-and-statutory/e-invoicing-and-fiscal-device-integration/references/implementation-rules.md | 49 | 288b0e781549 | Doctrine Boundary |
| doctrine/skills/08-tax-and-statutory/e-invoicing-and-fiscal-device-integration/references/source-basis.md | 27 | ceda1d56b0b0 | Evidence Discipline |
| doctrine/skills/08-tax-and-statutory/indirect-tax-vat-mechanics/SKILL.md | 123 | b40772b94bac | Indirect Tax VAT Mechanics |
| doctrine/skills/08-tax-and-statutory/indirect-tax-vat-mechanics/examples/worked-example.md | 42 | 5e79c1665240 | Scenario |
| doctrine/skills/08-tax-and-statutory/indirect-tax-vat-mechanics/references/implementation-rules.md | 49 | f3fb9db5b0d1 | Doctrine Boundary |
| doctrine/skills/08-tax-and-statutory/indirect-tax-vat-mechanics/references/source-basis.md | 27 | f9f42f3939a1 | Evidence Discipline |
| doctrine/skills/08-tax-and-statutory/tax-statutory-source-register-and-country-packs/SKILL.md | 130 | 68bd20ea7121 | Tax Statutory Source Register and Country Packs |
| doctrine/skills/08-tax-and-statutory/tax-statutory-source-register-and-country-packs/examples/country-pack-skeleton.md | 28 | a169c7303b79 | Example: Country Pack Skeleton |
| doctrine/skills/08-tax-and-statutory/tax-statutory-source-register-and-country-packs/examples/source-register-entry-draft.md | 27 | a081f9fdbe99 | Example: Draft Source-Register Entry |
| doctrine/skills/08-tax-and-statutory/tax-statutory-source-register-and-country-packs/examples/stale-source-rejection.md | 15 | 27dbb835cd85 | Example: Stale Source Rejection |
| doctrine/skills/08-tax-and-statutory/tax-statutory-source-register-and-country-packs/references/authority-hierarchy-east-africa.md | 16 | 5b69e8972778 | Authority Hierarchy East Africa |
| doctrine/skills/08-tax-and-statutory/tax-statutory-source-register-and-country-packs/references/country-pack-gates.md | 28 | fee5c57e4bae | Country Pack Gates |
| doctrine/skills/08-tax-and-statutory/tax-statutory-source-register-and-country-packs/references/source-register-contract.md | 38 | 39778ed79e25 | Source Register Contract |
| doctrine/skills/08-tax-and-statutory/transfer-pricing-documentation/SKILL.md | 123 | 4c7cb3a65e0f | Transfer Pricing Documentation |
| doctrine/skills/08-tax-and-statutory/transfer-pricing-documentation/examples/worked-example.md | 42 | 816ae7068c02 | Scenario |
| doctrine/skills/08-tax-and-statutory/transfer-pricing-documentation/references/implementation-rules.md | 49 | 8053a9018f6f | Doctrine Boundary |
| doctrine/skills/08-tax-and-statutory/transfer-pricing-documentation/references/source-basis.md | 27 | a11602814d95 | Evidence Discipline |
| doctrine/skills/08-tax-and-statutory/withholding-tax-and-treaties/SKILL.md | 123 | ae208dedc36d | Withholding Tax And Treaties |
| doctrine/skills/08-tax-and-statutory/withholding-tax-and-treaties/examples/worked-example.md | 42 | 734a92b304ef | Scenario |
| doctrine/skills/08-tax-and-statutory/withholding-tax-and-treaties/references/implementation-rules.md | 49 | 49b99810115e | Doctrine Boundary |
| doctrine/skills/08-tax-and-statutory/withholding-tax-and-treaties/references/source-basis.md | 27 | 455f249d706c | Evidence Discipline |
| doctrine/skills/09-budgeting-fpa-and-costing/README.md | 17 | 1d3719846c1a | Skills in this category |
| doctrine/skills/09-budgeting-fpa-and-costing/budgeting-and-rolling-forecasts/SKILL.md | 123 | ef295f68fe55 | Budgeting And Rolling Forecasts |
| doctrine/skills/09-budgeting-fpa-and-costing/budgeting-and-rolling-forecasts/examples/worked-example.md | 42 | 90060600b16c | Scenario |
| doctrine/skills/09-budgeting-fpa-and-costing/budgeting-and-rolling-forecasts/references/implementation-rules.md | 49 | c12b237bf8cb | Doctrine Boundary |
| doctrine/skills/09-budgeting-fpa-and-costing/budgeting-and-rolling-forecasts/references/source-basis.md | 26 | 66cc9ea4d291 | Evidence Discipline |
| doctrine/skills/09-budgeting-fpa-and-costing/cost-accounting-methods/SKILL.md | 123 | d07bc58e3ffc | Cost Accounting Methods |
| doctrine/skills/09-budgeting-fpa-and-costing/cost-accounting-methods/examples/worked-example.md | 42 | d640bc70d4c8 | Scenario |
| doctrine/skills/09-budgeting-fpa-and-costing/cost-accounting-methods/references/implementation-rules.md | 49 | 12f9d5775e41 | Doctrine Boundary |
| doctrine/skills/09-budgeting-fpa-and-costing/cost-accounting-methods/references/source-basis.md | 26 | 456d709fc830 | Evidence Discipline |
| doctrine/skills/09-budgeting-fpa-and-costing/pricing-discounts-rebates-and-refunds/SKILL.md | 123 | ecbd5747abad | Pricing Discounts Rebates And Refunds |
| doctrine/skills/09-budgeting-fpa-and-costing/pricing-discounts-rebates-and-refunds/examples/worked-example.md | 42 | 37d8b02a6e80 | Scenario |
| doctrine/skills/09-budgeting-fpa-and-costing/pricing-discounts-rebates-and-refunds/references/implementation-rules.md | 49 | 289597029e34 | Doctrine Boundary |
| doctrine/skills/09-budgeting-fpa-and-costing/pricing-discounts-rebates-and-refunds/references/source-basis.md | 26 | be0a90d07218 | Evidence Discipline |
| doctrine/skills/09-budgeting-fpa-and-costing/scenario-and-sensitivity-modelling/SKILL.md | 123 | 080071b82e89 | Scenario And Sensitivity Modelling |
| doctrine/skills/09-budgeting-fpa-and-costing/scenario-and-sensitivity-modelling/examples/worked-example.md | 42 | 784ee2a4de28 | Scenario |
| doctrine/skills/09-budgeting-fpa-and-costing/scenario-and-sensitivity-modelling/references/implementation-rules.md | 49 | eb5c03830a78 | Doctrine Boundary |
| doctrine/skills/09-budgeting-fpa-and-costing/scenario-and-sensitivity-modelling/references/source-basis.md | 26 | 739a7e716f99 | Evidence Discipline |
| doctrine/skills/09-budgeting-fpa-and-costing/variance-analysis-and-kpi-reporting/SKILL.md | 123 | 39c365df452e | Variance Analysis And Kpi Reporting |
| doctrine/skills/09-budgeting-fpa-and-costing/variance-analysis-and-kpi-reporting/examples/worked-example.md | 42 | 30bc1feb73be | Scenario |
| doctrine/skills/09-budgeting-fpa-and-costing/variance-analysis-and-kpi-reporting/references/implementation-rules.md | 49 | 2fb45bf9a667 | Doctrine Boundary |
| doctrine/skills/09-budgeting-fpa-and-costing/variance-analysis-and-kpi-reporting/references/source-basis.md | 26 | 8100f26e8cda | Evidence Discipline |
| doctrine/skills/10-controls-governance-and-fraud/README.md | 18 | c65af88726a2 | Skills in this category |
| doctrine/skills/10-controls-governance-and-fraud/aml-kyc-and-suspicious-transaction-reporting/SKILL.md | 123 | b2d8a1f27054 | AML KYC And Suspicious Transaction Reporting |
| doctrine/skills/10-controls-governance-and-fraud/aml-kyc-and-suspicious-transaction-reporting/examples/worked-example.md | 42 | 60b0d7e49d9c | Scenario |
| doctrine/skills/10-controls-governance-and-fraud/aml-kyc-and-suspicious-transaction-reporting/references/implementation-rules.md | 49 | 8ea66cbc460b | Doctrine Boundary |
| doctrine/skills/10-controls-governance-and-fraud/aml-kyc-and-suspicious-transaction-reporting/references/source-basis.md | 25 | a50353688299 | Evidence Discipline |
| doctrine/skills/10-controls-governance-and-fraud/engagement-quality-and-plain-language-output/SKILL.md | 131 | 4ce6582e8d42 | Engagement Quality and Plain-Language Output |
| doctrine/skills/10-controls-governance-and-fraud/engagement-quality-and-plain-language-output/examples/independence-ethics-caveat-template.md | 14 | b27912a60b8a | Example: Independence and Ethics Caveat |
| doctrine/skills/10-controls-governance-and-fraud/engagement-quality-and-plain-language-output/examples/rejected-missing-plain-language-layer.md | 18 | 578a9d8938bd | Fixture: Rejected Output Missing Plain-Language Layer |
| doctrine/skills/10-controls-governance-and-fraud/engagement-quality-and-plain-language-output/examples/sign-off-template.md | 27 | cf6106a1883d | Example: Sign-Off Template |
| doctrine/skills/10-controls-governance-and-fraud/engagement-quality-and-plain-language-output/references/plain-language-output-pattern.md | 39 | 06f413557c33 | Plain-Language Output Pattern |
| doctrine/skills/10-controls-governance-and-fraud/engagement-quality-and-plain-language-output/references/quality-and-ethics-gates.md | 28 | 58241f93801c | Quality and Ethics Gates |
| doctrine/skills/10-controls-governance-and-fraud/engagement-quality-and-plain-language-output/references/reviewer-matrix.md | 21 | 02f38bc27cd7 | Reviewer Matrix |
| doctrine/skills/10-controls-governance-and-fraud/finance-doctrine-conformance-scanner/SKILL.md | 124 | 2dd614e78cf7 | Finance Doctrine Conformance Scanner |
| doctrine/skills/10-controls-governance-and-fraud/finance-doctrine-conformance-scanner/examples/sample-scan-report.md | 29 | b09288d7b3d7 | Sample Scan Report |
| doctrine/skills/10-controls-governance-and-fraud/finance-doctrine-conformance-scanner/references/output-template.md | 55 | 1ad7bdd33212 | Output Template |
| doctrine/skills/10-controls-governance-and-fraud/finance-doctrine-conformance-scanner/references/review-rubric.md | 43 | 888f3b567040 | Review Rubric |
| doctrine/skills/10-controls-governance-and-fraud/forensic-accounting-and-anti-fraud/SKILL.md | 123 | 72dee7184ff7 | Forensic Accounting And Anti Fraud |
| doctrine/skills/10-controls-governance-and-fraud/forensic-accounting-and-anti-fraud/examples/worked-example.md | 42 | 673fd7f1f0cc | Scenario |
| doctrine/skills/10-controls-governance-and-fraud/forensic-accounting-and-anti-fraud/references/implementation-rules.md | 49 | bda71c72fa89 | Doctrine Boundary |
| doctrine/skills/10-controls-governance-and-fraud/forensic-accounting-and-anti-fraud/references/source-basis.md | 26 | 10a0b7cfe55a | Evidence Discipline |
| doctrine/skills/10-controls-governance-and-fraud/internal-controls-library/SKILL.md | 242 | c7c69afdb273 | Internal Controls Library |
| doctrine/skills/10-controls-governance-and-fraud/internal-controls-library/examples/payment-approval-flow.md | 49 | 52916d4ca571 | Example - Payment Approval Flow |
| doctrine/skills/10-controls-governance-and-fraud/internal-controls-library/references/exception-indicators.md | 49 | c27972b146dd | Exception Indicators |
| doctrine/skills/10-controls-governance-and-fraud/internal-controls-library/references/sod-conflict-matrix.md | 48 | 73ce96d73ae5 | Segregation of Duties Conflict Matrix |
| doctrine/skills/10-controls-governance-and-fraud/sox-style-icfr-documentation/SKILL.md | 123 | bf442fe77ad7 | Sox Style Icfr Documentation |
| doctrine/skills/10-controls-governance-and-fraud/sox-style-icfr-documentation/examples/worked-example.md | 42 | 4a2a519a5804 | Scenario |
| doctrine/skills/10-controls-governance-and-fraud/sox-style-icfr-documentation/references/implementation-rules.md | 49 | 87cd0899fe19 | Doctrine Boundary |
| doctrine/skills/10-controls-governance-and-fraud/sox-style-icfr-documentation/references/source-basis.md | 26 | c3a3b589cac2 | Evidence Discipline |
| doctrine/skills/10-controls-governance-and-fraud/whistleblowing-and-finance-ethics/SKILL.md | 123 | 4890674146ee | Whistleblowing And Finance Ethics |
| doctrine/skills/10-controls-governance-and-fraud/whistleblowing-and-finance-ethics/examples/worked-example.md | 42 | 8da75d1c7fa8 | Scenario |
| doctrine/skills/10-controls-governance-and-fraud/whistleblowing-and-finance-ethics/references/implementation-rules.md | 49 | c8d8089742ed | Doctrine Boundary |
| doctrine/skills/10-controls-governance-and-fraud/whistleblowing-and-finance-ethics/references/source-basis.md | 26 | c990d2a751c3 | Evidence Discipline |
| doctrine/skills/11-sector-and-fund-accounting/README.md | 20 | 694a56d245a2 | Skills in this category |
| doctrine/skills/11-sector-and-fund-accounting/agribusiness-and-cooperative-pack/SKILL.md | 123 | 2c2fecbb2a27 | Agribusiness And Cooperative Pack |
| doctrine/skills/11-sector-and-fund-accounting/agribusiness-and-cooperative-pack/examples/worked-example.md | 42 | ae02fc588bfd | Scenario |
| doctrine/skills/11-sector-and-fund-accounting/agribusiness-and-cooperative-pack/references/implementation-rules.md | 49 | 0b7b0d40aa63 | Doctrine Boundary |
| doctrine/skills/11-sector-and-fund-accounting/agribusiness-and-cooperative-pack/references/source-basis.md | 26 | cba362ed1667 | Evidence Discipline |
| doctrine/skills/11-sector-and-fund-accounting/clinic-and-healthcare-accounting-pack/SKILL.md | 123 | 2eaecb4ad64b | Clinic And Healthcare Accounting Pack |
| doctrine/skills/11-sector-and-fund-accounting/clinic-and-healthcare-accounting-pack/examples/worked-example.md | 42 | 6f419f6c4126 | Scenario |
| doctrine/skills/11-sector-and-fund-accounting/clinic-and-healthcare-accounting-pack/references/implementation-rules.md | 49 | 037eb944243d | Doctrine Boundary |
| doctrine/skills/11-sector-and-fund-accounting/clinic-and-healthcare-accounting-pack/references/source-basis.md | 26 | 3f48e3e3abf4 | Evidence Discipline |
| doctrine/skills/11-sector-and-fund-accounting/fintech-and-payments-pack/SKILL.md | 123 | d5427c59f269 | Fintech And Payments Pack |
| doctrine/skills/11-sector-and-fund-accounting/fintech-and-payments-pack/examples/worked-example.md | 42 | db0871a4c7a3 | Scenario |
| doctrine/skills/11-sector-and-fund-accounting/fintech-and-payments-pack/references/implementation-rules.md | 49 | e725cdade5d7 | Doctrine Boundary |
| doctrine/skills/11-sector-and-fund-accounting/fintech-and-payments-pack/references/source-basis.md | 26 | 78b539a101f3 | Evidence Discipline |
| doctrine/skills/11-sector-and-fund-accounting/hospitality-and-restaurant-pack/SKILL.md | 123 | 384473cc79c0 | Hospitality And Restaurant Pack |
| doctrine/skills/11-sector-and-fund-accounting/hospitality-and-restaurant-pack/examples/worked-example.md | 42 | 76d896031e28 | Scenario |
| doctrine/skills/11-sector-and-fund-accounting/hospitality-and-restaurant-pack/references/implementation-rules.md | 49 | 76c260c2046e | Doctrine Boundary |
| doctrine/skills/11-sector-and-fund-accounting/hospitality-and-restaurant-pack/references/source-basis.md | 26 | ac3b1f858a5e | Evidence Discipline |
| doctrine/skills/11-sector-and-fund-accounting/ngo-and-fund-accounting/SKILL.md | 123 | 23bef53ec827 | Ngo And Fund Accounting |
| doctrine/skills/11-sector-and-fund-accounting/ngo-and-fund-accounting/examples/worked-example.md | 42 | 194c45ac53ad | Scenario |
| doctrine/skills/11-sector-and-fund-accounting/ngo-and-fund-accounting/references/implementation-rules.md | 49 | 8d8f9436fa5a | Doctrine Boundary |
| doctrine/skills/11-sector-and-fund-accounting/ngo-and-fund-accounting/references/source-basis.md | 26 | 1c4fdce483f4 | Evidence Discipline |
| doctrine/skills/11-sector-and-fund-accounting/real-estate-and-property-pack/SKILL.md | 123 | 796436cadaab | Real Estate And Property Pack |
| doctrine/skills/11-sector-and-fund-accounting/real-estate-and-property-pack/examples/worked-example.md | 42 | ee3cf6d75fbd | Scenario |
| doctrine/skills/11-sector-and-fund-accounting/real-estate-and-property-pack/references/implementation-rules.md | 49 | 9c62eca16d2e | Doctrine Boundary |
| doctrine/skills/11-sector-and-fund-accounting/real-estate-and-property-pack/references/source-basis.md | 26 | 4e0243546dd6 | Evidence Discipline |
| doctrine/skills/11-sector-and-fund-accounting/retail-and-pos-accounting-pack/SKILL.md | 123 | d2373d227781 | Retail And POS Accounting Pack |
| doctrine/skills/11-sector-and-fund-accounting/retail-and-pos-accounting-pack/examples/worked-example.md | 42 | 786aa20a961a | Scenario |
| doctrine/skills/11-sector-and-fund-accounting/retail-and-pos-accounting-pack/references/implementation-rules.md | 49 | 98bc012a8d1c | Doctrine Boundary |
| doctrine/skills/11-sector-and-fund-accounting/retail-and-pos-accounting-pack/references/source-basis.md | 26 | bb74d7a990d3 | Evidence Discipline |
| doctrine/skills/11-sector-and-fund-accounting/school-and-education-accounting-pack/SKILL.md | 123 | 70c96fbdddd7 | School And Education Accounting Pack |
| doctrine/skills/11-sector-and-fund-accounting/school-and-education-accounting-pack/examples/worked-example.md | 42 | e9d29518cd99 | Scenario |
| doctrine/skills/11-sector-and-fund-accounting/school-and-education-accounting-pack/references/implementation-rules.md | 49 | ac4710c091d8 | Doctrine Boundary |
| doctrine/skills/11-sector-and-fund-accounting/school-and-education-accounting-pack/references/source-basis.md | 26 | 34306aa9f5a9 | Evidence Discipline |
| doctrine/skills/12-public-sector-and-ipsas/README.md | 15 | 17520f54c2a9 | Skills in this category |
| doctrine/skills/12-public-sector-and-ipsas/donor-funded-project-fiscal-compliance/SKILL.md | 123 | 113bec35abaa | Donor Funded Project Fiscal Compliance |
| doctrine/skills/12-public-sector-and-ipsas/donor-funded-project-fiscal-compliance/examples/worked-example.md | 42 | 5012fab64648 | Scenario |
| doctrine/skills/12-public-sector-and-ipsas/donor-funded-project-fiscal-compliance/references/implementation-rules.md | 49 | 2387ab7d7ac7 | Doctrine Boundary |
| doctrine/skills/12-public-sector-and-ipsas/donor-funded-project-fiscal-compliance/references/source-basis.md | 26 | 304b9b0b6f73 | Evidence Discipline |
| doctrine/skills/12-public-sector-and-ipsas/government-procurement-and-fiscal-controls/SKILL.md | 123 | 5d13fb8ef040 | Government Procurement And Fiscal Controls |
| doctrine/skills/12-public-sector-and-ipsas/government-procurement-and-fiscal-controls/examples/worked-example.md | 42 | 0abfd3c420d0 | Scenario |
| doctrine/skills/12-public-sector-and-ipsas/government-procurement-and-fiscal-controls/references/implementation-rules.md | 49 | 3e4092e3085c | Doctrine Boundary |
| doctrine/skills/12-public-sector-and-ipsas/government-procurement-and-fiscal-controls/references/source-basis.md | 26 | 01fcaa1a607e | Evidence Discipline |
| doctrine/skills/12-public-sector-and-ipsas/ipsas-public-sector-overlay/SKILL.md | 123 | 1a16357b095e | IPSAS Public Sector Overlay |
| doctrine/skills/12-public-sector-and-ipsas/ipsas-public-sector-overlay/examples/worked-example.md | 42 | 18d104f367e1 | Scenario |
| doctrine/skills/12-public-sector-and-ipsas/ipsas-public-sector-overlay/references/implementation-rules.md | 49 | 388a88ac2ae9 | Doctrine Boundary |
| doctrine/skills/12-public-sector-and-ipsas/ipsas-public-sector-overlay/references/source-basis.md | 26 | 62209697015f | Evidence Discipline |
| doctrine/skills/13-project-and-contract-accounting/README.md | 15 | 19430dddb413 | Skills in this category |
| doctrine/skills/13-project-and-contract-accounting/construction-contract-accounting/SKILL.md | 123 | 516b6fc76400 | Construction Contract Accounting |
| doctrine/skills/13-project-and-contract-accounting/construction-contract-accounting/examples/worked-example.md | 42 | 400a2ceb40eb | Scenario |
| doctrine/skills/13-project-and-contract-accounting/construction-contract-accounting/references/implementation-rules.md | 49 | fa003fcb6990 | Doctrine Boundary |
| doctrine/skills/13-project-and-contract-accounting/construction-contract-accounting/references/source-basis.md | 26 | 715e79e58396 | Evidence Discipline |
| doctrine/skills/13-project-and-contract-accounting/professional-services-time-and-materials/SKILL.md | 123 | 463483e65745 | Professional Services Time And Materials |
| doctrine/skills/13-project-and-contract-accounting/professional-services-time-and-materials/examples/worked-example.md | 42 | 34192e66c59f | Scenario |
| doctrine/skills/13-project-and-contract-accounting/professional-services-time-and-materials/references/implementation-rules.md | 49 | 312f27e12f18 | Doctrine Boundary |
| doctrine/skills/13-project-and-contract-accounting/professional-services-time-and-materials/references/source-basis.md | 26 | c9ad3690ed0a | Evidence Discipline |
| doctrine/skills/13-project-and-contract-accounting/project-and-contract-accounting/SKILL.md | 123 | 9a15a6d3867f | Project And Contract Accounting |
| doctrine/skills/13-project-and-contract-accounting/project-and-contract-accounting/examples/worked-example.md | 42 | 584bee85026c | Scenario |
| doctrine/skills/13-project-and-contract-accounting/project-and-contract-accounting/references/implementation-rules.md | 49 | 62df7022e842 | Doctrine Boundary |
| doctrine/skills/13-project-and-contract-accounting/project-and-contract-accounting/references/source-basis.md | 26 | 92e8d818c4ef | Evidence Discipline |
| doctrine/skills/14-systems-integration-and-data/README.md | 16 | 4993593c3b00 | Skills in this category |
| doctrine/skills/14-systems-integration-and-data/bank-feed-and-payment-gateway-integration/SKILL.md | 123 | bf4f0d32c1dd | Bank Feed And Payment Gateway Integration |
| doctrine/skills/14-systems-integration-and-data/bank-feed-and-payment-gateway-integration/examples/worked-example.md | 42 | 0c98028bccc3 | Scenario |
| doctrine/skills/14-systems-integration-and-data/bank-feed-and-payment-gateway-integration/references/implementation-rules.md | 49 | 905142799492 | Doctrine Boundary |
| doctrine/skills/14-systems-integration-and-data/bank-feed-and-payment-gateway-integration/references/source-basis.md | 25 | 8fd67595e750 | Evidence Discipline |
| doctrine/skills/14-systems-integration-and-data/erp-and-finance-system-integration-patterns/SKILL.md | 123 | e5a4bc6d1bdd | ERP And Finance System Integration Patterns |
| doctrine/skills/14-systems-integration-and-data/erp-and-finance-system-integration-patterns/examples/worked-example.md | 42 | 08b3180994ca | Scenario |
| doctrine/skills/14-systems-integration-and-data/erp-and-finance-system-integration-patterns/references/implementation-rules.md | 49 | 3e5675cdb7a5 | Doctrine Boundary |
| doctrine/skills/14-systems-integration-and-data/erp-and-finance-system-integration-patterns/references/source-basis.md | 25 | 2fb9cc5cb0fb | Evidence Discipline |
| doctrine/skills/14-systems-integration-and-data/finance-data-contracts-and-warehouse-models/SKILL.md | 123 | 74179823c0a3 | Finance Data Contracts And Warehouse Models |
| doctrine/skills/14-systems-integration-and-data/finance-data-contracts-and-warehouse-models/examples/worked-example.md | 42 | 5d1d861a8116 | Scenario |
| doctrine/skills/14-systems-integration-and-data/finance-data-contracts-and-warehouse-models/references/implementation-rules.md | 49 | 124e767c3348 | Doctrine Boundary |
| doctrine/skills/14-systems-integration-and-data/finance-data-contracts-and-warehouse-models/references/source-basis.md | 25 | 80f87173196f | Evidence Discipline |
| doctrine/skills/14-systems-integration-and-data/open-banking-and-direct-debit-mandates/SKILL.md | 123 | 297f2743997a | Open Banking And Direct Debit Mandates |
| doctrine/skills/14-systems-integration-and-data/open-banking-and-direct-debit-mandates/examples/worked-example.md | 42 | 6b2149ec0969 | Scenario |
| doctrine/skills/14-systems-integration-and-data/open-banking-and-direct-debit-mandates/references/implementation-rules.md | 49 | 19ec3ba4e582 | Doctrine Boundary |
| doctrine/skills/14-systems-integration-and-data/open-banking-and-direct-debit-mandates/references/source-basis.md | 25 | 0c2aa4fa0f73 | Evidence Discipline |
| doctrine/skills/15-security-privacy-and-continuity/README.md | 15 | c30d8110388c | Skills in this category |
| doctrine/skills/15-security-privacy-and-continuity/business-continuity-and-disaster-recovery-finance/SKILL.md | 123 | 7e1f65f63ae9 | Business Continuity And Disaster Recovery Finance |
| doctrine/skills/15-security-privacy-and-continuity/business-continuity-and-disaster-recovery-finance/examples/worked-example.md | 42 | 0fc58bebabc3 | Scenario |
| doctrine/skills/15-security-privacy-and-continuity/business-continuity-and-disaster-recovery-finance/references/implementation-rules.md | 49 | 6189a37afa03 | Doctrine Boundary |
| doctrine/skills/15-security-privacy-and-continuity/business-continuity-and-disaster-recovery-finance/references/source-basis.md | 25 | 171e45ad332e | Evidence Discipline |
| doctrine/skills/15-security-privacy-and-continuity/finance-cybersecurity-controls/SKILL.md | 123 | 4913434c380c | Finance Cybersecurity Controls |
| doctrine/skills/15-security-privacy-and-continuity/finance-cybersecurity-controls/examples/worked-example.md | 42 | 8faf0aaa93b9 | Scenario |
| doctrine/skills/15-security-privacy-and-continuity/finance-cybersecurity-controls/references/implementation-rules.md | 49 | eb57990ff8ee | Doctrine Boundary |
| doctrine/skills/15-security-privacy-and-continuity/finance-cybersecurity-controls/references/source-basis.md | 25 | f164624f4323 | Evidence Discipline |
| doctrine/skills/15-security-privacy-and-continuity/finance-data-privacy-and-retention/SKILL.md | 123 | b603ae4e9703 | Finance Data Privacy And Retention |
| doctrine/skills/15-security-privacy-and-continuity/finance-data-privacy-and-retention/examples/worked-example.md | 42 | 6d9c1239e736 | Scenario |
| doctrine/skills/15-security-privacy-and-continuity/finance-data-privacy-and-retention/references/implementation-rules.md | 49 | b7a334154c66 | Doctrine Boundary |
| doctrine/skills/15-security-privacy-and-continuity/finance-data-privacy-and-retention/references/source-basis.md | 25 | 34e350c27a03 | Evidence Discipline |
| doctrine/skills/16-ux-and-presentation/README.md | 16 | 5e9f843b8941 | Skills in this category |
| doctrine/skills/16-ux-and-presentation/finance-accessibility-and-inclusive-design/SKILL.md | 123 | 92329b90a1f6 | Finance Accessibility And Inclusive Design |
| doctrine/skills/16-ux-and-presentation/finance-accessibility-and-inclusive-design/examples/worked-example.md | 42 | f784c3891d25 | Scenario |
| doctrine/skills/16-ux-and-presentation/finance-accessibility-and-inclusive-design/references/implementation-rules.md | 49 | 8fa619a369bf | Doctrine Boundary |
| doctrine/skills/16-ux-and-presentation/finance-accessibility-and-inclusive-design/references/source-basis.md | 25 | c4a768b9e6e3 | Evidence Discipline |
| doctrine/skills/16-ux-and-presentation/finance-mobile-and-offline-patterns/SKILL.md | 123 | 045a2d93d1c1 | Finance Mobile And Offline Patterns |
| doctrine/skills/16-ux-and-presentation/finance-mobile-and-offline-patterns/examples/worked-example.md | 42 | 7e0a54865240 | Scenario |
| doctrine/skills/16-ux-and-presentation/finance-mobile-and-offline-patterns/references/implementation-rules.md | 49 | a0a4a2994083 | Doctrine Boundary |
| doctrine/skills/16-ux-and-presentation/finance-mobile-and-offline-patterns/references/source-basis.md | 25 | 7d7008a9f169 | Evidence Discipline |
| doctrine/skills/16-ux-and-presentation/finance-ui-pattern-library/SKILL.md | 162 | c09b38af853c | Finance UI Pattern Library |
| doctrine/skills/16-ux-and-presentation/finance-ui-pattern-library/examples/cashier-record-sale.md | 113 | ad3a8f640c53 | Example — Cashier Record-Sale Screen (Workflow Surface, Mobile) |
| doctrine/skills/16-ux-and-presentation/finance-ui-pattern-library/examples/ledger-trial-balance.md | 56 | e9a6180266df | Example - Trial Balance Ledger Surface |
| doctrine/skills/16-ux-and-presentation/finance-ui-pattern-library/examples/reconciliation-triage.md | 55 | a71f51385130 | Example - Reconciliation Triage |
| doctrine/skills/16-ux-and-presentation/finance-ui-pattern-library/references/components.md | 157 | a1ef53091508 | Component Contracts |
| doctrine/skills/16-ux-and-presentation/finance-ui-pattern-library/references/lint-checks.md | 103 | 82dcc277792c | UI Lint Checks |
| doctrine/skills/16-ux-and-presentation/finance-ui-pattern-library/references/print-stylesheet-template.md | 177 | 9dfb9d649479 | Print Stylesheet Template |
| doctrine/skills/16-ux-and-presentation/finance-ui-pattern-library/references/tokens.md | 154 | 4cf6959a3c82 | Design Tokens |
| doctrine/skills/16-ux-and-presentation/finance-ux-for-non-accountants/SKILL.md | 225 | d5ea2deb1945 | Finance UX for Non-Accountants |
| doctrine/skills/16-ux-and-presentation/finance-ux-for-non-accountants/examples/cashier-day-flow.md | 66 | b7ebf36e5857 | Example - Cashier Day Flow |
| doctrine/skills/16-ux-and-presentation/finance-ux-for-non-accountants/references/microcopy-style.md | 66 | be995129545a | Microcopy Style |
| doctrine/skills/16-ux-and-presentation/finance-ux-for-non-accountants/references/workflow-vocabulary.md | 58 | 2c7e64d2e2fb | Workflow Vocabulary |
| doctrine/skills/17-ai-automation-and-emerging/README.md | 16 | 449a1fe37478 | Skills in this category |
| doctrine/skills/17-ai-automation-and-emerging/ai-in-finance-governance/SKILL.md | 123 | 3f31bc3e3892 | AI In Finance Governance |
| doctrine/skills/17-ai-automation-and-emerging/ai-in-finance-governance/examples/worked-example.md | 42 | c820e637382d | Scenario |
| doctrine/skills/17-ai-automation-and-emerging/ai-in-finance-governance/references/implementation-rules.md | 49 | 88654c400c37 | Doctrine Boundary |
| doctrine/skills/17-ai-automation-and-emerging/ai-in-finance-governance/references/source-basis.md | 25 | f0efa850e930 | Evidence Discipline |
| doctrine/skills/17-ai-automation-and-emerging/carbon-and-emissions-accounting/SKILL.md | 123 | 423e55e689a7 | Carbon And Emissions Accounting |
| doctrine/skills/17-ai-automation-and-emerging/carbon-and-emissions-accounting/examples/worked-example.md | 42 | 907be28203c1 | Scenario |
| doctrine/skills/17-ai-automation-and-emerging/carbon-and-emissions-accounting/references/implementation-rules.md | 49 | 77271156912e | Doctrine Boundary |
| doctrine/skills/17-ai-automation-and-emerging/carbon-and-emissions-accounting/references/source-basis.md | 26 | ecf660c5dd39 | Evidence Discipline |
| doctrine/skills/17-ai-automation-and-emerging/digital-assets-and-crypto-accounting/SKILL.md | 123 | 7ec2c505e964 | Digital Assets And Crypto Accounting |
| doctrine/skills/17-ai-automation-and-emerging/digital-assets-and-crypto-accounting/examples/worked-example.md | 42 | b510365da0d0 | Scenario |
| doctrine/skills/17-ai-automation-and-emerging/digital-assets-and-crypto-accounting/references/implementation-rules.md | 49 | 177c02b1f06f | Doctrine Boundary |
| doctrine/skills/17-ai-automation-and-emerging/digital-assets-and-crypto-accounting/references/source-basis.md | 25 | dcda34e78c7d | Evidence Discipline |
| doctrine/skills/17-ai-automation-and-emerging/rpa-and-automation-controls-for-finance/SKILL.md | 123 | 516806a75be8 | RPA And Automation Controls For Finance |
| doctrine/skills/17-ai-automation-and-emerging/rpa-and-automation-controls-for-finance/examples/worked-example.md | 42 | 49b0b1f014da | Scenario |
| doctrine/skills/17-ai-automation-and-emerging/rpa-and-automation-controls-for-finance/references/implementation-rules.md | 49 | 5535b810feba | Doctrine Boundary |
| doctrine/skills/17-ai-automation-and-emerging/rpa-and-automation-controls-for-finance/references/source-basis.md | 25 | 6386643ecc0d | Evidence Discipline |
| skills/ai/ai-agent-commercial-operations/references/ai-agent-abandonment-and-refund-policy/entrypoint.md | 219 | ff34cbbb65cd | AI Agent Abandonment and Refund Policy |
| skills/ai/ai-agent-commercial-operations/references/ai-agent-abandonment-and-refund-policy/references/abandonment-taxonomy.md | 166 | fce74f19c610 | Abandonment Taxonomy |
| skills/ai/ai-agent-commercial-operations/references/ai-agent-abandonment-and-refund-policy/references/refund-execution.md | 334 | d15866566041 | Refund Execution Pipeline |
| skills/ai/ai-agent-commercial-operations/references/ai-agent-revenue-recognition/references/asc-606-for-agents.md | 172 | 634a4167053d | ASC 606 / IFRS 15 for Agent Products |
| skills/ai/ai-agent-governance-and-limits/SKILL.md | 65 | c206646360c3 | AI Agent Governance And Limits |
| skills/ai/ai-agent-governance-and-limits/references/routing.md | 9 | cf4380e74538 | Consolidated Routing |
| skills/ai/ai-agent-governance-and-limits/references/ai-agent-cost-and-step-budgets/entrypoint.md | 254 | 352e8dd17219 | AI Agent Cost and Step Budgets |
| skills/ai/ai-agent-governance-and-limits/references/ai-agent-cost-and-step-budgets/references/budget-enforcement-pipeline.md | 232 | 89f76fd29377 | Budget Enforcement Pipeline — Implementation |
| skills/ai/ai-agent-governance-and-limits/references/ai-agent-reversibility-and-blast-radius/entrypoint.md | 163 | fb573b271833 | AI Agent Reversibility and Blast-Radius |
| skills/ai/ai-agent-governance-and-limits/references/ai-agent-reversibility-and-blast-radius/references/dry-run-patterns.md | 186 | 89d2dccbd63b | Dry-Run Patterns for Agent Tools |
| skills/ai/ai-agent-governance-and-limits/references/ai-agent-reversibility-and-blast-radius/references/transactional-group-patterns.md | 172 | e51a222d779f | Transactional Group Patterns for Agent Tool Chains |
| skills/ai/ai-agent-multi-agent-coordination/references/handoff-protocols.md | 153 | e4cde064a5d3 | Agent-to-Agent Handoff Protocols |
| skills/ai/ai-agent-runtime-architecture/SKILL.md | 232 | 8f5bc1e3c7b4 | AI Agent Runtime Architecture |
| skills/ai/ai-agent-runtime-architecture/references/agent-loop-state-machine.md | 172 | 596a6cb36bd5 | Agent Loop State Machine — Formal Reference |
| skills/ai/ai-agent-runtime-architecture/references/agent-vs-workflow-vs-cron-decision.md | 101 | e82484dea728 | Agent vs Workflow vs Cron — Decision Matrix |
| skills/ai/ai-agent-runtime-architecture/references/agentic-ai-operating-model-source-synthesis.md | 121 | b5632501f3c5 | Agentic AI Operating Model Source Synthesis |
| skills/ai/ai-agent-runtime-architecture/references/routing.md | 9 | 4b99ee084121 | Consolidated Routing |
| skills/ai/ai-agent-runtime-architecture/references/ai-agent-async-and-long-running-tasks/entrypoint.md | 213 | e9272fe4bbd5 | AI Agent Async and Long-Running Tasks |
| skills/ai/ai-agent-runtime-architecture/references/ai-agent-async-and-long-running-tasks/references/durable-state-patterns.md | 265 | 7292c0206500 | Durable State Patterns for Long-Running Agent Tasks |
| skills/ai/ai-agent-runtime-architecture/references/ai-agent-memory/entrypoint.md | 210 | 34dcf420d145 | AI Agent Memory |
| skills/ai/ai-agent-runtime-architecture/references/ai-agent-memory/references/forget-on-erase-cascade.md | 207 | 7077315e9104 | Forget-on-Erase Cascade — GDPR / CCPA Through Agent Memory |
| skills/ai/ai-agent-runtime-architecture/references/ai-agent-memory/references/memory-tiers.md | 208 | f32a09f74941 | Memory Tiers — Schemas and Lifecycle |
| skills/ai/ai-agent-tooling-and-hitl/references/ai-agents-tools/entrypoint.md | 443 | 9a8405562690 | AI Agents and Tool Use — Fundamentals |
| skills/ai/ai-app-architecture/SKILL.md | 342 | 3ee15e68e3f9 | AI Application Architecture |
| skills/ai/ai-app-architecture/references/ai-transformation-operating-model.md | 87 | f0faa78d62b2 | AI Transformation Operating Model |
| skills/ai/ai-app-architecture/references/practical-ai-engineering.md | 192 | 2af885879ba4 | Practical AI Engineering |
| skills/ai/ai-app-architecture/references/routing.md | 9 | cb279ffa0c42 | Consolidated Routing |
| skills/ai/ai-app-architecture/references/ai-architecture-patterns/entrypoint.md | 352 | f75488650b6c | AI Architecture Patterns |
| skills/ai/ai-app-architecture/references/ai-on-saas-architecture/entrypoint.md | 246 | e1422f053f00 | AI on Multi-Tenant SaaS — Unifying Architecture |
| skills/ai/ai-app-architecture/references/ai-on-saas-architecture/references/control-plane-ai-services.md | 123 | be43104da601 | Control-Plane AI Services — Reference |
| skills/ai/ai-app-architecture/references/ai-on-saas-architecture/references/llm-gateway-design.md | 66 | b6fff99e5d06 | LLM Gateway Design — Reference |
| skills/ai/openai-agents-sdk/SKILL.md | 408 | 109d570f18c4 | OpenAI Agents SDK |
| skills/android/android-development/references/ai-agent-guidelines.md | 197 | 094c928a33bb | AI Agent Implementation Guidelines |
| skills/android/android-development/references/architecture-patterns.md | 252 | a492d532e30b | Architecture Patterns |
| skills/architecture/api-design-first/SKILL.md | 266 | aecf25a3802e | API Design First |
| skills/architecture/api-design-first/references/api-error-handling.md | 117 | 7169f66fce19 | Platform Notes |
| skills/architecture/api-design-first/references/api-pagination.md | 201 | 1d89d17d2a1c | Platform Notes |
| skills/architecture/api-design-first/references/api-testing-verification.md | 378 | abb5d6c12708 | API Testing Verification |
| skills/architecture/api-design-first/references/api-you-wont-hate-rules.md | 65 | fe7e5ebcd8a4 | API Rules From Practical API Building |
| skills/architecture/api-design-first/references/auth-and-security.md | 158 | 505719d392dd | Authentication, Security Headers, and Rate Limiting |
| skills/architecture/api-design-first/references/implementation-checklist.md | 61 | a574ada096f6 | Implementation Checklist and Observability Notes |
| skills/architecture/api-design-first/references/openapi-workflow.md | 169 | 2fc1a3499eae | OpenAPI Spec-First Workflow |
| skills/architecture/api-design-first/references/practical-api-architecture.md | 174 | e03010c1ac84 | Practical API Architecture |
| skills/architecture/api-design-first/references/rest-conventions.md | 151 | ff7bff958112 | REST Conventions |
| skills/architecture/api-design-first/references/skill-deep-dive.md | 11 | 2dd27edba00a | api-design-first Deep Dive (index) |
| skills/architecture/api-design-first/references/source-register-api-you-wont-hate.md | 13 | 7f52ead0d331 | API Source Register |
| skills/architecture/api-error-handling/references/contract-validation.md | 476 | 947aa4628aac | API Contract Validation - Detailed Guide |
| skills/architecture/api-error-handling/references/skill-deep-dive.md | 491 | 14b88c5bc98b | api-error-handling Deep Dive |
| skills/architecture/api-pagination/references/skill-deep-dive.md | 367 | 02989e5f2751 | api-pagination Deep Dive |
| skills/architecture/distributed-systems-patterns/SKILL.md | 182 | c634b1ef7c6f | Distributed Systems Patterns |
| skills/architecture/distributed-systems-patterns/references/consistency-decision-matrix.md | 35 | 088f5e4199ca | Consistency Decision Matrix |
| skills/architecture/distributed-systems-patterns/references/event-driven-architecture.md | 439 | cd47cb0cd3d3 | Event-Driven Architecture |
| skills/architecture/distributed-systems-patterns/references/messaging-checklist.md | 31 | 86b36804a56d | Messaging Checklist |
| skills/architecture/distributed-systems-patterns/references/realtime-systems.md | 425 | 645a126a796c | Real-Time Systems |
| skills/architecture/ecommerce-platform-audit-requirements/SKILL.md | 79 | 3d1020cfb31c | E-Commerce Platform Audit Requirements |
| skills/architecture/ecommerce-platform-audit-requirements/references/audit-scope-and-standards.md | 42 | 937e0c1da66c | Audit Scope and Standards |
| skills/architecture/ecommerce-platform-audit-requirements/references/eac-data-protection-table.md | 23 | 6abf194fa75d | EAC Data Protection Table |
| skills/architecture/ecommerce-platform-audit-requirements/references/remediation-backlog-template.md | 30 | 3a842efd5b57 | Remediation Backlog Template |
| skills/architecture/graphql-patterns/SKILL.md | 498 | 28c49f5ee244 | GraphQL Patterns (Apollo + TypeScript) |
| skills/architecture/graphql-patterns/references/graphql-security.md | 406 | 3de1517ea221 | GraphQL Security Hardening |
| skills/architecture/microservices-ai-integration/ALIAS.md | 373 | 676d6b459edd | Microservices AI Integration |
| skills/architecture/microservices-architecture/SKILL.md | 61 | 2425c3276c7f | Microservices Architecture |
| skills/architecture/microservices-architecture/references/microservices-architecture-models.md | 469 | ce6ae6883ac7 | Microservices Architecture Models |
| skills/architecture/microservices-architecture/references/microservices-communication.md | 499 | 64460e4dca49 | Microservices Communication |
| skills/architecture/microservices-architecture/references/microservices-fundamentals.md | 229 | 30dd43dea8cb | Microservices Fundamentals |
| skills/architecture/microservices-architecture/references/microservices-resilience.md | 331 | 3ee57bb7824f | Microservices Resilience |
| skills/architecture/microservices-architecture-models/references/proxy-gateway-ops.md | 200 | 9d3a4c431e31 | Reverse-Proxy and API-Gateway Ops — Deep Dive |
| skills/architecture/microservices-communication/references/workflow-engines.md | 291 | 6cea2c9c2f0b | Workflow Automation Engines — Deep Reference |
| skills/architecture/orchestration-best-practices/references/skill-deep-dive.md | 115 | bcfea996c577 | orchestration-best-practices Deep Dive |
| skills/architecture/system-architecture-design/SKILL.md | 235 | a51a5d38049b | System Architecture Design |
| skills/architecture/system-architecture-design/references/adr-template.md | 39 | 92ab0de27ea3 | ADR Template |
| skills/architecture/system-architecture-design/references/architecture-execution-model.md | 19 | e7c23107e32c | Architecture Execution Model |
| skills/architecture/system-architecture-design/references/practical-architecture-knowledge.md | 238 | 7d7ba2d27995 | Practical Architecture Knowledge |
| skills/architecture/validation-contract/SKILL.md | 158 | 941fdf8896ea | Validation Contract |
| skills/architecture/validation-contract/references/declaration-form.md | 62 | a38e39828fee | Declaration Form — `## Evidence Produced` |
| skills/architecture/validation-contract/references/evidence-categories.md | 98 | 993d6c479259 | Evidence Categories |
| skills/architecture/validation-contract/references/integration-rollout.md | 40 | a44c7c82402f | Integration Rollout — Audit Trail |
| skills/architecture/validation-contract/references/release-evidence-bundle-template.md | 69 | 2994dfdcffd5 | Release Evidence Bundle — Template |
| skills/backend-databases/mysql-best-practices/references/indexing-deep-dive.md | 417 | 732cb82a9ee7 | MySQL Indexing Deep Dive |
| skills/devops-cloud/cicd-devsecops/references/security-gate-governance.md | 22 | 521a4f66976e | Security Gate Governance |
| skills/devops-cloud/cicd-pipeline-design/references/pipeline-governance.md | 18 | 1912a03367bc | Pipeline Governance |
| skills/devops-cloud/cicd-pipelines/references/anti-patterns.md | 117 | 5eb65127149c | CI/CD Anti-Patterns: Broken vs Fixed |
| skills/devops-cloud/cicd-pipelines/references/reference-architectures.md | 168 | e647c75148ac | Three Reference Architectures |
| skills/devops-cloud/cloud-architecture/SKILL.md | 383 | d5027e94251e | Cloud Architecture |
| skills/devops-cloud/cloud-architecture/references/aws-core-services.md | 269 | 8a70d88f58e5 | AWS Core Services — CLI Reference |
| skills/devops-cloud/cloud-architecture/references/deployment-patterns.md | 159 | c7303a3eda6c | Deployment Patterns — Runbooks |
| skills/devops-cloud/cloud-architecture/references/docker-compose-patterns.md | 167 | 467bdbc362c3 | Docker Compose Patterns |
| skills/devops-cloud/cloud-architecture/references/environment-management.md | 50 | d628c869099d | Staging / Production Environment Management |
| skills/devops-cloud/cloud-architecture/references/github-actions-overview.md | 84 | 585aacaef620 | GitHub Actions CI/CD — Overview Reference |
| skills/devops-cloud/kubernetes-fundamentals/references/anti-patterns.md | 167 | 41a1828ceec3 | Kubernetes Anti-Patterns |
| skills/finance-accounting/finance/finance-module-audit/references/audit-protocol.md | 102 | 5a6882be01ec | Audit Protocol |
| skills/finance-accounting/finance/finance-ui-pattern-library/references/print-stylesheet-template.md | 177 | 9dfb9d649479 | Print Stylesheet Template |
| skills/frontend-ux/image-compression/references/quality-metrics.md | 11 | e4414d7838ae | Quality vs Size (Example) |
| skills/frontend-ux/image-compression/references/readme-notes.md | 6 | e8f35afd52ee | Notes |
| skills/frontend-ux/nextjs-app-router/SKILL.md | 461 | 1709c171658f | Next.js App Router Patterns |
| skills/frontend-ux/pos-restaurant-ui-standard/ALIAS.md | 445 | e53bf4dfb356 | Platform Notes |
| skills/frontend-ux/pos-restaurant-ui-standard/references/restaurant-pos-ui-standard.md | 63 | b7502ca59b2a | Restaurant POS UI Standard (Reference) |
| skills/gis/gis-mapping/references/leaflet-arcgis-equivalents/integration-guide.md | 69 | dfb476dc8c2d | Integration Guide |
| skills/gis/gis-postgis-backend/references/spatial-indexes.md | 180 | b1eb0e7e2965 | Spatial Indexes |
| skills/ios/ios-architecture/SKILL.md | 63 | c12fd30af408 | iOS Architecture |
| skills/ios/ios-architecture/references/app-intelligence-architecture-wwdc26.md | 61 | 9ee3d37987d6 | App Intelligence Architecture WWDC26 |
| skills/ios/ios-architecture/references/ios-architecture-advanced.md | 193 | 9ec16e643b8e | iOS Architecture — Advanced |
| skills/ios/ios-architecture/references/ios-at-scale.md | 484 | 379da9a30cb7 | iOS Development at Scale |
| skills/ios/ios-architecture/references/ios-production-patterns.md | 128 | 920fa4d31629 | iOS Production Patterns |
| skills/ios/ios-architecture/references/ios-swift-design-patterns.md | 163 | ac7129cac858 | iOS Swift Design Patterns |
| skills/ios/ios-architecture/references/ios-architecture-advanced/skill-deep-dive.md | 350 | ff099890036b | ios-architecture-advanced Deep Dive |
| skills/ios/ios-architecture/references/ios-production-patterns/skill-deep-dive.md | 430 | d4bb3eb89d85 | ios-production-patterns Deep Dive |
| skills/ios/ios-architecture/references/ios-swift-design-patterns/skill-deep-dive.md | 396 | 775868e54e4d | ios-swift-design-patterns Deep Dive |
| skills/ios/ios-data-persistence/references/semantic-indexing-and-ai-caches-wwdc26.md | 57 | 5cd216efd73a | Semantic Indexing And AI Caches WWDC26 |
| skills/ios/ios-quality-and-release/SKILL.md | 63 | 9d2eb9576e8b | iOS Quality And Release |
| skills/ios/ios-quality-and-release/references/app-store-review.md | 115 | 97baaa572611 | Platform Notes |
| skills/ios/ios-quality-and-release/references/ios-debugging-mastery.md | 464 | 72bd3b18adaa | iOS Debugging Mastery |
| skills/ios/ios-quality-and-release/references/ios-stability-solutions.md | 107 | e60b6173d744 | iOS Stability Solutions Guide |
| skills/ios/ios-quality-and-release/references/ios-tdd.md | 121 | 0aaa627a857f | Platform Notes |
| skills/ios/ios-quality-and-release/references/wwdc26-quality-release.md | 65 | 7ec8182ca032 | WWDC26 Quality And Release |
| skills/ios/ios-quality-and-release/references/app-store-review/skill-deep-dive.md | 440 | 660410753dcc | app-store-review Deep Dive |
| skills/ios/ios-quality-and-release/references/ios-stability-solutions/skill-deep-dive.md | 474 | c070261bb5e0 | ios-stability-solutions Deep Dive |
| skills/ios/ios-quality-and-release/references/ios-tdd/advanced-tdd-patterns.md | 434 | 1f1f5abf1ba2 | Advanced TDD Patterns |
| skills/ios/ios-quality-and-release/references/ios-tdd/architecture-testing.md | 161 | 06229c870805 | Architecture Pattern Testing |
| skills/ios/ios-quality-and-release/references/ios-tdd/skill-deep-dive.md | 492 | e72b0162162b | ios-tdd Deep Dive |
| skills/languages/language-standards/references/business-english-advanced.md | 442 | f8138a94bf82 | Business English Advanced Masterclass — Reference Notes |
| skills/languages/language-standards/references/skill-deep-dive.md | 500 | 75b17bcea135 | language-standards Deep Dive |
| skills/languages/php-modern-standards/SKILL.md | 159 | 987483b5aa10 | PHP Modern Standards |
| skills/languages/php-modern-standards/references/attack-prevention.md | 328 | 04d9e2529f33 | Attack Prevention Patterns |
| skills/languages/php-modern-standards/references/cache-invalidation.md | 378 | d4d178a19088 | Cache Invalidation Strategies for PHP |
| skills/languages/php-modern-standards/references/code-quality-tooling.md | 464 | e87941c17810 | PHP Code Quality & Tooling Reference |
| skills/languages/php-modern-standards/references/database-orm-patterns.md | 461 | 23cb9d85fb79 | Database & ORM Patterns |
| skills/languages/php-modern-standards/references/javascript-php-integration.md | 441 | 081ac1d43856 | JavaScript + PHP Integration |
| skills/languages/php-modern-standards/references/message-queues.md | 358 | 8030c091bd42 | Message Queues & Async Processing for PHP |
| skills/languages/php-modern-standards/references/performance-efficiency.md | 516 | 5ec878aad022 | PHP Performance & Efficiency Reference |
| skills/languages/php-modern-standards/references/php-security.md | 395 | ee8ccc1c32e8 | PHP Security |
| skills/languages/php-modern-standards/references/php-vs-nextjs.md | 260 | 821c98a978fa | PHP vs Next.js: Technology Decision Framework |
| skills/languages/php-modern-standards/references/rate-limiting.md | 309 | d089ff8ba0a1 | Rate Limiting Algorithms for PHP |
| skills/languages/php-modern-standards/references/resilience-patterns.md | 364 | 7d52dd64ec7b | Resilience Patterns for PHP Services |
| skills/languages/php-modern-standards/references/restful-api-patterns.md | 423 | 371e847fd7bb | RESTful API Patterns |
| skills/languages/php-modern-standards/references/security-patterns.md | 30 | 04ff1da4693e | Security Patterns — Cross-Reference |
| skills/languages/php-modern-standards/references/skill-deep-dive.md | 455 | 5b5e04f29c11 | php-modern-standards Deep Dive |
| skills/languages/php-modern-standards/references/source-register-dev-engine.md | 19 | 0f0c3c694aff | Development Engine Source Register |
| skills/languages/php-modern-standards/references/world-class-php-oop-clean-architecture.md | 66 | 73a485335e1a | World-Class PHP OOP And Clean Architecture |
| skills/languages/python-data-analytics/references/analytics-method-selection-and-governance.md | 122 | 8dd2b28ddcf4 | Analytics Method Selection and Governance |
| skills/languages/python-data-pipelines/references/pipeline-architecture.md | 210 | dc3bc10b4d9a | Pipeline Architecture |
| skills/languages/python-modern-standards/SKILL.md | 351 | 0854ac98f9ee | Python Modern Standards |
| skills/languages/python-modern-standards/references/anti-patterns.md | 438 | e488d4bdce63 | Anti-Patterns |
| skills/languages/python-modern-standards/references/api-container-sidecar-engineering.md | 45 | 14eaf5de8b40 | API And Container Sidecar Engineering For Python |
| skills/languages/python-modern-standards/references/async-vs-sync.md | 183 | 766f554ab181 | Async vs Sync |
| skills/languages/python-modern-standards/references/error-handling.md | 302 | 15caabf85d49 | Error Handling |
| skills/languages/python-modern-standards/references/logging-structlog.md | 265 | 79eb358f33c9 | Logging with structlog |
| skills/languages/python-modern-standards/references/project-layout.md | 233 | acca2157f970 | Project Layout |
| skills/languages/python-modern-standards/references/pydantic-v2-patterns.md | 271 | 99358b2ab687 | Pydantic v2 Patterns |
| skills/languages/python-modern-standards/references/python-saas-integration.md | 331 | d9142e48bd25 | Python SaaS Integration |
| skills/languages/python-modern-standards/references/security-baseline.md | 339 | aaea39a4a320 | Security Baseline |
| skills/languages/python-modern-standards/references/testing-pytest.md | 299 | 6ec25a1f0a0a | Testing with pytest |
| skills/languages/python-modern-standards/references/tooling-uv-ruff.md | 201 | fc8c597ecdff | Tooling: uv, ruff, pre-commit, CI |
| skills/languages/python-modern-standards/references/typing-mypy-pyright.md | 288 | f019fc900582 | Typing: mypy --strict and pyright |
| skills/languages/typescript-effective/references/anti-patterns.md | 393 | 2d2498d0be36 | TypeScript anti-patterns |
| skills/mobile-cross/mobile-platform-operations/references/mobile-saas-planning/architecture-patterns.md | 472 | c2afbd4c0979 | Architecture & Code Patterns Reference |
| skills/product-business/content-writing/references/blog-writer/references/editorial-standards.md | 325 | f1a68358c764 | Editorial Standards Reference — Blog Writer Skill |
| skills/product-business/content-writing/references/blog-writer/references/human-voice-standards.md | 319 | 53088d1deb3b | Human Voice Standards — Anti-AI Writing Reference |
| skills/product-business/customer-service-excellence/references/service-quality-measurement.md | 118 | 338221969c66 | Service Quality Measurement |
| skills/product-business/excel-spreadsheets/references/design-standards.md | 306 | f71b07a55164 | Excel Design Standards |
| skills/product-business/excel-spreadsheets/references/quality-checklist.md | 99 | cbc812dbbbf3 | Excel Quality Checklist |
| skills/product-business/growth-telemetry-pipeline/references/anti-patterns-catalog.md | 46 | 28604844c3c2 | Anti-Patterns Catalog |
| skills/product-business/product-discovery/references/feature-planning/protocols/naming-convention.md | 14 | a0ad098bbcd4 | Naming Convention — docs/plans |
| skills/product-business/product-discovery/references/feature-planning/references/06-creating-plans-guide.md | 100 | f148527bffa6 | 🎯 Creating a Plan: Step-by-Step |
| skills/product-business/product-strategy-vision/references/verganti-overcrowded.md | 205 | 058ea68ef862 | Overcrowded — Roberto Verganti (MIT Press, 2016) |
| skills/product-business/professional-word-output/references/quality-checklist.md | 99 | f54eb681dba7 | Professional Word Document — Quality Checklist |
| skills/product-business/professional-word-output/references/manual-guide/entrypoint.md | 248 | 26da9989091a | Platform Notes |
| skills/product-business/professional-word-output/references/python-document-generation/references/branding-system.md | 270 | 6d65a774f758 | Branding System |
| skills/saas/modular-saas-architecture/SKILL.md | 361 | 4ae8cac519b9 | Modular SAAS Architecture |
| skills/saas/modular-saas-architecture/documentation/implementation-guide.md | 724 | 45b2b17b0969 | Modular SAAS Implementation Guide |
| skills/saas/modular-saas-architecture/references/database-schema.md | 414 | 9e43b1535126 | Modular SAAS Database Schema |
| skills/saas/modular-saas-architecture/references/implementation.md | 218 | 6d6bd3f577d4 | Modular SaaS — Full Implementation Reference |
| skills/saas/multi-tenant-saas-architecture/SKILL.md | 446 | ce93f02dabf7 | Multi-Tenant SaaS Architecture |
| skills/saas/multi-tenant-saas-architecture/documentation/migration.md | 263 | 3c7f7eae6544 | Migration Patterns for Multi-Tenant SaaS |
| skills/saas/multi-tenant-saas-architecture/references/database-schema.md | 220 | 35b48d9326f7 | Database Schema Reference |
| skills/saas/multi-tenant-saas-architecture/references/permission-model.md | 353 | 17327d782307 | RBAC Permission Model |
| skills/saas/multi-tenant-saas-architecture/references/saas-deployment-models-decision-tree.md | 66 | 9a71ea4009dd | SaaS Deployment Models — Decision Tree (Reference) |
| skills/saas/multi-tenant-saas-architecture/references/tenant-context-propagation.md | 136 | b10b2da9d4fe | Tenant Context Propagation — Reference |
| skills/saas/saas-architecture-strategy/SKILL.md | 86 | b53ab758328e | SaaS Architecture Strategy |
| skills/saas/saas-architecture-strategy/references/architecture-to-business-capability-map.md | 118 | c68358862d9b | Architecture to Business Capability Map |
| skills/saas/saas-architecture-strategy/references/deployment-mapping-and-iaas-assumptions.md | 106 | 80217005d809 | Deployment Mapping and IaaS Assumptions |
| skills/saas/saas-architecture-strategy/references/multi-tenant-consumption-models.md | 105 | 35c4a5eb86c0 | Multi-Tenant Consumption Models |
| skills/saas/saas-architecture-strategy/references/saas-maturity-matrix.md | 72 | 0ad544b52f94 | SaaS Maturity Matrix — Reference |
| skills/saas/saas-architecture-strategy/references/saas-strategy-anti-patterns.md | 148 | 56d8b0a31463 | SaaS Architecture Anti-Patterns |
| skills/saas/saas-architecture-strategy/references/scaling-and-blast-radius.md | 122 | a45113a83ece | Scaling and Blast Radius |
| skills/saas/saas-seeder/references/architecture.md | 247 | e3afc3fdcde3 | SaaS Seeder Architecture Standards |
| skills/sdlc-meta/anti-ai-slop/SKILL.md | 110 | 5b2106dcf25d | Anti AI Slop |
| skills/sdlc-meta/custom-sub-agents/ALIAS.md | 142 | 6146e45bb65f | Platform Notes |
| skills/sdlc-meta/custom-sub-agents/references/01-agent-folder-structure.md | 783 | 433720e4545a | 📁 Agent Folder Structure - Complete Guide |
| skills/sdlc-meta/custom-sub-agents/references/02-agent-config-documentation.md | 661 | c435c5f4ef75 | ⚙️ Agent Configuration & Documentation |
| skills/sdlc-meta/custom-sub-agents/references/03-entry-points-patterns.md | 567 | 0f597fd0bc74 | 📄 Entry Points & Export Patterns |
| skills/sdlc-meta/custom-sub-agents/references/04-testing-tools.md | 1616 | 922183e562db | 🧪 Testing & Utility Frameworks |
| skills/sdlc-meta/custom-sub-agents/references/05-advanced-patterns.md | 2573 | 482c232902c6 | 🚀 Advanced Patterns & Orchestration |
| skills/sdlc-meta/custom-sub-agents/references/06-parent-sub-agent.md | 1826 | 75a627d30d0d | 🏗️ Parent & Sub-Agent Architecture |
| skills/sdlc-meta/custom-sub-agents/references/07-project-organization.md | 2012 | 299ffa7f8245 | 🏗️ Project Organization & Registry Patterns |
| skills/sdlc-meta/custom-sub-agents/references/08-integration-deployment.md | 1787 | 498cb4ffa58f | 🚀 Integration & Deployment Patterns |
| skills/sdlc-meta/custom-sub-agents/references/CUSTOM_SUB_AGENTS_GUIDE.md | 87 | 82457e70e32a | Custom Sub-Agents Guide |
| skills/sdlc-meta/doc-architect/protocols/workflow.md | 41 | af9c414a5263 | Doc Architect Workflow |
| skills/sdlc-meta/engineering-strategy/references/strategy-altitude-and-policy.md | 86 | a4868a2b45a2 | Strategy Altitude and Guiding Policy |
| skills/sdlc-meta/engineering-strategy/references/strategy-anti-patterns.md | 95 | 61dab55891e4 | Strategy Anti-Patterns |
| skills/sdlc-meta/sdlc-design/templates/code-documentation-standards.md | 475 | d252c226068e | Code Documentation Standards -- Template & Guide |
| skills/sdlc-meta/sdlc-planning/templates/quality-assurance-plan.md | 309 | a8632a7225f1 | Quality Assurance Plan — Template & Guide |
| skills/sdlc-meta/sdlc-user-deploy/templates/readme-file.md | 390 | f1a7c4949290 | README File Template |
| skills/sdlc-meta/skill-composition-standards/SKILL.md | 332 | 731605aa81e5 | Skill Composition Standards |
| skills/sdlc-meta/skill-composition-standards/references/access-patterns-template.md | 89 | 9f5199e89641 | Access Patterns Template |
| skills/sdlc-meta/skill-composition-standards/references/adr-template.md | 80 | 0cd6c119bcb2 | ADR Template |
| skills/sdlc-meta/skill-composition-standards/references/baseline-contract-register.md | 164 | e56fab9bffce | Baseline Contract Register |
| skills/sdlc-meta/skill-composition-standards/references/context-map-template.md | 88 | 253de8310ffe | Context Map Template |
| skills/sdlc-meta/skill-composition-standards/references/critical-flow-template.md | 69 | 3954780b1118 | Critical-Flow Template |
| skills/sdlc-meta/skill-composition-standards/references/delivery-definition-of-done.md | 114 | de334de09b0b | Delivery Definition of Done - the handoff gate |
| skills/sdlc-meta/skill-composition-standards/references/entity-model-template.md | 119 | 52b2877b9457 | Entity Model Template |
| skills/sdlc-meta/skill-composition-standards/references/error-model.md | 94 | 58e5c4826453 | Error Model Template |
| skills/sdlc-meta/skill-composition-standards/references/house-style-checklist.md | 75 | 079a96ca60aa | House-Style Checklist |
| skills/sdlc-meta/skill-composition-standards/references/migration-plan-template.md | 136 | 18423b6f774c | Migration Plan Template |
| skills/sdlc-meta/skill-composition-standards/references/normalisation-playbook.md | 201 | 7bbd3a9aafbb | Normalisation Playbook |
| skills/sdlc-meta/skill-composition-standards/references/openapi-contract.md | 122 | 7c1fdf097504 | OpenAPI Contract Template |
| skills/sdlc-meta/skill-composition-standards/references/orchestration-best-practices.md | 452 | fe08d50e2838 | Platform Notes |
| skills/sdlc-meta/skill-composition-standards/references/release-plan-template.md | 110 | 78b5dbddc11a | Release Plan Template |
| skills/sdlc-meta/skill-composition-standards/references/rollback-plan-template.md | 111 | a21682ba4b84 | Rollback Plan Template |
| skills/sdlc-meta/skill-composition-standards/references/runbook-template.md | 164 | 30be2b9ca134 | Runbook Template |
| skills/sdlc-meta/skill-composition-standards/references/slo-template.md | 82 | 36c232729811 | SLO Template |
| skills/sdlc-meta/skill-composition-standards/references/test-plan-template.md | 121 | 70d43868076c | Test Plan Template |
| skills/sdlc-meta/skill-composition-standards/references/threat-model-template.md | 139 | c104eee92eb4 | Threat Model Template |
| skills/sdlc-meta/update-claude-documentation/SKILL.md | 381 | ea4ec0fc5bde | Platform Notes |
| skills/sdlc-meta/update-claude-documentation/references/module-header-template.md | 39 | 00f8952d22e2 | Module Header Template (Claude Friendly) |
| skills/sdlc-meta/world-class-engineering/references/language-standards.md | 113 | 218c9826e0b1 | Language Standards — Multi-Language Tone & Grammar |
