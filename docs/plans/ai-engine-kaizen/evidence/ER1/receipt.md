# AC-ER1 release evidence inventory

- **Observed starting revision:** `7965083c0dedbfd5c6e52847d1c2db9ddfec3dba`
- **Acceptance:** AC-ER1
- **Inventory:** [front-door-inventory.md](front-door-inventory.md), structured claims in [claim-inventory.json](claim-inventory.json)
- **Producer integration evidence:** [build-attestations.json](build-attestations.json) is a public-safe transcription of the four task-supplied build integration attestations checked 2026-11-23. All four producer repositories report integrated; the private Development engine's revision identifiers are deliberately omitted.
- **Observed output:** [check.txt](check.txt)
- **Local integrated revision recorded:** `7965083c0dedbfd5c6e52847d1c2db9ddfec3dba`
- **Accepted packet revisions:** E01 `e5c2bb62e2cd2c36be4993d3e4172f6c8a167238`; E02 `94de845b8482823ba516dacbd7e73a4e03c93413`; E03 `006b535063c452cc23feae3a9eb9d619c07beb88`; E04 `e721eb2a0f81c16c1a6f95ae13ec74dcdb7bbafe`; E05 `c3bd56826e4fbc9568ecd34e87b02f55caf9e64d`; E06 `dd03a4170539feaa34535ec953558d328f1398b2`. All six are local ancestors at the recorded integrated revision.
- **Fixture digest:** `casebook.md` SHA-256 `cb00e249cef5153b0926a03affe42e7f901d7ab906c5d52c92b656ed3bcf8921`.
- **Targeted procedure:** `python -B docs/plans/ai-engine-kaizen/evidence/ER1/check_inventory.py`
- **Independent oracle:** the checker resolves entry points/evidence on disk, confirms each accepted revision is a Git ancestor of the recorded integrated revision, compares the frozen casebook digest, checks preserved license/history destinations, and runs an in-memory missing-owner negative control.
- **Observed result:** `PASS: AC-ER1 inventory, 6 claims, 6 accepted packets, front-door destinations resolve`; `PASS: negative control rejects a missing claim owner`.
- **Negative control:** the checker removes the first claim's owner in memory; its required-field assertion fails as expected. No fixture or source file is mutated.
- **Rework:** an initial entry-point review found four example README paths that did not exist. The inventory now links to the actual runnable scripts and skills. The checker then passed all route, receipt, revision and digest assertions.

## Limits and currentness

All six packet revisions are accepted by `build.contract.json` and are local ancestors of the integrated revision. The results support only the environments and limits recorded per claim. The model release notes were checked on 2026-11-23: the official pages describe GPT-6.2 Astra/Sol announcements dated 2026-11-17 and Work/Codex preview availability. Actual account/runtime availability is `NOT_ASSESSED`. `.codex/ensure_model_policy.py --runtime codex --check` reports `DRIFT: root model policy drift`; no host configuration was changed and no model-policy change is proposed.

The ER1 inventory and consistency check are not human user acceptance. Hosted inference, real model quality, production behavior, live routing, platform-specific installation replay, and independent supervisor final verification remain outside this slice or `NOT_ASSESSED`. Manual anti-slop review found specific claims and named limits, with no blocking unsupported claim in this inventory; structural genericness scoring and independent human review were not performed (`NOT_ASSESSED`).
