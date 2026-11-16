"""Owner input drift during a run must prevent subsequent work."""
import contextlib
import io
import json
import sys
import unittest
from unittest.mock import patch

import test_driver as fixtures


class LiveOwnerTests(unittest.TestCase):
    setUp = fixtures.DriverTests.setUp
    tearDown = fixtures.DriverTests.tearDown

    def runner(self):
        import execution
        self.base.mkdir(parents=True, exist_ok=True)
        run = execution.Execution(self.d, self.cfg, self.base, False)
        run.setup()
        return run

    def test_plan_withdrawal_blocks_both_adapters(self):
        for host in ('codex', 'claude'):
            self.cfg['runner'] = host
            run = self.runner()
            plan = self.root / self.cfg['plan']
            original = plan.read_bytes()
            try:
                plan.write_text('STATUS: BLOCKED - withdrawn\n')
                with patch.object(run, 'job') as launch:
                    with self.assertRaisesRegex(self.d.Stop, 'Owner input changed'):
                        run.loop()
                    launch.assert_not_called()
            finally:
                plan.write_bytes(original)

    def test_committed_contract_change_blocks_any_new_job(self):
        from test_intent_boundary import IntentBoundaryTests
        IntentBoundaryTests.prepare(self)
        run = self.runner()
        path = self.root / self.cfg['plan_contract']
        contract = json.loads(path.read_text())
        contract['tasks'][0]['title'] = 'Different owner request'
        path.write_text(json.dumps(contract))
        fixtures.git(self.root, 'add', self.cfg['plan_contract'])
        fixtures.git(self.root, 'commit', '-qm', 'new owner request')
        for kind in ('agent', 'verifying', 'publishing'):
            with self.subTest(kind=kind), self.assertRaisesRegex(self.d.Stop, 'Owner input changed'):
                run.job(kind, [sys.executable, '-c', 'pass'], 20)
        self.assertFalse((self.base / 'jobs').exists())

    def test_changed_owner_after_gate_is_not_accepted(self):
        owner = self.root / self.cfg['plan']
        sentinel = self.root.parent / 'must-not-run.txt'
        self.cfg['verify'] = [
            [sys.executable, '-c', 'from pathlib import Path; Path(%r).unlink()' % str(owner)],
            [sys.executable, '-c', 'from pathlib import Path; Path(%r).touch()' % str(sentinel)],
        ]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.d.run(self.cfg, self.base), 2)
        self.assertFalse(sentinel.exists())
        status = json.loads((self.base / 'status.json').read_text())
        self.assertEqual(status['state'], 'blocked')
        self.assertEqual(status['accepted_slices'], 0)
        self.assertIsNotNone(status['operation'])

    def test_other_owner_work_keeps_plan_valid(self):
        run = self.runner()
        (self.root / 'other.txt').write_text('other work')
        run.check_owner_baseline()
        fixtures.git(self.root, 'add', 'other.txt')
        fixtures.git(self.root, 'commit', '-qm', 'other work')
        run.check_owner_baseline()

    def test_resume_observes_active_job_and_blocks_unlaunched_job(self):
        import durable
        for phase in ('prepared', 'running'):
            with self.subTest(phase=phase):
                case = LiveOwnerTests()
                case.setUp()
                try:
                    run = case.runner()
                    command = [sys.executable, '-c', 'pass']
                    operation = {'id': 'resume-fixture', 'kind': 'verifying', 'before': run.head()}
                    run.state['operation'] = operation
                    durable.prepare(case.base / 'jobs' / operation['id'], command, run.work, 20)
                    (case.root / case.cfg['plan']).unlink()
                    with patch.object(durable, 'inspect', return_value={'state': phase}), \
                            patch.object(durable, 'wait', return_value={'state': 'passed', 'exit_code': 0}) as observe:
                        with self.assertRaisesRegex(case.d.Stop, 'Owner input changed'):
                            run.job('verifying', command, 20)
                        self.assertEqual(observe.call_count, 1 if phase == 'running' else 0)
                    self.assertEqual(run.state['operation'], operation)
                    self.assertEqual(run.state['accepted_slices'], 0)
                finally:
                    case.tearDown()


if __name__ == '__main__':
    unittest.main()
