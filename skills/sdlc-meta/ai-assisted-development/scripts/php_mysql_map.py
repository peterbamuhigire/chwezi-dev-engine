#!/usr/bin/env python3
"""Map PHP routes to the MySQL tables they touch, with evidence tags.

Read-only and deterministic: it only reads files under --root and never runs PHP,
connects to a database or writes inside the target repository.

Route discovery (first match wins, or force with --routes):
  laravel   `routes/*.php` Route::verb('/uri', [Controller::class, 'method']) or 'Controller@method'
  files     every PHP file under `public/api/` (or --route-dir) is one route (file-routed apps)

Edges are followed:  route -> controller/endpoint file -> imported classes (PSR-4 from
composer.json, depth-limited) and local `require` files -> SQL string literals and
stored-procedure calls -> tables. Stored-procedure bodies are parsed from `*.sql` files
under --sql-dir (default: database/, db/, sql/ where present); a later definition of the
same procedure (by sorted path) replaces an earlier one.

Tags:
  EXTRACTED  table named in a literal SQL string, or in the body of a literal procedure call
  INFERRED   table name assembled from a literal fragment next to concatenation or
             interpolation (e.g. "FROM " . $prefix . "invoices"), or reached through a
             procedure whose name itself is assembled
  AMBIGUOUS  SQL whose table position is a variable (e.g. "SELECT * FROM {$table}")

When CREATE TABLE statements are found, only known table names are reported; other
names (aliases, CTEs, temporary tables) are counted as dropped.

Usage:
  python -X utf8 php_mysql_map.py --root DIR [--routes auto|laravel|files] [--route-dir public/api]
         [--sql-dir database] [--depth 3] [--table NAME] [--json OUT.json]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

SKIP_DIRS = {"vendor", "node_modules", ".git", "storage", "var", "cache"}
SQL_KEYWORD = re.compile(r"\b(select|insert|update|delete|replace|call|from|join|into)\b", re.I)
TABLE_AFTER = re.compile(
    r"\b(?:from|join|into|update|delete\s+from|replace\s+into|insert\s+(?:ignore\s+)?into|truncate(?:\s+table)?)\s+"
    r"(?!@)(?P<t>`?[A-Za-z_][A-Za-z0-9_]*`?(?:\.`?[A-Za-z_][A-Za-z0-9_]*`?)?|\{?\$[A-Za-z_][A-Za-z0-9_>\-\[\]'\"]*\}?)",
    re.I,
)
CALL_LITERAL = re.compile(r"\bcall\s+`?(?P<p>[A-Za-z_][A-Za-z0-9_]*)`?\s*\(", re.I)
SP_METHOD_CALL = re.compile(r"->\s*(?:call|callProcedure|callSp|sp|procedure|callOne|callAll)\s*\(\s*(['\"])(?P<p>[A-Za-z_][A-Za-z0-9_]*)\1", re.I)
CREATE_TABLE = re.compile(r"\bcreate\s+(?:temporary\s+)?table\s+(?:if\s+not\s+exists\s+)?`?(?P<t>[A-Za-z_][A-Za-z0-9_]*)`?", re.I)
CREATE_PROC = re.compile(
    r"\bcreate\s+(?:definer\s*=\s*\S+\s+)?(?:procedure|function)\s+(?:if\s+not\s+exists\s+)?`?(?:[A-Za-z_][A-Za-z0-9_]*`?\.`?)?(?P<p>[A-Za-z_][A-Za-z0-9_]*)`?",
    re.I,
)
PHP_STRING = re.compile(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"", re.S)
HEREDOC = re.compile(r"<<<\s*['\"]?(?P<id>[A-Za-z_][A-Za-z0-9_]*)['\"]?\s*\n(?P<body>.*?)\n\s*(?P=id)\b", re.S)
USE_STMT = re.compile(r"^\s*use\s+(?P<fqcn>[A-Za-z_\\][A-Za-z0-9_\\]*)(?:\s+as\s+(?P<alias>[A-Za-z_][A-Za-z0-9_]*))?\s*;", re.M)
NEW_OR_STATIC = re.compile(r"(?:new\s+\\?(?P<a>[A-Za-z_\\][A-Za-z0-9_\\]*)|\\?(?P<b>[A-Z][A-Za-z0-9_\\]*)::)")
REQUIRE = re.compile(r"\b(?:require|require_once|include|include_once)\s*\(?\s*__DIR__\s*\.\s*(['\"])(?P<p>[^'\"]+)\1")
LARAVEL_ROUTE = re.compile(
    r"Route::(?P<verb>get|post|put|patch|delete|any|match)\s*\(\s*(?P<q1>['\"])(?P<uri>[^'\"]*)(?P=q1)\s*,\s*"
    r"(?:\[\s*\\?(?P<ctl>[A-Za-z_\\][A-Za-z0-9_\\]*)::class\s*,\s*(?P<q2>['\"])(?P<m>[A-Za-z_][A-Za-z0-9_]*)(?P=q2)\s*\]"
    r"|(?P<q3>['\"])(?P<ctl2>[A-Za-z_\\][A-Za-z0-9_\\]*)@(?P<m2>[A-Za-z_][A-Za-z0-9_]*)(?P=q3))",
    re.I,
)
SCHEMA_CREATE = re.compile(r"Schema::create\(\s*(['\"])(?P<t>[A-Za-z_][A-Za-z0-9_]*)\1")
QUERY_BUILDER = re.compile(r"(?:DB::table|->table|->from)\(\s*(['\"])(?P<t>[A-Za-z_][A-Za-z0-9_]*)\1")
ELOQUENT_TABLE = re.compile(r"protected\s+\$table\s*=\s*(['\"])(?P<t>[A-Za-z_][A-Za-z0-9_]*)\1")
RANK = {"EXTRACTED": 0, "INFERRED": 1, "AMBIGUOUS": 2}


def strip_php_comments(text: str) -> str:
    """Remove // # and /* */ comments while keeping strings and line numbers."""
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c in "'\"":
            m = PHP_STRING.match(text, i)
            if m:
                out.append(m.group(0))
                i = m.end()
                continue
        if text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append("\n" * text.count("\n", i, j))
            i = j
            continue
        if text.startswith("//", i) or (c == "#" and not text.startswith("#[", i)):
            j = text.find("\n", i)
            j = n if j < 0 else j
            i = j
            continue
        out.append(c)
        i += 1
    return "".join(out)


def strip_sql_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    return re.sub(r"(--|#)[^\n]*", " ", text)


def clean_table(raw: str) -> str:
    name = raw.replace("`", "")
    return name.split(".")[-1].lower()


class Mapper:
    def __init__(self, root: Path, sql_dirs: list[Path], depth: int):
        self.root = root
        self.depth = depth
        self.known_tables: set[str] = set()
        self.procs: dict[str, dict] = {}
        self.psr4 = self._load_psr4()
        self.dropped: set[str] = set()
        self._file_cache: dict[Path, str] = {}
        self._load_sql(sql_dirs)

    # ---------- SQL side ----------
    def _load_sql(self, sql_dirs: list[Path]) -> None:
        files: list[Path] = []
        for d in sql_dirs:
            if d.is_dir():
                files.extend(p for p in d.rglob("*.sql") if not (set(p.relative_to(self.root).parts) & SKIP_DIRS))
        for path in sorted(set(files), key=lambda p: p.as_posix().lower()):
            text = strip_sql_comments(self._read(path))
            for m in CREATE_TABLE.finditer(text):
                self.known_tables.add(m.group("t").lower())
            starts = list(CREATE_PROC.finditer(text))
            for idx, m in enumerate(starts):
                end = starts[idx + 1].start() if idx + 1 < len(starts) else len(text)
                body = text[m.end():end]
                delim = re.search(r"\n\s*DELIMITER\b", body, re.I)
                if delim:
                    body = body[: delim.start()]
                tables = {clean_table(t.group("t")) for t in TABLE_AFTER.finditer(body) if not t.group("t").startswith(("$", "{"))}
                calls = {c.group("p").lower() for c in CALL_LITERAL.finditer(body)}
                # dynamic SQL: table names held in quoted literals feed PREPARE/EXECUTE
                dynamic = set()
                if re.search(r"\bprepare\b", body, re.I):
                    dynamic = {q.lower() for q in re.findall(r"'([A-Za-z_][A-Za-z0-9_]*)'", body)}
                # a procedure redefined in several files: keep the union (over-report, never under-report)
                entry = self.procs.setdefault(m.group("p").lower(), {"tables": set(), "dynamic": set(), "calls": set(), "defined_in": []})
                entry["tables"] |= tables
                entry["dynamic"] |= dynamic
                entry["calls"] |= calls
                entry["defined_in"].append(path.relative_to(self.root).as_posix())
        # Laravel-style PHP migrations: Schema::create('table', ...)
        php_migrations: list[Path] = []
        for d in sql_dirs:
            if d.is_dir():
                php_migrations.extend(p for p in d.rglob("*.php") if not (set(p.relative_to(self.root).parts) & SKIP_DIRS))
        for path in sorted(set(php_migrations), key=lambda p: p.as_posix().lower()):
            for m in SCHEMA_CREATE.finditer(self._read(path)):
                self.known_tables.add(m.group("t").lower())

    def proc_tables(self, name: str, seen: set[str] | None = None) -> dict[str, str]:
        """Tables a procedure touches, transitively: {table: tag}."""
        seen = seen if seen is not None else set()
        if name in seen or name not in self.procs:
            return {}
        seen.add(name)
        proc = self.procs[name]
        out: dict[str, str] = {t: "INFERRED" for t in proc["dynamic"] if t in self.known_tables}
        out.update({t: "EXTRACTED" for t in proc["tables"]})
        for callee in sorted(proc["calls"]):
            for t, tag in self.proc_tables(callee, seen).items():
                if t not in out or RANK[tag] < RANK[out[t]]:
                    out[t] = tag
        return out

    # ---------- PHP side ----------
    def _read(self, path: Path) -> str:
        if path not in self._file_cache:
            try:
                self._file_cache[path] = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                self._file_cache[path] = ""
        return self._file_cache[path]

    def _load_psr4(self) -> list[tuple[str, Path]]:
        comp = self.root / "composer.json"
        maps: list[tuple[str, Path]] = []
        try:
            data = json.loads(comp.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return maps
        for prefix, dirs in ((data.get("autoload") or {}).get("psr-4") or {}).items():
            for d in dirs if isinstance(dirs, list) else [dirs]:
                maps.append((prefix, self.root / d))
        return sorted(maps, key=lambda x: -len(x[0]))

    def resolve_class(self, fqcn: str) -> Path | None:
        fqcn = fqcn.lstrip("\\")
        for prefix, base in self.psr4:
            if fqcn.startswith(prefix):
                candidate = base / (fqcn[len(prefix):].replace("\\", "/") + ".php")
                if candidate.is_file():
                    return candidate
        return None

    def php_edges(self, path: Path) -> tuple[list[tuple[str, str, str]], list[Path]]:
        """Return ([(table, tag, detail)], [next files]) for one PHP file."""
        text = strip_php_comments(self._read(path))
        edges: list[tuple[str, str, str]] = []
        rel = path.relative_to(self.root).as_posix()

        literals: list[tuple[str, int, bool]] = []  # (content, offset, adjoining concatenation)
        string_matches = list(PHP_STRING.finditer(text))
        for idx, m in enumerate(string_matches):
            s = m.group(0)
            before = text[max(0, m.start() - 3):m.start()]
            after = text[m.end():m.end() + 3]
            concat_after = after.strip()[:1] == "."
            concat = "." in before.strip()[-1:] or concat_after
            literals.append((s[1:-1], m.start(), concat or (s[0] == '"' and "$" in s)))
            # "... FROM " . $prefix . "invoices": the table name is split across the concatenation
            if concat_after and re.search(r"\b(from|join|into|update)\s*$", s[1:-1], re.I):
                line = text.count("\n", 0, m.start()) + 1
                stmt_end = text.find(";", m.end())
                stmt_end = len(text) if stmt_end < 0 else stmt_end
                nxt_lit = string_matches[idx + 1] if idx + 1 < len(string_matches) else None
                if nxt_lit and nxt_lit.start() < stmt_end:
                    ident = re.match(r"\s*`?([A-Za-z_][A-Za-z0-9_]*)", nxt_lit.group(0)[1:-1])
                    if ident:
                        edges.append((ident.group(1).lower(), "INFERRED", f"{rel}:{line} concatenated name"))
                        continue
                edges.append(("?dynamic", "AMBIGUOUS", f"{rel}:{line} table from a variable"))
        for rx in (QUERY_BUILDER, ELOQUENT_TABLE):
            for m in rx.finditer(text):
                edges.append((m.group("t").lower(), "EXTRACTED", f"{rel}:{text.count(chr(10), 0, m.start()) + 1}"))
        for m in HEREDOC.finditer(text):
            literals.append((m.group("body"), m.start(), "$" in m.group("body")))

        for content, offset, dynamic in literals:
            line = text.count("\n", 0, offset) + 1
            if not SQL_KEYWORD.search(content):
                continue
            for c in CALL_LITERAL.finditer(content):
                for t, tag in sorted(self.proc_tables(c.group("p").lower()).items()):
                    edges.append((t, tag, f"{rel}:{line} CALL {c.group('p')}"))
            for t in TABLE_AFTER.finditer(content):
                raw = t.group("t")
                if raw.startswith(("$", "{")):
                    edges.append(("?" + raw.strip("{}"), "AMBIGUOUS", f"{rel}:{line} dynamic table"))
                    continue
                # a fragment right before concatenation may be incomplete
                tag = "INFERRED" if dynamic and content.rstrip().endswith(raw) else "EXTRACTED"
                edges.append((clean_table(raw), tag, f"{rel}:{line}"))
        for m in SP_METHOD_CALL.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            for t, tag in sorted(self.proc_tables(m.group("p").lower()).items()):
                edges.append((t, tag, f"{rel}:{line} sp {m.group('p')}"))

        nxt: list[Path] = []
        imports = {}
        for u in USE_STMT.finditer(text):
            short = u.group("alias") or u.group("fqcn").split("\\")[-1]
            imports[short] = u.group("fqcn")
        referenced = set()
        for m in NEW_OR_STATIC.finditer(text):
            name = m.group("a") or m.group("b")
            referenced.add(name)
        for short, fqcn in imports.items():
            if short in referenced or re.search(rf"\b{re.escape(short)}\b", text[text.find(fqcn) + len(fqcn):] if fqcn in text else text):
                target = self.resolve_class(fqcn)
                if target:
                    nxt.append(target)
        for name in referenced:
            if "\\" in name:
                target = self.resolve_class(name)
                if target:
                    nxt.append(target)
        for r in REQUIRE.finditer(text):
            target = (path.parent / r.group("p").lstrip("/")).resolve()
            if target.is_file():
                nxt.append(target)
        return edges, sorted(set(nxt))

    def route_tables(self, entry: Path, shared: set[Path]) -> dict[str, dict]:
        result: dict[str, dict] = {}
        frontier = [(entry, 0)]
        seen: set[Path] = set()
        while frontier:
            path, depth = frontier.pop(0)
            if path in seen:
                continue
            seen.add(path)
            edges, nxt = self.php_edges(path)
            for table, tag, detail in edges:
                if not table.startswith("?") and self.known_tables and table not in self.known_tables:
                    self.dropped.add(table)
                    continue
                cur = result.get(table)
                if cur is None or RANK[tag] < RANK[cur["tag"]]:
                    result[table] = {"tag": tag, "evidence": [detail]}
                elif RANK[tag] == RANK[cur["tag"]] and len(cur["evidence"]) < 3 and detail not in cur["evidence"]:
                    cur["evidence"].append(detail)
            if depth < self.depth:
                frontier.extend((p, depth + 1) for p in nxt if p not in shared)
        return dict(sorted(result.items()))


def discover_routes(root: Path, mode: str, route_dir: str) -> list[tuple[str, Path]]:
    routes: list[tuple[str, Path]] = []
    if mode in ("auto", "laravel") and (root / "routes").is_dir():
        mapper_psr = Mapper(root, [], 0)
        for rf in sorted((root / "routes").glob("*.php")):
            text = strip_php_comments(rf.read_text(encoding="utf-8", errors="replace"))
            imports = {u.group("alias") or u.group("fqcn").split("\\")[-1]: u.group("fqcn") for u in USE_STMT.finditer(text)}
            for m in LARAVEL_ROUTE.finditer(text):
                ctl = m.group("ctl") or m.group("ctl2")
                fq = imports.get(ctl, ctl if "\\" in ctl else f"App\\Http\\Controllers\\{ctl}")
                target = mapper_psr.resolve_class(fq)
                if target:
                    routes.append((f"{m.group('verb').upper()} {m.group('uri')} -> {ctl}@{m.group('m') or m.group('m2')}", target))
        if routes or mode == "laravel":
            return routes
    base = root / route_dir
    for p in sorted(base.rglob("*.php"), key=lambda x: x.as_posix()):
        rel = p.relative_to(root).as_posix()
        if p.name.startswith("_"):
            continue
        routes.append((rel, p))
    return routes


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Map PHP routes to MySQL tables (read-only).")
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--routes", choices=["auto", "laravel", "files"], default="auto")
    ap.add_argument("--route-dir", default="public/api")
    ap.add_argument("--sql-dir", action="append", default=None)
    ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--exclude-dir", action="append", default=None,
                    help="Directories treated as cross-cutting infrastructure and not followed (default: bootstrap, config).")
    ap.add_argument("--shared-threshold", type=float, default=0.3,
                    help="Skip files required by more than this share of routes (bootstrap/common files).")
    ap.add_argument("--table", default=None, help="Answer 'what touches table X'.")
    ap.add_argument("--json", type=Path, default=None, help="Write the full map as JSON to this path.")
    args = ap.parse_args(argv)

    root = args.root.resolve()
    if not root.is_dir():
        print(f"usage error: {root} is not a directory", file=sys.stderr)
        return 2
    sql_dirs = [root / d for d in (args.sql_dir or ["database", "db", "sql"])]
    mapper = Mapper(root, sql_dirs, args.depth)
    routes = discover_routes(root, args.routes, args.route_dir)

    # shared includes: files directly required/imported by most routes
    counts: dict[Path, int] = defaultdict(int)
    for _name, path in routes:
        for p in mapper.php_edges(path)[1]:
            counts[p] += 1
    # the share heuristic needs enough routes to mean anything
    shared = {p for p, c in counts.items() if len(routes) >= 20 and c / len(routes) > args.shared_threshold}
    for d in (args.exclude_dir or ["bootstrap", "config"]):
        base = (root / d).resolve()
        if base.is_dir():
            shared |= {p.resolve() for p in base.rglob("*.php")}

    out = {
        "root": root.as_posix(),
        "route_mode": args.routes,
        "known_tables": len(mapper.known_tables),
        "procedures": len(mapper.procs),
        "shared_files_skipped": sorted(p.relative_to(root).as_posix() for p in shared),
        "routes": {},
    }
    by_table: dict[str, list[str]] = defaultdict(list)
    for name, path in routes:
        tables = mapper.route_tables(path, shared)
        out["routes"][name] = tables
        for t, info in tables.items():
            by_table[t].append(f"{name} [{info['tag']}]")
    out["tables"] = {t: sorted(v) for t, v in sorted(by_table.items())}
    out["dropped_unknown_names"] = sorted(mapper.dropped)

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(out, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    if args.table:
        hits = out["tables"].get(args.table.lower(), [])
        print(f"table {args.table}: {len(hits)} route(s)")
        for h in hits:
            print(f"  {h}")
    else:
        tags = defaultdict(int)
        for tables in out["routes"].values():
            for info in tables.values():
                tags[info["tag"]] += 1
        print(f"php-mysql-map: {len(routes)} routes, {len(mapper.known_tables)} known tables, {len(mapper.procs)} procedures")
        print("edges: " + ", ".join(f"{k}={tags[k]}" for k in ("EXTRACTED", "INFERRED", "AMBIGUOUS")))
        for name, tables in out["routes"].items():
            print(f"{name}: " + ", ".join(f"{t}({i['tag'][0]})" for t, i in tables.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
