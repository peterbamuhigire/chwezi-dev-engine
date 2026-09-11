# Email Template Library Removal

Date: 2026-09-11

Deletion commit: `fe883a7`

## Decision

The bundled Tabler Emails collection was removed from
`skills/saas/saas-lifecycle-email-orchestration/references/`.

The engineering engine now owns email behaviour: event contracts, lifecycle sequences,
suppression, consent, deliverability, attribution, monitoring, and release evidence. The external
design engine owns purpose-fit email and newsletter design through
`skills/13-presentations-and-documents/email-and-newsletter-design`.

## Reason

A runtime that can load both this engineering engine and `design-system-skills` does not need a
commercial template library as a design substitute. The design engine already defines authored
visual direction, resilient email HTML, accessibility, dark mode, image-off behaviour, and
rendered-client QA. Removing the collection also avoids carrying a large licensed asset tree in a
public engineering catalogue.

## Scope

- Removed 1,388 files under the former `tabler-email-templates/templates/` tree plus its
  entrypoint and licence file, approximately 76 MB in the working tree before deletion.
- Updated all live skill and reference routes that depended on `tabler-email-templates`.
- Updated the current catalogue-consolidation route in `docs/skills-trimminhg.md`.
- Preserved old audit, discovery, extraction, and inventory documents as historical evidence. Their
  mentions describe the repository state at the time and must not be treated as current routing.

## Verification

Run:

```powershell
python -X utf8 scripts\skill_catalog_guardrails.py --report-only
python -X utf8 scripts\routing_smoke_test.py --report-only
python -X utf8 -m pytest tests -q -p no:cacheprovider
```

Search live routes separately from historical records:

```powershell
rg -n "tabler-email-templates" skills docs\skills-trimminhg.md README.md AGENTS.md SKILL.md
```

The expected live-route result is empty. Historical analysis files may still contain the old name.
