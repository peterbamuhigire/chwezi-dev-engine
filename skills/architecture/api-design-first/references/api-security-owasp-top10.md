# API Security Review against OWASP API Security Top 10 (2023)

Parent skill: [`api-design-first`](../SKILL.md). Companion: `vibe-security-skill`
(threat model and abuse cases), `graphql-security` (GraphQL specifics). Load
this reference when designing an API's authorisation model, reviewing an API
contract before release, or triaging an API security finding.

This is a design-time and review-time control set. It does not replace a
threat model, a penetration test, or runtime monitoring; any of those not
performed is `NOT_ASSESSED`, never "pass".

## Inputs

| Input | Source | If missing |
| --- | --- | --- |
| OpenAPI / SDL / proto / AsyncAPI contract | `api-design-first` | Review is limited to code; state that |
| Auth model and role/scope matrix | `references/auth-and-security.md` | Block: authorisation cannot be reviewed |
| Object ownership rules (tenant, user, branch) | Domain / database design | Block BOLA review |
| Inventory of hosts, versions, environments, third-party APIs consumed | Platform / gateway config | Mark API9 and API10 `NOT_ASSESSED` |
| Business flows with abuse value (checkout, OTP, referral, booking) | Product owner | Mark API6 `NOT_ASSESSED` |

## Procedure

1. Build the endpoint inventory from the contract and the gateway: method,
   path/operation, auth required, scopes, object IDs accepted, data classes
   returned, rate-limit class, owner. Anything in the gateway but not in the
   contract is a finding (shadow API).
2. For each endpoint, walk the ten risks below and record `pass`, `fail`,
   `not applicable` (with reason), or `NOT_ASSESSED`.
3. Write one negative test per `pass` that proves it (for example: user A
   requests user B's invoice and receives `404`). A control without a failing
   attempt recorded is an assumption, not a pass.
4. File each `fail` with severity, affected operations, and the fix pattern.
5. Re-run the checklist on every contract change that adds an object ID,
   a property, a role, a flow, or an outbound integration.

## The ten risks: design controls and proofs

| ID | Risk | Design control | Proof (negative test) |
| --- | --- | --- | --- |
| API1:2023 | Broken Object Level Authorization | Every handler that takes an object ID loads it through a query scoped by the caller's tenant and ownership (`WHERE tenant_id = :token_tenant AND id = :id`); IDs are non-sequential; wrong-tenant returns `404` | Cross-tenant and cross-user ID swap on every ID-bearing operation, including nested IDs in bodies and batch arrays |
| API2:2023 | Broken Authentication | Standard flows only (OAuth 2 / OIDC, hashed API keys); short-lived access tokens; rate limits and lockout on login, OTP, and password reset; token audience and issuer validated | Expired, wrong-audience, `alg:none`, and replayed tokens rejected; OTP brute force throttled |
| API3:2023 | Broken Object Property Level Authorization | Explicit request allow-list per role (no mass assignment); response built from a role-specific schema (no excessive data exposure) | Send `role`, `tenant_id`, `balance`, `is_verified` in a body: ignored or rejected; response diff for low-privilege role shows no internal fields |
| API4:2023 | Unrestricted Resource Consumption | Limits on body size, page size, array length, upload size, query cost, execution time; per-client and per-tenant rate limits; spend caps on paid downstream calls (SMS, mobile money, LLM tokens) | Oversize body -> 413; `per_page=100000` clamped; burst over quota -> 429 with `Retry-After`; SMS-sending endpoint cannot be looped to drain credit |
| API5:2023 | Broken Function Level Authorization | Admin and privileged operations on separate route groups with deny-by-default middleware; role/scope checked per operation, not per UI screen | Low-privilege token calls every admin operation (including HTTP-method swaps, e.g. `DELETE` on a read resource) -> 403/404 |
| API6:2023 | Unrestricted Access to Sensitive Business Flows | Identify flows with abuse value; add flow-level friction: per-account and per-device velocity limits, human verification where legitimate, anomaly alerts | Scripted repetition of the flow (bulk booking, referral farming, scalping) is throttled and alerted |
| API7:2023 | Server Side Request Forgery | Any user-supplied URL (webhook target, avatar URL, import URL) passes an allow-list and is fetched through an egress proxy that blocks private, link-local, and metadata ranges; redirects re-validated | Target `http://169.254.169.254/`, `http://localhost`, internal DNS names, and redirect chains: all blocked |
| API8:2023 | Security Misconfiguration | TLS only (plain HTTP refused, not redirected, for API hosts); strict CORS allow-list; security headers; verbose errors off; unused methods disabled; hardened defaults in gateway | Config scan per environment; error responses contain no stack traces; `OPTIONS`/`TRACE` behaviour checked |
| API9:2023 | Improper Inventory Management | Every host, version, and environment listed with owner and retirement date; old versions carry `Deprecation`/`Sunset` and are actually shut down; non-production environments hold no production data | Gateway route list diffed against contract inventory; forgotten `v1`/staging hosts found by DNS and certificate-transparency sweep |
| API10:2023 | Unsafe Consumption of APIs | Treat third-party and partner responses as untrusted input: validate against schema, bound sizes, time out, follow no redirects blindly, TLS verified | Malformed or oversized upstream response, and upstream redirect to an internal host, are handled safely |

## Style-specific additions

- GraphQL: depth, cost, alias and batch limits; persisted operations in
  production; field-level authorisation (API3 applies per field). Load
  `graphql-security`.
- gRPC: reflection off on reachable servers; mTLS between services; deadlines.
- Webhooks (outbound): signed payloads, SSRF-safe egress for customer-supplied
  targets (API7). Webhooks (inbound): verify signature and timestamp before
  parsing the body, de-duplicate by event ID.
- WebSocket: validate `Origin`; authorise privileged messages individually,
  not only at handshake.
- AI-agent consumers: see `apis-for-ai-agents-and-data.md`. Tool calls are
  API calls made on a user's behalf; every control above still applies, plus
  prompt-injection-aware authorisation (the model is never the authoriser).

## Original worked example: mobile-money wallet API (Uganda)

| Finding | Risk | Fix |
| --- | --- | --- |
| `GET /v1/wallets/{msisdn}` accepts any phone number and returns balance | API1 + API3 | Resolve wallet from token subject; drop MSISDN path lookup; return balance only to owner |
| `POST /v1/otp/send` has no per-number limit; each call costs an SMS | API4 + API6 | Per-MSISDN and per-device velocity limits, daily SMS spend cap, alert on spikes |
| Merchant callback URL fetched directly by the payment worker | API7 | Egress proxy with private-range block; allow-list merchant domains at onboarding |
| Staging host `api-staging.example.ug` still serves `v1` with production data copy | API8 + API9 | Remove production data; put staging behind VPN; retire `v1` with Sunset date |

## Premium vs generic output

| Generic AI output | Senior-grade output |
| --- | --- |
| "We follow OWASP best practices." | Per-endpoint risk table with pass/fail/NOT_ASSESSED and a negative test per pass |
| Lists the 2019 edition's "Mass Assignment" and "Excessive Data Exposure" as separate items | Uses the 2023 IDs, where both sit under API3 |
| Rate limiting as a single global number | Per-client, per-tenant, per-flow limits plus spend caps on paid downstream calls |

## Quality gate

- [ ] Endpoint inventory matches gateway routes (no shadow or zombie APIs).
- [ ] All ten risks recorded per endpoint group with evidence or `NOT_ASSESSED`.
- [ ] Negative tests for API1, API3, API5 exist in the automated suite.
- [ ] Paid downstream calls have spend caps and alerts.
- [ ] Outbound fetches of user-supplied URLs go through the SSRF-safe egress path.

## Evidence and currentness

Accessed 2026-09-24:

- OWASP API Security Project (api-security.owasp.org, redirected from owasp.org/API-Security): the current edition is 2023; the site lists 2023 and 2019 only, with no 2025/2026 edition published. Item IDs and names above are copied from that list.
- OWASP GenAI Security Project announced a 2026 edition of the Top 10 for LLM Applications (announcement dated 2026-09-01) and published a Top 10 for Agentic Applications (December 2025). Their item IDs are `NOT_ASSESSED` here; load the AI security skills for them.
- Correction to older guidance: HTTP-to-HTTPS redirects on API hosts leak credentials sent on the first plain request; refuse plain HTTP instead (HSTS applies to browsers, not most API clients). This is engineering rationale, not a quoted source requirement.

Sources: Dynowski and Dulak (2025) *Learning API Styles*; Johnson (2025) *Practical JSON Design and Usage*; OWASP API Security Top 10 2023; engine skills `vibe-security-skill`, `graphql-security`.
