# Skills Engine — Thorough Review (2026-05-01)

**Analyst:** Claude Opus 4.7 (1M ctx) | **Skills audited:** 245 (was 210 on 2026-04-16) | **Prior overall:** 9.0 / 10

---

## Headline

The repository has grown by **+35 skills** in two weeks, broadening into design fundamentals,
growth/experimentation, Apple platform depth (macOS + Xcode), email infrastructure, and a
PWA / e2e / observability platform tier. Capability is wider than at the last review.

But the **mechanical contract enforcement that earned the 9.0 score has regressed**. The
contract gate that previously reported `210 scanned | 0 errors | 0 warnings | 10 exempt`
now reports `226 scanned | 0 errors | 17 warnings | 10 exempt`. Seventeen of the new
specialists were merged without an `## Evidence Produced` section, breaking the
"every specialist declares canonical evidence" invariant.

Net score: **9.1 / 10** (+0.1). Coverage and reasoning depth gains outweigh the gate
regression, but the regression should be reversed before the next score moves up.

---

## 8-Dimension Scorecard (2026-05-01)

| Dimension | 2026-04-16 | 2026-05-01 | Δ | Notes |
|---|---:|---:|---:|---|
| Coverage | 9.5 | **9.5** | 0 | Already world-class; new design + growth + Apple families fill in long-tail breadth without changing the ceiling. |
| Baseline Strength | 9.5 | **9.5** | 0 | 14 baselines unchanged. No new baseline skill, no demotion. |
| Instruction Quality | 9.0 | **8.5** | −0.5 | 17 new specialists missing canonical Evidence Produced. Floor regressed; ceiling unchanged. |
| System Architecture | 9.5 | **9.5** | 0 | Capability matrix and skill-composition-standards still authoritative. |
| Reasoning Depth | 8.5 | **9.0** | +0.5 | Several new skills (`product-led-growth`, `e2e-testing`, `pwa-offline-first`, `experiment-engineering`, `kubernetes-platform`) ship explicit decision tables with thresholds. |
| Cross-Domain Integration | 9.0 | **9.0** | 0 | New skills cross-reference but no new contract. |
| Production Readiness | 9.5 | **9.0** | −0.5 | `contract_gate.py` is now warning-noisy, so the "structurally forced production-grade output" claim is weaker than two weeks ago. |
| Output Quality Potential | 9.0 | **9.0** | 0 | New skills lift ceiling on design/growth output; floor regressed in the same areas where evidence sections were skipped. |

**Average: 9.1 / 10** (was 9.0 on 2026-04-16, 8.9 on 2026-04-15 follow-up, 8.4 morning, 7.1 original).

---

## What's New Since 2026-04-16

### Design fundamentals (8 skills)
`every-layout`, `color-theory`, `design-by-nature`, `grid-systems`, `motion-design`,
`interaction-design-patterns`, `practical-ui-design`, `cognitive-ux-framework`,
`enterprise-ux-process`, `frontend-performance`, `habit-forming-products`.

These give the engine book-grounded design depth (Heydon Pickering's *Every Layout*,
Bringhurst-style typography, Norman/Krug/Hooked frameworks) that the prior pass flagged
as "ceiling, not floor" weakness.

### Growth & experimentation (5 skills)
`product-discovery`, `product-led-growth`, `saas-growth-metrics`, `experiment-engineering`,
`growth-telemetry-pipeline`. Closes the loop from product discovery → instrumentation →
experiment statistics → growth-loop design.

### AI extensions (4 skills)
`ai-agentic-ui`, `ai-output-design`, `deepseek-integration`, `openai-agents-sdk`. The
agentic-UI checkpoint primitives + permission framework are genuinely novel material
not previously in the repo.

### Platform tier (5 skills)
`pwa-offline-first` (closes the East-Africa connectivity gap flagged on 2026-04-16),
`e2e-testing` (closes the Playwright/Cypress gap from earlier audits),
`observability-platform`, `infrastructure-as-code`, `kubernetes-platform`,
`network-security`, `orchestration-best-practices`.

### Apple platform depth (5+ skills)
`macos-appkit-interop`, `macos-app-sandbox-security`, `macos-git-libgit2`,
`xcode-cloud-testflight`, `xcode-instruments-performance`, `xcode-project-engineering`,
`swift-concurrency-macos`, `swiftui-pro-patterns`, `ios-bluetooth-printing`.

### Business / domain (5 skills)
`saas-accounting-system`, `software-business-models`, `software-pricing-strategy`,
`technology-grant-writing`, `tabler-email-templates` (80 production HTML email templates
with light + dark variants).

### Data / reporting (3 skills)
`excel-spreadsheets`, `professional-word-output`, `demand-forecasting` (moved into
catalog and stub-marked on 2026-05-01).

### Misc
`blog-writer`, `blog-idea-generator`, `content-writing`, `competitive-analysis-pm`,
`east-african-english`, `feature-planning`, `dpia-generator`, `uganda-dppa-compliance`,
`code-safety-scanner`, `ai-slop-prevention`, `image-compression`, `photo-management`.

---

## Regressions

### 1. Contract-gate warnings reintroduced (HIGH)

```
contract-gate: evidence: scanned 226 | 0 errors | 17 warnings | 10 exempt
```

Skills missing `## Evidence Produced`:

```
ai-agentic-ui, ai-output-design, color-theory, design-by-nature, e2e-testing,
enterprise-ux-process, every-layout, experiment-engineering, growth-telemetry-pipeline,
infrastructure-as-code, kubernetes-platform, observability-platform, product-discovery,
product-led-growth, pwa-offline-first, saas-growth-metrics, tabler-email-templates
```

Several of these (e.g. `pwa-offline-first`, `e2e-testing`, `kubernetes-platform`,
`observability-platform`, `infrastructure-as-code`) are **production-readiness skills**
specifically — exactly the layer where evidence enforcement matters most. The others
are book-grounded design skills where evidence may be qualitative; those should still
declare a canonical category (e.g. `Design / UX Artifact`) or be added to the exempt list.

### 2. Repository-root pollution (cleared 2026-05-01)

The following empty leftover directories were removed and `demand-forecasting/` was
moved into `skills/`:

- `cicd-devsecops/` (empty — canonical lives in `skills/cicd-devsecops/`)
- `cicd-jenkins-debian/` (empty)
- `cicd-pipeline-design/` (empty)
- `demand-forecasting/` → `skills/demand-forecasting/` (moved + stub marker added)

### 3. `kubernetes-platform` is short (135 lines)

Compared to the existing `kubernetes-fundamentals`, `kubernetes-production`, and
`kubernetes-saas-delivery` (which are full skills), `kubernetes-platform` is half the
length and looks like a stub. Either fold it into the existing 3-skill family or
expand to match.

### 4. `enterprise-ux-process` is short (96 lines)

Compared to peer UX skills (`ux-principles-101`, `ux-psychology`, `cognitive-ux-framework`,
`web-usability-krug`), this skill is markedly thinner. Promotion candidate.

### 5. `00-index.md` and `01-executive-summary.md` are stale

The index says `Skills Audited: 210`. Actual count is 245. Executive summary still
lists Cloud / Payments / CI/CD as `Critical` gaps even though they have shipped.

---

## Per-Domain Heat Map (2026-05-01)

| Domain | Skills | State | Notes |
|---|---:|---|---|
| iOS | 23 | World-class | No change |
| AI / LLM | 32 | World-class | +4 (agentic-ui, output-design, deepseek, openai-agents-sdk) |
| Web frontend (React/Next/TS/Tailwind) | 14 | World-class | No change |
| Design fundamentals | 11 | World-class **(new)** | every-layout, color-theory, design-by-nature, grid-systems, motion-design, interaction-design-patterns, cognitive-ux-framework |
| Growth / experimentation | 5 | World-class **(new)** | product-discovery, product-led-growth, saas-growth-metrics, experiment-engineering, growth-telemetry-pipeline |
| MySQL | 7 | World-class | No change |
| PostgreSQL | 6 | World-class | No change |
| Apple ecosystem (macOS + Xcode + Swift) | 10 | Strong → World-class | New macOS + Xcode skills |
| Android | 11 | Solid | No change |
| KMP | 3 | Solid | No change |
| Microservices / distributed | 5 | World-class | No change |
| Kubernetes | 4 | World-class | +1 stubby `kubernetes-platform` (consolidate) |
| Cloud / IaC | 3 | Solid | +`infrastructure-as-code`, +`network-security` |
| CI/CD | 4 | Solid | No change |
| Observability / SRE | 4 | World-class | +`observability-platform` (regression: missing evidence section) |
| Testing | 6 | World-class | +`e2e-testing` (regression: missing evidence section) |
| Security | 11 | World-class | +`network-security`, +`code-safety-scanner` |
| PWA / offline | 1 | Strong **(new)** | `pwa-offline-first` closes prior gap |
| Email infrastructure | 1 | World-class **(new)** | `tabler-email-templates` (80 templates) |
| Document generation | 3 | Strong | `professional-word-output`, `excel-spreadsheets`, `python-document-generation` |
| SaaS business / pricing | 8 | World-class | +`software-business-models`, +`software-pricing-strategy` |
| Reporting / forecasting | 3 | Solid | `demand-forecasting` (stub), `mobile-reports`, `report-print-pdf` |
| GIS | 4 | Strong | No change |
| Compliance (regional) | 3 | Strong | uganda-dppa, dpia-generator, east-african-english |
| Content / blogging | 3 | Foundational | blog-writer, blog-idea-generator, content-writing |

---

## Top 10 Recommendations (Re-prioritised)

1. **Restore the contract-gate floor.** Add `## Evidence Produced` to the 17 flagged skills (or extend the exempt list with explicit justification). Then bump `MISSING_SECTION_SEVERITY` from `warning` to `error` in `contract_gate.py` so this regression cannot recur.
2. **Refresh `00-index.md` and `01-executive-summary.md`.** Skill count, scorecard, and gap list are 35 skills behind reality.
3. **Decide the fate of `kubernetes-platform`.** Merge it into `kubernetes-fundamentals` / `kubernetes-production` / `kubernetes-saas-delivery`, or expand to match peer length.
4. **Promote `enterprise-ux-process`** to the same depth as `ux-principles-101` / `ux-psychology`, or merge into one of them.
5. **Promote `demand-forecasting`** out of stub status: add `references/forecast-methods.md` (moving avg / Holt-Winters / Croston decision matrix), `references/backtesting-evidence.md`, and `references/sql-templates.md`.
6. **Define `## Inputs Contract` / `## Outputs Contract` table schema** in `skill-composition-standards`. The `contract_gate.py` stub for these has been waiting since 2026-04-16.
7. **Book-grounded reference depth for new families.** Python (6), TypeScript (4), GIS (4), Kubernetes (4) still cite no books in their `references/`. Use the audit + per-skill plan in `docs/superpowers/specs/`.
8. **Add a `growth-experimentation` baseline skill.** With 5 specialist skills now in this family, a baseline skill in the spirit of `world-class-engineering` would lock in cross-references and decision rules across them.
9. **Complete the design baseline.** Consider adding `typography-systems` (Bringhurst grounding) and `accessibility-wcag-22`. The design family is one or two skills away from elite parity with the engineering baseline tier.
10. **Schedule a quarterly contract-gate sweep**: a recurring agent (every 14 days) running `contract_gate.py` and opening a PR if warnings or errors return to non-zero.

---

## What You Can Now Build (That You Couldn't Two Weeks Ago)

- **Offline-first PWAs for East African connectivity** — Workbox + Service Workers + IndexedDB
- **Production e2e test pyramids** — Playwright + Cypress with quarantine and flake budgets
- **Production-grade transactional email** — 80 cross-client tested HTML templates, no hand-rolled responsive markup
- **Agentic AI UIs with checkpoint primitives** — permission framework + progress tiers for long-running agent flows
- **Disciplined growth experiments** — power calc → SRM checks → variance reduction → decision rule
- **macOS-side native components** — AppKit/SwiftUI interop, app sandbox security, libgit2 bindings
- **Xcode Cloud + TestFlight rollout pipelines** — codified release engineering for Apple platforms

---

## What Still Cannot Be Built At World-Class Level

- **High-frequency / real-time systems** — `realtime-systems` is 1 skill, foundational only. Out of scope for product engineering.
- **Compiler / language internals** — intentionally out of scope.
- **Mobile cross-platform with React Native** — the gap from the original 2026-04-12 audit remains. KMP is covered; RN is not.
- **Rust systems programming** — no skill. May be worth adding for performance-critical backend services.
- **WebAssembly / edge runtimes** — no skill. Worth tracking through 2026-2027 as Cloudflare / Fastly / Vercel edge usage grows.
- **Compliance (international)** — Uganda DPPA + DPIA covered; ISO 27001 / SOC 2 / PCI-DSS / HIPAA control-mapping skills are absent.

---

## Strategic Position (2026–2040)

The library now has roughly the same shape as the internal tooling at a senior product
engineering function inside a Tier-1 product company (Stripe / Shopify / Linear), plus
distinctive depth in:

- **East African compliance and connectivity** — DPPA, DPIA, offline-first
- **AI-differentiated product layer** — 32 skills covering integration → safety → monetisation
- **Apple platform depth** — 23 iOS + 10 macOS/Xcode skills

Wealth-accumulation thesis from `07-wealth-accumulation-engine.md` is supported on the
engineering side. The remaining wedges are:

1. **Contract enforcement discipline** (mechanical, fix this quarter)
2. **Book-grounding of new families** (content depth, fix this year)
3. **Operating cadence** — schedule the quarterly contract-gate sweep so the floor never
   regresses again

---

*Replaces nothing — the prior `00-index.md` through `07-wealth-accumulation-engine.md`
remain as historical record. This file is the 2026-05-01 update.*
