# AC-E06 public skill discovery

The four original requests in routing.json use the public catalogue's normal lexical routing harness. It indexed 171 active skills. The same inputs on the starting revision and candidate moved ticket classification from rank 102 to 1 and grounded answers from 7 to 1. Incident recovery and AI-assisted code review stayed first. The two owned negative requests distinguish retrieval from prediction and database performance work from code review. These results measure discovery. E01–E05 contain the separate execution evidence.

Run `python -B -X utf8 scripts/routing_smoke_test.py --lint-fixtures`. The suite had 253 cases, 233 first-choice matches, 253 top-three matches and zero lint findings. Of 93 negative cases, 89 passed and four cross-engine cases remained unassessed locally. The public RAG and predictive skills own the changed intents. No new overlapping skill was needed. All four added prompts are original synthetic project examples with no private data or external media.

Run `python -B -X utf8 scripts/routing_smoke_test.py --collisions --collision-gate` and `python -B -X utf8 scripts/skill_catalog_guardrails.py`. The first catalogue attempt rejected two descriptions over 350 characters. Shorter descriptions preserved first-place routing for all four queries. The catalogue then passed with 17 warnings. The collision scan reported an allowed database-engine pair and one warning for level design versus content strategy.

The dated source check at 2026-11-23 failed with eight findings. Source-check output was byte-for-byte identical on the starting revision and this candidate. Existing overdue records remain open under their owners. See source-check.txt for the complete result.
