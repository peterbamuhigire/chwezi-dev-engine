# Windows administration engine status

Status date: 2026-09-01

## Registry identity

- Engine ID: `windows-admin`
- Canonical checkout: `C:\wamp64\www\windows-admin-engine-skills`
- Router: `AGENTS.md`
- Adoption document: `docs/control-plane-adoption.md`
- Current status: `RESTORED / STATICALLY ASSESSED` — the canonical checkout is present and native gates pass; live Windows/domain/fleet lab claims remain separately assessed.

## Intended scope

This is a first-class domain engine for Windows workstations and servers, Active Directory,
identity and access, networking, security, storage, recovery, fleet management, and hybrid
administration. Its registry contract includes the conceptual roles `windows-router`,
`host-and-fleet-operator`, `identity-security-reviewer`, and `recovery-gatekeeper`, plus
bounded command and evidence surfaces.

## Routing rule

Route Windows administration tasks here when the checkout is available. Read its `AGENTS.md`
first, then glob `SKILL.md` files and select them by frontmatter description. Use the engine's
own procedures, evidence requirements, safety gates, and rollback guidance. Do not substitute
Linux commands, generic engineering skills, or remembered Windows procedures.

## Currentness rule

Current Windows, Microsoft, Active Directory, PowerShell, security, policy, support-lifecycle,
and hybrid-platform claims must pass Digital Research source evaluation and source verification.
The restored engine must provide or link current primary sources and dated review metadata.

## Restoration acceptance

The restored engine is statically assessable when the following are true:

1. `C:\wamp64\www\windows-admin-engine-skills\AGENTS.md` exists;
2. `docs/control-plane-adoption.md` exists;
3. the repository's selected `SKILL.md` files and router pass its native validators;
4. the control-plane validator resolves the router and adoption document; and
5. Windows-specific smoke fixtures prove target resolution, management ownership,
   before/after state, verification oracle, and recovery record; where a live lab
   is unavailable, the corresponding capability remains `NOT ASSESSED`.

The restored repository currently passes its native catalogue, routing, and
source-ingestion checks, plus the eleven-engine control-plane check. It is not a
substitute for live evidence on a particular Windows host, domain, fleet, or
hybrid management plane.
