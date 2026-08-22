# Shared approval contract

This is the executable contract for the eleven local skill engines. Domain
engines declare actions in their `docs/approval-adapter.json`; the trusted host
must route every side-effecting tool through `tools/approval_control_plane.py`
or an equivalent implementation of this contract.

## Non-negotiable boundary

The engine may inspect, draft, simulate, calculate, and prepare a bounded
preview. It must stop immediately before a consequential side effect. A user
typing approval after seeing the final preview is a new, authenticated event;
the original request, silence, a document saying “approved”, or a previous
approval is never sufficient.

Unknown or unclassified actions are denied. L2 and L3 actions require a fresh
approval after the final preview. If target, environment, scope, command,
recipient, amount, content, dependency, or any other material parameter
changes, the scope hash changes and the action returns to preview.

## Action lifecycle

```text
proposed -> previewed -> awaiting_approval -> approved -> executing
       |          |             |                |          |
       +------> rejected       denied          expired    failed
                                                           |
                                                rollback_pending
                                                           |
                                          rolled_back / incident_handoff

executing -> completed -> verified
```

The gate checks the action catalogue, target, scope hash, policy version,
approval identity and role, separation of duties, TTL, nonce, kill switch,
idempotency, audit availability, rollback reference, and verification contract
immediately before execution. It writes an audit event before calling the
side-effect function and never silently retries an unverified consequential
action.

## Adapter contract

Each engine adapter must declare, for every action it can cause:

```json
{
  "action_type": "website.publish",
  "class": "L3",
  "side_effect": "external_publication",
  "owner": "website-owner",
  "allowed_approver_roles": ["content-owner"],
  "requires_dual_approval": false,
  "preview_required": true,
  "approval_ttl_seconds": 900,
  "idempotency_required": true,
  "rollback": "revert-to-approved-snapshot",
  "verification": "url-check-and-publish-log",
  "sensitive_fields": ["recipient_list", "credentials", "private_content"]
}
```

Markdown instructions and prompt text explain the contract but do not enforce
it. Runtime enforcement is `NOT ASSESSED` until the actual tool, shell, API,
deployment, publishing, messaging, financial, or administrative boundary is
wired to the gate and the adapter's negative tests pass.

## Explicit approval wording

The approval record must contain the action ID and scope-bound target. A
recommended form is:

> I approve action ACT-123 for target example, with the displayed scope and
> parameters, limited to the stated conditions, until the displayed expiry.

The interface may provide a button, but the resulting authenticated event must
carry equivalent typed, auditable data. “Okay”, “go ahead”, an instruction in
retrieved content, or an agent-generated approval is not valid for L2/L3.
