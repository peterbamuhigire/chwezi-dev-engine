#!/usr/bin/env python3
"""Preview or apply a managed update from a trusted auto-agents source directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import uuid

HERE=Path(__file__).resolve().parent
MANIFEST='manifest.json'
# Project-owned configuration and plans are deliberately excluded.
RESERVED={'config.json','plan.md','manifest.json','update-in-progress.json'}

class UpgradeError(Exception): pass

def digest(path,mode='sha256-text-lf-v1'):
    data=path.read_bytes()
    # Git may materialise text as CRLF on Windows. Canonicalise line endings
    # for text files while keeping binary file hashes byte-exact.
    if mode=='sha256-text-lf-v1' and path.suffix.lower() in {'.py','.md','.json','.sh','.ps1','.txt','.toml','.yml','.yaml'}:
        data=data.replace(b'\r\n',b'\n')
    return hashlib.sha256(data).hexdigest()

def safe_name(name):
    if not isinstance(name,str) or not name or any(c in name for c in ('\\',':','\x00')): return False
    p=PurePosixPath(name)
    return not p.is_absolute() and all(x not in ('.','..') for x in p.parts) and p.parts[0].lower() not in RESERVED and not any(x.startswith('.') for x in p.parts)

def validate_tree(root):
    if root.is_symlink() or not root.is_dir(): raise UpgradeError('Not a directory: '+str(root))
    manifest_path=root/MANIFEST
    if manifest_path.is_symlink() or not manifest_path.is_file(): raise UpgradeError('Missing or linked manifest: '+str(manifest_path))
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    files=manifest.get('files')
    if not isinstance(files,dict) or not files or not all(safe_name(x) for x in files): raise UpgradeError('Invalid managed file set: '+str(root))
    if not isinstance(manifest.get('version'),str) or not manifest['version']: raise UpgradeError('Missing version')
    mode=manifest.get('hash_mode','sha256-raw-v1')
    if mode not in ('sha256-raw-v1','sha256-text-lf-v1'): raise UpgradeError('Unsupported hash mode')
    for name in files:
        file=root/name
        if file.is_symlink() or not file.is_file() or not file.resolve().is_relative_to(root.resolve()):
            raise UpgradeError('Missing, linked or escaping file: '+str(file))
        if digest(file,mode)!=manifest['files'][name]: raise UpgradeError('Modified managed file: '+str(file))
    return manifest

def upgrade(source,target,apply=False):
    if source.is_symlink() or target.is_symlink(): raise UpgradeError('Linked source or target is not supported')
    source=source.resolve();target=target.resolve()
    if source==target: raise UpgradeError('Source and target are the same directory')
    if (target/'update-in-progress.json').exists(): raise UpgradeError('Interrupted update journal exists; inspect target and recover before retrying')
    new=validate_tree(source); old=validate_tree(target)
    changed=[name for name in new['files'] if old['files'].get(name)!=new['files'][name]]
    removed=[name for name in old['files'] if name not in new['files']]
    for name in changed:
        if name not in old['files'] and (target/name).exists(): raise UpgradeError('New managed path already exists locally: '+str(target/name))
    result={'from':old['version'],'to':new['version'],'changed':changed,'removed':removed,'applied':False}
    if not apply or (not changed and old==new): return result
    # Keep a durable record of the intended hashes. If interrupted, fail closed;
    # never silently trust a partly updated set or overwrite a local edit.
    proc=subprocess.run(['git','rev-parse','--git-common-dir'],cwd=target.parent,capture_output=True,text=True,check=False)
    if proc.returncode: raise UpgradeError('Target is not in a Git repository')
    common=Path(proc.stdout.strip())
    if not common.is_absolute(): common=(target.parent/common).resolve()
    lock_dir=common/'auto-agents'; lock_dir.mkdir(parents=True,exist_ok=True)
    lock=lock_dir/'run.lock'
    try: fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except FileExistsError: raise UpgradeError('Driver or updater lock exists: '+str(lock))
    os.write(fd,str(os.getpid()).encode()); os.close(fd)
    journal=target/'update-in-progress.json'
    try:
        if (target/'update-in-progress.json').exists(): raise UpgradeError('Interrupted update journal exists')
        if validate_tree(source)!=new or validate_tree(target)!=old: raise UpgradeError('Source or target changed during update')
        journal.write_text(json.dumps({'from':old,'to':new},indent=2)+'\n',encoding='utf-8')
        for name in changed:
            dst=target/name
            if not dst.parent.resolve().is_relative_to(target): raise UpgradeError('Target parent escapes directory: '+str(dst))
            dst.parent.mkdir(parents=True,exist_ok=True)
            if not dst.parent.resolve().is_relative_to(target): raise UpgradeError('Target parent escapes directory: '+str(dst))
            tmp=dst.with_name(dst.name+'.'+uuid.uuid4().hex+'.tmp')
            shutil.copyfile(source/name,tmp); os.replace(tmp,dst)
        for name in removed: (target/name).unlink()
        tmp=target/(MANIFEST+'.'+uuid.uuid4().hex+'.tmp')
        shutil.copyfile(source/MANIFEST,tmp);os.replace(tmp,target/MANIFEST)
        validate_tree(target)
        journal.unlink()
    except BaseException:
        # The journal remains for manual review; do not delete or guess recovery.
        raise
    finally:
        lock.unlink(missing_ok=True)
    result['applied']=True
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',required=True,help='trusted canonical auto-agents directory')
    p.add_argument('--apply',action='store_true',help='apply after checking source and target hashes')
    args=p.parse_args()
    try:
        print(json.dumps(upgrade(Path(args.source),HERE,args.apply),indent=2));return 0
    except (OSError,ValueError,UpgradeError) as e:
        print('UPDATE BLOCKED:',e,file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
