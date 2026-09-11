# Methodology, Evidence, and Currentness

## Scope

| Item | Value |
| --- | --- |
| Primary engine | `C:\wamp64\www\skills-web-dev` |
| Comparison source | `C:\Users\Peter\Downloads\skills-main\skills-main` |
| Source repository | `https://github.com/mattpocock/skills` |
| Source commit | `3cca18b368ae95cdbdebbff572ccafa662551015` |
| Source version | `1.2.3` |
| Access date | 2026-09-11 |
| Intended consumer | A fresh Kaizen agent operating across Chwezi engines |
| Change authority used | Report creation and live email-route cleanup only |

## Method

1. Read the Chwezi router, architecture, routing index, anti-slop gates, Kaizen workflow, skill
   authoring contract, audit rubric, currentness gate, design doctrine, and portfolio craft standard.
2. Pull `skills-web-dev` using `git pull --ff-only`; it was initially current at commit `21fcacd`.
   During the study the user committed the authorised email-template deletion as `fe883a7` and the
   responsible AI-slop publishing work as `beb72d2`; the report and route repairs preserve and build
   on those user changes.
3. Inventory all 179 active Chwezi skills and their references by family.
4. Run catalogue, routing, control-plane, contract, source-ingestion, and test checks.
5. Read the source repository's root instructions, context model, plugin manifests, release process,
   ADRs, lifecycle buckets, all 37 `SKILL.md` files, their Codex adapters, support files, human docs,
   scripts, templates, out-of-scope records, package metadata, and changelog.
6. Make a fresh shallow clone of upstream and compare all 164 non-Git files to the Downloads copy
   by relative path and SHA-256 after normalising CRLF/LF. Result: zero content differences.
7. Compare source mechanisms against existing Chwezi owners before proposing a new skill.
8. Apply the permanent audit cap and mark unavailable proof `NOT ASSESSED`.

No subagent review was used because the available interface did not expose a spawn mechanism that
could guarantee the repository-required role/model pin and fresh context. Independent-review
evidence is therefore `NOT ASSESSED`.

## Reproducible evidence

| Check | Result |
| --- | --- |
| `git pull --ff-only` | Already up to date |
| Working base before this report commit | `beb72d2` (includes user commits through the responsible AI-slop publishing update) |
| Chwezi catalogue guardrails | 179 active skills, 0 findings |
| Chwezi routing smoke test | 144/158 top-1 (91%); 158/158 top-3 (100%); 0 failures |
| Chwezi control-plane validator | 12 registry entries and all 12 installed checkouts; 0 findings after canonical research-path repair |
| Assembled runtime skill budget | 214 skills; 46,853 description characters; 51,680 metadata characters; 0 findings |
| Chwezi source-ingestion guardrail | 0 findings |
| Chwezi tests | 72 passed, 3 skipped |
| Chwezi portable-contract scan | 153/179 fully compliant; 26 with one or more gaps |
| Chwezi evidence contract | 0 errors, 66 warnings for missing `Evidence Produced` |
| Codex model-policy helper | Drift repaired with the authorised bounded helper; follow-up check passed |
| Matt source inventory | 37 skills, 164 files, 112 Markdown files |
| Matt promoted set | 25 skills; 25 plugin entries; 25 human docs pages |
| Matt invocation adapters | 37/37 present; 0 Claude/Codex invocation mismatches |
| Matt package/plugin versions | `1.2.3` and `1.2.3`; check passed |
| Matt source-ingestion guardrail | 0 findings |
| Matt against Chwezi contract | 0/37 fully conformant; expected schema/governance gap |
| Downloads versus fresh upstream clone | 164/164 files; 0 normalised-content differences |

## Currentness register

| Source | Scope | Publication/version date | Access | Freshness | Review | Support status | Uncertainty |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `github.com/mattpocock/skills`, commit `3cca18b` | Comparison repository | 2026-09-04 | 2026-09-11 | Volatile | 2026-10-11 | Active upstream | Local ZIP has no Git metadata; fresh-clone equality resolves content identity |
| `developers.openai.com/api/docs/models` plus local `models_cache.json` | Model IDs, positioning, and local catalogue visibility | Live page and cache fetched 2026-09-11 | 2026-09-11 | Highly volatile | 2026-10-11 | Active/locally visible | Cache visibility does not prove account entitlement or successful new-session startup |
| NIST AI RMF 1.0 and NIST AI 600-1 | AI risk governance | 2023-01 and 2024-07 | 2026-09-11 | Under revision | 2026-10-11 | AI RMF 1.0 active but revision announced | Do not freeze implementation against the revision in progress |
| NIST SP 800-218 | Secure development | SSDF 1.1 final 2022-02; 1.2 draft 2025-12 | 2026-09-11 | Mixed final/draft | 2026-10-11 | 1.1 final; 1.2 draft | Do not label the draft as final |
| OWASP ASVS | Application security verification | 5.0.0, 2025-05-30 | 2026-09-11 | Current | 2026-12-11 | Stable | Requirement-level adoption still needs mapping and tests |
| W3C WCAG 2.2 / ISO/IEC 40500:2025 | Accessibility | W3C Recommendation; ISO adoption 2025 | 2026-09-11 | Current | 2027-03-11 | Active | Product conformance requires human and automated evaluation |
| ISO/IEC 42001:2023 | AI management systems | 2023-12 | 2026-09-11 | Durable/current | 2027-03-11 | Published | Full normative text was not acquired; clause-level mapping is `NOT ASSESSED` |

Authoritative URLs:

- https://github.com/mattpocock/skills
- https://developers.openai.com/api/docs/models
- https://www.nist.gov/itl/ai-risk-management-framework
- https://csrc.nist.gov/projects/ssdf/publications
- https://owasp.org/www-project-application-security-verification-standard/
- https://www.w3.org/TR/WCAG22/
- https://www.w3.org/WAI/standards-guidelines/wcag/
- https://www.iso.org/standard/42001

## Model-policy record

Official OpenAI documentation currently lists `gpt-6-astra` for the hardest complex work and
`gpt-5.6-luna` for cost-sensitive high-volume work. These IDs match the repository policy's root
and worker choices. The installed CLI is `codex-cli 0.154.0`; its inspected command surface did not
list the account catalogue, but the local model cache fetched on 2026-09-11 contains
`gpt-6-astra` with visibility `list`. The policy helper initially reported
`DRIFT: root model policy drift`. The repository-authorised bounded `--apply` repair was then run,
and a follow-up `--check` returned `PASS: Codex model policy is correct`. A running session is not
claimed to have changed models because configuration was repaired. The detailed evidence is in
[`docs/audits/2026-09-11-ai-slop-kaizen-model-currentness.md`](../audits/2026-09-11-ai-slop-kaizen-model-currentness.md).

Decision: **retain the documented model policy. Configuration and local catalogue visibility pass
after repair; account entitlement, successful new-session startup, and independent Astra review
remain `NOT ASSESSED`.**

## Scoring rule

The study uses the repository's strict rubric. Default scores stay in the 45-65 range. A score
above 70 requires applied, repeatable evidence from real projects. The baseline is frozen before
the recommended Kaizen work and is capped at 65 for publication.
