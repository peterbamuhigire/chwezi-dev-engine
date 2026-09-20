---
name: regex-vs-llm-structured-text
description: Decision framework for choosing between regex and an LLM call when parsing structured or semi-structured text (forms, invoices, quiz/exam content, scraped listings) — start with regex, add an LLM only for the low-confidence remainder. Relevant to this engine's scraping and document-processing work.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
  origin: "Adapted from affaan-m/ECC skills/regex-vs-llm-structured-text/SKILL.md"
---

# Regex vs LLM for Structured Text Parsing

A practical decision framework for parsing structured text. The key insight: regex handles 95–98%
of cases cheaply and deterministically when the source text is genuinely repetitive. Reserve
expensive, nondeterministic LLM calls for the remaining edge cases — and route straight to an LLM
when the text is not repetitive enough for regex to be worth building in the first place.

## When to Activate

- Parsing structured text with repeating patterns (questions, forms, tables, invoices)
- Deciding between regex and LLM extraction for a document- or scraping-processing pipeline
- Building a hybrid pipeline that combines both approaches
- Optimizing cost/accuracy tradeoffs in text extraction work

## Decision Framework

```
Is the text format consistent and repeating?
├── Yes (>90% follows a pattern) → Start with regex
│   ├── Regex handles 95%+ of items → done, no LLM needed
│   └── Regex handles <95%          → add an LLM call for the flagged edge cases only
└── No (free-form, highly variable) → use an LLM directly; do not spend time on a regex that will
                                        rot the first time the format shifts
```

## Architecture Pattern

```
Source Text
    │
    ▼
[Regex Parser] ─── extracts structure (95–98% accuracy on repetitive input)
    │
    ▼
[Text Cleaner] ─── removes noise (markers, page numbers, OCR artifacts)
    │
    ▼
[Confidence Scorer] ─── flags low-confidence extractions
    │
    ├── High confidence (≥0.95) → direct output
    │
    └── Low confidence (<0.95) → LLM validator → output
```

## Implementation

### 1. Regex parser (handles the majority)

```python
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class ParsedItem:
    id: str
    text: str
    choices: tuple[str, ...]
    answer: str
    confidence: float = 1.0

def parse_structured_text(content: str) -> list[ParsedItem]:
    pattern = re.compile(
        r"(?P<id>\d+)\.\s*(?P<text>.+?)\n"
        r"(?P<choices>(?:[A-D]\..+?\n)+)"
        r"Answer:\s*(?P<answer>[A-D])",
        re.MULTILINE | re.DOTALL,
    )
    items = []
    for match in pattern.finditer(content):
        choices = tuple(
            c.strip() for c in re.findall(r"[A-D]\.\s*(.+)", match.group("choices"))
        )
        items.append(ParsedItem(
            id=match.group("id"),
            text=match.group("text").strip(),
            choices=choices,
            answer=match.group("answer"),
        ))
    return items
```

### 2. Confidence scoring

```python
@dataclass(frozen=True)
class ConfidenceFlag:
    item_id: str
    score: float
    reasons: tuple[str, ...]

def score_confidence(item: ParsedItem) -> ConfidenceFlag:
    reasons = []
    score = 1.0
    if len(item.choices) < 3:
        reasons.append("few_choices"); score -= 0.3
    if not item.answer:
        reasons.append("missing_answer"); score -= 0.5
    if len(item.text) < 10:
        reasons.append("short_text"); score -= 0.2
    return ConfidenceFlag(item_id=item.id, score=max(0.0, score), reasons=tuple(reasons))

def identify_low_confidence(items: list[ParsedItem], threshold: float = 0.95) -> list[ConfidenceFlag]:
    flags = [score_confidence(item) for item in items]
    return [f for f in flags if f.score < threshold]
```

### 3. LLM validator (edge cases only)

Use the cheapest capable model tier for validation — this is a bounded correction task, not open
generation. Send only the flagged item and its original text span, never the full document.

### 4. Hybrid pipeline

```python
def process_document(content, *, llm_client=None, confidence_threshold=0.95):
    items = parse_structured_text(content)
    low_confidence = identify_low_confidence(items, confidence_threshold)
    if not low_confidence or llm_client is None:
        return items
    low_conf_ids = {f.item_id for f in low_confidence}
    result = []
    for item in items:
        if item.id in low_conf_ids:
            result.append(validate_with_llm(item, content, llm_client))
        else:
            result.append(item)
    return result
```

## Real-World Metrics (from a production 410-item parsing pipeline)

| Metric | Value |
|---|---|
| Regex success rate | 98.0% |
| Low-confidence items | 8 (2.0%) |
| LLM calls needed | ~5 |
| Cost savings vs. all-LLM | ~95% |
| Test coverage | 93% |

Treat these as an illustration of the achievable ratio on genuinely repetitive input, not a
universal benchmark — measure your own pipeline's regex hit rate before trusting the split.

## Best Practices

- Start with regex, even an imperfect one — it gives a baseline to improve against
- Use confidence scoring to programmatically decide what needs LLM help, rather than eyeballing it
- Use the cheapest capable model for validation
- Never mutate parsed items — return new instances from cleaning/validation steps
- TDD works well for parsers: write tests for known patterns first, then edge cases
- Log pipeline metrics (regex success rate, LLM call count) to track health over time

## Anti-Patterns to Avoid

- Sending all text to an LLM when regex handles 95%+ of cases
- Using regex for free-form, highly variable text — an LLM is the right tool there from the start
- Skipping confidence scoring and hoping regex "just works"
- Mutating parsed objects during cleaning/validation
- Not testing edge cases (malformed input, missing fields, encoding issues)

## When to Use

Quiz/exam question parsing, form data extraction, invoice/receipt processing, document structure
parsing (headers, sections, tables), and any other structured-text extraction where repeating
patterns exist and cost/determinism matters. For agentic RAG and query-refinement patterns, see
`skills/ai/ai-rag-patterns`; this skill is specifically about the regex-vs-LLM parsing decision, not
retrieval.
