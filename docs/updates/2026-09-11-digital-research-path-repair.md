# Digital Research Canonical Path Repair

Date: 2026-09-11

## Outcome

Repaired active routes and installed-checkout validation from the absent
`C:\wamp64\www\digital-research-skills` directory to the registered canonical checkout at
`C:\wamp64\www\digital-research-engine`.

The canonical checkout was verified to contain `AGENTS.md`, `docs/control-plane-adoption.md`, the
Kaizen currentness gate, and the portfolio Kaizen standard. The repair covers the root router, root
skill, Kaizen skill, control-plane documentation and validator, live tests, English-output source
pointer, release gate, engineering standard map, and current source-register ownership.

Historical inventories and external repository URLs retain their original text where it records a
past state or the actual upstream repository name.

## Verification

Run:

```powershell
python -X utf8 scripts\validate_engine_control_plane.py --workspace-root C:\wamp64\www
python -X utf8 -m pytest tests -q -p no:cacheprovider
```
