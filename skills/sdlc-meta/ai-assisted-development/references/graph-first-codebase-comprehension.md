# Graph-First Codebase Comprehension

Load before changing code you do not yet understand: a legacy module, an unfamiliar repository, or a
change whose blast radius you must state. The rule is to ask a structural index first and read files
second, and to treat every answer from an index as evidence with a freshness date, not as truth.

This reference is tool-agnostic. It names kinds of index, not products. Nothing here asks you to
install a tool on the host. Under the Skills Kaizen P06 decision (27 Sep 2026) Graphify is rejected
for this host and an LSP pilot is deferred; use only what the project already has.

## 1. Query-first order

Work down this list and stop as soon as you have enough:

1. **Existing index.** Whatever the project already maintains and pins: a language server (LSP)
   running in the editor, a `tags` file from ctags, a committed project map (`docs/architecture/`,
   a module list, a route list), or a graph file that is already present and pinned to a commit.
2. **Scoped query.** Ask the index a narrow question: "who calls `CreditNoteService::post`",
   "which routes reach `InvoiceController`", "what reads `credit_notes`".
3. **Targeted reads.** Open only the files and line ranges the query named. Read the callers and
   the callee, not the whole directory.
4. **Broad search last.** `git grep` or ripgrep across the repository, used to confirm or fill gaps
   in what the index said, never as the first move on a large codebase.

Record which step answered the question. "Callers found by LSP at `a1b2c3d`" is evidence; "I looked
around" is not.

## 2. Staleness rules

An index describes the code as it was when it was built.

- **File newer than the index:** if the target file's last change is later than the index build,
  the index is stale for that file.
- **Rebuild after** a pull, merge, rebase or branch switch. The build time alone is not enough: the
  checked-out commit must match the one the index was built from.
- **Stale means verify in source.** A stale answer is a lead. Confirm it by reading the file before
  you edit anything or report a blast radius.
- Record the index's build time and the full commit SHA beside any claim that relies on it (see
  `implementation-status-auditor/references/drill-down-templates.md` for the status column).

## 3. Evidence tags

Tag every structural claim:

| Tag | Meaning | What you may do with it |
|---|---|---|
| EXTRACTED | Read directly from source text: a literal call, a literal SQL table name, an import | Rely on it for this commit |
| INFERRED | Resolved by a tool or by reasoning: a method resolved through an interface, a table name built from a constant | Verify in source before editing |
| AMBIGUOUS | Cannot be resolved statically: dynamic method names, table names from user input, reflection, magic methods | Flag for review; never count it as absent |

## 4. PHP caveat

Many indexers do not resolve PHP member calls such as `$this->repository->save()` or
`$this->service->post()` to their target class, so they under-report callers. The same applies to
facades, `__call`, container lookups by string and dynamic `$method()` calls.

- "Zero callers" from any index is **never** accepted for PHP without a text search for the method
  name: `git grep -n "->post(" -- "*.php"` and `git grep -n "::post(" -- "*.php"`.
- Route files, service-container bindings, event listeners and queued jobs are callers too; search
  them by class name.
- A blast-radius answer for PHP lists index callers (INFERRED) and grep callers (EXTRACTED)
  separately.

## 5. Grep recipe for PHP/MySQL (routes → controllers → services → tables)

When there is no usable index, this sequence gives a first map. All commands are read-only.

```bash
# Routes and their controller actions (Laravel-style; adjust the glob for plain PHP routers)
git grep -nE "Route::(get|post|put|patch|delete|match|any|resource)\(" -- "routes/*.php"
# Controllers and the services they take in their constructors
git grep -nE "public function __construct\(" -- "app/Http/Controllers"
# Literal table names in query builders and Eloquent models
git grep -nE "DB::table\('[a-z_]+'\)|protected \\\$table *= *'[a-z_]+'" -- "*.php"
# Raw SQL that names a table
git grep -nEi "\b(from|into|update|join)\s+\`?[a-z_]+\`?" -- "*.php"
# Tables created or changed by migrations
git grep -nE "Schema::(create|table)\('[a-z_]+'" -- "database/migrations"
```

Tag results by the rules in section 3: a literal table name is EXTRACTED; a name built from a
constant or a model default (plural of the class name) is INFERRED; a name from a variable is
AMBIGUOUS. `scripts/php_mysql_map.py` in this skill automates this recipe and applies the tags; see
its pilot record before relying on it.

## 6. Windows notes

- Run `git grep` from Git Bash or PowerShell; quote patterns in single quotes in Bash and escape `$`
  as shown above. In PowerShell, prefer `git grep` over `Select-String` for speed on large trees.
- Path separators: tools on Windows may print `app\Http\...`; normalise to `/` before comparing with
  index output.
- Line endings do not change line numbers, but a file converted between CRLF and LF shows as
  changed and can make an index look stale. Check `git status` before trusting a staleness verdict.
- Long paths: enable `core.longpaths` in the clone if a vendor tree fails to index.

## 7. Output

A comprehension note states: the question, the index used (kind, build time, full commit SHA), the
answer with a tag per claim, the grep confirmations, and what remains AMBIGUOUS. Keep it beside the
plan so a reviewer can re-run it.

(Query-first order, staleness rules and the EXTRACTED/INFERRED/AMBIGUOUS vocabulary adapted from
Graphify-Labs/graphify, Apache-2.0, https://github.com/Graphify-Labs/graphify, commit
`d6eaa8aae8df155874ebb1044302c055c286342a`. Paraphrased; no file or substantial text copied.)
