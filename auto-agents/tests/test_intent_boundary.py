"""Exercise changed acceptance and ordinary progress through both host adapters."""
import contextlib
import io
import json
import unittest
from unittest.mock import patch

import test_driver as fixtures


class IntentBoundaryTests(unittest.TestCase):
    setUp = fixtures.DriverTests.setUp
    tearDown = fixtures.DriverTests.tearDown

    def prepare(self):
        self.cfg['plan_contract'] = 'auto-agents/tasks.json'
        data = {'schema_version': 1, 'tasks': [{
            'id': 'TASK-01', 'title': 'Required behavior', 'depends_on': [],
            'scope': ['src'], 'state': 'pending', 'evidence': [],
            'acceptance': [{'id': 'AC-01', 'description': 'Required observable behavior',
                            'evidence_oracle': 'Observe the required behavior'}]}]}
        path = self.root / self.cfg['plan_contract']
        path.write_text(json.dumps(data), encoding='utf8')
        fixtures.git(self.root, 'add', self.cfg['plan_contract'])
        fixtures.git(self.root, 'commit', '-qm', 'approve intent')
        return path, data

    def test_dirty_owner_contract_cannot_launch(self):
        path, data = self.prepare()
        data['tasks'][0]['scope'] = ['different']
        path.write_text(json.dumps(data), encoding='utf8')
        with self.assertRaisesRegex(self.d.Stop, 'Commit.*contract'):
            self.d.preflight(self.cfg)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.d.run(self.cfg, self.base), 2)
        self.assertFalse((self.base / 'jobs').exists())

    def test_executor_cannot_weaken_oracle_on_either_host(self):
        self.prepare()
        self.fake.write_text('''import json,pathlib,subprocess,sys
sys.stdin.read()
p=pathlib.Path('auto-agents/tasks.json'); d=json.loads(p.read_text())
d['tasks'][0]['acceptance'][0]['evidence_oracle']='Accept any output'
p.write_text(json.dumps(d))
subprocess.run(['git','add',str(p)],check=True)
subprocess.run(['git','commit','-qm','change oracle'],check=True)
''', encoding='utf8')
        for runner in ('codex', 'claude'):
            with self.subTest(runner=runner), contextlib.redirect_stdout(io.StringIO()):
                self.cfg['runner'] = runner
                self.assertEqual(self.d.run(self.cfg, self.base), 2)
                result = json.loads((self.base / 'status.json').read_text())
                self.assertIn('approved task definitions', result['reason'])
                self.assertEqual(result['accepted_slices'], 0)

    def test_progress_changes_do_not_change_intent(self):
        import copy
        import plan_contract
        _, data = self.prepare()
        before = plan_contract.definition_digest(data)
        candidate = copy.deepcopy(data)
        candidate['tasks'][0]['state'] = 'running'
        self.assertEqual(before, plan_contract.definition_digest(candidate))
        candidate['tasks'][0]['scope'] = ['unexpected']
        self.assertNotEqual(before, plan_contract.definition_digest(candidate))

    def test_new_recovery_worker_needs_valid_approved_context(self):
        import execution
        import plan_contract
        _, approved = self.prepare()
        run = execution.Execution(self.d, self.cfg, self.base, False)
        run.setup()
        run.state['reconcile'] = True
        path = run.work / self.cfg['plan_contract']
        changed = json.loads(json.dumps(approved))
        changed['tasks'][0]['scope'] = ['unapproved']
        for text in (json.dumps(changed), '{incomplete'):
            path.write_text(text, encoding='utf8')
            with patch.object(run, 'job') as launch:
                with self.assertRaises((self.d.Stop, plan_contract.ContractError)):
                    run.loop()
                launch.assert_not_called()
        approved['tasks'][0]['state'] = 'running'
        path.write_text(json.dumps(approved), encoding='utf8')
        with patch.object(run, 'job', side_effect=RuntimeError('valid recovery reached')):
            with self.assertRaisesRegex(RuntimeError, 'valid recovery reached'):
                run.loop()


if __name__ == '__main__':
    unittest.main()
