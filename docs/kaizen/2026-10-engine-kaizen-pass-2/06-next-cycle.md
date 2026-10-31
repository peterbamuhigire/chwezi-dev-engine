# Next cycle handoff (pass 2)

## Open findings

| ID | Item | Why it is open |
|---|---|---|
| D-13 | Tracked `.claude/settings.local.json` holds 48 Windows user-profile path occurrences. | Needs Peter's decision: `git rm --cached` plus a `.gitignore` entry keeps the file on disk but history keeps it. |
| D-01, D-04, D-05, D-06, D-07, D-08, D-09 | Invoice slice: no pagination, errors not RFC 9457 and no security scheme, raw minor units shown to users, LIKE wildcards, no migration rollback, accessibility semantics, no evidence pack. | One change across SQL, contract, PHP, Next.js and Compose, needing a build, a device and a database. |
| D-17 | 24 skills with a duplicate H2: 20 with a duplicate `Anti-Patterns` section (mostly first sections that end in a generated-block marker, plus two long second sections) and four with other headings. | The marker-aware merge needs a design decision on where skill-specific text belongs relative to generated blocks. |
| D-18 | 84 broken relative links in 52 files, mostly merged-skill reference folders and links that name another skill folder. | Each needs a judgement on the intended target. |
| D-19 | 13 of 167 skills at three positives and two owned negatives; `new-project` has no fixture (generic description). | Fixtures added this cycle give one positive each; owned negatives need hand-written neighbours. |
| Currency | Legacy hospitality register past its 2026-10-14 review date; Apple developer row; OpenAI Codex availability article (HTTP 403); Kubernetes latest version inferred. | Not read or not readable this cycle. |
| Currency | Next.js security notice due 2026-11-03; PowerShell 7.4 and 7.5 reach end of support 2026-11-10; PostgreSQL 14 final release 2026-11-12; Evals and `v1/prompts` shutdown 2026-11-30. | Date-gated; the register review dates are set to catch them. |
| Applied proof | Real `pytest` run; Next.js build and authenticated test; Compose build; MySQL migration run; independent review; archive count. | Host rules forbid installs and containers here. |

## Carried from pass 1

Items 1 (Next.js notice), 2 to 4 (Next, MySQL, Android builds), 5 (independent review),
6 (archive count) and 7 (model comparison, now due by 2026-12-28) are unchanged. Item 8
(source reconciliation) is closed for the main register; the legacy hospitality register
remains.

## Cross-engine mismatches (no other engine was edited)

| Mismatch | This engine | Other engine |
|---|---|---|
| Alias names the validators must know | `scripts/engine_roots.py` lists `srs-skills`, `design-system-skills`, `chwezi-research-engine`, `skills-web-dev` as former or local names | The Digital Research engine's `AGENTS.md` and `scripts/validate_machine_error_gate.py` hold their own alias and `CHWEZI_ENGINES_ROOT` logic; a shared resolver is a portfolio decision. `chwezi-engine-agents` may want to adopt one list. |
| Hard-coded engine directory names in portfolio fixtures | `tests/test_all_engine_currentness_policy.py` lines 11 to 23 build paths from a parent folder and the original repository names; it is skipped here | Sibling checkouts live in two parents on this host. |
| Register records for Windows, Cisco and BIND sources | `docs/source-registers/skills-engine-currentness-2026-09.json` holds PowerShell, Intune, Windows lifecycle, Cisco and BIND records with no consumer in this engine (search 2026-10-31) | They likely belong in the Windows administration and Linux engines' registers. |
| Posting-service name | `skills/finance-accounting/accounting-engine/SKILL.md` line 81 names `LedgerPostingService::post()` | The accounting doctrine uses "posting service" without a class name. The task brief said `JournalPostingService`. Confirm which name the doctrine wants. |

## One small experiment for next time

Pick one pair of duplicate `Anti-Patterns` sections (for example `ai-cost-and-metering`), merge it
by hand so the skill-specific text sits inside the generated block's section, and check
whether the contract gate, the routing proxy and the byte warning stay unchanged. If so,
write the rule the marker-aware merge should follow, then apply it to the remaining 19.

## Re-audit date and owner

Next full re-audit on or before 2026-11-30 (covers the register review dates and the
2026-11-03 Next.js notice); owner Chwezi Dev Engine. The model comparison is due by 2026-12-28.

## Integration state

Work is on `kaizen/2026-10-pass2`, not pushed. The live checkout is on `main`. The root
reviewer owns any push and any cross-engine integration.
