# LLM Application Pattern Decision Catalogue

Load when choosing how to put an LLM into an application feature: which pattern
fits, what it costs, how it fails, and what proof is needed before shipping.
Use it before writing prompt code, and again at design review. For security
controls around these patterns, pair with
`ai-security/references/llm-and-agent-threat-control-map.md`.

## 1. The governing idea: narrow the path

Every pattern below exists to reduce the space of outputs the model can
produce for a given input: tighter instructions, structured context, fewer
tools, typed outputs, smaller single-purpose calls. When a feature is
unreliable, the first question is "what can we remove or constrain?", not
"which bigger model?".

Decision order for any new feature:

1. Can deterministic code do it? If yes, do not use a model.
2. Is it one bounded transformation (classify, extract, rewrite, summarise)?
   Use a single discrete component with structured output.
3. Is it a known sequence of steps? Use a prompt chain or workflow with the
   model at judgement points only.
4. Does the path depend on what is discovered at run time? Only then use an
   agent loop with tools, budgets and approval gates (`ai-agent-runtime-architecture`).

## 2. Pattern catalogue as decision rules

| Pattern | Use when | Do not use when | Failure mode to design for |
|---|---|---|---|
| Discrete component (predicate, classifier, extractor) | A yes/no or typed decision inside ordinary code | The answer needs multi-step discovery | Out-of-set labels; always validate against the enum and route unknowns |
| Prompt object / prompt registry | More than a handful of prompts, or prompts edited by non-engineers | Throwaway prototypes | Unversioned edits change behaviour silently; store prompt, model, parameters, schema and eval baseline together, with author and change log |
| Prompt template | Same structure, variable data | Templates start holding business logic | Missing or injected variables; escape and delimit every inserted value, fail on missing keys |
| Structured I/O | Output feeds code | Free-form creative text for humans | Parse failure or schema drift; use native structured outputs (section 3) |
| Prompt chaining | Task decomposes into fixed stages (retrieve policies, then draft, then check) | Stages are not known in advance | Error compounding; validate between stages and log each stage's input and output |
| Query analyser and rewriter | Retrieval quality depends on intent, language or vocabulary mismatch (e.g. Luganda or Swahili queries against English documents) | Queries are already structured | Rewrites drift from user intent; keep the original query and evaluate retrieval on both |
| Retrieval-augmented generation | Answers must come from your documents and cite them | The knowledge fits in a short, stable prompt | Ungrounded answers, stale or cross-tenant chunks; see `ai-rag-patterns` |
| Tool use | The model must read live data or take actions | A fixed API call in code would do | Excessive agency; see `ai-agent-tooling-and-hitl/references/least-privilege-tool-and-mcp-security.md` |
| API facade | A general assistant needs a large third-party API | The API surface is two or three calls | Facade becomes a hidden super-tool; give it its own narrow scope |
| Result interpreter | Raw tool/API output must be explained to a person | The output is consumed by code | Interpretation invents facts; ground on the raw result and show it alongside |
| Multitude of workers | Many small, independently testable AI jobs compose a process | A single call is enough | Orchestration sprawl; each worker has one job, one schema, one eval set |
| Few-shot seeded transcript | Showing is clearer than describing tone or format | Seeds contain real customer data | Seeds leak into outputs; use synthetic seeds, version them with the prompt |
| Self-healing data | Low-criticality malformed data (formatting, address normalisation) can be repaired | Ledgers, medical, legal or payment data | Silent corruption; see decision gate below |
| Intelligent error handling | A tool error can be explained to the model so it retries with corrected arguments | The error text contains secrets or internal detail | Leakage and retry loops; return typed safe errors and cap retries |
| Human escalation | Confidence, risk or policy thresholds are crossed | Used as the only control for high-volume flows | Reviewer fatigue; measure approval rates and time-to-decision |
| Eval and guardrail | Always | Never skipped | See section 4 |

Avoid using a model to simulate computation ("pretend to execute this
pseudo-code"). Run real code in a sandbox and give the model the result.

### Self-healing data gate

Automated correction is allowed only when all are true: the field is
classified non-critical; the correction is logged with before/after values,
model version and prompt version; the original is retained; and a sample is
reviewed by a human on a fixed cadence. Financial, clinical, legal and identity
records get flag-and-review, never silent repair.

## 3. Structured output: current practice

- Prefer provider-native constrained decoding over "please reply in JSON":
  - Anthropic: `output_config.format` with `type: "json_schema"` for responses,
    and `strict: true` on tool definitions. Generally available.
  - OpenAI: Responses API `text.format` with `type: "json_schema"` and
    `strict: true`; strict function calling for tools. Handle the separate
    `refusal` content type.
- Schemas must set `additionalProperties: false`; constraints the provider does
  not enforce (for example numeric ranges and string lengths on Anthropic) are
  validated in application code.
- The older trick of pre-filling the start of the assistant's reply and using a
  stop sequence ("response fencing") is rejected with an error by Claude 4.6 and
  later models. Use structured outputs instead; keep prefill only for older
  models that still accept it, and test the fallback.
- Constrained decoding guarantees shape, not truth. Content still passes
  business-rule validation and, where it matters, an eval or guardrail.

## 4. Eval-driven development loop

Treat prompts, schemas, tools and model versions as code that ships only when
evals pass.

1. **Specify** the component contract: inputs, output schema, constraints,
   success criteria and what "abstain" looks like.
2. **Build the eval set before the prompt**: typical cases, edge cases,
   adversarial cases and every production incident. Include local realities the
   product will meet (mixed-language input, UGX amounts with and without
   separators, MTN and Airtel number formats, poor OCR from phone photos).
3. **Choose graders by cost of error**: deterministic checks first (schema,
   exact match, regex, business rules), reference-based scoring where a gold
   answer exists, a rubric-based model grader only for qualities code cannot
   check. The grader should be a different model or configuration from the
   system under test, and it is itself calibrated against human labels.
4. **Baseline, then change one thing** (prompt, model, retrieval, tool
   description) and compare against the baseline on the full set.
5. **Gate in CI**: regressions beyond the agreed tolerance block merge; see
   `ai-evaluation/references/ai-eval-harness/references/eval-ci-gate.md`.
6. **Reuse reference-free evals as runtime guardrails** where latency and cost
   allow (groundedness, policy, language, PII), with a defined action on fail:
   regenerate, abstain, or route to a human.
7. **Close the loop**: sample production traces, label them, and add failures
   to the eval set. Re-run on every model version change, including provider
   "silent" updates behind an unpinned alias.

Non-determinism is expected even at low temperature; score distributions over
repeated runs for critical cases instead of trusting one pass.

## 5. Premium versus generic output

| Generic AI output | Senior engineer output |
|---|---|
| One large prompt doing retrieval, reasoning, formatting and safety at once | Small components, each with one schema and one eval set |
| "Return JSON" in the prompt, `json_decode` and hope | Native structured outputs plus code validation plus a typed failure path |
| Prompts inline in controllers | Versioned prompt registry entries with owner, model pin and eval baseline |
| Evals written after launch, if ever | Eval set exists before the first prompt and gates every change |
| Agent by default | Agent only when the path cannot be known in advance, with budgets and gates |

## 6. Quality gate

- [ ] The pattern choice is justified against the decision order in section 1.
- [ ] Every model call has a versioned prompt, pinned model, output schema and max token limit.
- [ ] Every model output that reaches code or users is validated, with a typed failure path.
- [ ] The eval set exists, includes adversarial and incident cases, and runs in CI.
- [ ] Self-healing and escalation paths state their criticality gate and review cadence.

## Evidence/currentness

Access date 2026-09-24.

- Anthropic structured outputs (GA; `output_config.format`, `strict: true`; unsupported schema constraints): platform.claude.com/docs/en/build-with-claude/structured-outputs - verified.
- Claude 4.6 and later reject last-turn assistant prefill: platform.claude.com prefill and migration documentation (search result summaries of official pages) - verified at summary level.
- OpenAI Structured Outputs on the Responses API with `strict: true` and refusal handling: developers.openai.com/api/docs/guides/structured-outputs - verified.
- Model names, pricing and per-model feature support change frequently: `NOT_ASSESSED` here; check provider docs at build time.

Sources: Fernandez, O. (2024) *Patterns of Application Development Using AI*; Borges, D. and Campbell, D. (2026, early release) *AI Security Engineering*; Anthropic and OpenAI platform documentation.
