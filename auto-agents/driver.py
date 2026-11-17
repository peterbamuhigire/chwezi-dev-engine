#!/usr/bin/env python3
"""Sequential, resumable unattended coding driver; run only in an authorised environment."""
import argparse
import datetime as dt
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parent))
from durable import write_json

ROOT = Path(__file__).resolve().parent.parent
CFG = ROOT / 'auto-agents' / 'config.json'
LANE = re.compile(r'^[a-z0-9][a-z0-9-]{0,39}$')

class Stop(Exception):
    pass

def call(argv, cwd, timeout=None, input_text=None, capture=True, env=None):
    return subprocess.run(argv, cwd=cwd, input=input_text, text=True, encoding='utf-8', errors='replace', stdout=subprocess.PIPE if capture else None, stderr=subprocess.STDOUT if capture else None, timeout=timeout, check=False, env=env)

def git(root, *args, check=True):
    p = call(['git', *args], root)
    if check and p.returncode:
        raise Stop('git ' + ' '.join(args) + ': ' + p.stdout[-1500:])
    return p.stdout.strip()

def commands(value):
    return isinstance(value,list) and all(isinstance(c,list) and c and all(isinstance(s,str) and s for s in c) for c in value)

def config(lane=None):
    d = json.loads(CFG.read_text(encoding='utf-8'))
    if not isinstance(d,dict): raise Stop('Configuration must be a JSON object')
    if 'lane' in d: raise Stop('lane is chosen with --lane, not in config.json')
    if lane is not None:
        # A lane is an independent run of this repository with its own plan,
        # state, worktree and branch; its overlay file changes only what differs.
        if not isinstance(lane,str) or not LANE.match(lane): raise Stop('lane must match '+LANE.pattern)
        overlay_path = CFG.parent / 'lanes' / (lane + '.json')
        if not overlay_path.is_file(): raise Stop('Lane configuration missing: auto-agents/lanes/'+lane+'.json')
        overlay = json.loads(overlay_path.read_text(encoding='utf-8'))
        if not isinstance(overlay,dict) or 'lane' in overlay: raise Stop('Lane configuration must be a JSON object without a lane key')
        d.update(overlay)
        d['lane'] = lane
    required = ('runner','plan','verify','session_timeout_seconds','max_hours','max_sessions','publish','remote','target_branch')
    missing = [x for x in required if x not in d]
    if missing: raise Stop('Missing config: ' + ', '.join(missing))
    if d['runner'] not in ('codex','claude'): raise Stop('runner must be codex or claude')
    if not isinstance(d['verify'], list) or not d['verify'] or any(not isinstance(c,list) or not c or not all(isinstance(s,str) and s for s in c) for c in d['verify']):
        raise Stop('Configure at least one verification command as an array of arguments.')
    if not isinstance(d.get('final_verify',[]),list) or any(not isinstance(c,list) or not c or not all(isinstance(s,str) and s for s in c) for c in d.get('final_verify',[])):
        raise Stop('final_verify must contain command argument arrays')
    if d.get('login_mode','plan') not in ('plan','inherit'): raise Stop('login_mode must be plan or inherit')
    if not isinstance(d.get('runner_args',[]),list) or any(not isinstance(x,str) for x in d.get('runner_args',[])): raise Stop('runner_args must be a list of strings')
    profiles=d.get('runner_args_by_runner',{})
    if not isinstance(profiles,dict) or any(k not in ('codex','claude') or not isinstance(v,list) or any(not isinstance(x,str) for x in v) for k,v in profiles.items()):
        raise Stop('runner_args_by_runner must map codex/claude to string argument lists')
    if type(d.get('max_rate_retries',3)) is not int or d.get('max_rate_retries',3)<0: raise Stop('max_rate_retries must be a nonnegative integer')
    if type(d.get('max_gate_failures',3)) is not int or d.get('max_gate_failures',3)<1: raise Stop('max_gate_failures must be a positive integer')
    for k in ('initial_backoff_seconds','max_backoff_seconds','usage_wait_seconds','verification_timeout_seconds'):
        if type(d.get(k,1)) not in (int,float) or not math.isfinite(d.get(k,1)) or d.get(k,1)<=0: raise Stop(k+' must be finite and positive')
    if d.get('recovery_policy','manual') not in ('manual','local-only'): raise Stop('recovery_policy must be manual or local-only')
    if type(d.get('verification_replay_safe',False)) is not bool: raise Stop('verification_replay_safe must be true or false')
    if type(d.get('max_recovery_attempts',2)) is not int or d.get('max_recovery_attempts',2)<0: raise Stop('max_recovery_attempts must be a nonnegative integer')
    if type(d['publish']) is not bool: raise Stop('publish must be true or false')
    if type(d.get('integrate',False)) is not bool: raise Stop('integrate must be true or false')
    if d.get('integrate') and not d['publish']: raise Stop('integrate needs publish')
    for k in ('gate_slots','max_integration_attempts'):
        if k in d and (type(d[k]) is not int or d[k]<1): raise Stop(k+' must be a positive integer')
    if type(d.get('gate_slot_poll_seconds',10)) not in (int,float) or not math.isfinite(d.get('gate_slot_poll_seconds',10)) or d.get('gate_slot_poll_seconds',10)<=0:
        raise Stop('gate_slot_poll_seconds must be finite and positive')
    for k in ('integration_commands','integration_verify'):
        if not commands(d.get(k,[])): raise Stop(k+' must contain command argument arrays')
    for k in ('session_timeout_seconds','max_hours','max_sessions'):
        if type(d[k]) not in (int,float) or not math.isfinite(d[k]) or d[k] <= 0: raise Stop(k + ' must be finite and positive')
    if type(d['max_sessions']) is not int: raise Stop('max_sessions must be an integer')
    if not isinstance(d['remote'],str) or not d['remote'] or d['remote'].startswith('-'): raise Stop('invalid remote')
    if not isinstance(d['target_branch'],str) or not d['target_branch'] or d['target_branch'].startswith('-'): raise Stop('invalid target branch')
    if not isinstance(d['plan'],str): raise Stop('plan must be a relative path string')
    q=Path(d['plan'])
    if q.is_absolute() or '..' in q.parts or not d['plan']: raise Stop('plan must be a relative path within the repository')
    if 'plan_contract' in d:
        if not isinstance(d['plan_contract'],str): raise Stop('plan_contract must be a relative path string')
        q=Path(d['plan_contract'])
        if not d['plan_contract'] or q.is_absolute() or '..' in q.parts: raise Stop('plan_contract must stay inside the repository')
    return d

def timestamp(): return dt.datetime.now(dt.timezone.utc).isoformat()
def executable(name):
    p=shutil.which(name+'.cmd') if os.name=='nt' else None
    p=p or shutil.which(name)
    if not p: raise Stop('Executable not found: '+name)
    return p

def agent_command(cfg):
    # No permission, sandbox, model or billing settings are overridden here.
    args=cfg.get('runner_args_by_runner',{}).get(cfg['runner'],cfg.get('runner_args',[]))
    if cfg['runner']=='codex': return [executable('codex'),'exec',*args,'-']
    return [executable('claude'),'-p',*args]

def status_path(lane=None):
    common=git(ROOT,'rev-parse','--git-common-dir')
    p=Path(common)
    base=(p if p.is_absolute() else ROOT / p).resolve() / 'auto-agents'
    if lane is None: return base
    if not isinstance(lane,str) or not LANE.match(lane): raise Stop('lane must match '+LANE.pattern)
    return base / 'lanes' / lane

def show(base):
    p=base/'status.json'
    print(p.read_text(encoding='utf-8') if p.exists() else 'No run recorded.')


def preflight(cfg):
    """Read-only readiness checks. Never authenticates, edits or runs a model."""
    if Path(git(ROOT,'rev-parse','--show-toplevel')).resolve()!=ROOT.resolve():
        raise Stop('Install auto-agents directly beneath the repository root.')
    plan=(ROOT/cfg['plan']).resolve()
    if not plan.is_relative_to(ROOT.resolve()) or not plan.is_file():
        raise Stop('Configure a plan file inside this repository.')
    if not git(ROOT,'ls-files','--',cfg['plan']) or git(ROOT,'status','--porcelain','--',cfg['plan']):
        raise Stop('Commit the approved plan before starting.')
    lines=plan.read_text(encoding='utf-8').splitlines()
    if not lines or lines[0].strip()=='# Plan template' or lines[0].startswith('STATUS: BLOCKED'):
        raise Stop('The plan is empty, a setup placeholder or blocked. Set config.json plan to the approved docs/plans/ file and commit it.')
    agent_command(cfg)
    for command in cfg['verify']+cfg.get('final_verify',[])+cfg.get('integration_commands',[])+cfg.get('integration_verify',[]):
        if not shutil.which(command[0]) and not (ROOT/command[0]).is_file():
            raise Stop('Verification executable unavailable: '+command[0])
    if cfg.get('plan_contract'):
        import plan_contract
        path=(ROOT/cfg['plan_contract']).resolve()
        if (not path.is_relative_to(ROOT.resolve()) or not path.is_file()
                or not git(ROOT,'ls-files','--',cfg['plan_contract'])
                or git(ROOT,'status','--porcelain','--',cfg['plan_contract'])):
            raise Stop('Commit the plan contract inside the repository.')
        result=plan_contract.validate_contract(plan_contract.load_contract(path),ROOT)
        if not result['valid']: raise Stop('; '.join(result['errors']))
    print('READY: '+('lane '+cfg['lane']+'; ' if cfg.get('lane') else '')+cfg['runner']+'; plan '+cfg['plan']+'; '+str(len(cfg['verify']))+' slice checks and '+str(len(cfg.get('final_verify',[])))+' final checks.')
    print('Authentication, test services and semantic acceptance remain project-specific checks. Publication: '+str(cfg['publish']).lower())
    return 0

def run(cfg, base, resume_only=False, recover=False):
    from execution import execute
    from types import SimpleNamespace
    return execute(SimpleNamespace(**globals()), cfg, base, resume_only, recover)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=('check','run','resume','recover','start','status','watch','stop','cancel'))
    p.add_argument('--interval',type=float,default=5)
    p.add_argument('--once',action='store_true')
    p.add_argument('--lane',help='run, inspect or stop one lane (auto-agents/lanes/LANE.json)')
    args=p.parse_args()
    try:
        base=status_path(args.lane)
        if args.action=='status':
            show(base)
            return 0
        if args.action=='watch':
            from execution import watch
            return watch(base, args.action=='watch' and not args.once, args.interval)
        if args.action in ('stop','cancel'):
            base.mkdir(parents=True,exist_ok=True)
            (base/'STOP').write_text('stop requested\n',encoding='utf-8')
            if args.action=='cancel': (base/'CANCEL').touch()
            print('Stop requested:',base/'STOP')
            return 0
        cfg=config(args.lane)
        if args.action=='check': return preflight(cfg)
        if args.action=='start':
            preflight(cfg)
            from durable import detached
            base.mkdir(parents=True,exist_ok=True)
            child=detached([sys.executable,'-B',str(Path(__file__).resolve()),'run',*(['--lane',args.lane] if args.lane else [])],ROOT,base/'launcher.log')
            print('Started supervisor PID',child.pid,'; inspect with watch. Log:',base/'launcher.log')
            return 0
        return run(cfg,base,args.action=='resume',args.action=='recover')
    except (Stop,OSError,ValueError,RuntimeError,json.JSONDecodeError) as e:
        print('BLOCKED:',e,file=sys.stderr)
        return 2

if __name__=='__main__': sys.exit(main())
