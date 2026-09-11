# Source Structure and Mechanism

## Repository shape

```text
skills-main/
|-- CLAUDE.md                  repository contract
|-- AGENTS.md                  pointer to CLAUDE.md
|-- CONTEXT.md                 repository domain language
|-- README.md                  public router and install guide
|-- .agents/                   invocation, docs, install, and ADR policy
|-- .claude-plugin/            curated promoted-skill manifest
|-- .changeset/                versioned change records
|-- .github/workflows/         release automation
|-- docs/                      one human page per promoted skill
|-- scripts/                   linking, listing, and version sync
`-- skills/
    |-- engineering/           promoted engineering workflows
    |-- productivity/          promoted general workflows
    |-- misc/                  available but not promoted
    |-- in-progress/           public beta, excluded from plugin
    `-- deprecated/            retired capability bucket
```

## The operating model

The source repository separates two concerns that Chwezi often combines:

| Layer | Source mechanism | Why it works |
| --- | --- | --- |
| Human orchestration | User-invoked skills | The human chooses consequential flow changes and spends cognitive load deliberately |
| Reusable discipline | Model-invoked skills | The model can apply TDD, diagnosis, domain modelling, research, and design vocabulary when triggered |
| Repository memory | `CONTEXT.md` plus ADRs | Domain terms and decisions survive across sessions without replaying a conversation |
| Work state | Issue tracker or local Markdown | Specs, decision maps, tickets, triage states, and blocking edges live outside model context |
| Distribution | Plugin manifest or skills installer | Promoted capabilities are curated; experimental and miscellaneous skills remain available but excluded |
| Human discovery | README plus docs pages | Users can remember when to invoke commands without loading all explanations into every model turn |
| Runtime adaptation | `agents/openai.yaml` per skill | Codex UI metadata and implicit-invocation policy sit beside canonical content |

## Invocation ownership

The source has 22 user-invoked and 15 model-invoked skills across all buckets. In the promoted set,
orchestration routes such as `ask-matt`, `grill-with-docs`, `to-spec`, `to-tickets`, `implement`,
`triage`, and `wayfinder` are human-only. Disciplines such as `grilling`, `tdd`, `diagnosing-bugs`,
`domain-modeling`, `codebase-design`, `code-review`, `prototype`, and `research` are model-reachable.

This produces a clean dependency rule: a user-invoked wrapper may call a model-invoked primitive,
but one human-only command cannot silently trigger another human-only command. Chwezi should adopt
the semantic distinction, but express it through portable metadata plus tested runtime adapters,
not assume every host honours the source repository's fields.

## Context and cognitive load

`writing-for-agents` provides the source's most transferable doctrine:

- A context pointer names out-of-context material and states the branches that should load it.
- Context load is the cost paid by always-visible descriptions and project instructions.
- Cognitive load is the cost paid by the human who must remember an explicit command.
- Progressive disclosure protects information hierarchy, not merely token count.
- Completion criteria resist premature completion caused by visible later steps.
- Leading words recruit stable model priors and compress repeated explanations.
- Environment-visible facts should not be cached into prose unless lookup is genuinely expensive.
- Sediment, no-op instructions, duplication, and scattered definitions are maintenance defects.

Chwezi has progressive disclosure and metadata budgets, but it lacks this compact attention model.

## Workflow spine

| Phase | Source skill | Distinctive mechanism |
| --- | --- | --- |
| Configure | `setup-matt-pocock-skills` | Discovers tracker and documentation layout, confirms a draft, writes only the existing router |
| Clarify | `grilling` / `grill-with-docs` | Decision tree, dependency frontier, facts-versus-decisions boundary, shared-understanding gate |
| Model | `domain-modeling` | Ubiquitous language in `CONTEXT.md`; decisions in ADRs; lazy creation |
| Specify | `to-spec` | Synthesises established context without reopening the interview |
| Slice | `to-tickets` | End-to-end tracer bullets, explicit blocking graph, expand-contract exception |
| Build | `implement` plus `tdd` | One issue at a time, pre-agreed test seams, red-green evidence |
| Review | `code-review` | Standards and spec fidelity run independently |
| Continue | `handoff` | Compact pointer-rich state, no duplication of existing artefacts |

## Side loops

- `diagnosing-bugs`: feedback loop -> reproduce -> minimise -> ranked hypotheses -> targeted
  instrumentation -> regression test -> cleanup.
- `improve-codebase-architecture`: use Git hot spots, find shallow modules, produce an architecture
  review, then grill and design alternative interfaces.
- `prototype`: use throwaway code to answer one state, logic, or UI question; preserve the result as
  a primary source on a throwaway branch and remove prototype scaffolding from production.
- `wayfinder`: map a destination through fog using decision tickets, a visible frontier, claims,
  blocking edges, and one decision per session.
- `triage`: issue/PR state machine with verification before briefing and a durable out-of-scope
  knowledge base.
- `wizard`: create a staged script for human-only setup work with confirmation, redacted secret
  capture, idempotent writes, and a static verification pass.

## Lifecycle and release mechanism

Promoted skills must appear in four synchronised surfaces: canonical `SKILL.md`, plugin manifest,
bucket/root README routing, and a human docs page. Every skill also has a Codex adapter. Changesets
drive semantic versioning; one release workflow runs on main. The local package/plugin version
check passed at `1.2.3`.

The lifecycle buckets are useful. The hand-maintained four-surface duplication is not automatically
useful for Chwezi's 179-skill catalogue. Chwezi should generate derived inventories where possible
and retain one canonical skill body.

## Structural weaknesses to avoid importing

1. No required capability, permission, degraded-mode, recovery, evidence, or output contracts.
2. Several skills require subagents without an availability fallback or bounded handoff schema.
3. Tracker and publication operations can mutate external state as part of the normal flow.
4. The source is Bash/GitHub/Claude heavy; portability comes through installer metadata rather than
   capability-neutral procedures.
5. `improve-codebase-architecture` calls its report self-contained while loading Tailwind and
   Mermaid from CDNs; it is network-dependent and visually generic by Chwezi design standards.
6. The Claude Git guard is regex-based and can both miss equivalent commands and block harmless
   text. It is not a security boundary.
7. Only one release workflow is present; catalogue, link, invocation, docs, reference, and negative
   behavioural invariants are documented more strongly than they are enforced.
8. One promoted docs page, `wait-what`, misses the required `Common questions` section.
9. Current platform and CLI commands are not protected by a source register or review dates.
10. The source's strength comes from brevity, but some very short wrappers provide no degraded path
    when the referenced skill tool is unavailable.
