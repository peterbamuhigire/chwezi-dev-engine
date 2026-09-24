# LLM And Agent Threat-To-Control Map

Load when threat-modelling, reviewing, or release-gating any LLM feature or agent:
you need the current OWASP taxonomies, a defence-in-depth design for prompt
injection, and a control/test matrix that a security reviewer will accept.

This file is the crosswalk. Deeper material stays where it already lives:
`ai-prompt-injection-and-tenant-safety` (STRIDE template, red-team suite),
`ai-tenant-isolation-patterns` (storage-side isolation),
`ai-agent-safety-and-red-team` (agent perimeter attacks),
`ai-agent-tooling-and-hitl/references/least-privilege-tool-and-mcp-security.md`
(tool and MCP design).

## 1. Operating principles (decision rules, not slogans)

| Principle | Decision rule an agent must apply | Typical violation |
|---|---|---|
| Untrusted input | Every token that did not come from your own code is data, including retrieved chunks, tool results, file contents, emails, web pages, images and other agents' messages. | Filtering the chat box but passing a fetched web page straight into context. |
| The prompt is not a security boundary | Anything a prompt "forbids" must also be impossible in code: authorisation, scopes, network egress, spend limits. | "Never reveal other customers' data" in the system prompt with a tool that can read every tenant. |
| Least privilege and least agency | Grant the smallest tool set, the narrowest credential and the lowest autonomy level that completes the task; add more only against evidence. | One `run_sql` tool with a read-write DSN because it made the demo work. |
| Separation of duties | Split planning, execution and verification across components with different identities; the verifier must not share the executor's model, prompt or credentials. | The same model grades its own output and approves its own action. |
| Independent layers | A control counts as a layer only if it fails for a different reason than its neighbours. Two LLM classifiers with the same model are one layer. | Input classifier + output classifier, both the same prompt-injected model. |
| Fail closed | Validation, policy, budget or approval failure reduces capability: deny, pause, or degrade to read-only. Never retry into a wider permission. | On schema failure, fall back to "free-text mode" that skips the validator. |
| Control decay | Every AI control has an owner and a re-test date; exceptions and allow-list growth are reviewed, not accumulated. | Egress allow-list that has grown from 2 hosts to 40 with no review. |
| Observe what you cannot prevent | Log enough to reconstruct who asked, what context was assembled, what the model proposed, what policy decided and what executed. | Only final answers are logged; tool arguments and policy decisions are invisible. |

## 2. The exfiltration triad (fast risk triage)

A component is high-risk for data theft when it has all three at once:

1. access to private or tenant data,
2. exposure to content an attacker can influence,
3. a channel that can move data out (outbound HTTP, email, webhooks, rendered
   images/links, file writes, even a chat reply to a different user).

Decision rule: **break at least one leg in code before release.** Options, in
order of preference: remove the outbound channel (or restrict it to a fixed
allow-list with no model-controlled URL parts); split the flow so the component
that reads untrusted content has no private data (quarantined reader passing
only typed, validated fields to a privileged planner); or require a human
approval bound to the exact outbound payload. A classifier alone does not break
a leg; it only lowers probability.

## 3. Prompt-injection defence in depth

Assume injection will sometimes succeed. Design so that a successful injection
yields nothing valuable.

| Layer | Control | Fails differently because |
|---|---|---|
| L1 Architecture | Capability separation: untrusted-content readers get no tools and no secrets; privileged planners never read raw untrusted text, only typed extractions. | Structural; does not depend on model judgement. |
| L2 Context hygiene | Role separation (system/developer/user/tool), explicit delimiters and provenance labels on every untrusted block, length caps, strip active content (HTML, hidden text, zero-width characters, markdown image links). | Deterministic transformation. |
| L3 Detection signal | Injection classifier or heuristics on inputs and on retrieved/tool content. Treat as a *signal* that raises scrutiny, never as the gate. Regex blocklists catch only naive attacks. | Different model or rules from the main model. |
| L4 Constrained output | Native structured outputs / strict tool schemas (see pattern catalogue in `ai-llm-integration`), enums instead of free strings, IDs instead of URLs. | Decoder-level constraint plus code validation. |
| L5 Policy enforcement | Every proposed tool call passes a deterministic policy engine: caller identity, tenant, scope, argument allow-lists, rate and spend budget. | Code with its own identity source. |
| L6 Human approval | For irreversible, external or financial actions, a human approves the exact arguments; approval token expires and is bound to a hash of those arguments. | A human with context the model lacks. |
| L7 Output handling | Encode on render, never `eval`, parameterise any SQL, sandbox any code, strip or proxy links and images in replies. | Standard AppSec controls. |
| L8 Detect and respond | Traces, anomaly alerts on tool frequency/cost/denials, kill switch, incident runbook (`ai-incident-response`). | Operates after the fact. |

Release rule: a feature that can reach a privileged or external action must
show evidence for L1 or L5, plus L6 for irreversible actions. L2-L3 alone never
passes review.

## 4. Crosswalk: OWASP Top 10 for LLM Applications (2025)

| ID | Risk | Primary engineering control | Minimum test before release |
|---|---|---|---|
| LLM01 | Prompt Injection | Layers L1-L6 above; indirect content treated as data | Direct and indirect injection cases from the standing red-team suite; privileged action must not execute |
| LLM02 | Sensitive Information Disclosure | Data classification before context assembly; tenant-scoped retrieval; redaction; no secrets in prompts | Cross-tenant probe, PII echo probe, secret-in-context scan |
| LLM03 | Supply Chain | Pinned model versions, provider DPA, model/package provenance, SBOM including prompts, skills and MCP servers | Dependency and model-version diff in CI; hallucinated-package check on AI-written code |
| LLM04 | Data and Model Poisoning | Provenance and write-controls on RAG corpora, fine-tune data and memory; review queue for new sources | Poisoned-document canary in staging corpus |
| LLM05 | Improper Output Handling | Treat output as untrusted user input to every downstream sink | XSS, SQL, shell, SSRF payloads emitted by a coerced model are neutralised |
| LLM06 | Excessive Agency | Narrow tools, scoped credentials, autonomy level, approval gates | Tool-scope matrix review; out-of-scope call is denied by policy, not by prompt |
| LLM07 | System Prompt Leakage | Keep no secrets, credentials or authorisation logic in prompts; assume the prompt is public | Extraction attempts yield nothing sensitive even when they succeed |
| LLM08 | Vector and Embedding Weaknesses | Per-tenant namespaces or enforced metadata filters; access checks on retrieved chunks; embedding-store access control | Tenant B query never returns tenant A chunks; ACL change propagates to index |
| LLM09 | Misinformation | Grounding with citations, abstain paths, confidence routing to humans, UX that shows uncertainty | Groundedness and abstention evals on the golden set |
| LLM10 | Unbounded Consumption | Per-user/tenant rate limits, token and step budgets, max output tokens, spend alerts | Load and loop tests hit hard limits and stop safely |

Note the 2023 v1.1 names (Insecure Output Handling, Training Data Poisoning,
Model DoS, Insecure Plugin Design, Overreliance, Model Theft) are superseded.

## 5. Crosswalk: OWASP Top 10 for Agentic Applications (2026)

| ID | Risk | Primary engineering control | Evidence a reviewer should see |
|---|---|---|---|
| ASI01 | Agent Goal Hijack | Goal and plan fixed by code/task contract; re-check plan against task scope before each privileged step | Trace showing policy rejected an injected goal change |
| ASI02 | Tool Misuse and Exploitation | Narrow typed tools, argument allow-lists, side-effect budgets, dry-run for destructive tools | Tool catalogue with side-effect class and budget per tool |
| ASI03 | Identity and Privilege Abuse | Agent has its own identity; acts on behalf of the user with user-scoped, short-lived, audience-bound tokens; no shared service super-token | Token audience/lifetime config; no token passthrough |
| ASI04 | Agentic Supply Chain Vulnerabilities | Allow-listed, pinned, reviewed tools, MCP servers, skills and prompt libraries; detect tool-description changes | Registry with version pins and review records |
| ASI05 | Unexpected Code Execution | No shell or `eval` from model output; sandboxed interpreters with no network or secrets by default | Sandbox profile and escape test |
| ASI06 | Memory and Context Poisoning | Validate before writing memory; provenance on memory items; per-user isolation; expiry; correction and erasure path | Poisoned-memory test; erasure proof (`ai-agent-memory-erasure-proof`) |
| ASI07 | Insecure Inter-Agent Communication | Authenticated channels, typed messages, receiving agent re-applies its own policy; no authority inherited by message content | Message schema and per-hop authorisation check |
| ASI08 | Cascading Failures | Circuit breakers, per-run step/cost budgets, bounded retries, blast-radius limits | Fault-injection run stops within budget |
| ASI09 | Human-Agent Trust Exploitation | Approval UI shows exact effect and provenance, flags model-authored rationale as such, resists approval fatigue | Approval UX review; rubber-stamp rate metric |
| ASI10 | Rogue Agents | Registry of every deployed agent with owner, scope and kill switch; behavioural drift monitoring | Registry entry, drill evidence for kill path |

## 6. Where MITRE ATLAS and NIST fit

- **MITRE ATLAS** supplies adversary tactics and techniques (including agent
  tool poisoning, memory poisoning and exfiltration via tool invocation). Use it
  to name attack steps in red-team plans and detections; cite technique IDs from
  the live matrix at test time rather than copying them into skills, because the
  matrix is released roughly monthly.
- **NIST AI RMF 1.0** (Govern, Map, Measure, Manage) and the **Generative AI
  Profile, NIST AI 600-1** are the governance frame: Map produces the threat
  model and context, Measure produces evals and red-team evidence, Manage
  produces controls, incident response and decommissioning, Govern assigns
  owners and risk tolerance. See
  `ai-agent-governance-and-limits/references/agent-governance-and-oversight.md`.

## 7. Worked example: mobile-money loan assistant

A Kampala SACCO adds an assistant that reads members' uploaded payslips and
bank statements, answers questions, and can "send a repayment reminder" by SMS.

- Triad check: private data (statements) + attacker-influenced content (an
  uploaded PDF can contain hidden text) + outbound channel (SMS to any number).
  All three legs present: block release.
- Fix: the SMS tool takes `member_id` and a template ID only; the phone number
  is resolved server-side from the member record, and the message body comes
  from an approved template with typed slots (amount, due date). The document
  reader runs with no tools and returns a typed extraction. The outbound leg is
  now fixed-destination and fixed-content.
- Residual risk recorded: misinformation in the extraction (LLM09) routed to a
  loan officer when confidence or cross-check against the ledger fails.

## 8. Premium versus generic output

| Generic AI output | Senior security engineer output |
|---|---|
| "Sanitise inputs and add a strong system prompt." | Names the trust boundary, the triad legs present, and which leg is broken in code. |
| Lists OWASP entries with definitions. | Maps each relevant entry to a control, an owner, a test ID and a release effect; marks non-applicable entries with the reason. |
| Claims injection is "prevented". | States residual risk and the detection and response path. |
| Uses 2023 OWASP names. | Uses LLM 2025 and ASI 2026 identifiers, dated. |

## 9. Quality gate

- [ ] Data-flow diagram marks every untrusted source, including tool outputs and memory.
- [ ] Triad check recorded per component; each high-risk component has a broken leg in code.
- [ ] Every privileged tool call passes a deterministic policy check outside the model.
- [ ] Every LLM 2025 and ASI 2026 entry is mapped or marked not applicable with reason.
- [ ] Each control has an owner, a test in CI or the red-team suite, and a re-test date.
- [ ] Residual risks and accepted exceptions are signed by a named owner.

## Evidence/currentness

Access date 2026-09-24.

- OWASP Top 10 for LLM Applications 2025 names and IDs: genai.owasp.org/llm-top-10 (verified).
- OWASP Top 10 for Agentic Applications 2026, published 2025-12-09: genai.owasp.org resource page and release post (publication verified). ASI01-ASI10 names taken from the OWASP GenAI release post and search summaries of it; the full PDF text was not opened, so exact wording is `NOT_ASSESSED` beyond the names shown.
- OWASP AI Agent Security Cheat Sheet (cheatsheetseries.owasp.org): approval binding to exact parameters, memory isolation, inter-agent trust boundaries (verified).
- MITRE ATLAS: github.com/mitre-atlas/atlas-data releases, v2026.09 dated 2026-09-15 (16 tactics; agent techniques added through 2026). Technique counts change monthly; do not hard-code.
- NIST AI RMF 1.0 (2023-01-26) and NIST AI 600-1 (2024-07-26): nist.gov AI RMF page; AI RMF revision announced but not published as of access date (`NOT_ASSESSED` for revision content).

Sources: Borges, D. and Campbell, D. (2026, early release) *AI Security Engineering*; Fernandez, O. (2024) *Patterns of Application Development Using AI*; OWASP GenAI Security Project; MITRE ATLAS; NIST.
