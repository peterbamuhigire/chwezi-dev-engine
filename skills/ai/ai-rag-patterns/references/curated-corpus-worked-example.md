# Curated Corpus Worked Example: Lexical Retrieval with Calibrated Abstention

Load when the knowledge base is small, curated and owned (a few hundred to a few thousand short
records), when answers must cite a specific record, or when "I do not have a rule for that" is a
better answer than a plausible guess. The example is synthetic: a corpus of engineering-standard
snippets for an internal assistant. No real client data or third-party dataset is used.

## 1. The corpus

Each record is short, has one owner and one purpose:

```json
{ "id": "ENG-DB-014", "domain": "database", "title": "Money columns",
  "text": "Store money as DECIMAL(15,2) in MySQL, never FLOAT or DOUBLE. Round only at posting.",
  "owner": "platform-team", "updated": "2026-08-12" }
```

Rules for the corpus:

- one rule per record; split a record that needs "and also";
- a stable ID that answers cite;
- a `domain` field (database, security, api, testing, ui) used for score floors;
- an `updated` date and an owner, so stale records can be found.

About 600 such records fit comfortably in memory. A vector database is not needed at this size.

## 2. Lexical ranking

Rank with BM25 over `title` and `text`, with the title weighted higher. The scoring formula,
tokenisation and the hybrid (BM25 + vector + reciprocal rank fusion) option are covered in
[production-rag.md](production-rag.md) ("Failure Mode Playbook", hybrid search); do not
re-implement them differently here. For a curated corpus, plain BM25 is usually enough because
the vocabulary is controlled: the records and the questions use the same engineering terms.

Normalise before indexing: lower-case, strip punctuation except inside identifiers
(`DECIMAL(15,2)` stays one token), and keep British and American spellings as synonyms
(`normalise`/`normalize`).

## 3. Per-domain score floors

Raw BM25 scores are not comparable across domains: a short security record scores differently
from a long API record. Set a floor per domain from the golden set (section 5):

| Domain | Floor (BM25) | How set |
|---|---|---|
| database | 7.5 | Lowest score of a correct top-1 answer in the calibration split, minus a margin |
| security | 9.0 | Higher: a wrong security answer costs more than no answer |
| api | 6.0 | As database |
| testing | 6.5 | As database |

A result below its domain floor is not shown as an answer.

## 4. Calibrated abstention as a first-class result

Abstention is an answer type, not an error:

```json
{ "status": "ABSTAIN", "reason": "below_floor", "domain": "security",
  "best_candidate": { "id": "ENG-SEC-031", "score": 6.2, "floor": 9.0 },
  "message": "No engineering standard covers this question closely enough. Ask the security owner." }
```

- The interface shows abstentions plainly and routes them to the record owner.
- Abstentions are logged; clusters of similar abstained questions show where a record is missing.
- The generator (if an LLM phrases the answer) receives only records above the floor. With none,
  it is not called.

## 5. Graded golden set, held-out split, fingerprinted baseline

Build a golden set of real questions with graded relevance, not just one "right" record:

```json
{ "q": "What column type for invoice totals?", "domain": "database",
  "grades": { "ENG-DB-014": 3, "ENG-DB-015": 1 }, "expect": "ANSWER" }
{ "q": "Can we store card numbers in the audit log?", "domain": "security",
  "grades": { "ENG-SEC-007": 3 }, "expect": "ANSWER" }
{ "q": "Which font should the admin panel use?", "domain": "ui",
  "grades": {}, "expect": "ABSTAIN" }
```

Grades: 3 = answers the question, 2 = relevant, 1 = related, 0 = not relevant. Include questions
whose correct result is abstention.

- **Split:** calibration (floors are tuned here) and held-out (reported, never tuned on), for
  example 70/30, fixed by question ID.
- **Metrics on held-out:** nDCG@5 for ranking, answer precision (answers shown that were correct),
  abstention precision and recall (abstained when it should, and only then).
- **Fingerprint the baseline:** record the SHA-256 of the corpus file, the golden-set file and the
  ranking configuration (floors, weights, tokeniser version) beside the metric values. A later run
  is comparable only if the fingerprints match, or the report says which one changed.

```json
{ "run": "2026-09-29", "corpus_sha256": "…", "golden_sha256": "…", "config_sha256": "…",
  "heldout": { "ndcg@5": 0.81, "answer_precision": 0.93, "abstain_precision": 0.88, "abstain_recall": 0.79 } }
```

## 6. Gates

- A corpus or floor change ships only if held-out answer precision does not fall and abstention
  recall does not fall, against the fingerprinted baseline.
- Every new record adds at least one golden question.
- Records older than the review period are listed for their owner.

(Retrieval harness design (curated corpus, lexical ranking, abstention and graded golden set)
adapted from nextlevelbuilder/ui-ux-pro-max-skill, MIT, commit
`09170eec67eefd46a7ae85de61b40c194020f997`. Only the harness design is adapted; no rows, font or
palette data are used.)
