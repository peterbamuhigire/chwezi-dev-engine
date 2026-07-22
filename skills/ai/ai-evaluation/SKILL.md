---
name: ai-evaluation
description: Use when setting up quality assurance for AI features — defining evaluation criteria, measuring output quality, using AI-as-judge, monitoring production AI, detecting drift, and building user feedback loops
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# AI Evaluation and Monitoring

## Operating contract

## Inputs

| Input | Required | Purpose |
|---|---|---|
| Domain evidence | yes | feature contract, representative dataset, quality dimensions, baseline, thresholds, and risk class |

## Outputs

- Produce: evaluation plan, scored results, confidence and failure slices, release verdict, and monitoring thresholds.

## Capability and permission boundaries

Default to read-only analysis. Read only scoped records; redact secrets and regulated data. Writes, execution, network calls, production configuration, customer communication, billing changes, and delegation require explicit authority and an identified owner. Never widen tenant, time-window, or system scope implicitly.

## Degraded mode

When required telemetry, evidence, execution, network access, or write authority is unavailable, return a partial result with each unassessed item labelled, preserve the safest existing state, and state the evidence or approval needed to continue. Never convert missing evidence into a pass.

## Decision rules

| Condition | Action |
|---|---|
| Scope, owner, or threshold is missing | Stop the affected decision and request it |
| Evidence is incomplete but read-only analysis is safe | Produce a qualified partial result and gap list |
| A mutation exceeds authority or tenant boundary | Block it and route for approval |
| Evidence meets the stated threshold | Issue the output with provenance and owner |

## Anti-Patterns

- Treating absent evidence as success. Fix: mark the check unassessed and name the missing source.
- Expanding one tenant or workflow to all tenants. Fix: enforce supplied scope at every query and action.
- Performing a production write during analysis. Fix: emit a reviewed change plan until authority is explicit.
- Reporting a metric without population, window, or source. Fix: attach all three.
- Hiding a failed threshold inside an average. Fix: report failure slices and the remediation owner.

Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Use when setting up quality assurance for AI features — defining evaluation criteria, measuring output quality, using AI-as-judge, monitoring production AI, detecting drift, and building user feedback loops

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Correctness | AI evaluation harness configuration | Markdown doc covering eval set, scoring rubric, and acceptance thresholds | `docs/ai/eval-harness-assistant.md` |
| Correctness | Latest AI evaluation results | Markdown doc reporting pass-rate, regression deltas, and outlier examples | `docs/ai/eval-results-2026-04-16.md` |

## References

- Use the links and companion skills already referenced in this file when deeper context is needed.
<!-- dual-compat-end -->
## Overview

Evaluation is the biggest bottleneck to successful AI deployment. Define evaluation criteria BEFORE building. Without evaluation, you cannot know if your AI feature is working, degrading, or harming users.

**Core principle:** Evaluation-driven development. Like TDD for AI — define what "good" means first, then build.

## Evaluation Contract

Every production AI feature needs an evaluation contract before release:

- **Task definition**: what the model must do, for whom, in which workflow.
- **Business metric**: time saved, revenue influenced, conversion lift, defect reduction, service quality, risk reduction, or cost avoided.
- **Quality metrics**: correctness, completeness, relevance, tone, actionability, citation quality, and domain compliance.
- **System metrics**: latency, cost per successful task, availability, retry rate, fallback rate, and tool failure rate.
- **Safety metrics**: PII exposure, prompt-injection resistance, harmful output, policy violations, and unauthorized action attempts.
- **Release threshold**: minimum pass rates and maximum regression allowed versus the current production baseline.
- **Rollback trigger**: metrics or incidents that require disabling the feature or reverting prompt/model/tool versions.

---

## Evaluation Dimensions

| Dimension | What to Measure | Method |
|---|---|---|
| **Format** | Is output valid JSON/schema? Correct length? | Automated rules |
| **Factual accuracy** | Does output match the provided context? | AI-as-judge or RAG citation check |
| **Safety** | Toxic, harmful, or brand-risk content? | Classifier or AI-as-judge |
| **Instruction-following** | Did it follow format/tone/language rules? | Automated + AI-as-judge |
| **Relevance** | Does output address the user's question? | AI-as-judge |
| **Cost** | Tokens per request; cost per feature | Logged automatically |
| **Latency** | Time to first token; total response time | Logged automatically |

---

## Evaluation Workflow

```
1. Define criteria before building
2. Create golden test set (20–50 examples with expected outputs)
3. Run automated format checks on every new model/prompt version
4. Run AI-as-judge for quality checks
5. Compare against previous version — only deploy if metrics hold or improve
6. Monitor production: track live metrics + user feedback
7. Retrain/reprompt when drift detected
```

## Evaluation Dataset Design

- Build separate sets for development, release gating, adversarial testing, and production monitoring.
- Include real examples, expert-created examples, edge cases, multilingual/local examples, low-resource context, and abuse attempts.
- Version each case with task, tenant/domain, source, expected behavior, rubric, and data sensitivity.
- Keep leakage out of evals: do not let the same generated examples drive both prompt tuning and final release scoring.
- Refresh cases after production incidents, new user behavior, platform changes, policy changes, or model migrations.

## Release Gates

| Gate | Required Evidence |
|---|---|
| Prompt/model change | Eval comparison against previous version, cost and latency delta |
| New tool/action | Permission tests, dry-run tests, approval-path tests, failure-mode tests |
| RAG/index change | Retrieval precision samples, citation checks, stale-data checks, tenant isolation checks |
| Fine-tune | Baseline comparison showing prompts/RAG were insufficient, holdout eval results, rollback plan |
| Production launch | Monitoring dashboard, alert thresholds, owner, incident playbook, user feedback channel |

Do not ship an AI feature because a demo looked good. Ship it because it passes the evaluation contract.

---

## Creating a Golden Test Set

```sql
CREATE TABLE ai_eval_cases (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  feature_name    VARCHAR(100),       -- 'invoice_analysis', 'sales_report'
  input           TEXT NOT NULL,      -- the user query or document
  expected_output TEXT,               -- ideal output (or key elements of it)
  eval_criteria   JSON,               -- {"format": "json", "must_contain": ["total", "vendor"]}
  created_by      INT,
  created_at      TIMESTAMP DEFAULT NOW()
);
```

Build test cases from:
1. Real production queries (once live)
2. Domain expert-crafted examples
3. Edge cases: empty input, wrong language, very long input, adversarial input

---

## Automated Evaluation (No LLM Cost)

Run these on every deployment:

```php
class AiEvaluator {
    public function evaluateFormat(string $output, array $criteria): EvalResult {
        $score = 0;
        $issues = [];

        // JSON validity
        if (($criteria['format'] ?? null) === 'json') {
            $decoded = json_decode($output, true);
            if (json_last_error() !== JSON_ERROR_NONE) {
                $issues[] = 'Invalid JSON';
            } else {
                $score += 25;
                // Required keys
                foreach ($criteria['required_keys'] ?? [] as $key) {
                    if (!array_key_exists($key, $decoded)) {
                        $issues[] = "Missing key: $key";
                    } else {
                        $score += 10;
                    }
                }
            }
        }

        // Length constraints
        if (isset($criteria['max_words'])) {
            $wordCount = str_word_count($output);
            if ($wordCount > $criteria['max_words']) {
                $issues[] = "Too long: {$wordCount} words (max {$criteria['max_words']})";
            } else {
                $score += 15;
            }
        }

        // Must-contain terms
        foreach ($criteria['must_contain'] ?? [] as $term) {
            if (stripos($output, $term) === false) {
                $issues[] = "Missing expected term: $term";
            } else {
                $score += 10;
            }
        }

        return new EvalResult($score, $issues);
    }
}
```

---

## AI-as-Judge

Use a strong model to evaluate your AI feature's outputs. Reliable for quality, relevance, and tone.

```php
function judgeAiOutput(string $input, string $output, string $criteria): array {
    $judgePrompt = <<<PROMPT
You are evaluating the quality of an AI assistant's response.

Evaluation criteria:
{$criteria}

User input:
---
{$input}
---

AI response to evaluate:
---
{$output}
---

Score the response on each criterion from 1–5 (5 = excellent).
Explain your reasoning briefly, then give an overall score (1–5).
Format your response as JSON:
{
  "relevance": {"score": X, "reason": "..."},
  "accuracy": {"score": X, "reason": "..."},
  "tone": {"score": X, "reason": "..."},
  "overall": X
}
PROMPT;

    return callLLM('gpt-4o', $judgePrompt, temperature: 0.1);
}
```

**AI-judge best practices:**
- Use a stronger model as judge than the one being evaluated
- Ask for reasoning BEFORE score (reduces positional bias)
- Use pairwise comparison (A vs B) for relative quality rather than absolute scores
- Multiple judges + average for high-stakes decisions
- Watch for self-serving bias (GPT-4 favours GPT-4 outputs)

---

## Production Monitoring

### Metrics to Track Per Feature

```sql
CREATE TABLE ai_quality_metrics (
  id             BIGINT AUTO_INCREMENT PRIMARY KEY,
  tenant_id      INT NOT NULL,
  feature_name   VARCHAR(100),
  prompt_version VARCHAR(10),
  model          VARCHAR(50),
  format_valid   BOOLEAN,
  latency_ms     INT,
  tokens_in      INT,
  tokens_out     INT,
  judge_score    DECIMAL(3,2),         -- 1.00–5.00 from AI judge (async)
  user_rating    TINYINT,              -- 1–5 from explicit feedback
  thumbs_up      BOOLEAN,              -- quick user feedback
  created_at     TIMESTAMP DEFAULT NOW(),
  INDEX idx_feature_date (feature_name, created_at),
  INDEX idx_tenant_date (tenant_id, created_at)
);
```

### Key Metrics by Priority

1. **Format failure rate** — % of responses failing JSON/schema validation
2. **User thumbs-down rate** — explicit negative feedback
3. **Early termination rate** — user stops generation mid-way
4. **Average judge score** — from async AI-as-judge on random sample
5. **p50/p90/p99 latency** — track at percentiles, not average
6. **Cost per request** — tokens × price per token

### Alerting Thresholds

```php
$alerts = [
    'format_failure_rate' => 0.05,    // Alert if > 5% of responses fail format
    'thumbs_down_rate'    => 0.15,    // Alert if > 15% negative feedback
    'p99_latency_ms'      => 8000,    // Alert if p99 latency > 8 seconds
    'cost_per_request'    => 0.05,    // Alert if avg cost > $0.05 per request
];
```

---

## Drift Detection

Drift = your AI feature is silently getting worse. Causes:
1. **Model API updates** — providers silently update model versions
2. **System prompt edits** — even small changes change behaviour
3. **User behaviour shift** — users learn to write differently over time
4. **Data drift** — RAG documents become stale

### Detection

```sql
-- Weekly average quality score — watch for downward trend
SELECT
    YEARWEEK(created_at) AS week,
    feature_name,
    AVG(judge_score) AS avg_quality,
    AVG(CASE WHEN thumbs_up = FALSE THEN 1 ELSE 0 END) AS negative_rate,
    AVG(latency_ms) AS avg_latency
FROM ai_quality_metrics
WHERE tenant_id = ? AND created_at > DATE_SUB(NOW(), INTERVAL 8 WEEK)
GROUP BY week, feature_name
ORDER BY week;
```

**Act when:**
- Average quality score drops > 0.5 points vs last 4-week average
- Format failure rate doubles vs baseline
- User negative feedback rate increases > 5% week-over-week

---

## User Feedback Signals

| Signal | Type | Strength |
|---|---|---|
| Thumbs up / down | Explicit | Medium |
| Star rating | Explicit | Medium |
| "That's wrong" in chat | Implicit | High |
| User edits output | Implicit | Very high |
| Early generation stop | Implicit | Medium |
| Rephrases same question | Implicit | High |
| Regenerates response | Implicit | Medium |

**Collect user edits as preference data:** original output = rejected, edited version = preferred.

---

## Evaluation Before vs After Deployment

| Phase | What to Evaluate | How |
|---|---|---|
| **Pre-deploy** | New prompt version vs old | A/B on golden test set |
| **Pre-deploy** | New model vs old | Same test set, compare scores |
| **Post-deploy** | Production quality | Sample 5% of requests → AI judge |
| **Post-deploy** | User satisfaction | Feedback collection |
| **Ongoing** | Drift detection | Weekly metric trend |

**Never deploy a new prompt or model without running the golden test set first.**

---

## Anti-Patterns

- **No golden test set** — you cannot measure regression
- **Only measuring average latency** — track p90/p99; outliers hurt users
- **Skipping evaluation to ship faster** — silent quality degradation is worse than delay
- **No prompt versioning** — you cannot roll back a broken prompt
- **Judge uses same model as evaluated** — self-serving bias inflates scores
- **No user feedback mechanism** — your most valuable signal goes uncollected

---

## Sources
Chip Huyen — *AI Engineering* (2025) Ch.3–4,10; Chip Huyen — *Designing ML Systems* (2022) Ch.8

## Multi-Tenant Eval Harness

This skill covers evaluation concepts. The engineering of the eval harness as a control-plane service in a multi-tenant SaaS — per-tenant golden datasets, CI gate that blocks regressing prompt/model changes, judge-LLM calibration, production sampling, drift detection, and pre-promotion gates for flagship tenants — lives in `ai-eval-harness`.

Cross-references:
- `ai-eval-harness` — the harness as a service.
- `ai-hallucination-slo-and-grounding` — uses eval signals to budget hallucination.
- `ai-feature-rollout-and-experimentation` — gates rollouts on eval.
- `ai-on-saas-architecture` — control-plane positioning.
## Consolidated Child References

- Load [references/routing.md](references/routing.md) to map retired AI child skill slugs to their reference modules.
