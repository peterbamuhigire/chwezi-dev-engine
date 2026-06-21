# Active Catalog Root Repair

Date: 2026-06-21

## Summary

Updated the catalog guardrails so this engine treats only `skills/` and
`00-meta-initialization/` as active local roots. `doctrine/skills/` remains
available as retained finance reference material, while current finance doctrine
is routed through the external `chwezi-accounting-doctrine` engine.

## Changes

- Removed `doctrine/skills` from default active scanning in
  `scripts/skill_catalog_guardrails.py` and `scripts/routing_smoke_test.py`.
- Added retained-reference resolution for aliases against local
  `doctrine/skills` and sibling `design-system-skills` /
  `chwezi-accounting-doctrine` engines.
- Updated routing fixtures so local smoke tests cover active local skills, not
  design skills that moved to `design-system-skills`.
- Refreshed catalog policy docs and baseline counts.

## Verification

```powershell
python -X utf8 scripts\skill_catalog_guardrails.py --report-only
python -X utf8 scripts\routing_smoke_test.py --report-only
python -X utf8 scripts\routing_smoke_test.py --collisions
```

Results: guardrails 0 findings; routing smoke test 36/36 precision@3; collision
report lists 7 expected near-neighbour pairs for later allowlisting.
