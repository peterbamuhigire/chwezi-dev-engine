import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

import test_driver as fixtures

DRIVER, git = fixtures.DRIVER, fixtures.git


class PowerLoss(BaseException):
    pass


class RecoveryTests(unittest.TestCase):
    setUp = fixtures.DriverTests.setUp
    tearDown = fixtures.DriverTests.tearDown

    def run_driver(self, resume=False, recover=False):
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            result = self.d.run(self.cfg, self.base, resume, recover)
        self.last_output = captured.getvalue()
        return result

    def test_prepared_job_never_launches_after_offline_budget_expiry(self):
        import durable
        with patch.object(durable, 'wait', side_effect=PowerLoss):
            with self.assertRaises(PowerLoss):
                self.run_driver()
        journal = self.base / 'run-codex.json'
        saved = json.loads(journal.read_text())
        saved['deadline'] = time.time() - 1
        durable.write_json(journal, saved)
        self.assertEqual(self.run_driver(resume=True), 2)
        folder = self.base / 'jobs' / saved['operation']['id']
        self.assertFalse((folder / 'result.json').exists())

    def test_cancel_requires_deliberate_recovery(self):
        self.cfg.update(recovery_policy='local-only')
        self.base.mkdir(parents=True)
        (self.base / 'CANCEL').touch()
        self.assertEqual(self.run_driver(), 2)
        (self.base / 'STOP').touch()
        self.assertEqual(self.run_driver(resume=True), 0)
        self.assertTrue((self.base / 'STOP').exists())
        self.assertEqual(self.run_driver(recover=True), 0)
        self.assertFalse((self.base / 'STOP').exists())
        self.assertFalse((self.base / 'CANCEL').exists())

    def test_crash_during_recovery_cleanup_preserves_stop_barrier(self):
        self.cfg.update(recovery_policy='local-only')
        self.base.mkdir(parents=True)
        (self.base / 'CANCEL').touch()
        self.assertEqual(self.run_driver(), 2)
        original = Path.unlink
        def crash(path, *args, **kwargs):
            result = original(path, *args, **kwargs)
            if path == self.base / 'CANCEL':
                raise PowerLoss()
            return result
        with patch.object(Path, 'unlink', crash):
            with self.assertRaises(PowerLoss):
                self.run_driver(recover=True)
        self.assertTrue((self.base / 'STOP').exists())
        jobs = list((self.base / 'jobs').iterdir())
        self.assertEqual(self.run_driver(resume=True), 2)
        self.assertEqual(jobs, list((self.base / 'jobs').iterdir()))
        self.assertEqual(self.run_driver(recover=True), 0)

    def test_both_runners_use_same_verified_recovery_contract(self):
        for runner in ('codex', 'claude'):
            with self.subTest(runner=runner):
                self.cfg['runner'] = runner
                self.assertEqual(self.run_driver(), 0)
                receipt = json.loads((self.base / f'verified-{runner}.json').read_text())
                self.assertEqual(receipt['head'], git(self.base / 'worktrees' / runner, 'rev-parse', 'HEAD'))
                self.assertEqual(json.loads((self.base / 'status.json').read_text())['state'], 'done')

    def test_crash_after_candidate_receipt_does_not_call_agent_again(self):
        import execution
        original = execution.Execution.clear_operation
        def crash(obj, **fields):
            if obj.pending_path.exists() and obj.state.get('operation', {}).get('kind') == 'agent':
                raise PowerLoss()
            return original(obj, **fields)
        with patch.object(execution.Execution, 'clear_operation', crash):
            with self.assertRaises(PowerLoss):
                self.run_driver()
        self.fake.write_text("raise RuntimeError('Agent must not run again')")
        self.assertEqual(self.run_driver(resume=True), 0)
        self.assertEqual(json.loads((self.base / 'status.json').read_text())['state'], 'done')

    def test_crash_after_gate_receipt_skips_only_that_exact_gate(self):
        import execution
        marker = self.root.parent / 'gate-count'
        self.cfg['verify'] = [[sys.executable, '-c',
             f"from pathlib import Path; p=Path({str(marker)!r}); p.write_text(p.read_text()+'x' if p.exists() else 'x')"],
             [sys.executable, '-c', 'pass']]
        original = execution.Execution.clear_operation
        def crash(obj, **fields):
            if obj.state.get('operation') and obj.state['operation']['kind'] == 'verifying':
                raise PowerLoss()
            return original(obj, **fields)
        with patch.object(execution.Execution, 'clear_operation', crash):
            with self.assertRaises(PowerLoss):
                self.run_driver()
        self.assertEqual(self.run_driver(resume=True), 0)
        self.assertEqual(marker.read_text(), 'x')

    def test_boot_change_replays_old_gate_only_when_declared_safe(self):
        import execution
        import durable
        self.cfg['verification_replay_safe'] = True
        marker = self.root.parent / 'boot-gate-count'
        self.cfg['verify'] = [[sys.executable, '-c',
             f"from pathlib import Path; p=Path({str(marker)!r}); p.write_text(p.read_text()+'x' if p.exists() else 'x')"]]
        original = execution.Execution.clear_operation
        def crash(obj, **fields):
            if obj.state.get('operation') and obj.state['operation']['kind'] == 'verifying':
                raise PowerLoss()
            return original(obj, **fields)
        with patch.object(durable, 'boot_identity', return_value='boot-a'), patch.object(execution.Execution, 'clear_operation', crash):
            with self.assertRaises(PowerLoss):
                self.run_driver()
        self.assertEqual(marker.read_text(), 'x')
        with patch.object(durable, 'boot_identity', return_value='boot-b'):
            self.assertEqual(self.run_driver(resume=True), 0)
        self.assertEqual(marker.read_text(), 'xx')

    def test_owner_plan_change_does_not_reinterpret_saved_operation(self):
        import durable
        with patch.object(durable, 'wait', side_effect=PowerLoss):
            with self.assertRaises(PowerLoss):
                self.run_driver()
        journal = (self.base / 'run-codex.json').read_bytes()
        (self.root / self.cfg['plan']).write_text('# Different scope\n')
        git(self.root, 'add', self.cfg['plan'])
        git(self.root, 'commit', '-qm', 'revise intended outcome')
        self.assertEqual(self.run_driver(resume=True), 2)
        self.assertEqual((self.base / 'run-codex.json').read_bytes(), journal)

    def test_adapters_preserve_explicit_arguments_and_add_no_bypass(self):
        import driver
        with patch.object(driver, 'executable', side_effect=lambda name: name):
            pre={'skills':'preload','subagents':'inherit'}
            self.assertEqual(driver.agent_command({**pre,'runner':'codex','runner_args':['--json']}), ['codex','exec','--json','-'])
            self.assertEqual(driver.agent_command({**pre,'runner':'claude','runner_args':['--output-format','json']}), ['claude','-p','--output-format','json'])
            cfg={**pre,'runner':'claude','runner_args_by_runner':{'codex':['--model','example-model'],'claude':[]}}
            self.assertEqual(driver.agent_command(cfg), ['claude','-p'])
            # Defaults (skills=on-demand, subagents=economy) insert only the skill profile and, for Claude,
            # the subagent file, before the owner's arguments. Codex has no subagent arguments.
            self.assertEqual(driver.agent_command({'runner':'codex','runner_args':['--json']}), ['codex','exec','-p',driver.CODEX_SKILL_PROFILE,'--json','-'])
            argv=driver.agent_command({'runner':'claude','runner_args':['--output-format','json']})
            self.assertEqual((argv[:3], argv[4], argv[6:]), (['claude','-p','--settings'], '--agents', ['--output-format','json']))
            self.assertTrue(argv[3].endswith('skills-on-demand.claude.json'))
            self.assertTrue(argv[5].endswith('subagents-economy.claude.json'))
            argv=driver.agent_command({'runner':'claude','subagents':'inherit','runner_args':[]})
            self.assertNotIn('--agents', argv)

    def test_preflight_checks_readiness_without_starting_a_job(self):
        self.assertEqual(self.d.preflight(self.cfg), 0)
        self.assertFalse(self.base.exists())
        (self.root / self.cfg['plan']).write_text('STATUS: BLOCKED - Select approved plan\n')
        git(self.root,'add',self.cfg['plan'])
        git(self.root,'commit','-qm','setup guard')
        with self.assertRaises(self.d.Stop):
            self.d.preflight(self.cfg)

    def test_long_gate_has_separate_timeout_from_agent_session(self):
        self.cfg.update(session_timeout_seconds=10, verification_timeout_seconds=20)
        self.cfg['verify'] = [[sys.executable, '-c', 'import time; time.sleep(10.4)']]
        self.assertEqual(self.run_driver(), 0)
        self.assertEqual(json.loads((self.base / 'status.json').read_text())['state'], 'done')

    def test_final_gate_runs_only_on_completion_candidate(self):
        self.fake.write_text('''import pathlib,subprocess,sys
sys.stdin.read()
p=pathlib.Path('auto-agents/PLAN.md')
p.write_text('STATUS: DONE\\n' if 'first slice' in p.read_text() else '# Plan\\nfirst slice\\n')
subprocess.run(['git','add',str(p)],check=True)
subprocess.run(['git','commit','-qm','slice'],check=True)
''')
        marker = self.root.parent / 'final-count'
        self.cfg['final_verify'] = [[sys.executable, '-c',
            f"from pathlib import Path; p=Path({str(marker)!r}); p.write_text(p.read_text()+'x' if p.exists() else 'x')"]]
        self.cfg['max_sessions'] = 3
        self.assertEqual(self.run_driver(), 0, getattr(self, 'last_output', 'No diagnostic output'))
        self.assertEqual(marker.read_text(), 'x')

    def test_done_marker_cannot_override_incomplete_contract(self):
        name = 'auto-agents/tasks.json'
        data = {'schema_version': 1, 'tasks': [{'id': 'TASK-1', 'title': 'Required behavior', 'depends_on': [],
            'scope': ['src'], 'acceptance': [{'id': 'AC-1', 'description': 'Observable outcome', 'evidence_oracle': 'Inspect outcome'}],
            'state': 'pending', 'evidence': []}]}
        (self.root / name).write_text(json.dumps(data))
        git(self.root, 'add', name)
        git(self.root, 'commit', '-qm', 'add contract')
        self.cfg['plan_contract'] = name
        self.assertEqual(self.run_driver(), 2)
        status = json.loads((self.base / 'status.json').read_text())
        self.assertIn('incomplete plan-contract', status['reason'])
        import execution
        watch = execution.render(self.base)
        self.assertIn('0/1 tasks complete', watch)
        self.assertIn('TASK-1 | pending | Required behavior', watch)

    def test_existing_done_marker_still_requires_current_verification(self):
        plan = self.root / self.cfg['plan']
        plan.write_text('STATUS: DONE\n')
        git(self.root, 'add', self.cfg['plan'])
        git(self.root, 'commit', '-qm', 'completion claim')
        marker = self.root.parent / 'checked'
        self.cfg['verify'] = [[sys.executable, '-c', f"from pathlib import Path; Path({str(marker)!r}).touch()"]]
        self.fake.write_text("raise RuntimeError('Completed plan needs verification, not an agent')")
        self.assertEqual(self.run_driver(), 0)
        self.assertTrue(marker.exists())

    def test_wait_resume_retains_deadline_and_retry_time(self):
        import execution
        self.fake.write_text("import sys; sys.stdin.read(); print('usage limit'); sys.exit(1)")
        self.cfg.update(usage_wait_seconds=.1, max_rate_retries=1)
        original = execution.Execution.wait_quota
        def crash(obj):
            if obj.state.get('retry_at'):
                raise PowerLoss()
            return original(obj)
        with patch.object(execution.Execution, 'wait_quota', crash):
            with self.assertRaises(PowerLoss):
                self.run_driver()
        saved = json.loads((self.base / 'run-codex.json').read_text())
        self.assertEqual(saved['rate_retries'], 1)
        self.assertIsNotNone(saved['retry_at'])
        self.assertEqual(self.run_driver(resume=True), 2)
        resumed = json.loads((self.base / 'run-codex.json').read_text())
        self.assertEqual(saved['deadline'], resumed['deadline'])
        self.assertEqual(saved['run_id'], resumed['run_id'])

    def test_live_driver_death_reattaches_same_gate(self):
        marker = self.root.parent / 'gate-count'
        self.cfg['verify'] = [[sys.executable, '-c',
            f"import time; from pathlib import Path; p=Path({str(marker)!r}); p.write_text(p.read_text()+'x' if p.exists() else 'x'); time.sleep(3)"]]
        launcher = self.root.parent / 'driver-launch.py'
        launcher.write_text(
            f"import sys; from pathlib import Path; sys.path.insert(0,{str(DRIVER.parent)!r}); import driver; "
            f"driver.ROOT=Path({str(self.root)!r}); driver.agent_command=lambda cfg:[sys.executable,{str(self.fake)!r}]; "
            f"sys.exit(driver.run({self.cfg!r},Path({str(self.base)!r}),len(sys.argv)>1))", encoding='utf-8')
        with (self.root.parent / 'driver-output').open('wb') as output:
            process = subprocess.Popen([sys.executable, '-B', str(launcher)], stdout=output, stderr=subprocess.STDOUT)
            try:
                deadline = time.time() + 20
                while not marker.exists() and time.time() < deadline:
                    time.sleep(.1)
                self.assertTrue(marker.exists())
                saved = json.loads((self.base / 'run-codex.json').read_text())
                job_id = saved['operation']['id']
                process.kill()
                process.wait(timeout=10)
                resume = subprocess.run([sys.executable, '-B', str(launcher), 'resume'], stdout=output, stderr=subprocess.STDOUT, timeout=20)
                self.assertEqual(resume.returncode, 0, (self.root.parent / 'driver-output').read_text())
                self.assertEqual(marker.read_text(), 'x')
                self.assertEqual(json.loads((self.base / 'jobs' / job_id / 'result.json').read_text())['state'], 'passed')
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait(timeout=10)


if __name__ == '__main__':
    unittest.main()
