"""The executor can report progress, but cannot redefine approved acceptance."""
import contextlib
import io
import json
import sys
import unittest
from unittest.mock import patch

import test_driver as fixtures


class ContractAuthorityTests(unittest.TestCase):
    setUp = fixtures.DriverTests.setUp
    tearDown = fixtures.DriverTests.tearDown

    def prepare_contract(self):
        self.cfg['plan_contract'] = 'auto-agents/contract.json'
        self.contract_path = self.root / self.cfg['plan_contract']
        self.contract_data = {'schema_version': 1, 'tasks': [{
            'id': 'TASK-01', 'title': 'Preserve the required output',
            'depends_on': [], 'scope': ['output.txt'], 'state': 'pending',
            'acceptance': [{'id': 'AC-01', 'description': 'Output contains required text',
                            'evidence_oracle': 'Reviewer observes the required text'}],
            'evidence': [],
        }]}
        self.contract_path.write_text(json.dumps(self.contract_data), encoding='utf8')
        fixtures.git(self.root, 'add', self.cfg['plan_contract'])
        fixtures.git(self.root, 'commit', '-qm', 'approved contract')

    def test_recovery_session_repairs_contract_left_invalid_by_interrupted_work(self):
        # Garage 18 Nov 2026: a session hit the usage limit after naming an unstaged evidence
        # file in the contract; every recovery then blocked before an agent could repair it.
        self.prepare_contract()
        seen = self.root.parent / 'recovery-prompt.txt'
        marker = self.root.parent / 'first-done'
        self.fake.write_text('''import json,pathlib,subprocess,sys
prompt=sys.stdin.read()
m=pathlib.Path(%r)
p=pathlib.Path('auto-agents/contract.json')
d=json.loads(p.read_text())
if not m.exists():
    m.write_text('x')
    pathlib.Path('ev.md').write_text('evidence')
    head=subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
    d['tasks'][0]['evidence']=[{'criterion_id':'AC-01','path':'ev.md','tested_revision':head,
        'sha256':'0'*64,'command':'check','result':'PASS'}]
    p.write_text(json.dumps(d))
    print("You've hit your usage limit")
    sys.exit(1)
pathlib.Path(%r).write_text(prompt)
d['tasks'][0]['evidence']=[]
p.write_text(json.dumps(d))
pathlib.Path('output.txt').write_text('required text')
subprocess.run(['git','add','-A'],check=True)
subprocess.run(['git','commit','-qm','recover slice'],check=True)
''' % (str(marker), str(seen)), encoding='utf8')
        self.cfg.update(max_sessions=2, usage_wait_seconds=0.01, max_rate_retries=2, recovery_policy='local-only')
        with contextlib.redirect_stdout(io.StringIO()):
            self.d.run(self.cfg, self.base)
        status = json.loads((self.base / 'status.json').read_text())
        self.assertNotEqual(status['state'], 'blocked', status.get('reason'))
        self.assertEqual(status['accepted_slices'], 1)
        self.assertIn('plan contract invalid', seen.read_text())
        self.assertIn('contract_feedback', (self.base / 'events.jsonl').read_text())

    def test_gate_contract_feedback_starts_a_repair_session(self):
        # Garage 19 Nov 2026: the gate turned an invalid sidecar into feedback, then the
        # pre-launch check blocked the very repair session that feedback asked for.
        self.prepare_contract()
        seen = self.root.parent / 'repair-prompt.txt'
        marker = self.root.parent / 'first-done'
        self.fake.write_text('''import json,pathlib,subprocess,sys
prompt=sys.stdin.read()
m=pathlib.Path(%r)
p=pathlib.Path('auto-agents/contract.json')
d=json.loads(p.read_text())
if not m.exists():
    m.write_text('x')
    pathlib.Path('ev.md').write_text('evidence')
    subprocess.run(['git','add','ev.md'],check=True)
    d['tasks'][0]['evidence']=[{'criterion_id':'AC-01','path':'ev.md','tested_revision':'0'*40,
        'sha256':'0'*64,'command':'check','result':'PASS'}]
    p.write_text(json.dumps(d))
    subprocess.run(['git','add',str(p)],check=True)
    subprocess.run(['git','commit','-qm','slice with a bad sidecar'],check=True)
    sys.exit(0)
pathlib.Path(%r).write_text(prompt)
d['tasks'][0]['evidence']=[]
p.write_text(json.dumps(d))
subprocess.run(['git','add',str(p)],check=True)
subprocess.run(['git','commit','-qm','repair sidecar'],check=True)
''' % (str(marker), str(seen)), encoding='utf8')
        self.cfg.update(max_sessions=2)
        with contextlib.redirect_stdout(io.StringIO()):
            self.d.run(self.cfg, self.base)
        status = json.loads((self.base / 'status.json').read_text())
        self.assertNotEqual(status['state'], 'blocked', status.get('reason'))
        self.assertTrue(seen.exists(), 'repair session never started')
        self.assertIn('Plan contract check failed', seen.read_text())
        self.assertEqual(status['accepted_slices'], 1)

    def test_recovery_still_blocks_changed_approved_definitions(self):
        self.prepare_contract()
        marker = self.root.parent / 'first-done'
        self.fake.write_text('''import json,pathlib,sys
sys.stdin.read()
m=pathlib.Path(%r)
if m.exists():
    sys.exit(0)
m.write_text('x')
p=pathlib.Path('auto-agents/contract.json')
d=json.loads(p.read_text())
d['tasks'][0]['acceptance'][0]['evidence_oracle']='Anything is acceptable'
p.write_text(json.dumps(d))
print("You've hit your usage limit")
sys.exit(1)
''' % str(marker), encoding='utf8')
        self.cfg.update(max_sessions=3, usage_wait_seconds=0.01, max_rate_retries=2, recovery_policy='local-only')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.d.run(self.cfg, self.base), 2)
        status = json.loads((self.base / 'status.json').read_text())
        self.assertIn('approved task definitions', status['reason'])

    def test_preflight_rejects_uncommitted_contract(self):
        self.prepare_contract()
        self.contract_data['tasks'][0]['scope'] = ['different.txt']
        self.contract_path.write_text(json.dumps(self.contract_data), encoding='utf8')
        with self.assertRaisesRegex(self.d.Stop, 'Commit.*contract'):
            self.d.preflight(self.cfg)

    def test_direct_run_rejects_uncommitted_contract(self):
        self.prepare_contract()
        self.contract_path.write_text('{}', encoding='utf8')
        with contextlib.redirect_stdout(io.StringIO()):
            result = self.d.run(self.cfg, self.base)
        self.assertEqual(result, 2)
        self.assertFalse((self.base / 'jobs').exists())

    def test_executor_cannot_replace_acceptance_for_either_host(self):
        self.prepare_contract()
        self.fake.write_text('''import json,pathlib,subprocess,sys
sys.stdin.read()
p=pathlib.Path('auto-agents/contract.json')
d=json.loads(p.read_text())
d['tasks'][0]['acceptance'][0]['evidence_oracle']='Anything is acceptable'
p.write_text(json.dumps(d))
subprocess.run(['git','add',str(p)],check=True)
subprocess.run(['git','commit','-qm','weaken acceptance'],check=True)
''', encoding='utf8')
        for runner in ('codex', 'claude'):
            with self.subTest(runner=runner), contextlib.redirect_stdout(io.StringIO()):
                self.cfg['runner'] = runner
                result = self.d.run(self.cfg, self.base)
                self.assertEqual(result, 2)
                status = json.loads((self.base / 'status.json').read_text())
                self.assertIn('approved task definitions', status['reason'])
                self.assertNotEqual(status['state'], 'done')

    def test_progress_and_evidence_can_complete_original_contract(self):
        self.prepare_contract()
        self.fake.write_text('''import hashlib,json,pathlib,subprocess,sys
sys.stdin.read()
p=pathlib.Path('auto-agents/contract.json')
d=json.loads(p.read_text())
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
e=pathlib.Path('evidence.txt'); e.write_text('Observed required output')
d['tasks'][0]['state']='complete'
d['tasks'][0]['evidence']=[{'criterion_id':'AC-01','path':'evidence.txt',
 'tested_revision':head,'sha256':hashlib.sha256(e.read_bytes()).hexdigest(),
 'command':'manual fixture observation','result':'PASS'}]
p.write_text(json.dumps(d))
plan=pathlib.Path('auto-agents/PLAN.md'); plan.write_text('STATUS: DONE\\n')
subprocess.run(['git','add',str(p),str(e),str(plan)],check=True)
subprocess.run(['git','commit','-qm','record completion'],check=True)
''', encoding='utf8')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.d.run(self.cfg, self.base), 0)
        self.assertEqual(json.loads((self.base / 'status.json').read_text())['state'], 'done')

    def test_changed_owner_contract_does_not_reinterpret_saved_job(self):
        import durable
        class Interrupted(BaseException):
            pass
        self.prepare_contract()
        with patch.object(durable, 'wait', side_effect=Interrupted):
            with self.assertRaises(Interrupted):
                self.d.run(self.cfg, self.base)
        journal = self.base / 'run-codex.json'
        saved = journal.read_bytes()
        self.contract_data['tasks'][0]['scope'] = ['new-scope.txt']
        self.contract_path.write_text(json.dumps(self.contract_data), encoding='utf8')
        fixtures.git(self.root, 'add', self.cfg['plan_contract'])
        fixtures.git(self.root, 'commit', '-qm', 'change owner intent')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.d.run(self.cfg, self.base, resume_only=True), 2)
        self.assertEqual(journal.read_bytes(), saved)

    def test_reordering_preserves_definition_but_changed_scope_does_not(self):
        import copy
        import plan_contract
        self.prepare_contract()
        first = self.contract_data['tasks'][0]
        second = copy.deepcopy(first)
        second.update(id='TASK-02', depends_on=['TASK-01'])
        second['acceptance'][0]['id'] = 'AC-02'
        self.contract_data['tasks'].append(second)
        original = plan_contract.definition_digest(self.contract_data)
        self.contract_data['tasks'].reverse()
        self.assertEqual(original, plan_contract.definition_digest(self.contract_data))
        first['scope'] = ['unexpected-path.txt']
        self.assertNotEqual(original, plan_contract.definition_digest(self.contract_data))

    def test_reconciliation_validates_definitions_before_next_worker(self):
        import copy
        import execution
        import plan_contract
        self.prepare_contract()
        runner = execution.Execution(self.d, self.cfg, self.base, False)
        runner.setup()
        runner.state['reconcile'] = True
        path = runner.work / self.cfg['plan_contract']
        weakened = copy.deepcopy(self.contract_data)
        weakened['tasks'][0]['acceptance'][0]['evidence_oracle'] = 'Anything'
        for data in (json.dumps(weakened), '{broken'):
            with self.subTest(data=data):
                path.write_text(data, encoding='utf8')
                with patch.object(runner, 'job') as job:
                    with self.assertRaises((self.d.Stop, plan_contract.ContractError)):
                        runner.loop()
                    job.assert_not_called()
        progress = copy.deepcopy(self.contract_data)
        progress['tasks'][0]['state'] = 'running'
        path.write_text(json.dumps(progress), encoding='utf8')
        with patch.object(runner, 'job', side_effect=RuntimeError('worker reached')):
            with self.assertRaisesRegex(RuntimeError, 'worker reached'):
                runner.loop()

    def test_live_owner_plan_change_blocks_next_worker_for_both_hosts(self):
        import execution
        for host in ('codex', 'claude'):
            for committed in (False, True):
                with self.subTest(host=host, committed=committed):
                    fixture = fixtures.DriverTests()
                    fixture.setUp()
                    try:
                        fixture.cfg['runner'] = host
                        fixture.base.mkdir(parents=True)
                        runner = execution.Execution(fixture.d, fixture.cfg, fixture.base, False)
                        runner.setup()
                        (fixture.root / fixture.cfg['plan']).write_text('STATUS: BLOCKED - owner withdrew task\n')
                        if committed:
                            fixtures.git(fixture.root, 'add', fixture.cfg['plan'])
                            fixtures.git(fixture.root, 'commit', '-qm', 'withdraw task')
                        with patch.object(runner, 'job') as job:
                            with self.assertRaisesRegex(fixture.d.Stop, 'Owner plan or contract changed'):
                                runner.loop()
                            job.assert_not_called()
                    finally:
                        fixture.tearDown()

    def test_live_owner_contract_change_blocks_new_job(self):
        import execution
        self.prepare_contract()
        self.base.mkdir(parents=True)
        runner = execution.Execution(self.d, self.cfg, self.base, False)
        runner.setup()
        self.contract_data['tasks'][0]['scope'] = ['changed.txt']
        self.contract_path.write_text(json.dumps(self.contract_data), encoding='utf8')
        with self.assertRaisesRegex(self.d.Stop, 'Owner plan or contract changed'):
            runner.job('agent', runner.agent, 20, 'fixture')
        self.assertFalse((self.base / 'jobs').exists())

    def test_owner_change_during_gate_prevents_next_gate_and_acceptance(self):
        marker = self.root.parent / 'second-gate.txt'
        owner_plan = self.root / self.cfg['plan']
        self.cfg['verify'] = [
            [sys.executable, '-c', 'from pathlib import Path; Path(%r).write_text("STATUS: BLOCKED - changed intent\\n")' % str(owner_plan)],
            [sys.executable, '-c', 'from pathlib import Path; Path(%r).write_text("unexpected")' % str(marker)],
        ]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.d.run(self.cfg, self.base), 2)
        self.assertFalse(marker.exists())
        status = json.loads((self.base / 'status.json').read_text())
        self.assertIn('Owner plan or contract changed', status['reason'])
        self.assertEqual(status['accepted_slices'], 0)
        self.assertIsNotNone(status['operation'])
        checkpoint = json.loads((self.base / 'verified-codex.json').read_text())
        self.assertNotIn('at', checkpoint)

    def test_unrelated_owner_changes_do_not_block_progress(self):
        import execution
        self.base.mkdir(parents=True)
        runner = execution.Execution(self.d, self.cfg, self.base, False)
        runner.setup()
        (self.root / 'unrelated.txt').write_text('owner work')
        runner.owner_intent()
        fixtures.git(self.root, 'add', 'unrelated.txt')
        fixtures.git(self.root, 'commit', '-qm', 'unrelated owner work')
        runner.owner_intent()

    def test_saved_job_reconciles_active_receipt_but_never_launches_prepared_drift(self):
        import durable
        import execution
        for job_state in ('prepared', 'running'):
            with self.subTest(job_state=job_state):
                fixture = fixtures.DriverTests()
                fixture.setUp()
                try:
                    fixture.base.mkdir(parents=True)
                    runner = execution.Execution(fixture.d, fixture.cfg, fixture.base, False)
                    runner.setup()
                    op = {'kind': 'verifying', 'id': 'fixture-job', 'before': runner.head()}
                    runner.state['operation'] = op
                    command = [sys.executable, '-c', 'pass']
                    folder = fixture.base / 'jobs' / op['id']
                    durable.prepare(folder, command, runner.work, 20)
                    (fixture.root / fixture.cfg['plan']).write_text('STATUS: BLOCKED - new intent\n')
                    receipt = {'state': 'passed', 'exit_code': 0}
                    with patch.object(durable, 'inspect', return_value={'state': job_state}), \
                            patch.object(durable, 'wait', return_value=receipt) as wait:
                        with self.assertRaisesRegex(fixture.d.Stop, 'Owner plan or contract changed'):
                            runner.job('verifying', command, 20)
                        self.assertEqual(wait.call_count, int(job_state == 'running'))
                    self.assertEqual(runner.state['operation'], op)
                    self.assertEqual(runner.state['accepted_slices'], 0)
                finally:
                    fixture.tearDown()


if __name__ == '__main__':
    unittest.main()
