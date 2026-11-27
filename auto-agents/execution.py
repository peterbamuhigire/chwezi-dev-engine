"""Revision-bound execution and recovery for both CLI adapters."""
import contextlib
import fnmatch
import datetime as dt
import hashlib
import json
import os
import re
import shutil
from pathlib import Path
import time
import uuid

import durable


USAGE_TERMS = ('usage limit', 'hit your limit', 'session limit reached', 'weekly limit', '5-hour limit', 'out of extra usage')
RATE_TERMS = ('rate limit', 'too many requests', 'http 429')
RESET = re.compile(r'resets\s+(?:at\s+)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)?(?:\s*\(([A-Za-z_]+/[A-Za-z_/]+)\))?', re.I)


def provider_limit(message, now=None):
    """Classify a failed agent's output as a provider usage or rate limit.

    Returns (kind, seconds_until_reset_or_None); kind is None when no limit
    was reported. Provider CLIs word the usage limit differently (Claude Code
    prints "You've hit your 5-hour limit Â· resets 7:10am (Africa/Kampala)"),
    so a stated reset time is used when it can be read.
    """
    text = message.lower()
    usage = any(term in text for term in USAGE_TERMS) or bool(re.search(r"hit your [\w -]*limit", text))
    if not usage and not any(term in text for term in RATE_TERMS):
        return None, None
    if not usage:
        return 'rate', None
    match = RESET.search(message)
    if not match:
        return 'usage', None
    hour, minute, half, zone = int(match.group(1)), int(match.group(2) or 0), (match.group(3) or '').lower(), match.group(4)
    if half == 'pm' and hour < 12:
        hour += 12
    elif half == 'am' and hour == 12:
        hour = 0
    if hour > 23 or minute > 59:
        return 'usage', None
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo(zone) if zone else None
    except Exception:
        tz = None
    current = dt.datetime.fromtimestamp(now if now is not None else time.time(), tz) if tz else \
        dt.datetime.fromtimestamp(now if now is not None else time.time()).astimezone()
    target = current.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= current:
        target += dt.timedelta(days=1)
    return 'usage', (target - current).total_seconds()


TERMINAL = {'done', 'stopped', 'blocked'}
# Keys that only relocate files; they do not change what a run means, so they
# stay out of the configuration digest and an unfinished run can be moved.
LOCATION_KEYS = {'worktree_root'}
# Transport failures reported by the agent CLI when the model API is unreachable.
NETWORK_TERMS = ("can't reach the api server", 'enotfound', 'eai_again', 'econnreset', 'econnrefused',
                 'etimedout', 'network error', 'connection error', 'socket hang up')
PUSH_REJECTED = ('non-fast-forward', 'fetch first', '[rejected]')


def config_digest(cfg):
    material = {k: v for k, v in cfg.items() if k not in LOCATION_KEYS}
    return hashlib.sha256(json.dumps(material, sort_keys=True).encode()).hexdigest()


def worktree_path(root, cfg, base):
    """Worktree location. The default stays under the Git common dir (compatible
    with existing runs); `worktree_root` (absolute, or relative to the repository
    root) moves it outside `.git`, where agent CLIs that guard `.git` paths as
    sensitive (Claude Code refuses every edit there) can still edit files."""
    configured = cfg.get('worktree_root')
    if configured:
        folder = Path(configured)
        folder = folder if folder.is_absolute() else Path(root) / folder
        lane = cfg.get('lane')
        return folder.resolve() / (('lane-' + lane + '-' if lane else '') + cfg['runner'])
    return Path(base) / 'worktrees' / cfg['runner']


class Halted(Exception):
    """STOP or the run budget ended the run before a prepared job launched."""


class SimpleLease:
    def __init__(self, lease):
        self.lease = lease

    def close(self):
        self.lease.__exit__(None, None, None)


def stamp(value=None):
    return dt.datetime.fromtimestamp(value or time.time(), dt.timezone.utc).isoformat()


class Execution:
    def __init__(self, api, cfg, base, resume_only):
        self.a, self.cfg, self.base = api, cfg, Path(base)
        self.resume_only = resume_only
        self.journal = self.base / ('run-' + cfg['runner'] + '.json')
        self.checkpoint = self.base / ('verified-' + cfg['runner'] + '.json')
        self.pending_path = self.base / ('pending-' + cfg['runner'] + '.json')
        self.work = worktree_path(api.ROOT, cfg, self.base)
        lane = cfg.get('lane')
        self.branch = 'auto-agents/' + ('lane-' + lane + '-' if lane else '') + cfg['runner']
        # Lanes keep their own state under <shared>/lanes/<lane>; gate slots are
        # shared by every lane and the default run of the repository.
        self.shared = self.base.parent.parent if lane else self.base
        self.state = {}

    def save(self, state=None, reason=None, **fields):
        if state is not None:
            self.state['state'] = state
        if reason is not None:
            self.state['reason'] = reason
        self.state.update(fields, updated=stamp())
        durable.write_json(self.journal, self.state)
        durable.write_json(self.base / 'status.json', self.state)

    def event(self, event, **fields):
        with (self.base / 'events.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps({'at': stamp(), 'run_id': self.state['run_id'],
                                     'event': event, **fields}) + '\n')
            stream.flush()

    def fail(self, reason):
        raise self.a.Stop(reason)

    def head(self):
        return self.a.git(self.work, 'rev-parse', 'HEAD')

    def dirty(self):
        status = self.a.git(self.work, 'status', '--porcelain')
        if status and self.restore_eol_only(status):
            status = self.a.git(self.work, 'status', '--porcelain')
        return status

    def restore_eol_only(self, status):
        """Restore tracked files whose only difference is CR/LF line endings.

        Tools and editors on Windows rewrite line endings without changing content
        (Garage 18 Nov 2026: a menu file blocked the run as "agent left uncommitted
        changes" while `git diff` was empty). Only unstaged, unquoted modifications
        are considered, and only when git confirms no difference beyond CR at EOL.
        """
        eol_only = []
        # api.git() strips output, which would eat the leading space of " M"; read it raw.
        raw = self.a.call(['git', 'status', '--porcelain'], self.work)
        for line in (raw.stdout if raw.returncode == 0 else '').splitlines():
            if len(line) < 4 or line[:2] != ' M' or line[3] == '"':
                continue
            path = line[3:]
            if self.a.call(['git', 'diff', '--quiet', '--ignore-cr-at-eol', '--', path], self.work).returncode == 0:
                eol_only.append(path)
        if not eol_only:
            return False
        self.a.git(self.work, 'checkout', '--', *eol_only)
        if self.state.get('run_id'):
            self.event('eol_restored', files=eol_only[:50], count=len(eol_only))
        return True

    def owner_follows_run(self, key, blob):
        """Accept a changed owner plan or contract when the owner checkout only caught up with this run.

        The runner publishes from its worktree, so pulling the target into the owner checkout
        brings the run's own plan edits (Aqar 27 Nov 2026). When the owner HEAD is an ancestor
        of the worktree HEAD, the run already holds every owner commit, so its intent is not new.
        An owner commit the run lacks still blocks.
        """
        if not self.work.exists() or not self.state.get('run_id'):
            return False
        root = self.a.git(self.a.ROOT, 'rev-parse', 'HEAD')
        if self.a.call(['git', 'merge-base', '--is-ancestor', root, self.head()], self.work).returncode:
            return False
        self.event('owner_checkout_followed', key=key, previous=self.state.get(key), blob=blob, root_head=root)
        self.save(**{key: blob})
        return True

    def check_branch(self, before):
        if self.a.git(self.work, 'branch', '--show-current') != self.branch:
            self.fail('agent changed the driver branch')
        if self.a.call(['git', 'merge-base', '--is-ancestor', before, self.head()], self.work).returncode:
            self.fail('agent rewrote branch history')

    def setup(self):
        a, cfg = self.a, self.cfg
        digest = config_digest(cfg)
        previous = durable.read_json(self.journal) if self.journal.exists() else None
        if previous and previous['state'] in ('blocked', 'stopped') and self.close_completed(previous):
            return False
        if self.resume_only and (previous is None or previous['state'] in TERMINAL):
            return False
        if previous and previous['state'] not in TERMINAL:
            self.state = previous
            if previous.get('worktree') and Path(previous['worktree']).resolve() != self.work.resolve():
                # An operator moved the worktree (`git worktree move`) between sessions.
                self.state['worktree'] = str(self.work)
            if previous['config_digest'] != digest:
                self.preserve_journal = True
                self.fail('Configuration changed during an unfinished run; reconcile the saved operation first.')
        else:
            if previous and previous.get('operation'):
                self.fail('An operation remains unresolved; inspect its job receipt before starting a new run.')
            self.state = {'schema': 1, 'run_id': uuid.uuid4().hex, 'runner': cfg['runner'],
                          'plan': cfg['plan'], 'config_digest': digest, 'started_at': time.time(),
                          'deadline': time.time() + cfg['max_hours'] * 3600,
                          'session': 0, 'accepted_slices': 0, 'rate_retries': 0,
                          'recovery_attempts': 0, 'state': 'starting', 'reason': '',
                          'operation': None, 'retry_at': None}
        if (self.base / 'STOP').exists():
            self.fail('STOP file is present; remove it deliberately to resume')
        self.agent = a.agent_command(cfg)
        extra = a.managed_args(cfg)
        if extra and self.agent[2:2 + len(extra)] == extra:
            a.managed_args(cfg, write=True)  # refresh the skill profile and subagent file the agent will load
        for command in cfg['verify'] + cfg.get('final_verify', []):
            if not shutil.which(command[0]) and not (a.ROOT / command[0]).is_file():
                self.fail('Verification executable is unavailable: ' + command[0])
        if Path(a.git(a.ROOT, 'rev-parse', '--show-toplevel')).resolve() != a.ROOT.resolve():
            self.fail('Driver must be installed at the repository root')
        if not (a.ROOT / cfg['plan']).is_file() or not a.git(a.ROOT, 'ls-files', '--', cfg['plan']):
            self.fail('Commit the plan before starting.')
        if a.git(a.ROOT, 'status', '--porcelain', '--', cfg['plan']):
            self.fail('Commit the plan changes before starting.')
        root_plan_blob = a.git(a.ROOT, 'rev-parse', 'HEAD:' + cfg['plan'])
        if (self.state.get('root_plan_blob', root_plan_blob) != root_plan_blob
                and not self.owner_follows_run('root_plan_blob', root_plan_blob)):
            self.preserve_journal = True
            self.fail('The owner checkout plan changed; reconcile its new intent with the saved run before resuming.')
        self.state['root_plan_blob'] = root_plan_blob
        if cfg.get('plan_contract'):
            import plan_contract
            name = cfg['plan_contract']
            owner_path = (a.ROOT / name).resolve()
            if (not owner_path.is_relative_to(a.ROOT.resolve()) or not owner_path.is_file()
                    or not a.git(a.ROOT, 'ls-files', '--', name)
                    or a.git(a.ROOT, 'status', '--porcelain', '--', name)):
                self.fail('Commit the plan contract inside the owner repository before starting.')
            owner_blob = a.git(a.ROOT, 'rev-parse', 'HEAD:' + name)
            if (self.state.get('root_contract_blob', owner_blob) != owner_blob
                    and not self.owner_follows_run('root_contract_blob', owner_blob)):
                self.preserve_journal = True
                self.fail('The owner plan contract changed; reconcile its new intent with the saved run before resuming.')
            owner_data = plan_contract.load_contract(owner_path)
            owner_result = plan_contract.validate_contract(owner_data, a.ROOT)
            if not owner_result['valid']:
                self.fail('Invalid owner plan contract: ' + '; '.join(owner_result['errors']))
            self.state['root_contract_blob'] = owner_blob
            self.state['contract_definition_digest'] = plan_contract.definition_digest(owner_data)
        boot = durable.boot_identity()
        previous_boot = self.state.get('boot_identity')
        if previous and (not boot or not previous_boot or boot != previous_boot) and self.pending_path.exists():
            pending = durable.read_json(self.pending_path)
            if pending.get('index', 0):
                if not cfg.get('verification_replay_safe', False):
                    self.preserve_journal = True
                    self.fail('Host boot changed or is unknown; earlier gate evidence needs safe replay and environment checks.')
                operation = self.state.get('operation')
                if operation:
                    receipt = durable.inspect(self.base / 'jobs' / operation['id'])
                    if operation['kind'] != 'verifying' or receipt['supervisor_active']:
                        self.preserve_journal = True
                        self.fail('Host restart reconciliation found an active or non-verification operation; inspect its effects first.')
                    self.state.update(operation=None, job_id=None, job_state=None)
                pending['index'] = 0
                durable.write_json(self.pending_path, pending)
        self.state['boot_identity'] = boot
        created = not self.work.exists()
        self.work.parent.mkdir(parents=True, exist_ok=True)
        if created:
            exists = a.call(['git', 'show-ref', '--verify', '--quiet', 'refs/heads/' + self.branch], a.ROOT).returncode == 0
            if exists and not self.checkpoint.exists():
                self.fail('Existing driver branch has no verification checkpoint; inspect it before use.')
            a.git(a.ROOT, 'worktree', 'add', *([] if exists else ['-b', self.branch]),
                  str(self.work), self.branch if exists else 'HEAD')
        if Path(a.git(self.work, 'rev-parse', '--show-toplevel')).resolve() != self.work.resolve():
            self.fail('Unexpected driver worktree')
        self.reconcile_integration()
        self.check_branch(self.head())
        plan = (self.work / cfg['plan']).resolve()
        if not plan.is_relative_to(self.work.resolve()) or not plan.is_file():
            self.fail('Plan is absent from driver branch or escapes its worktree.')
        if not self.state.get('operation') and not self.state.get('reconcile'):
            self.contract()
        elif cfg.get('plan_contract'):
            self.state['plan_contract'] = cfg['plan_contract']
        if created and not self.checkpoint.exists():
            durable.write_json(self.checkpoint, {'head': self.head()})
        if not self.checkpoint.exists():
            self.fail('Verification checkpoint missing for existing worktree; inspect and recover manually.')
        accepted = durable.read_json(self.checkpoint)
        if accepted.get('run_id') == self.state['run_id']:
            self.state['accepted_slices'] = accepted.get('accepted_slices', self.state['accepted_slices'])
        if self.dirty() and not self.state.get('operation') and not (
                self.state.get('reconcile') and cfg.get('recovery_policy') == 'local-only'):
            self.fail('Driver worktree has uncommitted changes without a recovery record.')
        self.save(worktree=str(self.work), branch=self.branch, lane=cfg.get('lane'),
                  verified_head=durable.read_json(self.checkpoint)['head'])
        self.event('started', resumed=bool(previous), runner=cfg['runner'], lane=cfg.get('lane'))
        return True

    def close_completed(self, previous):
        """Mark a blocked or stopped run done when the owner has finished its plan.

        Writing engine, 24 Nov 2026: the runner blocked on an owner decision, the
        owner resolved it and committed `STATUS: DONE` on the target branch, and
        the run stayed "blocked" for good. A run closes only when the committed
        owner plan says DONE, its contract (if any) is completion-ready, no
        operation is unresolved and every runner commit is already in the owner
        branch, so nothing the runner made can be lost.
        """
        a, cfg = self.a, self.cfg
        if previous.get('operation') or previous.get('plan') != cfg['plan']:
            return False
        if not a.git(a.ROOT, 'ls-files', '--', cfg['plan']) or a.git(a.ROOT, 'status', '--porcelain', '--', cfg['plan']):
            return False
        shown = a.call(['git', 'show', 'HEAD:' + cfg['plan']], a.ROOT)
        lines = shown.stdout.splitlines() if shown.returncode == 0 else []
        if not lines or lines[0].strip() != 'STATUS: DONE':
            return False
        if cfg.get('plan_contract'):
            import plan_contract
            name = cfg['plan_contract']
            path = (a.ROOT / name).resolve()
            if (not path.is_relative_to(a.ROOT.resolve()) or not path.is_file()
                    or not a.git(a.ROOT, 'ls-files', '--', name) or a.git(a.ROOT, 'status', '--porcelain', '--', name)):
                return False
            result = plan_contract.completion_readiness(plan_contract.load_contract(path), a.ROOT)
            if not result['valid'] or not result['completion_ready']:
                return False
        owner_head = a.git(a.ROOT, 'rev-parse', 'HEAD')
        runner_heads = []
        if self.checkpoint.exists():
            runner_heads.append(durable.read_json(self.checkpoint)['head'])
        if self.work.exists():
            if self.dirty():
                return False
            runner_heads.append(self.head())
        for head in runner_heads:
            if a.call(['git', 'merge-base', '--is-ancestor', head, owner_head], a.ROOT).returncode:
                return False
        self.state = previous
        self.pending_path.unlink(missing_ok=True)
        reason = ('Owner completed the plan at ' + owner_head[:12] + '; closed the ' + previous['state'] + ' run ('
                  + (previous.get('reason') or 'no reason recorded') + '). Runner gates did not run on owner commits.')
        self.save('done', reason, closed_by='owner', closed_from=previous['state'], owner_head=owner_head)
        self.event('closed', closed_from=previous['state'], owner_head=owner_head)
        print('DONE: ' + reason)
        return True

    def contract(self, require_complete=False):
        name = self.cfg.get('plan_contract')
        if not name:
            return
        import plan_contract
        path = (self.work / name).resolve()
        if not path.is_relative_to(self.work.resolve()) or not self.a.git(self.work, 'ls-files', '--', name):
            self.fail('Plan contract must be a tracked file inside the worktree.')
        data = plan_contract.load_contract(path)
        result = plan_contract.completion_readiness(data, self.work)
        if not result['valid']:
            self.fail('Invalid plan contract: ' + '; '.join(result['errors']))
        if plan_contract.definition_digest(data) != self.state.get('contract_definition_digest'):
            self.fail('Plan contract changed approved task definitions; return the scope or acceptance change to the owner.')
        if require_complete and not result['completion_ready']:
            self.fail('STATUS: DONE conflicts with incomplete plan-contract tasks or evidence.')
        self.state['plan_contract'] = name

    def owner_intent(self):
        """Recheck the owner checkout at operation boundaries, without rebasing work."""
        for name, saved_key in ((self.cfg['plan'], 'root_plan_blob'),
                                (self.cfg.get('plan_contract'), 'root_contract_blob')):
            if not name:
                continue
            path = (self.a.ROOT / name).resolve()
            if (not path.is_relative_to(self.a.ROOT.resolve()) or not path.is_file()
                    or not self.a.git(self.a.ROOT, 'ls-files', '--', name)
                    or self.a.git(self.a.ROOT, 'status', '--porcelain', '--', name)):
                self.fail('Owner plan or contract changed during this run; reconcile intent before further work.')
            blob = self.a.git(self.a.ROOT, 'rev-parse', 'HEAD:' + name)
            if blob != self.state.get(saved_key) and not self.owner_follows_run(saved_key, blob):
                self.fail('Owner plan or contract changed during this run; reconcile intent before further work.')

    def job(self, kind, argv, timeout, input_text=None):
        op = self.state.get('operation')
        if op is None:
            self.owner_intent()
            op = {'kind': kind, 'id': uuid.uuid4().hex, 'before': self.head(), 'created_at': time.time(),
                  'gate_index': self.state.get('gate_index')}
            self.save(operation=op)
        if op['kind'] != kind:
            self.fail('Unexpected saved operation kind; inspect recovery state.')
        folder = self.base / 'jobs' / op['id']
        if (folder / 'spec.json').exists():
            # Reattach to the ORIGINAL command, timeout and prompt. Rebuilding them
            # from today's remaining budget would change the job identity.
            spec = durable.read_spec(folder)
            # A job prepared before 2.5.0 lacks the subagent arguments, and one prepared before 2.4.0
            # also lacks the skill arguments; both reattach to their original command.
            accepted = [argv]
            if kind == 'agent':
                extra = self.a.managed_args(self.cfg)
                if extra and argv[2:2 + len(extra)] == extra:
                    skills = self.a.skill_args(self.cfg)
                    rest = argv[2 + len(extra):]
                    accepted += [argv[:2] + skills + rest, argv[:2] + rest]
            if spec['argv'] not in accepted or Path(spec['cwd']).resolve() != self.work.resolve():
                self.fail('Saved job command or working directory changed.')
        else:
            durable.prepare(folder, argv, self.work, timeout, input_text,
                            self.cfg.get('login_mode', 'plan') if kind == 'agent' else 'inherit')
        if durable.inspect(folder)['state'] == 'prepared':
            self.owner_intent()
            if time.time() >= self.state['deadline']:
                self.fail('Saved job was never launched; STOP or expired run budget prevents a new launch.')
            if (self.base / 'STOP').exists():
                # Nothing ran: drop the unlaunched job and stop cleanly. The
                # pending record is unchanged, so a resumed run repeats this step.
                reason = 'STOP requested before the ' + kind + ' job launched; nothing ran'
                self.clear_operation()
                self.event('launch_withheld', kind=kind, job_id=op['id'])
                raise Halted(reason)
        self.save(kind, '', job_id=op['id'], log=str(folder / 'output.log'), action=argv[0])
        last = [0.0]
        def observe(status):
            if time.monotonic() - last[0] >= 2 or status['state'] != 'running':
                self.save(job_state=status['state'], job_heartbeat=status.get('heartbeat_at'),
                          last_output_at=status.get('last_output_at'), output_bytes=status.get('output_bytes', 0))
                last[0] = time.monotonic()
        result = durable.wait(folder, observe=observe, cancel=lambda: (self.base / 'CANCEL').exists())
        self.event(kind + '_receipt', job_id=op['id'], outcome=result['state'], exit=result.get('exit_code'))
        self.credit_suspension(op['id'], result)
        self.owner_intent()
        return result, durable.tail(folder / 'output.log'), op

    def credit_suspension(self, job_id, result):
        """Give the run budget back the time the host slept during a job, once per job."""
        slept = float(result.get('suspended_seconds') or 0)
        if slept <= 0 or job_id in self.state.get('suspension_credited', []):
            return
        credited = (self.state.get('suspension_credited', []) + [job_id])[-20:]
        self.save(deadline=self.state['deadline'] + slept, suspension_credited=credited)
        self.event('host_suspended', job_id=job_id, seconds=round(slept, 1), new_deadline=stamp(self.state['deadline']))

    def clear_operation(self, **fields):
        self.save(operation=None, job_id=None, job_state=None, **fields)

    def prompt(self, pending):
        prompt = (f'Read AGENTS.md and CLAUDE.md if present, then {self.cfg["plan"]}. '
                  'Implement one bounded ready slice of the owner-authorised plan. Read its exact acceptance criteria, '
                  'dependencies and relevant live skills. Run targeted checks, update the concise durable handoff and commit. '
                  'Include completed and remaining task IDs, evidence paths and next action. Do not repeat passed checks '
                  'without a changed input or unresolved concern. Do not push, switch branches, reset, merge or expand permissions. '
                  'Preserve production data and external-effect boundaries. Mark STATUS: DONE on the first plan line only '
                  'when all required outcomes have evidence; use STATUS: BLOCKED - reason only when no independent work remains. '
                  'A marker, test exit, or reviewer score alone does not prove user acceptance. '
                  'Run every command in the foreground and wait for it (raise the tool timeout for long checks); '
                  'background tasks die with this non-interactive session. Commit before ending the session. '
                  'Write text files as UTF-8 (Windows PowerShell 5.1 Set-Content/Out-File default to ANSI; pass -Encoding utf8 '
                  'or use the Edit/Write tools).\n')
        if self.cfg.get('skills', 'on-demand') == 'on-demand':
            prompt += ('Skills are not preloaded. When a step needs one, run `python "' + str(Path(__file__).resolve().parent / 'find_skill.py') + '" "<task words>"` '
                       '(optionally --engine development|writing|orchestrator|accounting|knowledge-bank), read that engine\'s '
                       'router section, then Read only the one SKILL.md it names. Do not load whole skill folders.\n')
        if self.cfg.get('subagents', 'economy') == 'economy' and self.cfg['runner'] == 'claude':
            prompt += ('When locating something would take more than a few searches across many files, delegate it to the '
                       'Explore subagent (cheapest model class, read-only) and act on its path:line report. Keep judgement, '
                       'edits and verification in this session; do not start other subagents for searching.\n')
        if pending and pending.get('integration'):
            integration = pending['integration']
            prompt += ('INTEGRATION: ' + self.cfg['remote'] + '/' + self.cfg['target_branch'] + ' moved while your verified commits '
                       'waited to publish, and replaying them conflicts in: ' + ', '.join(integration['conflicts'][:30]) + '. '
                       'In this session only, and as the single exception to the rule against rebasing, run '
                       '`git -c core.editor=true rebase ' + integration['upstream'] + '` (already fetched), resolve each conflict '
                       'keeping the intent of both sides (regenerate generated files instead of hand-merging them), run the checks '
                       'of the touched modules and finish the rebase. Keep every commit and its subject; you may add one fix commit. '
                       'Do no other work in this session and do not push.\n')
        elif pending and pending.get('feedback'):
            prompt += 'Repair this independent gate failure before further work: ' + pending['feedback'][-1500:] + '\n'
        if self.state.get('reconcile'):
            prompt += ('RECOVERY: the previous agent was interrupted. Inspect git diff/status/history and the persisted handoff '
                       'before editing. Preserve useful partial work. Reconcile each intended outcome; do not repeat completed '
                       'effects or delete/reset uncertain changes. This run permits local-only recovery; external actions are '
                       'not replayable. Commit recovered work only after appropriate checks.\n')
            if self.state.get('contract_repair'):
                prompt += ('The interrupted work left the plan contract invalid. Repair it first (stage or commit every '
                           'evidence file it names, or leave evidence [] until the task is complete): '
                           + self.state['contract_repair'] + '\n')
        if self.cfg.get('plan_contract'):
            prompt += f'Update the tracked task/evidence sidecar {self.cfg["plan_contract"]}; keep task IDs and acceptance intent stable.\n'
        if self.cfg.get('final_verify'):
            prompt += 'The supervisor runs configured final_verify commands on a completion candidate. Use targeted checks during each slice; do not start a duplicate long final gate.\n'
        return prompt

    def wait_quota(self):
        retry_at = self.state.get('retry_at')
        while retry_at and time.time() < retry_at:
            if (self.base / 'STOP').exists() or time.time() >= self.state['deadline']:
                return False
            reason = ('Network failure reaching the model API; fresh session after a pause'
                      if self.state.get('net_retries') else
                      'Usage/rate limit; scheduled probe, not a confirmed provider reset.')
            self.save('waiting', reason, retry_at=retry_at)
            time.sleep(max(0, min(2, retry_at - time.time(), self.state['deadline'] - time.time())))
        if retry_at:
            self.save(retry_at=None)
        return True

    def recover(self, result, op):
        previous = durable.read_json(self.pending_path) if self.pending_path.exists() else {}
        if previous.get('integration'):
            # An interrupted integration session: abandon a half-done rebase, or
            # accept a finished one only if it kept every lane commit.
            if self.rebasing():
                self.a.call(['git', 'rebase', '--abort'], self.work)
                if self.rebasing():
                    self.fail('interrupted integration rebase could not be abandoned; inspect the worktree')
            if self.head() != op['before']:
                self.check_integration(previous['integration'])
        else:
            self.check_branch(op['before'])
        after = self.head()
        if not self.dirty() and after != op['before']:
            # Even an interrupted or failed agent may have committed. Verify that
            # exact descendant; do not spend another agent session repeating it.
            durable.write_json(self.pending_path, {'head': after, 'failures': previous.get('failures', 0), 'index': 0,
                               'config_digest': self.state['config_digest'],
                               **{k: previous[k] for k in ('integrations', 'rejections') if k in previous}})
            self.clear_operation(reconcile=False)
            return True
        if result['state'] in ('interrupted', 'timed_out') and self.cfg.get('recovery_policy') == 'local-only':
            count = self.state['recovery_attempts'] + 1
            if count <= self.cfg.get('max_recovery_attempts', 2):
                self.clear_operation(recovery_attempts=count, reconcile=True)
                self.event('reconcile_local', attempt=count)
                return True
        return False

    def loop(self):
        cfg = self.cfg
        while True:
            # Observe a saved job before acting on a new budget/stop boundary.
            # Its supervisor owns its original timeout; losing the observer does
            # not cancel or duplicate it.
            if not self.state.get('operation') and (not self.wait_quota() or time.time() >= self.state['deadline'] or (self.base / 'STOP').exists()):
                self.save('stopped', 'STOP requested' if (self.base / 'STOP').exists() else 'Run time budget reached')
                break
            if not self.state.get('operation'):
                self.owner_intent()
            pending = durable.read_json(self.pending_path) if self.pending_path.exists() else None
            checkpoint = durable.read_json(self.checkpoint)
            verified = checkpoint['head']
            accepted_current = (checkpoint.get('config_digest') == self.state['config_digest'] and bool(checkpoint.get('at')))
            before = self.head()
            op = self.state.get('operation')
            if op:
                receipt = durable.inspect(self.base / 'jobs' / op['id'])
                finished = not receipt['supervisor_active'] and receipt['state'] in ('passed', 'failed', 'interrupted', 'timed_out')
                # Reconcile crashes between durable transition writes. Never
                # infer completion merely from a changed index or HEAD.
                accepted = (accepted_current and before == verified and
                            ((pending and pending['head'] == before) or checkpoint.get('operation_id') == op['id']))
                transferred = (pending and op['kind'] == 'agent' and pending['head'] != op['before'])
                advanced = (pending and op['kind'] == 'verifying' and
                            pending.get('index', 0) >= (op.get('gate_index') or 1) and receipt['state'] == 'passed')
                if finished and (accepted or transferred or advanced):
                    self.clear_operation()
                    op = None
            if accepted_current and pending and pending['head'] == verified == before:
                self.pending_path.unlink()
                pending = None
            if pending and pending.get('config_digest') != self.state['config_digest']:
                if op:
                    self.fail('Verification configuration changed with an unresolved operation.')
                pending.update(index=0, config_digest=self.state['config_digest'])
                durable.write_json(self.pending_path, pending)
            if before != verified and not pending and not op and not self.state.get('reconcile'):
                self.fail('unverified commit without matching recovery record; inspect manually')
            if pending and pending['head'] != before and not (op and op['kind'] == 'agent'):
                self.fail('recovery record does not match worktree HEAD')
            if pending and pending.get('failures', 0) >= cfg.get('max_gate_failures', 3):
                self.fail('verification failure limit reached; inspect before resuming')
            need_agent = not pending or bool(pending.get('feedback'))
            if need_agent:
                lines = (self.work / cfg['plan']).read_text(encoding='utf-8', errors='replace').splitlines()
                first = lines[0].strip() if lines else ''
                if not pending and not op and not self.state.get('reconcile'):
                    if first == 'STATUS: DONE':
                        self.contract(require_complete=True)
                        if not accepted_current:
                            pending = {'head': before, 'failures': 0, 'index': 0, 'config_digest': self.state['config_digest']}
                            durable.write_json(self.pending_path, pending)
                            if self.verify(pending) == 'halt':
                                if self.state['state'] != 'stopped':
                                    self.save('stopped', 'STOP requested or run budget reached while waiting for a gate slot')
                                break
                            continue
                        self.save('done', 'Plan marked complete; committed slices passed configured verification')
                        break
                    if first.startswith('STATUS: BLOCKED'):
                        self.fail(first)
                if not op:
                    if self.state['session'] >= cfg['max_sessions']:
                        self.save('stopped', 'Session limit reached')
                        break
                    if not pending and not self.state.get('reconcile') and cfg.get('integrate'):
                        self.sync()
                    # Reconciliation may retain dirty local progress, but never
                    # launch a fresh worker against changed approved definitions.
                    # An invalid sidecar inside interrupted local work (e.g. evidence
                    # naming a file the agent wrote but never staged before a usage
                    # limit) is handed to the recovery session to repair; the gate
                    # re-checks the contract before anything is accepted.
                    try:
                        self.contract()
                        self.save(contract_repair=None)
                    except self.a.Stop as error:
                        # Also when the gate itself handed the contract defect back as feedback:
                        # otherwise the repair session it asked for could never start (Garage 19 Nov).
                        repairing = self.state.get('reconcile') or bool(pending and pending.get('feedback'))
                        if not (repairing and str(error).startswith('Invalid plan contract')):
                            raise
                        self.save(contract_repair=str(error)[:1500])
                        self.event('contract_feedback', reason=str(error)[:500], stage='recovery')
                    self.save(session=self.state['session'] + 1)
                remaining = max(1, self.state['deadline'] - time.time())
                result, output, op = self.job('agent', self.agent, min(cfg['session_timeout_seconds'], remaining), self.prompt(pending))
                if result['state'] != 'passed':
                    committed = not self.dirty() and self.head() != op['before']
                    if (result['state'] == 'timed_out' and remaining < cfg['session_timeout_seconds'] and not committed
                            and not float(result.get('suspended_seconds') or 0)
                            and cfg.get('recovery_policy') == 'local-only'):
                        # The run budget, not the session limit, ended this session (Garage 27 Nov 2026:
                        # cut off at the deadline with its recovery attempts used, so the run blocked).
                        # Keep the partial work for a reconcile session and stop on the budget.
                        self.clear_operation(reconcile=True)
                        self.event('budget_cut_session', job_id=op['id'], allowed=round(remaining, 1))
                        self.save('stopped', 'Run time budget reached during an agent session; recover reconciles its work')
                        break
                    if self.recover(result, op):
                        continue
                    kind, reset_in = provider_limit(output)
                    limited = kind is not None
                    unchanged = not self.dirty() and self.head() == op['before']
                    local_reconcile = cfg.get('recovery_policy') == 'local-only'
                    if limited and (unchanged or local_reconcile) and self.state['rate_retries'] < cfg.get('max_rate_retries', 3):
                        attempts = self.state['rate_retries'] + 1
                        if kind == 'usage':
                            # A stated reset time (plus a short margin) wins; the
                            # configured wait stays the ceiling and the fallback.
                            ceiling = cfg.get('usage_wait_seconds', 18000)
                            delay = min(ceiling, reset_in + 120) if reset_in is not None else ceiling
                        else:
                            delay = min(cfg.get('max_backoff_seconds', 3600), cfg.get('initial_backoff_seconds', 60) * 2 ** (attempts - 1))
                        self.clear_operation(rate_retries=attempts, retry_at=time.time() + delay, reconcile=not unchanged)
                        self.save('waiting', 'Provider limit; retry only within configured run budget')
                        self.event('rate_wait', seconds=delay, retry=attempts)
                        continue
                    network = any(term in output.lower() for term in NETWORK_TERMS)
                    if (network and result['state'] == 'failed' and (unchanged or local_reconcile)
                            and self.state.get('net_retries', 0) < cfg.get('max_network_retries', 24)):
                        # The model API was unreachable (DNS/connection). Pause, then a fresh
                        # session on the same worktree; bounded, and reset by each accepted slice.
                        attempts = self.state.get('net_retries', 0) + 1
                        delay = cfg.get('network_retry_seconds', 300)
                        self.clear_operation(net_retries=attempts, retry_at=time.time() + delay, reconcile=not unchanged)
                        self.save('waiting', 'Network failure reaching the model API; fresh session after a pause')
                        self.event('network_wait', seconds=delay, retry=attempts)
                        continue
                    self.fail('agent ' + result['state'] + '; inspect job log and reconcile worktree')
                if pending and pending.get('integration'):
                    if self.rebasing():
                        self.fail('integration session left a rebase in progress; inspect the worktree')
                    self.check_integration(pending['integration'], pending.get('head'))
                else:
                    self.check_branch(op['before'])
                if self.dirty():
                    self.fail('agent left uncommitted changes')
                after = self.head()
                if after == op['before'] and not (self.state.get('reconcile') and after != verified):
                    self.fail('agent made no commit')
                durable.write_json(self.pending_path, {'head': after, 'failures': pending.get('failures', 0) if pending else 0,
                                   'index': 0, 'config_digest': self.state['config_digest'],
                                   **{k: pending[k] for k in ('integrations', 'rejections') if pending and k in pending}})
                self.clear_operation(rate_retries=0, net_retries=0, reconcile=False)
                pending = durable.read_json(self.pending_path)
            if self.verify(pending) == 'halt':
                if self.state['state'] != 'stopped':
                    self.save('stopped', 'STOP requested or run budget reached while waiting for a gate slot')
                break

    def rebasing(self):
        for name in ('rebase-merge', 'rebase-apply'):
            path = Path(self.a.git(self.work, 'rev-parse', '--git-path', name))
            if (path if path.is_absolute() else self.work / path).exists():
                return True
        return False

    def reconcile_integration(self):
        """Repair the records after a crash inside integration or sync (called from setup)."""
        a = self.a
        pending = durable.read_json(self.pending_path) if self.pending_path.exists() else None
        if self.rebasing():
            if not pending or not (pending.get('integrating') or pending.get('integration')):
                self.fail('A rebase is in progress in the driver worktree without an integration record; inspect it.')
            # The driver's rebase, or an agent's integration session, was interrupted: abandon it.
            a.call(['git', 'rebase', '--abort'], self.work)
            if self.rebasing() or self.dirty():
                self.fail('Interrupted integration could not be abandoned cleanly; inspect the worktree.')
            self.event('integration_abandoned', head=self.head())
        if not pending:
            # A crash between sync's fast-forward and its checkpoint write.
            checkpoint = durable.read_json(self.checkpoint) if self.checkpoint.exists() else None
            tracking = 'refs/remotes/' + self.cfg['remote'] + '/' + self.cfg['target_branch']
            upstream = a.git(self.work, 'rev-parse', '--verify', '-q', tracking, check=False)
            head = self.head()
            if (checkpoint and head != checkpoint['head'] and head == upstream and not self.dirty()
                    and self.ancestor(checkpoint['head'], head)):
                checkpoint['head'] = head
                durable.write_json(self.checkpoint, checkpoint)
                self.event('synced', head=head, recovered=True)
            return
        head = self.head()
        integrating = pending.get('integrating')
        if integrating:
            if head == integrating['orig']:
                pending.pop('integrating')
            elif not self.dirty() and self.ancestor(integrating['upstream'], head):
                # The rebase finished but its record was not written.
                self.check_integration({'upstream': integrating['upstream'], 'subjects': integrating['subjects']})
                pending.pop('integrating')
                pending.update(head=head, index=0, replays=0, regen=bool(self.cfg.get('integration_commands')), quick=False)
            else:
                self.fail('Interrupted integration left an unexpected revision; inspect the worktree.')
            durable.write_json(self.pending_path, pending)
            return
        op = self.state.get('operation') or {}
        if op.get('kind') == 'integrating' and head != pending['head']:
            # An integration command committed before the crash.
            if self.dirty() or not self.ancestor(pending['head'], head):
                self.fail('Interrupted integration command left an unexpected revision; inspect the worktree.')
            pending.update(head=head, index=0, replays=0, regen=True, quick=False)
            durable.write_json(self.pending_path, pending)

    def ancestor(self, older, newer):
        return self.a.call(['git', 'merge-base', '--is-ancestor', older, newer], self.work).returncode == 0

    def fetch(self):
        """Fetch the target branch; None when it cannot be read (offline or not created yet)."""
        remote, target = self.cfg['remote'], self.cfg['target_branch']
        tracking = 'refs/remotes/' + remote + '/' + target
        try:
            result = self.a.call(['git', 'fetch', '-q', remote, '+refs/heads/' + target + ':' + tracking], self.work, timeout=300)
        except Exception as error:  # a hung fetch must not stop the lane
            self.event('fetch_failed', output=str(error)[-300:])
            return None
        if result.returncode:
            self.event('fetch_failed', output=result.stdout[-300:])
            return None
        return self.a.git(self.work, 'rev-parse', tracking)

    def sync(self):
        """Start a fresh session from the published target so lanes see each other's work."""
        checkpoint = durable.read_json(self.checkpoint)
        head = self.head()
        if head != checkpoint['head'] or self.dirty():
            return
        upstream = self.fetch()
        if upstream is None or upstream == head or not self.ancestor(head, upstream):
            return
        self.a.git(self.work, 'merge', '-q', '--ff-only', upstream)
        checkpoint['head'] = upstream
        durable.write_json(self.checkpoint, checkpoint)
        self.save(verified_head=upstream)
        self.event('synced', head=upstream)

    def check_integration(self, integration, orig=None):
        """An integration session may rewrite history only onto the fetched upstream, keeping every lane commit.

        A lane commit may be missing only when the upstream already superseded
        it: every file it changed was also changed upstream, and the integrated
        head keeps the upstream version of each of those files (seen when two
        lanes fixed the same flaky test). Anything else blocks.
        """
        upstream = integration['upstream']
        if self.a.git(self.work, 'branch', '--show-current') != self.branch:
            self.fail('integration session changed the driver branch')
        if not self.ancestor(upstream, self.head()):
            self.fail('integration session did not rebase onto the fetched upstream')
        subjects = self.a.git(self.work, 'log', '--reverse', '--format=%s', upstream + '..HEAD').splitlines()
        wanted = list(integration['subjects'])
        superseded = []
        position = 0
        for subject in subjects:
            while position < len(wanted) and subject != wanted[position] and self.superseded(wanted[position], upstream, orig):
                superseded.append(wanted[position])
                position += 1
            if position < len(wanted) and subject == wanted[position]:
                position += 1
        while position < len(wanted) and self.superseded(wanted[position], upstream, orig):
            superseded.append(wanted[position])
            position += 1
        if position != len(wanted):
            self.fail('integration session dropped or renamed lane commits; inspect before publishing')
        if superseded:
            self.event('integration_superseded', subjects=superseded[:10])

    def superseded(self, subject, upstream, orig):
        """True when the lane commit `subject` (in the pre-integration history `orig`) is fully replaced upstream."""
        if not orig:
            return False
        base = self.a.git(self.work, 'merge-base', upstream, orig, check=False)
        if not base:
            return False
        commits = [line.split(' ', 1) for line in self.a.git(
            self.work, 'log', '--format=%H %s', base + '..' + orig, check=False).splitlines() if ' ' in line]
        matches = [sha for sha, text in commits if text == subject]
        if len(matches) != 1:
            return False
        # An identical patch already upstream (git cherry marks it "-") is superseded
        # even when later lane commits changed the same files again.
        equivalent = {line[2:] for line in self.a.git(self.work, 'cherry', upstream, orig, base, check=False).splitlines()
                      if line.startswith('- ')}
        if matches[0] in equivalent:
            return True
        files = [f for f in self.a.git(self.work, 'diff-tree', '--no-commit-id', '--name-only', '-r', '--root',
                                        matches[0], check=False).splitlines() if f]
        if not files:
            return False
        upstream_changed = set(self.a.git(self.work, 'diff', '--name-only', base, upstream, check=False).splitlines())
        for name in files:
            if name not in upstream_changed:
                return False
            if self.blob('HEAD', name) != self.blob(upstream, name):
                return False
        return True

    def blob(self, rev, name):
        return self.a.git(self.work, 'rev-parse', '--verify', '-q', rev + ':' + name, check=False)

    def gate_slot(self, saved=None, integration=False, turn=False):
        """Hold one of the repository's shared gate slots; None when STOP or the budget ends the wait.

        Integration quick checks use their own pool (`integration_slots`,
        default 1 when `gate_slots` is set) so a short check never queues
        behind full gates while the target keeps moving.
        """
        count = self.cfg.get('gate_slots')
        pool, label = 'gate-slots', 'gate'
        if turn:
            # One run publishes at a time: it rebases, quick-checks and pushes
            # while holding the turn, so the target cannot move underneath it.
            count, pool, label = 1, 'publish-turn', 'publish turn'
        elif not count:
            return contextlib.nullcontext()
        elif integration:
            count = self.cfg.get('integration_slots', 1)
            if not count:
                return contextlib.nullcontext()
            pool, label = 'integration-slots', 'integration check'
        if saved and durable.inspect(self.base / 'jobs' / saved['id'])['state'] != 'prepared':
            # Reattaching to a gate that already started: it ran under a slot, and
            # waiting here could not stop it, only delay observing it.
            return contextlib.nullcontext()
        folder = self.shared / pool
        # First come, first served: a waiting run holds a ticket and may take a free
        # slot only when no older live ticket exists (polling alone let one lane
        # wait six hours while others took slots again and again).
        queue = folder / 'queue'
        queue.mkdir(parents=True, exist_ok=True)
        ticket = queue / ('%020d-%s.ticket' % (time.time_ns(), uuid.uuid4().hex[:12]))
        holder = durable.Lease(ticket)  # kernel lock: the ticket is live while this process holds it
        holder.__enter__()
        waiting = False
        try:
            while True:
                if not self.older_tickets(queue, ticket):
                    for index in range(count):
                        lease = durable.Lease(folder / ('slot-%d.mutex' % index))
                        try:
                            lease.__enter__()
                        except durable.Busy:
                            continue
                        if waiting:
                            self.event('gate_slot', slot=index)
                        return contextlib.closing(SimpleLease(lease))
                if (self.base / 'STOP').exists() or time.time() >= self.state['deadline']:
                    return None
                if not waiting:
                    self.save('waiting_gate', 'Another run is publishing; waiting for the publish turn' if turn
                              else 'All %d %s slots are busy; waiting for one' % (count, label))
                    waiting = True
                time.sleep(self.cfg.get('gate_slot_poll_seconds', 10))
        finally:
            holder.__exit__(None, None, None)
            ticket.unlink(missing_ok=True)

    @staticmethod
    def older_tickets(queue, ticket):
        """Live tickets queued before `ticket`; tickets nobody holds any more are removed."""
        older = []
        for other in sorted(queue.glob('*.ticket')):
            if other.name >= ticket.name:
                break
            try:
                young = time.time() - other.stat().st_mtime < 5  # its owner may not hold the lock yet
            except FileNotFoundError:
                continue
            if young or durable.held(other):
                older.append(other)
            else:
                other.unlink(missing_ok=True)
        return older

    def plan_line(self):
        lines = (self.work / self.cfg['plan']).read_text(encoding='utf-8', errors='replace').splitlines()
        return lines[0].strip() if lines else ''

    def integrate(self, pending, after, total):
        """Replay verified lane commits onto a moved target.

        Returns the head to publish, None to loop (full gate or repair session
        needed) or 'halt' (STOP while waiting for a gate slot).
        """
        cfg = self.cfg
        upstream = self.fetch()
        moved = upstream is not None and not self.ancestor(upstream, after)
        if not moved and not pending.get('regen'):
            return after
        overlap = []
        if moved:
            attempts = pending.get('integrations', 0) + 1
            if attempts > cfg.get('max_integration_attempts', 6):
                self.fail('integration attempts exhausted for this slice; the target keeps moving or keeps conflicting')
            base = self.a.git(self.work, 'merge-base', upstream, after)
            changed = lambda a, b: set(filter(None, self.a.git(self.work, 'diff', '--name-only', a, b).splitlines()))
            lane_files, incoming = changed(base, after), changed(base, upstream)
            # Files a project marks as rebuilt or append-only shared lists
            # (`integration_overlap_ignore`, fnmatch globs) do not force a full
            # gate: they merged cleanly and the quick check covers them.
            ignore = cfg.get('integration_overlap_ignore', [])
            overlap = sorted(f for f in lane_files & incoming if not any(fnmatch.fnmatch(f, g) for g in ignore))
            subjects = self.a.git(self.work, 'log', '--reverse', '--format=%s', upstream + '..' + after).splitlines()
            plan_before = self.plan_line()
            pending.update(integrating={'upstream': upstream, 'orig': after, 'subjects': subjects}, integrations=attempts)
            durable.write_json(self.pending_path, pending)
            env = dict(os.environ, GIT_EDITOR='true')
            result = self.a.call(['git', 'rebase', upstream], self.work, timeout=900, env=env)
            if result.returncode:
                conflicts = self.a.git(self.work, 'diff', '--name-only', '--diff-filter=U', check=False).splitlines()
                self.a.call(['git', 'rebase', '--abort'], self.work)
                if self.rebasing() or self.head() != after or self.dirty():
                    self.fail('integration rebase could not be abandoned cleanly; inspect the worktree')
                pending.pop('integrating')
                pending.update(index=0, replays=0, feedback='integration conflict',
                               integration={'upstream': upstream, 'subjects': subjects, 'conflicts': conflicts or ['(unknown)']})
                durable.write_json(self.pending_path, pending)
                self.event('integration_conflict', upstream=upstream, files=conflicts[:30])
                self.save('repairing', 'Verified commits conflict with the moved target; next session integrates them')
                return None
            pending.pop('integrating')
            # The quick check may replace the full gate only for disjoint changes
            # that leave the plan's completion state alone.
            pending.update(head=self.head(), index=0, replays=0, regen=bool(cfg.get('integration_commands')),
                           quick=not overlap and self.plan_line() == plan_before)
            durable.write_json(self.pending_path, pending)
        regenerated = False
        if pending.get('regen'):
            for command in cfg.get('integration_commands', []):
                before = self.head()
                result, output, _ = self.job('integrating', command, cfg.get('verification_timeout_seconds', 3600))
                self.clear_operation()
                if self.a.git(self.work, 'branch', '--show-current') != self.branch or not self.ancestor(before, self.head()):
                    self.fail('integration command changed the branch or rewrote history')
                if self.dirty():
                    self.fail('integration command left uncommitted changes')
                if self.head() != before:
                    regenerated = True
                    # Regenerating only files the project marks as rebuilt
                    # (`integration_overlap_ignore`) keeps the quick check; any
                    # other file forces the full gate. Without this a lane whose
                    # slice feeds a generated file re-ran the full gate on every
                    # move of the target and never published.
                    rebuilt = self.a.git(self.work, 'diff', '--name-only', before, self.head()).splitlines()
                    ignore = cfg.get('integration_overlap_ignore', [])
                    generated_only = bool(rebuilt) and all(any(fnmatch.fnmatch(f, g) for g in ignore) for f in rebuilt)
                    pending.update(head=self.head(), index=0, quick=pending.get('quick', False) and generated_only)
                durable.write_json(self.pending_path, pending)
                if result['state'] != 'passed':
                    pending.update(failures=pending.get('failures', 0) + 1, feedback=output[-1500:] or 'Integration command failed.')
                    durable.write_json(self.pending_path, pending)
                    self.save('repairing', 'Integration command failed; next session repairs it')
                    return None
            pending.pop('regen')
            durable.write_json(self.pending_path, pending)
        head = self.head()
        if moved:
            self.event('integrated', upstream=upstream, head=head, overlap=overlap[:30], regenerated=regenerated)
        if head == after:
            return after  # regeneration changed nothing on an unchanged head
        if not (moved and pending.get('quick') and cfg.get('integration_verify')):
            self.save('verifying', 'Integrated onto the moved target; the full gate runs again')
            return None
        for command in cfg['integration_verify']:
            slot = self.gate_slot(integration=True)
            if slot is None:
                return 'halt'  # pending index 0: the full gate runs on resume
            with slot:
                result, output, _ = self.job('integrating', command,
                    min(cfg.get('verification_timeout_seconds', 3600), max(1, self.state['deadline'] - time.time())))
            self.clear_operation()
            if self.head() != head or self.dirty():
                self.fail('integration check changed the worktree')
            if result['state'] != 'passed':
                self.event('integration_check_failed', head=head)
                self.save('verifying', 'Quick integration check failed; the full gate runs again')
                return None
        # The full gate passed on the same lane changes over a base whose
        # incoming changes touch none of the lane's files; the quick check passed
        # on the combined revision.
        pending.update(index=total)
        pending.pop('quick', None)
        durable.write_json(self.pending_path, pending)
        self.event('integration_verified', head=head)
        return head

    def verify(self, pending):
        cfg, after = self.cfg, pending['head']
        if not self.state.get('operation'):
            self.owner_intent()
        lines = (self.work / cfg['plan']).read_text(encoding='utf-8', errors='replace').splitlines()
        completing = bool(lines and lines[0].strip() == 'STATUS: DONE')
        try:
            self.contract(require_complete=completing)
        except (self.a.Stop, ValueError) as error:
            if isinstance(error, self.a.Stop) and not str(error).startswith('Invalid plan contract'):
                raise  # e.g. STATUS: DONE over incomplete tasks, or changed definitions, stays a hard block
            # The sidecar is agent-authored at this candidate. Hand the defect back as gate
            # feedback (bounded by max_gate_failures) instead of blocking the run.
            pending.update(failures=pending.get('failures', 0) + 1, index=0,
                           feedback='Plan contract check failed; repair ' + str(cfg.get('plan_contract')) +
                                    ' (evidence entries must be objects with criterion_id, path, tested_revision, '
                                    'sha256, command, result; leave evidence [] until the task is complete): ' + str(error))
            durable.write_json(self.pending_path, pending)
            self.clear_operation()
            self.save('repairing', 'Plan contract invalid; next session repairs it')
            self.event('contract_feedback', reason=str(error)[:500])
            return
        commands = cfg['verify'] + (cfg.get('final_verify', []) if completing else [])
        op = self.state.get('operation')
        if op and op['kind'] == 'integrating':
            # An integration command or quick check was interrupted. Both are
            # repeatable; pending already asks for the full gate on this head.
            if durable.inspect(self.base / 'jobs' / op['id'])['supervisor_active']:
                self.fail('An interrupted integration job is still running; resume after it ends.')
            self.clear_operation()
            self.event('integration_interrupted', job_id=op['id'])
        for index in range(pending.get('index', 0), len(commands)):
            if self.dirty() or self.head() != after or self.a.git(self.work, 'branch', '--show-current') != self.branch:
                self.fail('verification changed HEAD or branch, or worktree is dirty; inspect before resuming')
            slot = self.gate_slot(self.state.get('operation'))
            if slot is None:
                return 'halt'
            self.save(gate_index=index + 1, gate_total=len(commands), candidate_head=after)
            configured = cfg.get('verification_timeout_seconds', cfg['max_hours'] * 3600)
            remaining = max(1, self.state['deadline'] - time.time())
            with slot:
                result, output, op = self.job('verifying', commands[index], min(configured, remaining))
            if self.head() != after or self.a.git(self.work, 'branch', '--show-current') != self.branch:
                self.fail('verification changed HEAD or branch; inspect worktree before resuming')
            if self.dirty():
                self.fail('verification modified worktree')
            if result['state'] != 'passed':
                slept = result['state'] == 'timed_out' and float(result.get('suspended_seconds') or 0) > 0
                if (result['state'] == 'interrupted' or slept) and cfg.get('verification_replay_safe', False):
                    retries = pending.get('replays', 0) + 1
                    if retries <= cfg.get('max_recovery_attempts', 2):
                        pending['replays'] = retries
                        durable.write_json(self.pending_path, pending)
                        self.clear_operation()
                        self.event('verification_replay', index=index, attempt=retries)
                        return
                if (result['state'] == 'timed_out' and remaining < configured and not slept
                        and cfg.get('verification_replay_safe', False)):
                    # The run budget, not the gate, set this timeout (Aqar 27 Nov 2026: a 5400 s gate
                    # got 2 min before the deadline). The candidate was never judged: keep it pending
                    # with its saved operation and stop on the budget, so recover replays the gate
                    # (as for a blocked gate) instead of the run blocking for the owner.
                    durable.write_json(self.pending_path, pending)
                    self.event('budget_cut_gate', index=index, job_id=op['id'], allowed=round(remaining, 1))
                    self.save('stopped', 'Run time budget reached during verification; recover reruns the gate')
                    return 'halt'
                if result['state'] == 'failed' and result.get('exit_code') is not None:
                    pending.update(failures=pending.get('failures', 0) + 1, index=0, feedback=output[-1500:] or 'Verification exited nonzero; inspect job log.')
                    durable.write_json(self.pending_path, pending)
                    self.clear_operation()
                    self.save('repairing', 'Independent verification failed; next session repairs the observed failure')
                    return
                self.fail('verification ' + result['state'] + '; replay requires a safe verification contract')
            pending.update(index=index + 1, replays=0)
            durable.write_json(self.pending_path, pending)
            self.clear_operation()
            self.event('verification', index=index, exit=0, head=after)
        if cfg['publish']:
            turn = self.gate_slot(turn=True) if cfg.get('integrate') else contextlib.nullcontext()
            if turn is None:
                return 'halt'
            with turn:
                if cfg.get('integrate') and not self.state.get('operation'):
                    after = self.integrate(pending, after, len(commands))
                    if after is None or after == 'halt':
                        return after
                # Repeating this exact non-force ref update is idempotent. No merge,
                # force, branch switch or new revision is introduced on recovery.
                # A failed push that the remote did not reject (DNS/network outage) is
                # retried after a pause, bounded by max_publish_retries and the deadline.
                attempts = 0
                while True:
                    result, output, _ = self.job('publishing', ['git', 'push', cfg['remote'], after + ':refs/heads/' + cfg['target_branch']], 120)
                    rejected = any(term in output for term in PUSH_REJECTED)
                    if result['state'] == 'passed' or rejected:
                        break
                    attempts += 1
                    delay = cfg.get('publish_retry_seconds', 300)
                    if (attempts > cfg.get('max_publish_retries', 72) or (self.base / 'STOP').exists()
                            or time.time() + delay >= self.state['deadline']):
                        break
                    self.clear_operation()
                    self.save('waiting', f'Push failed; retry {attempts} in {delay}s: ' + output[-200:])
                    self.event('publish_retry', attempt=attempts, seconds=delay)
                    until = time.time() + delay
                    while time.time() < until and not (self.base / 'STOP').exists():
                        time.sleep(min(5, max(0.01, until - time.time())))
                if result['state'] != 'passed':
                    if cfg.get('integrate') and result['state'] == 'failed' and rejected:
                        # Another lane published first. Nothing was sent; integrate again.
                        self.clear_operation()
                        pending['rejections'] = pending.get('rejections', 0) + 1
                        if pending['rejections'] > 2 * cfg.get('max_integration_attempts', 6):
                            self.fail('push rejected too often for this slice; the target keeps moving or fetch keeps failing')
                        durable.write_json(self.pending_path, pending)
                        self.event('push_rejected', head=after, count=pending['rejections'])
                        time.sleep(min(60, 5 * pending['rejections']))
                        return
                    self.fail('push failed or interrupted; inspect remote ref and receipt: ' + output[-500:])
            self.event('published', head=after, target=cfg['target_branch'])
        self.owner_intent()
        durable.write_json(self.checkpoint, {'head': after, 'config_digest': self.state['config_digest'], 'at': stamp(),
                           'run_id': self.state['run_id'], 'accepted_slices': self.state['accepted_slices'] + 1,
                           'operation_id': (self.state.get('operation') or {}).get('id')})
        self.pending_path.unlink(missing_ok=True)
        self.clear_operation(verified_head=after, accepted_slices=self.state['accepted_slices'] + 1)
        self.event('accepted', head=after)


def deliberate_recovery(api, cfg, base):
    """Explicit operator action only. Scheduled resume never clears a stop."""
    journal = base / ('run-' + cfg['runner'] + '.json')
    if not journal.exists():
        raise api.Stop('No saved run to recover; configure and start a new run.')
    state = durable.read_json(journal)
    if state['state'] == 'done':
        raise api.Stop('This run is already complete.')
    if state['config_digest'] != config_digest(cfg):
        raise api.Stop('Restore the saved configuration before recovering; do not reinterpret an interrupted operation.')
    operation = state.get('operation')
    if operation:
        receipt = durable.inspect(base / 'jobs' / operation['id'])
        if receipt['supervisor_active']:
            raise api.Stop('Saved job is still active; observe it or cancel and wait for its terminal receipt.')
        if operation['kind'] == 'publishing' and receipt['state'] not in ('failed', 'interrupted', 'timed_out'):
            raise api.Stop('Reconcile the interrupted remote publication before recovery; local-only replay is insufficient.')
        if operation['kind'] == 'verifying' and not cfg.get('verification_replay_safe', False):
            raise api.Stop('Verification replay is not declared safe.')
    if cfg.get('recovery_policy') != 'local-only':
        raise api.Stop('Automatic edit reconciliation requires the previously configured local-only recovery policy.')
    work = worktree_path(api.ROOT, cfg, base)
    if api.git(work, 'branch', '--show-current') != state['branch']:
        raise api.Stop('Worktree branch changed; inspect before recovering.')
    before = operation['before'] if operation else durable.read_json(base / ('verified-' + cfg['runner'] + '.json'))['head']
    if api.call(['git', 'merge-base', '--is-ancestor', before, api.git(work, 'rev-parse', 'HEAD')], work).returncode:
        raise api.Stop('Worktree history changed; inspect before recovering.')
    if operation and operation['kind'] == 'publishing':
        # Replay the push only when the remote ref is the candidate itself or one
        # of its ancestors; any other remote state needs manual reconciliation.
        pending_path = base / ('pending-' + cfg['runner'] + '.json')
        candidate = durable.read_json(pending_path)['head'] if pending_path.exists() else None
        remote = api.call(['git', 'ls-remote', cfg['remote'], 'refs/heads/' + cfg['target_branch']], api.ROOT, timeout=120)
        if remote.returncode or not candidate:
            raise api.Stop('Remote unreachable or no pending candidate; cannot reconcile the failed publication yet.')
        sha = remote.stdout.split()[0] if remote.stdout.strip() else ''
        if sha != candidate and (not sha or api.call(['git', 'merge-base', '--is-ancestor', sha, candidate], work).returncode):
            raise api.Stop('Remote branch is not an ancestor of the candidate; reconcile the publication manually.')
    # STOP is the commit barrier for this explicit recovery transition. A crash
    # during marker cleanup must not expose a runnable state with stale CANCEL.
    (base / 'STOP').touch()
    state.update(state='recovering', reason='Operator requested local recovery and renewed budget',
                 operation=None, job_id=None, job_state=None, retry_at=None, session=0,
                 rate_retries=0, net_retries=0, recovery_attempts=0, reconcile=not operation or operation['kind'] == 'agent',
                 deadline=time.time() + cfg['max_hours'] * 3600, updated=stamp())
    durable.write_json(journal, state)
    with (base / 'events.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps({'at': stamp(), 'event': 'operator_recovery', 'run_id': state['run_id'],
                                 'previous_operation': operation, 'new_deadline': state['deadline']}) + '\n')
    (base / 'CANCEL').unlink(missing_ok=True)
    (base / 'STOP').unlink(missing_ok=True)


def execute(api, cfg, base, resume_only=False, recover=False):
    base = Path(base)
    base.mkdir(parents=True, exist_ok=True)
    lease = durable.Lease(base / 'run.mutex')
    try:
        lease.__enter__()
    except durable.Busy:
        raise api.Stop('A driver is already running for this repository.')
    marker = base / 'run.lock'
    try:
        if marker.exists():
            try:
                old = durable.read_json(marker)
            except ValueError:
                raise api.Stop('Legacy lock exists; verify the old driver is stopped before removing it.')
            if old.get('schema') != 1:
                raise api.Stop('Unknown lock owner; inspect before recovery.')
        if marker.exists():
            durable.write_json(marker, {'schema': 1, 'mutex': 'run.mutex'})
        else:
            try:
                fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            except FileExistsError:
                raise api.Stop('Updater acquired the repository lock; retry after it finishes.')
            with os.fdopen(fd, 'w', encoding='utf-8') as stream:
                stream.write('{"schema": 1, "mutex": "run.mutex"}\n')
                stream.flush()
                os.fsync(stream.fileno())
        if recover:
            deliberate_recovery(api, cfg, base)
        run = Execution(api, cfg, base, resume_only)
        try:
            if not run.setup():
                return 0
            run.loop()
        except Halted as halted:
            run.save('stopped', str(halted))
        except (api.Stop, OSError, ValueError, RuntimeError) as error:
            if run.state:
                if getattr(run, 'preserve_journal', False):
                    durable.write_json(base / 'status.json', {**run.state, 'state': 'blocked', 'reason': str(error)})
                else:
                    run.save('blocked', str(error))
                run.event('blocked', reason=str(error))
            print('BLOCKED:', error)
            return 2
        print(json.dumps(run.state, indent=2))
        return 0 if run.state['state'] in ('done', 'stopped') else 2
    finally:
        # Only remove our marker; do not remove a legacy/unknown owner's lock.
        if marker.exists():
            try:
                if durable.read_json(marker).get('schema') == 1:
                    marker.unlink()
            except ValueError:
                pass
        lease.__exit__(None, None, None)


def render(base):
    path = Path(base) / 'status.json'
    if not path.exists():
        return 'No run recorded.'
    state = durable.read_json(path)
    active = durable.held(Path(base) / 'run.mutex')
    lines = [f"{('LANE ' + state['lane'] + ' | ') if state.get('lane') else ''}{state['runner'].upper()} | {state['state'].upper()} | supervisor {'active' if active else 'offline'}",
             f"Plan: {state['plan']}", f"Worktree: {state.get('worktree', 'not prepared')}",
             f"Sessions started: {state['session']} | Revisions independently verified: {state['accepted_slices']}",
             f"Reason: {state.get('reason') or 'No blocker recorded'}",
             f"Limit probes: {state.get('rate_retries',0)} | Local recovery attempts: {state.get('recovery_attempts',0)}",
             f"Last durable update: {state['updated']}"]
    if state.get('action') and state.get('operation'):
        lines.append('Current executable: ' + state['action'])
    if state.get('verified_head'):
        lines.append('Verified revision: ' + state['verified_head'])
    checkpoint_path = Path(base) / ('verified-' + state['runner'] + '.json')
    if checkpoint_path.exists():
        checkpoint = durable.read_json(checkpoint_path)
        if checkpoint.get('at'):
            age = max(0, int(time.time() - dt.datetime.fromisoformat(checkpoint['at']).timestamp()))
            lines.append(f"Verification checkpoint: {checkpoint['at']} | age {age}s")
        else:
            lines.append('Verification checkpoint: initial baseline; no gate receipt yet')
    if state.get('gate_total'):
        lines.append(f"Verification: command {state['gate_index']} of {state['gate_total']}")
    if state.get('job_id'):
        job = durable.inspect(Path(base) / 'jobs' / state['job_id'])
        lines += [f"Job: {job['state']} | supervisor {'active' if job['supervisor_active'] else 'offline'}",
                  'Log: ' + job['log']]
        if job.get('heartbeat_at'):
            lines.append(f"Heartbeat age: {max(0, int(time.time()-job['heartbeat_at']))}s (liveness, not accepted progress)")
        if job.get('last_output_at'):
            lines.append('Last output: ' + stamp(job['last_output_at']) + f" | {job.get('output_bytes',0)} bytes")
    if state.get('retry_at'):
        lines.append('Next probe: ' + stamp(state['retry_at']) + ' (provider reset time unconfirmed)')
    lines += ['Budget ends: ' + stamp(state['deadline'])]
    if state.get('plan_contract') and state.get('worktree'):
        try:
            data = durable.read_json(Path(state['worktree']) / state['plan_contract'])
            tasks = data['tasks']
            completed = [task for task in tasks if task['state'] == 'complete']
            remaining = [task for task in tasks if task['state'] != 'complete']
            lines.append(f"Plan reports: {len(completed)}/{len(tasks)} tasks complete; {len(remaining)} remaining (metadata, not independent acceptance)")
            for task in remaining[:5]:
                lines.append(f"  {task['id']} | {task['state']} | {task['title']}")
        except (OSError, ValueError, KeyError, TypeError):
            lines.append('Task summary unavailable: contract may be mid-edit or invalid; no progress inferred.')
    else:
        lines.append('Task totals unknown: no JSON plan contract configured. Read the committed handoff.')
    if not active and state['state'] not in TERMINAL:
        lines.append('Recovery: run driver.py resume, or use the configured logon task. Existing jobs will be reconciled.')
    return '\n'.join(lines)


def watch(base, follow=False, interval=5):
    if not .2 <= interval <= 3600:
        raise ValueError('Watch interval must be between 0.2 and 3600 seconds')
    try:
        while True:
            print(render(base), flush=True)
            if not follow:
                return 0
            time.sleep(interval)
            print('\n--- refreshed ---', flush=True)
    except KeyboardInterrupt:
        return 0  # Closing the watch never stops the run.
