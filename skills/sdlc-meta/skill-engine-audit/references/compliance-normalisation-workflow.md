# Cross-Engine Compliance Normalisation

Parent: [Skill Engine Audit](../SKILL.md)

Use this workflow to audit and conform a canonical skill engine without loading every skill into model context.

## Token-efficient sequence

1. Read only the router, `AGENTS.md`, doctrine, and catalogue policy.
2. Run `scripts/engine_compliance.py` to inventory every active `SKILL.md`.
3. Work from compact failure counts and exception lists; do not paste all skill bodies into context.
4. Separate safe mechanical repairs from judgement-heavy normalisation.
5. Normalise governing and high-risk skills first so they become reference implementations.
6. Process remaining skills by family and failure signature.
7. Re-run routing, safety, reference, and catalogue guardrails after every cohort.

## Commands

```powershell
python -X utf8 scripts/engine_compliance.py --root <engine-root> --active-root skills
python -X utf8 scripts/engine_compliance.py --root <engine-root> --active-root skills --json
python -X utf8 scripts/engine_compliance.py --root <engine-root> --active-root skills --fix-safe
```

`--fix-safe` is limited to canonical portability metadata, exact repeated boilerplate lines, and mojibake repairs that reduce suspicious decoding markers. It must not invent domain inputs, outputs, decisions, permissions, thresholds, or examples.

## Cohorts

| Cohort | Selection | Work |
|---|---|---|
| P0 | Validators, routers, catalogues | Remove false positives and establish a trustworthy baseline |
| P1 | Governing meta-skills | Make the rules and examples internally compliant |
| P2 | Security, finance, production mutation | Add least privilege and stop conditions |
| P3 | High-traffic domain baselines | Add contracts and routing collision tests |
| P4 | Remaining specialists | Normalise by repeated failure signature |

## Safety boundary

Automate syntax, never judgement. Before a write pass, record worktree state, capture the pre-fix report, test each marker layout, and inspect deletion-heavy diffs immediately. Any unexplained deletion outside the intended lines is a stop condition.

## Evidence pack

Record the engine and active roots, pre/post failure counts, safe-automation file list, human-normalised skills, validation results, and remaining exceptions with owners and reasons.
