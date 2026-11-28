# Improvement backlog

| Priority | Decision and proof |
|---|---|
| P0 | No additional P0 demonstrated in the changed workflow. Security and licensing exceptions remain outside the score. |
| P1 | `scripts/skill_catalog_guardrails.py`. The YAML parser measures from the first line after the frontmatter delimiter. The author sees a different line number. Translate the marked line into file coordinates. Exercise malformed LF and CRLF inputs and retain the separate unmarked-error path. |
| P2 | The skill cap remains 200. Historical alias families are not installable entrypoints. The empty local .kaizen directory has no tracked contract in this cycle. Skills overlapping the retained catalogue remain in place; functional parity is unmeasured. |

Owner: repository maintainer. Counter-metric: Malformed line three points to line three, column fifteen. Valid skills and the error classification stay unchanged. Roll back the owning change and its paired regression together if the ordinary case fails. Retain all failed observations.

Nystrom (2021), *Crafting Interpreters*, §4.1.1. Report a diagnostic where the author can correct it. PyYAML's Mark counts from zero; verified against the local parser on both newline conventions and its public documentation, accessed 2026-11-28.
