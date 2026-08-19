# Eleven-engine control-plane update

Registered `windows-admin-engine-skills` as the eleventh canonical engine in
the shared control plane. The change adds the Windows router mapping, adoption
document, domain roles, real `wsa-*` command surfaces, lifecycle hooks, and
target/authority/verification/recovery evidence types.

Current routing and architecture documents now state the eleven-engine scope.
Historical ten-engine audit and release records remain unchanged because they
describe the portfolio state and validation results on their original dates.

Verification commands:

```powershell
python -X utf8 scripts\validate_engine_control_plane.py
python -X utf8 scripts\validate_engine_control_plane.py --workspace-root C:\wamp64\www
python -X utf8 scripts\skill_catalog_guardrails.py --report-only
python -X utf8 scripts\routing_smoke_test.py --report-only
```

Verification result on 2026-08-20:

- Control-plane registry: 11 engines, 0 findings, including workspace router
  and adoption-document resolution.
- Engineering catalogue: 175 active skills, 0 findings; 127 routing fixtures,
  0 failures.
- Windows engine: 16 skills validated, 16 routing fixtures passed, 0 source
  ingestion findings, 10 Python tests passed, 7 Pester tests passed, and the
  PowerShell smoke test passed.
- Live Windows Server, domain-controller, Hyper-V, remote WinRM, and fleet-lab
  checks were not run for this documentation change and remain `NOT_ASSESSED`.
- AI-slop audit: A (clean); no blocking markers, unsupported claims, or generic
  filler found in the changed routing and adoption documents.
