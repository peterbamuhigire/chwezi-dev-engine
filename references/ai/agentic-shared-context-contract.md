# Versioned shared-context contract

The local `tools.ai.shared_context` helper provides a provider-neutral,
versioned trust packet for a bounded agent task. A packet carries an objective,
facts, relationships, source locators and scopes, permission scopes, trust
labels, and a policy version. `packet_hash` and `render_snapshot()` are stable
for the same packet, so an agent and reviewer can inspect the same replayable
snapshot.

`SharedContextPacket.validate()` returns named findings and
`require_valid()` fails closed for:

- `MISSING_SOURCE` or `MISSING_SOURCE_LOCATOR`;
- `STALE_CONTEXT`;
- `MISMATCHED_OBJECTIVE`;
- `REVOKED_ACCESS` or `SOURCE_SCOPE_MISMATCH`; and
- invalid trust labels.

The source registry is an input to validation. This helper does not fetch,
authenticate, or infer source records. Production identity, source freshness,
and revocation feeds remain host responsibilities and are `NOT_ASSESSED` by
the fixture tests.

Example import from the repository root:

```python
from tools.ai.shared_context import SharedContextPacket
```

The current contract is `shared-context.v1`. A future schema must retain the
old reader or provide an explicit migration before replacing stored packets.
