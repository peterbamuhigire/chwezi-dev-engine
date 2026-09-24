# Least-Privilege Tool And MCP Security

Load when designing, reviewing or exposing tools to a model or agent, including
building or consuming MCP servers, and when you must prove that a tool cannot be
turned against its owner. Complements the tool catalogue and action-gating
reference (what tools exist and their approval tier) with how each tool is made
safe to call.

## 1. Inputs

| Input | Why |
|---|---|
| Task contract for the agent (goal, non-goals, autonomy level) | Tools are derived from the task, never the reverse |
| Target system APIs and their auth model | Determines credential shape and scope granularity |
| Data classification of every field a tool reads or returns | Decides redaction and whether a result may enter model context |
| Side-effect class per action (read, reversible write, irreversible, external, financial) | Drives approval tier and budgets |

## 2. Tool design decision rules

| Situation | Rule |
|---|---|
| A tool would take free-form SQL, shell, URL or code | Replace with a typed, intent-level action (`get_invoice(invoice_id)`, not `run_sql(query)`). If a general interpreter is truly required, run it in a sandbox with no network, no secrets and a disposable filesystem. |
| One tool covers read and write | Split into separate tools so each can carry its own scope, approval tier and audit label. |
| A tool needs an identifier the model could guess or forge (tenant, user, phone number, account) | Resolve it server-side from the authenticated session; the model supplies at most an opaque reference that is checked against the caller. |
| A tool returns large or sensitive payloads | Return the minimum fields the task needs; redact secrets and unrelated PII before the result re-enters context. |
| A tool calls an external URL | Fixed allow-list of hosts; the model may choose parameters, not hosts. Route through an egress proxy that blocks private, loopback and link-local ranges. |
| A tool is destructive | Offer `dry_run` that returns the exact effect; the real call requires an approval token bound to a hash of the dry-run arguments. |
| The tool errors | Return a short, typed error (`code`, safe `message`, `retryable`) so the model can recover; never echo stack traces, credentials, internal hostnames or raw upstream bodies. |
| Descriptions and names | Write them for the model: purpose, when to use, when not to use, argument semantics and units. Keep them in version control and review changes like code, because a changed description changes behaviour. |

Premium signal: a reviewer can read the tool list and see that no single tool,
even if called with adversarial arguments, can exceed the task contract.

## 3. Schema and argument validation

- Enable strict tool schemas where the provider supports them (Anthropic
  `strict: true` on the tool definition; OpenAI strict function calling). Strict
  mode guarantees shape, not safety.
- Still validate in code after decoding: ranges, lengths, formats, ownership and
  business rules. Provider-constrained decoding does not enforce every JSON
  Schema keyword (for example numeric and string-length bounds on Anthropic),
  so these must be checked by the application.
- Prefer enums and IDs to free strings. Reject unknown fields.
- Treat the validated arguments, not the model's narration, as the record of
  intent in the audit log.

## 4. Identity and credentials

- Give each agent its own workload identity; never reuse a human admin or a
  shared "integration" super-user.
- When the agent acts for a user, use delegated, user-scoped, short-lived tokens
  whose audience is the specific downstream API. The agent must not hold more
  authority than the user it serves.
- Keep credentials out of model context entirely. The tool runtime injects them
  at call time.
- Start from deny-all and add scopes one at a time with a recorded reason;
  review the scope list on a fixed cadence so it does not silently widen.

## 5. MCP-specific controls

MCP servers are API boundaries. Apply normal API security plus the protocol's
published security best practices.

| Threat | Required control |
|---|---|
| Token passthrough | An MCP server must not accept tokens not issued for itself and must not forward client tokens downstream. Validate audience; obtain separate tokens for downstream APIs. |
| Confused deputy (MCP proxy to third-party OAuth with a static client ID) | Server-owned per-client consent before forwarding to the third-party authoriser; exact-match redirect URI validation; single-use, short-lived `state` set only after consent; consent cookies bound to the client ID. |
| State handle hijacking | The current specification (2026-07-28) is stateless; any server-minted handle (cart ID, workflow ID) is not authentication. Generate handles with a CSPRNG, bind them server-side to the verified user, reject handles presented by another principal. Earlier protocol versions used session IDs; apply the same rule. |
| SSRF during OAuth discovery | Clients require HTTPS, block private/loopback/link-local ranges using a vetted library, validate every redirect hop, prefer an egress proxy, and guard against DNS rebinding. |
| Malicious authorization URLs | Allow only `https` (and `http` for loopback in development); never open URLs through a shell; apply CSP in web clients. |
| Local server compromise | Show the full launch command before one-click install, require explicit consent, run local servers sandboxed with minimal filesystem and network access; prefer `stdio` or authenticated IPC over open localhost HTTP. |
| Over-broad scopes | Minimal initial scope; step-up via targeted scope challenges when a privileged tool is first used; no wildcard or omnibus scopes; log elevation events. |
| Tool poisoning and description drift | Pin server versions; diff tool names, descriptions and schemas on every update; treat a changed description as a new tool needing review; never let a server's tool text instruct the model about other servers' tools. |

## 6. Tool results are untrusted input

A tool result may contain text written by an attacker (a web page, a ticket
body, an email). Label it with provenance in context, never let it change the
goal or the tool set, and apply the exfiltration triad check in
`ai-security/references/llm-and-agent-threat-control-map.md`.

## 7. Audit record per tool call

Minimum fields: `trace_id`, `run_id`, agent identity, on-behalf-of user and
tenant, tool name and version, validated arguments (redacted per
classification), policy decision and rule ID, approval ID and approver where
applicable, result status, side-effect reference (record IDs changed), cost and
latency. Join to the model trace with the same `trace_id`.
If you adopt OpenTelemetry GenAI conventions, check their current stability
first; keep prompt and completion content capture opt-in and redacted.

## 8. Test cases every tool set must pass

1. Adversarial arguments (another tenant's ID, oversized input, path traversal,
   internal URL) are rejected by code with a logged policy denial.
2. An injected instruction inside a tool result does not trigger any additional
   tool call outside the task contract.
3. Approval token replayed with modified arguments is rejected.
4. Expired or wrong-audience token is rejected by the MCP server.
5. Destructive tool without approval returns a dry-run only.
6. Tool error path returns the typed error without secrets.

## 9. Worked example: agricultural cooperative stock agent

An agent helps a coffee cooperative in Bushenyi reconcile warehouse stock and
pay farmers by mobile money.

- Tools: `get_delivery(delivery_id)`, `list_unreconciled(period)`,
  `propose_payment(farmer_id, delivery_ids[])` (returns a draft with computed
  amount), `submit_payment(draft_id, approval_token)`.
- The model never supplies a phone number or amount; both are derived from the
  farmer record and weighed deliveries. `submit_payment` is irreversible and
  financial, so it requires the treasurer's approval bound to the draft hash,
  and a per-day cap enforced in the payment service.
- The MoMo credential lives in the payment service, not the agent; the agent's
  token can create drafts but not disburse.

## Evidence/currentness

Access date 2026-09-24.

- MCP Security Best Practices, modelcontextprotocol.io/specification/latest (current spec 2026-07-28; stateless model, state handle hijacking, token passthrough forbidden, confused deputy, SSRF, local server compromise, OAuth URL validation, scope minimization) - verified.
- Anthropic structured outputs and strict tool use (GA; `output_config.format`, `strict: true`; unsupported numeric/string-length constraints): platform.claude.com docs - verified.
- OpenAI Structured Outputs and strict function calling: developers.openai.com docs - verified.
- OWASP AI Agent Security Cheat Sheet (approval bound to exact parameters, fail closed) - verified.
- OpenTelemetry GenAI semantic conventions moved to the `semantic-conventions-genai` repository; stability level `NOT_ASSESSED`.

Sources: Borges, D. and Campbell, D. (2026, early release) *AI Security Engineering*; Fernandez, O. (2024) *Patterns of Application Development Using AI*; Model Context Protocol specification; OWASP.
