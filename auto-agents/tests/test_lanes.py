"""Parallel lanes: isolated lane state, shared gate slots and integration onto a moving target branch."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

DRIVER = Path(__file__).resolve().parents[1] / 'driver.py'
sys.path.insert(0, str(DRIVER.parent))
import durable  # noqa: E402


def git(root, *args):
    return subprocess.run(['git', *args], cwd=root, check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True).stdout.strip()


AGENT = '''import pathlib,subprocess,sys
prompt=sys.stdin.read()
name=%r
if 'INTEGRATION' in prompt:
    subprocess.run(['git','-c','core.editor=true','rebase','-X','theirs','refs/remotes/origin/main'],check=True)
    sys.exit(0)
f=pathlib.Path(name); f.write_text('lane work\\n',encoding='utf8')
p=pathlib.Path('auto-agents/PLAN.md'); p.write_text('STATUS: DONE\\n',encoding='utf8')
subprocess.run(['git','add',str(f),str(p)],check=True)
subprocess.run(['git','commit','-qm','ROW-1: lane slice'],check=True)
'''


class LaneTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        top = Path(self.tmp.name)
        self.remote = top / 'remote.git'
        subprocess.run(['git', 'init', '--bare', '-q', '-b', 'main', str(self.remote)], check=True)
        self.root = top / 'repo'; self.root.mkdir()
        git(self.root, 'init', '-q', '-b', 'main')
        git(self.root, 'config', 'user.email', 'fixture@example.test'); git(self.root, 'config', 'user.name', 'Fixture')
        (self.root / 'auto-agents').mkdir()
        (self.root / 'auto-agents' / 'PLAN.md').write_text('# Plan\n', encoding='utf8')
        (self.root / 'shared.txt').write_text('base\n', encoding='utf8')
        git(self.root, 'add', '.'); git(self.root, 'commit', '-qm', 'initial')
        git(self.root, 'remote', 'add', 'origin', str(self.remote))
        git(self.root, 'push', '-q', 'origin', 'main')
        spec = importlib.util.spec_from_file_location('driver_lanes', DRIVER)
        self.d = importlib.util.module_from_spec(spec); spec.loader.exec_module(self.d)
        self.d.ROOT = self.root
        self.d.CFG = self.root / 'auto-agents' / 'config.json'
        self.fake = top / 'fake.py'
        self.write_agent('lane.txt')
        self.d.agent_command = lambda cfg: [sys.executable, str(self.fake)]
        self.counter = top / 'gates.txt'
        self.cfg = {'runner': 'codex', 'plan': 'auto-agents/PLAN.md', 'session_timeout_seconds': 30,
                    'verify': [[sys.executable, '-c', 'import pathlib;p=pathlib.Path(%r);p.write_text(p.read_text()+"g" if p.exists() else "g")' % str(self.counter)]],
                    'max_hours': 1, 'max_sessions': 3, 'publish': True, 'remote': 'origin', 'target_branch': 'main',
                    'integrate': True, 'lane': 'area-06'}
        self.base = self.d.status_path('area-06')

    def write_agent(self, name):
        self.fake.write_text(AGENT % name, encoding='utf8')

    def tearDown(self):
        for jobs in Path(self.tmp.name).rglob('jobs'):
            for job in jobs.iterdir():
                if job.is_dir() and durable.held(job / 'job.mutex'):
                    (job / 'CANCEL').touch()
                    until = time.monotonic() + 10
                    while durable.held(job / 'job.mutex') and time.monotonic() < until:
                        time.sleep(.05)
        self.tmp.cleanup()

    def advance_remote(self, path, text, subject='other lane'):
        other = Path(self.tmp.name) / 'other'
        if not other.exists():
            subprocess.run(['git', 'clone', '-q', str(self.remote), str(other)], check=True)
            git(other, 'config', 'user.email', 'o@example.test'); git(other, 'config', 'user.name', 'Other')
        git(other, 'pull', '-q', '--rebase', 'origin', 'main')
        (other / path).write_text(text, encoding='utf8')
        git(other, 'add', path); git(other, 'commit', '-qm', subject); git(other, 'push', '-q', 'origin', 'main')

    def events(self):
        return [json.loads(x) for x in (self.base / 'events.jsonl').read_text().splitlines()]

    # -- configuration -------------------------------------------------
    def test_lane_overlay_and_state_paths(self):
        base_cfg = dict(self.cfg); base_cfg.pop('lane')
        self.d.CFG.write_text(json.dumps(base_cfg), encoding='utf8')
        (self.root / 'auto-agents' / 'lanes').mkdir()
        (self.root / 'auto-agents' / 'lanes' / 'area-06.json').write_text(json.dumps({'plan': 'auto-agents/lanes/area-06.md'}), encoding='utf8')
        cfg = self.d.config('area-06')
        self.assertEqual(cfg['plan'], 'auto-agents/lanes/area-06.md')
        self.assertEqual(cfg['lane'], 'area-06')
        self.assertEqual(self.d.status_path('area-06'), (self.root / '.git' / 'auto-agents' / 'lanes' / 'area-06').resolve())
        self.assertEqual(self.d.status_path(None), (self.root / '.git' / 'auto-agents').resolve())
        for bad in ('../x', 'Area 6', '', 'a' * 41):
            with self.assertRaises(self.d.Stop):
                self.d.config(bad)
        with self.assertRaises(self.d.Stop):
            self.d.config('area-07')  # no overlay file
        (self.root / 'auto-agents' / 'lanes' / 'area-06.json').write_text(json.dumps({'gate_slots': 0}), encoding='utf8')
        with self.assertRaises(self.d.Stop):
            self.d.config('area-06')

    def test_lane_uses_own_branch_and_worktree(self):
        self.assertEqual(self.d.run(self.cfg, self.base), 0)
        status = json.loads((self.base / 'status.json').read_text())
        self.assertEqual(status['state'], 'done')
        self.assertEqual(status['branch'], 'auto-agents/lane-area-06-codex')
        self.assertEqual(Path(status['worktree']), self.base / 'worktrees' / 'codex')
        self.assertEqual(git(self.remote, 'rev-parse', 'main'), git(self.base / 'worktrees' / 'codex', 'rev-parse', 'HEAD'))

    # -- integration ---------------------------------------------------
    def mover(self, path, text, subject, once=True):
        """A gate command that publishes another lane's commit while this lane's gate runs."""
        hook = Path(self.tmp.name) / ('move-%d.py' % len(list(Path(self.tmp.name).glob('move-*.py'))))
        flag = hook.with_suffix('.done')
        hook.write_text(
            'import pathlib,subprocess,sys\n'
            'flag=pathlib.Path(%r)\n'
            'if %r and flag.exists(): sys.exit(0)\n'
            'flag.write_text("1")\n'
            'o=pathlib.Path(%r)\n'
            'subprocess.run(["git","pull","-q","--rebase","origin","main"],cwd=o,check=True)\n'
            '(o/%r).write_text(%r)\n'
            'subprocess.run(["git","add","-A"],cwd=o,check=True)\n'
            'subprocess.run(["git","commit","-qm",%r],cwd=o,check=True)\n'
            'subprocess.run(["git","push","-q","origin","main"],cwd=o,check=True)\n'
            % (str(flag), once, str(Path(self.tmp.name) / 'other'), path, text, subject), encoding='utf8')
        self.advance_remote('seed.txt', 'seed\n', 'seed other clone')
        git(self.root, 'fetch', '-q', 'origin'); git(self.root, 'merge', '-q', '--ff-only', 'origin/main')
        return [sys.executable, str(hook)]

    def test_disjoint_upstream_change_is_rebased_and_checked_cheaply(self):
        self.cfg['integration_verify'] = [[sys.executable, '-c', 'import pathlib;assert pathlib.Path("other.txt").exists()']]
        self.cfg['verify'].append(self.mover('other.txt', 'x\n', 'other lane slice'))
        self.assertEqual(self.d.run(self.cfg, self.base), 0)
        names = [e['event'] for e in self.events()]
        self.assertIn('integrated', names)
        self.assertIn('integration_verified', names)
        integrated = [e for e in self.events() if e['event'] == 'integrated'][0]
        self.assertEqual(integrated['overlap'], [])
        log = git(self.remote, 'log', '--format=%s', 'main')
        self.assertIn('ROW-1: lane slice', log); self.assertIn('other lane slice', log)
        self.assertEqual(self.counter.read_text(), 'g')  # the full gate ran once only
        self.assertEqual(git(self.remote, 'rev-list', '--merges', '--count', 'main'), '0')

    def test_overlapping_clean_rebase_reruns_full_gate(self):
        lines = ''.join('line %d\n' % i for i in range(20))
        (self.root / 'shared.txt').write_text(lines, encoding='utf8')
        git(self.root, 'commit', '-qam', 'longer shared'); git(self.root, 'push', '-q', 'origin', 'main')
        self.cfg['integration_verify'] = [[sys.executable, '-c', 'pass']]
        self.fake.write_text(AGENT.replace("f.write_text('lane work\\n',encoding='utf8')", "f.write_text('lane\\n'+f.read_text(),encoding='utf8')") % 'shared.txt', encoding='utf8')
        self.cfg['verify'].append(self.mover('shared.txt', lines + 'upstream tail\n', 'other lane edits shared'))
        self.assertEqual(self.d.run(self.cfg, self.base), 0)
        integrated = [e for e in self.events() if e['event'] == 'integrated'][0]
        self.assertEqual(integrated['overlap'], ['shared.txt'])
        self.assertEqual(self.counter.read_text(), 'gg')  # gate re-ran on the integrated head
        text = git(self.remote, 'show', 'main:shared.txt')
        self.assertTrue(text.startswith('lane')); self.assertTrue(text.endswith('upstream tail'))

    def test_conflict_is_integrated_by_next_session_and_regated(self):
        self.write_agent('shared.txt')
        self.cfg['verify'].append(self.mover('shared.txt', 'upstream rewrite\n', 'other lane rewrites shared'))
        self.assertEqual(self.d.run(self.cfg, self.base), 0)
        names = [e['event'] for e in self.events()]
        self.assertIn('integration_conflict', names)
        self.assertEqual(self.counter.read_text(), 'gg')
        log = git(self.remote, 'log', '--format=%s', 'main')
        self.assertIn('ROW-1: lane slice', log); self.assertIn('other lane rewrites shared', log)
        self.assertEqual(git(self.remote, 'show', 'main:shared.txt'), 'lane work')

    def test_fresh_session_starts_from_upstream(self):
        self.advance_remote('seed.txt', 'seed\n', 'other lane published')
        self.fake.write_text('import pathlib,subprocess,sys\nsys.stdin.read()\nassert pathlib.Path("seed.txt").exists(), "lane did not sync"\np=pathlib.Path("auto-agents/PLAN.md"); p.write_text("STATUS: DONE\\n")\nsubprocess.run(["git","commit","-qam","ROW-2"],check=True)\n', encoding='utf8')
        self.assertEqual(self.d.run(self.cfg, self.base), 0)
        self.assertIn('synced', [e['event'] for e in self.events()])
        self.assertIn('other lane published', git(self.remote, 'log', '--format=%s', 'main'))

    def test_integration_session_must_keep_lane_commits(self):
        ex = self.d
        from types import SimpleNamespace
        import execution
        run = execution.Execution(SimpleNamespace(**vars(ex)), self.cfg, self.base, False)
        run.state = {'run_id': 'x'}
        run.work = self.root
        run.branch = 'main'
        upstream = git(self.root, 'rev-parse', 'HEAD')
        (self.root / 'a.txt').write_text('a'); git(self.root, 'add', 'a.txt'); git(self.root, 'commit', '-qm', 'ROW-9: keep me')
        run.check_integration({'upstream': upstream, 'subjects': ['ROW-9: keep me']})
        with self.assertRaises(ex.Stop):
            run.check_integration({'upstream': upstream, 'subjects': ['ROW-9: keep me', 'ROW-10: lost']})

    def superseded_fixture(self, upstream_text):
        """Lane: ROW-1 (a.txt) then a flaky-test repair (t.txt). Upstream changed t.txt meanwhile.

        Returns (run, upstream, orig) with HEAD = upstream + ROW-1 only, as an
        integration session leaves it after dropping the repair.
        """
        ex = self.d
        from types import SimpleNamespace
        import execution
        run = execution.Execution(SimpleNamespace(**vars(ex)), self.cfg, self.base, False)
        run.state = {'run_id': 'x'}
        run.work = self.root
        run.branch = 'main'
        self.base.mkdir(parents=True, exist_ok=True)
        (self.root / 't.txt').write_text('old\n'); git(self.root, 'add', 't.txt'); git(self.root, 'commit', '-qm', 'base')
        base = git(self.root, 'rev-parse', 'HEAD')
        (self.root / 'a.txt').write_text('a\n'); git(self.root, 'add', 'a.txt'); git(self.root, 'commit', '-qm', 'ROW-1: lane work')
        (self.root / 't.txt').write_text('lane fix\n'); git(self.root, 'commit', '-qam', 'Gate repair: flaky test')
        orig = git(self.root, 'rev-parse', 'HEAD')
        git(self.root, 'checkout', '-q', '-b', 'other', base)
        if upstream_text is not None:
            (self.root / 't.txt').write_text(upstream_text); git(self.root, 'commit', '-qam', 'other lane fixed the flaky test')
        else:
            (self.root / 'u.txt').write_text('u\n'); git(self.root, 'add', 'u.txt'); git(self.root, 'commit', '-qm', 'other lane unrelated')
        upstream = git(self.root, 'rev-parse', 'HEAD')
        git(self.root, 'checkout', '-q', 'main')
        git(self.root, 'reset', '-q', '--hard', upstream)
        git(self.root, 'cherry-pick', orig + '~1')
        return run, upstream, orig

    def test_commit_superseded_upstream_may_be_dropped(self):
        run, upstream, orig = self.superseded_fixture('upstream fix\n')
        subjects = ['ROW-1: lane work', 'Gate repair: flaky test']
        run.check_integration({'upstream': upstream, 'subjects': subjects}, orig)
        self.assertIn('integration_superseded', [e['event'] for e in self.events()])
        with self.assertRaises(self.d.Stop):  # without the pre-integration head nothing can be proven
            run.check_integration({'upstream': upstream, 'subjects': subjects})

    def test_dropped_commit_not_changed_upstream_still_blocks(self):
        run, upstream, orig = self.superseded_fixture(None)
        with self.assertRaises(self.d.Stop):
            run.check_integration({'upstream': upstream, 'subjects': ['ROW-1: lane work', 'Gate repair: flaky test']}, orig)

    def test_dropped_commit_whose_file_differs_from_upstream_blocks(self):
        run, upstream, orig = self.superseded_fixture('upstream fix\n')
        (self.root / 't.txt').write_text('something else\n'); git(self.root, 'commit', '-qam', 'ROW-1: lane work, more')
        with self.assertRaises(self.d.Stop):
            run.check_integration({'upstream': upstream, 'subjects': ['ROW-1: lane work', 'Gate repair: flaky test']}, orig)

    # -- gate slots ----------------------------------------------------
    def test_gate_slots_are_shared_and_stop_aware(self):
        import execution
        from types import SimpleNamespace
        cfg = dict(self.cfg, gate_slots=1, gate_slot_poll_seconds=0.01)
        run = execution.Execution(SimpleNamespace(**vars(self.d)), cfg, self.base, False)
        run.state = {'run_id': 'x', 'deadline': time.time() + 60}
        self.base.mkdir(parents=True, exist_ok=True)
        self.assertEqual(run.shared, self.base.parent.parent)
        slot = run.gate_slot()
        self.assertIsNotNone(slot)
        with slot:
            other = execution.Execution(SimpleNamespace(**vars(self.d)), dict(cfg, lane='area-07'), self.d.status_path('area-07'), False)
            other.state = {'run_id': 'y', 'deadline': time.time() + 60}
            other.base.mkdir(parents=True, exist_ok=True)
            (other.base / 'STOP').write_text('stop')
            self.assertIsNone(other.gate_slot())  # busy, and STOP ends the wait
        (other.base / 'STOP').unlink()
        again = other.gate_slot()
        self.assertIsNotNone(again)
        with again:
            pass

    def test_integration_checks_do_not_queue_behind_full_gates(self):
        # Seen in Medic8 (17 Nov 2026): 5-minute quick checks waited 30-80
        # minutes behind full gates, the target moved meanwhile and a lane
        # exhausted its integration attempts.
        import execution
        from types import SimpleNamespace
        cfg = dict(self.cfg, gate_slots=1, gate_slot_poll_seconds=0.01)
        run = execution.Execution(SimpleNamespace(**vars(self.d)), cfg, self.base, False)
        run.state = {'run_id': 'x', 'deadline': time.time() + 60}
        self.base.mkdir(parents=True, exist_ok=True)
        gate = run.gate_slot()
        with gate:  # every full-gate slot is busy
            quick = run.gate_slot(integration=True)
            self.assertIsNotNone(quick)
            with quick:  # the single integration slot is busy too
                (self.base / 'STOP').write_text('stop')
                self.assertIsNone(run.gate_slot(integration=True))
                (self.base / 'STOP').unlink()
        self.assertTrue((run.shared / 'integration-slots' / 'slot-0.mutex').exists())

    def test_disjoint_change_with_gate_slots_uses_integration_pool(self):
        self.cfg.update(gate_slots=1, gate_slot_poll_seconds=0.01)
        self.cfg['integration_verify'] = [[sys.executable, '-c', 'import pathlib;assert pathlib.Path("other.txt").exists()']]
        self.cfg['verify'].append(self.mover('other.txt', 'x\n', 'other lane slice'))
        self.assertEqual(self.d.run(self.cfg, self.base), 0)
        self.assertIn('integration_verified', [e['event'] for e in self.events()])
        self.assertTrue((self.base.parent.parent / 'integration-slots').is_dir())


    # -- crash and interruption windows (review findings, 17 Nov 2026) --
    def execution(self, cfg=None):
        import execution
        from types import SimpleNamespace
        run = execution.Execution(SimpleNamespace(**vars(self.d)), cfg or self.cfg, self.base, False)
        run.state = {'run_id': 'x', 'deadline': time.time() + 60, 'config_digest': 'd'}
        self.base.mkdir(parents=True, exist_ok=True)
        return run

    def lane_worktree(self):
        work = self.base / 'worktrees' / 'codex'
        git(self.root, 'worktree', 'add', '-q', '-b', 'auto-agents/lane-area-06-codex', str(work), 'HEAD')
        git(work, 'config', 'user.email', 'l@example.test'); git(work, 'config', 'user.name', 'Lane')
        return work

    def test_crash_after_rebase_before_record_is_adopted(self):
        run = self.execution(); work = self.lane_worktree()
        orig = git(work, 'rev-parse', 'HEAD')
        (work / 'lane.txt').write_text('l'); git(work, 'add', 'lane.txt'); git(work, 'commit', '-qm', 'ROW-1: lane')
        lane_head = git(work, 'rev-parse', 'HEAD')
        self.advance_remote('other.txt', 'o\n', 'other')
        git(work, 'fetch', '-q', 'origin', '+refs/heads/main:refs/remotes/origin/main')
        upstream = git(work, 'rev-parse', 'refs/remotes/origin/main')
        durable.write_json(run.pending_path, {'head': lane_head, 'index': 1, 'failures': 0, 'config_digest': 'd',
                           'integrating': {'upstream': upstream, 'orig': lane_head, 'subjects': ['ROW-1: lane']}})
        git(work, 'rebase', '-q', upstream)  # the crash happened right after this
        run.reconcile_integration()
        pending = durable.read_json(run.pending_path)
        self.assertNotIn('integrating', pending)
        self.assertEqual(pending['head'], git(work, 'rev-parse', 'HEAD'))
        self.assertEqual(pending['index'], 0)  # never publish on the old gate result
        self.assertNotEqual(orig, pending['head'])

    def test_interrupted_driver_rebase_is_abandoned(self):
        run = self.execution(); work = self.lane_worktree()
        (work / 'shared.txt').write_text('lane\n'); git(work, 'commit', '-qam', 'ROW-1: lane')
        lane_head = git(work, 'rev-parse', 'HEAD')
        self.advance_remote('shared.txt', 'other\n', 'other')
        git(work, 'fetch', '-q', 'origin', '+refs/heads/main:refs/remotes/origin/main')
        upstream = git(work, 'rev-parse', 'refs/remotes/origin/main')
        durable.write_json(run.pending_path, {'head': lane_head, 'index': 1, 'failures': 0, 'config_digest': 'd',
                           'integrating': {'upstream': upstream, 'orig': lane_head, 'subjects': ['ROW-1: lane']}})
        subprocess.run(['git', 'rebase', upstream], cwd=work, capture_output=True)  # stops on the conflict
        self.assertTrue(run.rebasing())
        run.reconcile_integration()
        self.assertFalse(run.rebasing())
        self.assertEqual(git(work, 'rev-parse', 'HEAD'), lane_head)
        self.assertNotIn('integrating', durable.read_json(run.pending_path))

    def test_crash_after_integration_command_commit_requires_full_gate(self):
        run = self.execution(); work = self.lane_worktree()
        (work / 'lane.txt').write_text('l'); git(work, 'add', 'lane.txt'); git(work, 'commit', '-qm', 'ROW-1')
        rebased = git(work, 'rev-parse', 'HEAD')
        durable.write_json(run.pending_path, {'head': rebased, 'index': 0, 'failures': 0, 'config_digest': 'd', 'regen': True})
        (work / 'gen.txt').write_text('g'); git(work, 'add', 'gen.txt'); git(work, 'commit', '-qm', 'Integrate: regenerate')
        run.state['operation'] = {'kind': 'integrating', 'id': 'j'}
        run.reconcile_integration()
        pending = durable.read_json(run.pending_path)
        self.assertEqual(pending['head'], git(work, 'rev-parse', 'HEAD'))
        self.assertEqual((pending['index'], pending['regen'], pending['quick']), (0, True, False))

    def test_crash_inside_sync_is_adopted(self):
        run = self.execution(); work = self.lane_worktree()
        durable.write_json(run.checkpoint, {'head': git(work, 'rev-parse', 'HEAD')})
        self.advance_remote('other.txt', 'o\n', 'other')
        git(work, 'fetch', '-q', 'origin', '+refs/heads/main:refs/remotes/origin/main')
        git(work, 'merge', '-q', '--ff-only', 'refs/remotes/origin/main')  # crash before the checkpoint write
        run.reconcile_integration()
        self.assertEqual(durable.read_json(run.checkpoint)['head'], git(work, 'rev-parse', 'HEAD'))

    def test_interrupted_integration_session_retries(self):
        marker = Path(self.tmp.name) / 'limited'
        self.fake.write_text(AGENT.replace("""if 'INTEGRATION' in prompt:
""", """if 'INTEGRATION' in prompt:
    m=pathlib.Path(%r)
    if not m.exists():
        m.write_text('1')
        subprocess.run(['git','rebase','refs/remotes/origin/main'])
        print('usage limit'); sys.exit(1)
""" % str(marker)) % 'shared.txt', encoding='utf8')
        self.cfg.update(max_sessions=4, initial_backoff_seconds=0.01, max_backoff_seconds=0.01, usage_wait_seconds=0.01, max_rate_retries=2)
        self.cfg['verify'].append(self.mover('shared.txt', 'upstream rewrite\n', 'other lane rewrites shared'))
        self.assertEqual(self.d.run(self.cfg, self.base), 0)
        names = [e['event'] for e in self.events()]
        self.assertIn('rate_wait', names)
        self.assertEqual(json.loads((self.base / 'status.json').read_text())['state'], 'done')
        self.assertIn('ROW-1: lane slice', git(self.remote, 'log', '--format=%s', 'main'))

    def test_stop_while_waiting_for_slot_stops_cleanly(self):
        cfg = dict(self.cfg, gate_slots=1, gate_slot_poll_seconds=0.01)
        stop = self.base / 'STOP'
        self.fake.write_text(AGENT.replace("prompt=sys.stdin.read()", "prompt=sys.stdin.read(); pathlib.Path(%r).write_text('stop')" % str(stop)) % 'lane.txt', encoding='utf8')
        holder = durable.Lease(self.base.parent.parent / 'gate-slots' / 'slot-0.mutex')
        with holder:
            self.assertEqual(self.d.run(cfg, self.base), 0)
        status = json.loads((self.base / 'status.json').read_text())
        self.assertEqual(status['state'], 'stopped')
        self.assertIn('gate slot', status['reason'])
        self.assertNotIn('published', [e['event'] for e in self.events()])


    def test_stop_before_a_prepared_gate_launches_stops_cleanly_and_resumes(self):
        stop = self.base / 'STOP'
        self.fake.write_text(AGENT.replace("prompt=sys.stdin.read()", "prompt=sys.stdin.read(); pathlib.Path(%r).write_text('stop')" % str(stop)) % 'lane.txt', encoding='utf8')
        self.assertEqual(self.d.run(self.cfg, self.base), 0)
        status = json.loads((self.base / 'status.json').read_text())
        self.assertEqual(status['state'], 'stopped')
        self.assertIsNone(status.get('operation'))
        self.assertIn('launch_withheld', [e['event'] for e in self.events()])
        self.assertNotIn('published', [e['event'] for e in self.events()])
        stop.unlink()
        self.write_agent('lane.txt')
        self.assertEqual(self.d.run(self.cfg, self.base), 0)
        self.assertEqual(json.loads((self.base / 'status.json').read_text())['state'], 'done')
        self.assertIn('ROW-1: lane slice', git(self.remote, 'log', '--format=%s', 'main'))


if __name__ == '__main__':
    unittest.main()
