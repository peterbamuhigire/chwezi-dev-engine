#!/usr/bin/env python3
"""Find one Chwezi skill on demand instead of preloading every skill description.

Usage: python auto-agents/find_skill.py "words describing the task" [--engine writing] [--limit 5]

Searches only each engine's canonical skill folders (never dist/, marketplace or test copies),
ranks by the frontmatter name and description, and prints paths to Read. Content-free: it
reads frontmatter and the first paragraph only.
"""
import argparse, os, re, subprocess, sys
from pathlib import Path

# key: (folder names tried in order, globs relative to the engine root)
ENGINES = {
    'development': (('chwezi-development-engine',), ('skills/**/SKILL.md',)),
    'writing': (('chwezi-writing-engine',), ('skills/**/SKILL.md',)),
    'orchestrator': (('chwezi-engine-agents', 'skills-engine-agents'), ('core/instructions/*.md', 'skills/**/SKILL.md')),
    'accounting': (('chwezi-accounting-doctrine',), ('skills/**/SKILL.md',)),
    'knowledge-bank': (('chwezi-knowledge-bank',), ('plugins/*/skills/*/SKILL.md',)),
}
ROUTERS = ('AGENTS.md', 'CLAUDE.md', 'README.md')
STOP = set('the and for with from into that this then than when what your use using need needs task work make add new code file files'.split())


def engines_root(explicit=None):
    if explicit: return Path(explicit)
    if os.environ.get('CHWEZI_ENGINES_ROOT'): return Path(os.environ['CHWEZI_ENGINES_ROOT'])
    try:
        common = subprocess.run(['git', 'rev-parse', '--path-format=absolute', '--git-common-dir'],
                                capture_output=True, text=True, timeout=30, check=True).stdout.strip()
        # <projects>/<repo>/.git -> <projects>; worktrees share the main checkout's common dir.
        return Path(common).resolve().parent.parent
    except (OSError, subprocess.SubprocessError):
        return Path.cwd().resolve().parent


def locate(root, key):
    for folder in ENGINES[key][0]:
        if (root / folder).is_dir(): return root / folder
    return None


def frontmatter(path):
    try: text = path.read_text(encoding='utf-8', errors='replace')
    except OSError: return None, ''
    name, desc, body = None, '', text
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end > 0:
            head, body = text[3:end], text[end + 4:]
            lines = head.splitlines()
            for i, line in enumerate(lines):
                m = re.match(r'(name|description):\s*(.*)$', line)
                if not m: continue
                value = m.group(2).strip()
                if m.group(1) == 'description' and value in ('', '>', '|', '>-', '|-'):
                    value = ' '.join(l.strip() for l in lines[i + 1:] if l.startswith((' ', '\t')))
                value = value.strip('"\'')
                if m.group(1) == 'name': name = value
                else: desc = value
    if not desc:  # first prose paragraph
        for para in re.split(r'\n\s*\n', body):
            para = ' '.join(para.split())
            if para and not para.startswith(('#', '<!--', '|', '```')):
                desc = para; break
    return name or (path.parent.name if path.name == 'SKILL.md' else path.stem), desc


def words(text): return [w for w in re.findall(r'[a-z0-9]+', text.lower()) if len(w) > 2 and w not in STOP]


def search(root, query, keys, limit):
    terms = set(words(query))
    hits, missing = [], []
    for key in keys:
        base = locate(root, key)
        if base is None: missing.append(key); continue
        seen = set()
        for pattern in ENGINES[key][1]:
            for path in base.glob(pattern):
                if path in seen or not path.is_file(): continue
                seen.add(path)
                name, desc = frontmatter(path)
                rel = path.relative_to(base).as_posix().lower()
                nw, dw, pw = set(words(name.replace('-', ' '))), set(words(desc)), set(words(rel))
                score = 3 * len(terms & nw) + len(terms & dw) + len(terms & pw)
                if score: hits.append((score, key, name, path, desc))
    hits.sort(key=lambda h: (-h[0], h[1], h[2]))
    return hits[:limit], missing


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('query', nargs='*')
    ap.add_argument('--engine', action='append', choices=sorted(ENGINES))
    ap.add_argument('--limit', type=int, default=5)
    ap.add_argument('--engines-root')
    ap.add_argument('--list-engines', action='store_true')
    a = ap.parse_args(argv)
    root = engines_root(a.engines_root)
    keys = a.engine or list(ENGINES)
    if a.list_engines or not a.query:
        for key in keys:
            base = locate(root, key)
            router = next((base / r for r in ROUTERS if base and (base / r).is_file()), None) if base else None
            print(f'{key}: {router or "UNAVAILABLE under " + str(root)}')
        return 0
    hits, missing = search(root, ' '.join(a.query), keys, max(1, a.limit))
    for key in missing: print(f'NOTE: engine {key} unavailable under {root}', file=sys.stderr)
    if not hits:
        print('No match. Try other words, or --list-engines and read the engine router.'); return 1
    for score, key, name, path, desc in hits:
        print(f'[{key}] {name} (score {score})\n  {path}\n  {desc[:220]}')
    print('Read the engine router section first, then only the one SKILL.md you need.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
