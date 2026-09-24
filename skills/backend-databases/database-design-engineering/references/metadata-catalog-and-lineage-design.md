# Metadata Catalog and Lineage Design

Parent skill: [database-design-engineering](../SKILL.md).

Load when you design, select, populate, or audit a data catalog, business
glossary, classification scheme, or lineage capability, or when catalog metadata
must feed AI assistants, retrieval pipelines, or agents. Contract authoring is in
`data-contracts-and-schema-evolution.md`; lineage emission code is in
`../../../languages/python-data-pipelines/references/data-quality-checks-and-lineage.md`.
Requirements for a catalog (what it must achieve) belong in the SRS engine:
`02-requirements-engineering/fundamentals/during/05-conceptual-data-modeling/references/data-governance-catalog-lineage-requirements.md`.

## 1. Design stance

A catalog is a search engine over metadata, not a spreadsheet of tables. It holds
no data values, which is why it can be open to every employee while the data
itself stays access-controlled. Judge every design decision by one test: can a
person, or an agent, who has never met the owner find the right asset, understand
it, trust it, and request access within minutes?

## 2. Metamodel first

Write the metamodel (entity types and relations) before connecting any source.

| Entity | Minimum relations |
|---|---|
| Domain | contains data sources and data products; has domain owner and steward |
| Data source (generic, e.g. "PostgreSQL", "Power BI") | has specific instances |
| Data source instance | belongs to one domain; has a source owner; contains assets |
| Asset (table, file, report, topic, model) | has columns or fields; has owner, steward, description, glossary terms, classifications; lineage upstream and downstream |
| Data product | published through a data contract; independent of any one application; has consumers |
| Glossary term | defined by a term owner; has status; related terms, synonyms, acronyms |
| Person or role | owns, stewards, or consumes the above |

Prefer a catalog built on a graph model: relations such as "term X is used by
product Y, which feeds model Z" are the questions people and agents actually ask,
and a flexible metamodel lets you add entity types without migration.

## 3. Organising domains

1. Choose one organising principle for the top layers: business **capabilities**
   (what the organisation does) if enterprise architecture already maintains a
   capability map; **processes** (how it does it) if a controlled process map
   exists, as it does in regulated manufacturing, food, or pharma. Never mix the two.
2. Do not copy the organisation chart. Departments merge and split every year; a
   capability such as "Loan Portfolio Management" survives restructures.
3. Beneath the capability or process layer, register the generic data source,
   then each specific instance. The same product (say, one BI tool) serves many
   capabilities through different instances or workspaces.
4. Keep one root. Every asset lands in exactly one place; secondary views come
   from glossary terms and classifications, not duplicate placement.

## 4. Metadata an asset must carry

| Group | Fields | Source |
|---|---|---|
| Technical | system, location, format, schema, created, updated, row or file counts | Harvested by connector (pull) or published by the producer (push) |
| Descriptive | description with primary use (why it exists) and secondary use (who else could use it) | Asset steward |
| Ownership | domain owner, asset owner, steward | Domain owner |
| Glossary | global terms, domain terms, free tags | Steward; free tags by any user |
| Classification | content, confidentiality, sensitivity (Section 5) | Steward, checked by DPO and security |
| Contract | contract id, version, status, SLOs | Data contract, never retyped |
| Lineage | upstream and downstream edges, column level where regulated | Lineage events, never drawn by hand |
| Quality | latest check results and SLO attainment | Check runs |

Push beats pull for data products: the contract publishes its own catalog entry
on merge, so the catalog cannot drift from the interface.

A glossary is not a data dictionary. The data dictionary lists fields and their
technical meaning; the glossary defines business concepts and links them to
many assets.

## 5. Three independent classifications

Classify every asset on three separate axes; combine them freely.

| Axis | Question | Owner | Example values |
|---|---|---|---|
| Content | What is this data about? | Domain | Code path such as `LEND/PORTFOLIO/REPAYMENTS` |
| Confidentiality | How much damage if it leaked? | Security (CISO) | public, internal, confidential, restricted |
| Sensitivity | Does it relate to an identifiable person, and is it special personal data? | Data protection officer | non-personal, personal, special personal |

A payroll forecast can be highly confidential and non-personal; a public staff
directory is personal but not confidential. Collapsing the axes into one label
produces wrong access decisions. Under Uganda's Data Protection and Privacy Act
2019, special personal data is a defined category with its own restrictions
(section 9); map the sensitivity axis to the Act's definitions, not to a vendor default.

Column names are metadata that can leak: a column named after a medical
condition discloses more than its values' absence suggests. Review harvested
names before making a source visible catalog-wide.

## 6. Lifecycles to operate

**Asset lifecycle.** Create domain -> harvest or publish the asset -> review
automatically detected personal data and set the three classifications -> add
description, terms, owner -> verify lineage is live -> discoverable -> shared ->
derived assets registered downstream -> maintained (renames, term changes,
ownership changes) -> archived when the source is decommissioned.

**Glossary term lifecycle.** Draft -> reviewed by term or domain owner ->
approved and published -> applied to assets -> revised (related terms,
synonyms) -> replaced or deleted, with the history kept searchable.

**Source lifecycle.** A system decommissioning triggers a catalog query for its
confidential and regulated assets, which drives what must be migrated or
retained and what may be destroyed. The catalog itself is a system; archive its
metamodel and content when it is replaced.

## 7. Metadata quality

Measure the catalog, not only the data.

| Measure | Definition | Target to agree with the owner |
|---|---|---|
| Coverage | Assets in scope that are registered | Stated per domain |
| Curation completeness | Registered assets with owner, description, at least one approved term, and all three classifications | Stated per domain |
| Depth fit | Assets tagged at the most specific applicable term rather than a broad parent | Sampled review |
| Lineage liveness | Assets whose lineage updated within the expected run interval | Per feed schedule |
| Findability | Share of scripted discovery tasks completed within a time limit by users new to the domain | Usability test result |

An uncurated asset is not neutral: it dilutes search results for everything else.
Set a rule that raw assets older than an agreed period without an owner are hidden
from default search.

## 8. Metadata for AI assistants, retrieval, and agents

The catalog becomes a source for AI, not just a directory. Design for that deliberately.

1. **Ground answers in governed metadata.** Assistants that answer "which table
   holds X" or "who owns Y" retrieve from the catalog's graph and cite asset ids;
   they must not guess from model memory.
2. **Carry AI guidance in the contract.** ODCS v3.2.0 adds an optional `context`
   block at contract and schema-object level with `instructions`, `constraints`
   (negative guidance, such as "never sum amount across currencies"), and
   `verifiedStatements` (canonical questions with verified answers). Populate it
   for every product exposed to an agent or text-to-SQL tool, and test the
   agent against the verified statements.
3. **Filter by classification before retrieval.** Retrieval over catalog metadata
   or over documents indexed from it applies the caller's access rights and the
   sensitivity axis first; similarity ranking runs on what remains.
4. **Expose through a protocol with consent and least privilege.** When agents
   reach the catalog through the Model Context Protocol, publish read-only search
   and lookup as tools or resources, keep access requests as a separate tool that
   requires human approval, and treat tool descriptions from third-party servers as untrusted.
5. **Record provenance.** For every AI answer built from catalog content, log
   which assets, terms, and contract versions were retrieved, so a wrong answer
   can be traced to stale metadata or a retrieval fault.
6. **Keep metadata fresh enough for the model's job.** An agent acting on a
   deprecated contract is a defect; exclude `deprecated` and `retired` products
   from default agent retrieval.

Cross-links: `../../../ai/ai-rag-patterns/SKILL.md` for retrieval design and
`../../../ai/ai-agent-tooling-and-hitl/SKILL.md` for tool permission design.

## 9. Selection and anti-patterns

Choose a catalog by capability (lineage depth, push API for contracts,
classification model, graph metamodel, access-request workflow, API for bulk
curation, AI search with citations), not by vendor list. Implement one catalog.
A catalog of catalogs is justified only to unite earlier isolated catalogs,
separate legal entities, or sources a single catalog cannot reach.

- Domains mirrored from the organisation chart. Fix: capabilities or processes.
- One "classification" field. Fix: three axes with different owners.
- Hand-drawn lineage. Fix: event-driven lineage; manual steps only to activate harvesting.
- Catalog entries retyped from the contract. Fix: publish from the contract on merge.
- AI assistant answering from the catalog without access filtering. Fix: filter by caller rights and sensitivity before ranking.
- Descriptions that restate the table name. Fix: state primary use, secondary use, grain, and known limitations.

## Evidence/currentness

Access date: 2026-09-24.

- ODCS v3.2.0 `context` block (`instructions`, `constraints`,
  `verifiedStatements`, RFC-0038): bitol-io.github.io/open-data-contract-standard/latest/context
  and `schema/odcs-json-schema-v3.2.0.json`.
- Model Context Protocol: specification version 2026-07-28 (modelcontextprotocol.io/specification/latest);
  server features are resources, prompts, and tools; hosts must obtain consent
  before tool invocation and treat tool annotations as untrusted unless the server is trusted.
- Uganda Data Protection and Privacy Act, 2019 (Act 9 of 2019), section 9
  (special personal data), checked against the Laws.Africa/ULII text as at
  2019-05-03. A later consolidated version dated 2023-12-31 is listed by
  Laws.Africa; whether its section numbering differs is `NOT_ASSESSED`.
- Catalog vendor capabilities: `NOT_ASSESSED`; the book's vendor survey dates
  from 2022-23 and must not be reused as a current comparison.

Sources: Olesen-Bagneux (2023) *The Enterprise Data Catalog*; Olesen-Bagneux
(n.d., 2nd ed. early release) *The Enterprise Data Catalog*; Jones (2023)
*Driving Data Quality with Data Contracts*; Bitol project, ODCS v3.2.0 (2026);
Model Context Protocol specification 2026-07-28.
