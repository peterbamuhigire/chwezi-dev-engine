# Deep-Module Design and Design It Twice

A module is deep when a small, stable interface hides substantial policy, sequencing, failure, and
integration complexity. Depth is not line count. Prefer interfaces that reduce what callers must know.

## Depth review

| Question | Evidence |
| --- | --- |
| What complexity disappears behind the interface? | caller before/after knowledge list |
| Which concepts leak through? | parameters, errors, ordering, shared state, or setup callers must understand |
| Is the seam aligned to one capability and owner? | change history, responsibility, and data authority |
| Can the implementation be replaced? | adapter or contract test at the seam |
| What is the deletion test? | files, branches, and caller knowledge removed if the module owns the concern |

Avoid shallow forwarding layers that rename calls without hiding decisions. Avoid a large interface
that exposes every implementation option. Record locality: the smallest set of files and concepts a
maintainer must load to change one behaviour safely.

## Design it twice

Produce two genuinely different interfaces under the same drivers. Vary at least three constraints,
such as caller knowledge, state ownership, sync/async boundary, error model, evolution path, or test
seam. Do not compare cosmetic naming variants.

Score each option against user flow, invariants, change cost, operational failure, security, data
ownership, migration, testability, and rollback. Select one, preserve the rejected option and reason,
and name the evidence that would reopen the decision.

## Deepening experiment

Choose one frequently changed or defect-prone seam from history. Baseline caller complexity, files
touched, escaped defects, test duration, and rollback difficulty. Make the smallest boundary change,
exercise normal and failure paths, and retain it only when locality or leverage improves without
moving hidden risk elsewhere.

This reference adapts deep-module, seam, deletion-test, and design-it-twice mechanisms studied in
Matt Pocock's `mattpocock/skills` repository at commit `3cca18b`.
