# Tool provenance and pre-side-effect approval

`tools.ai.tool_provenance.ToolDispatcher` is a small host-side boundary for
tool calls. Each argument must carry provenance, and observations can be
converted to an argument with `observation_argument()`. Unknown tools,
malformed arguments, missing provenance and an unauthorised requester fail
before the operation callback runs.

External or irreversible tools receive an approval preview whose scope binds
the tool call ID, exact payload hash and argument provenance. The existing
approval gate then enforces expiry, policy version, identity, audit, kill,
idempotency and verification. A changed payload cannot reuse a completed call
ID, and replay returns the recorded result without repeating the callback.

The dispatcher does not authenticate identities, execute real tools, or
provide durable replay storage. Those host integrations and live red-team
coverage remain `NOT_ASSESSED`.
