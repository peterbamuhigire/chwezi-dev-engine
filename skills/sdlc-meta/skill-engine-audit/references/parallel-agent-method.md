# Reference: The Parallel-Agent Audit Method

Run independent concerns in PARALLEL so strict scores emerge without single-viewpoint bias, then
synthesize. This is the method, proven on the design-system-skills audit (overall 51/100).

## The standard fleet (one agent per concern, each writes its own report file)

1. **Standards benchmark** — "what does world-class look like NOW for this domain?" Run under a
   research engine's **no-hallucination rule** (every version/standard/award fact carries a real
   URL; mark unverified items). → `06-standards-benchmark.md`
2. **Reading / source list** — material to buy and extract, tiered and mapped to groups, cited
   (real ISBNs/URLs). → `08-reading-list.md`
3. **Existing-skills audit** — read EVERY SKILL.md + references; score each skill and group
   strictly. → `03-existing-groups-audit.md`
4. **Taxonomy & gap analysis** — is the structure sufficient/exhaustive/balanced; enumerate
   MISSING skills with P0/P1/P2 priority. → `02-coverage-and-taxonomy.md`, `04-gap-analysis.md`
5. **Per-output-type readiness** — score every deliverable type the engine must produce. →
   `05-per-output-type-readiness.md`
6. **Hardening plan** — concrete `references/*` + `examples/*` to add per skill. →
   `07-hardening-existing-skills.md`

## Briefing each agent (non-negotiables)

- Give each the engine path, the BAR (top 0.1% of the domain), and the **strictness directive**
  verbatim (default 45–65; 70+ needs extraordinary justification; if tempted, not strict enough).
- Give research agents the **no-hallucination rule** and point them at a research engine's
  source-verification skill; require inline source URLs + a confidence/gaps note.
- Each agent writes ONLY its own report file(s) — no overlap, no git — so they run concurrently
  without conflict. The orchestrator commits.
- Tell each to justify every score with named, concrete deficiencies.

## Synthesis (the orchestrator does this, not delegated)

After the fleet returns, write the connective files yourself, reconciling their scores:
`00-executive-summary.md`, `01-methodology-and-rubric.md`, `09-master-scorecard.md`,
`10-roadmap-to-world-class.md`, and a `README.md` index. Weight execution/coverage above
philosophy (see `scoring-rubric.md`) so a strong doctrine on a thin skill layer still lands the
overall below 70.

## Scale
~6 agents is the standard fleet. For a very large engine, split the existing-skills audit by
group (one agent per group). Keep the rubric identical across agents so scores are comparable.
