#!/usr/bin/env python3
"""Regenerate the canonical tool manifest after reviewed source changes."""
import argparse
import json
from pathlib import Path
import sys
from upgrade import safe_name, digest

ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--version',required=True)
    p.add_argument('--add',action='append',default=[])
    p.add_argument('--drop',action='append',default=[])
    args=p.parse_args()
    manifest=ROOT/'manifest.json'
    previous=json.loads(manifest.read_text(encoding='utf8')) if manifest.exists() else {'files':{}}
    paths=(set(previous['files'])|set(args.add))-set(args.drop)
    if not paths or any(not safe_name(x) for x in paths): raise ValueError('invalid file set')
    files={}
    for name in sorted(paths):
        file=ROOT/name
        if file.is_symlink() or not file.is_file() or not file.resolve().is_relative_to(ROOT): raise ValueError('unsafe or missing path: '+name)
        files[name]=digest(file)
    manifest.write_text(json.dumps({'version':args.version,'hash_mode':'sha256-text-lf-v1','files':files},indent=2)+'\n',encoding='utf8')
    print('Wrote',manifest)

if __name__=='__main__':
    try: main()
    except (ValueError,OSError) as exc: print('RELEASE BLOCKED:',exc,file=sys.stderr);sys.exit(2)
