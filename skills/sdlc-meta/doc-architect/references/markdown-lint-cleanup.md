# Markdown Lint Cleanup

Parent skill: [doc-architect](../SKILL.md). Absorbed from the retired `markdown-lint-cleanup`
skill (2026-09-24); the original text is retained in
`skills/sdlc-meta/markdown-lint-cleanup/ALIAS.md`.

Load this reference when Markdown lint warnings must be cleared, or a documentation set needs
mechanical formatting normalisation without any change of meaning.

## Rules most often at fault

| Rule | Alias | Fix |
|---|---|---|
| MD022 | blanks-around-headings | Blank line before and after each heading |
| MD031 | blanks-around-fences | Blank line before and after each fenced block |
| MD032 | blanks-around-lists | Blank line before and after each list |
| MD036 | no-emphasis-as-heading | Replace a bold-only line used as a title with a real `##` heading |
| MD040 | fenced-code-language | Add a language tag (`bash`, `php`, `sql`, `json`, `text`) |

Before and after for MD036 and MD040:

````text
**Deployment**            ->   ## Deployment

```                       ->   ```bash
php artisan migrate            php artisan migrate
```                            ```
````

## Procedure

1. Run the project's configured linter (`markdownlint-cli2`, `markdownlint`, or the repository's
   own script) and capture warnings with file and line numbers. Honour the repository's lint
   configuration over these defaults.
2. Apply the narrowest fix per warning.
3. Re-run until clean, or record each intentionally retained exception with its reason.

## Safety rules

- Never reword prose, reorder content, or change meaning; formatting only.
- Preserve links, anchors, and references exactly. If a heading change alters an anchor, find
  and update every in-repo link to it, or leave the heading alone.
- Do not guess a fence language; use `text` when unsure.
- Do not reformat vendored, generated, or third-party files unless asked.
- If a fix would alter meaning, stop and report it separately.

## Output

Cleaned files, the lint command and its final result, and a list of retained exceptions.
Without execution, return the patch and name the lint command still required; never claim a
clean run without evidence.

## Evidence and currentness

Rule IDs and aliases follow the `DavidAnson/markdownlint` rule set. Not re-verified against the
live rule documentation on 2026-09-24 (NOT_ASSESSED); confirm rule names if the linter version
is unusual.
