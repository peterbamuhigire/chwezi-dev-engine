import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'durable.py'
spec = importlib.util.spec_from_file_location('durable_fixture', MODULE)
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)


class DurableTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_duplicate_launch_executes_once_and_terminal_is_reused(self):
        job = self.root / 'job'
        marker = self.root / 'count'
        d.prepare(job, [sys.executable, '-c',
                  f"from pathlib import Path; import time; p=Path({str(marker)!r}); p.write_text(p.read_text()+'x' if p.exists() else 'x'); time.sleep(.4)"], self.root, 10)
        processes = [d.launch(job), d.launch(job)]
        result = d.wait(job)
        for process in processes:
            process.wait(timeout=10)
        self.assertEqual(result['state'], 'passed')
        self.assertEqual(d.wait(job)['state'], 'passed')
        self.assertEqual(marker.read_text(), 'x')

    def test_observer_lease_during_start_does_not_drop_the_job(self):
        job = self.root / 'job'
        d.prepare(job, [sys.executable, '-c', 'pass'], self.root, 10)
        with d.Lease(job / 'job.mutex'):
            process = d.launch(job)
            time.sleep(.3)
            self.assertIsNone(process.poll())
        self.assertEqual(d.wait(job)['state'], 'passed')
        process.wait(timeout=10)

    def test_job_outlives_launcher_and_output_is_live(self):
        job = self.root / 'job'
        d.prepare(job, [sys.executable, '-u', '-c', "import time; print('started',flush=True); time.sleep(1); print('finished')"], self.root, 10)
        launcher = self.root / 'launcher.py'
        launcher.write_text(f"import sys; sys.path.insert(0,{str(MODULE.parent)!r}); import durable; durable.launch({str(job)!r})")
        subprocess.run([sys.executable, str(launcher)], check=True, timeout=10)
        until = time.time() + 10
        while 'started' not in d.tail(job / 'output.log') and time.time() < until:
            time.sleep(.05)
        self.assertIn('started', d.tail(job / 'output.log'))
        self.assertEqual(d.wait(job)['state'], 'passed')
        self.assertIn('finished', d.tail(job / 'output.log'))

    def test_timeout_is_not_pass_and_kills_descendants(self):
        job = self.root / 'job'
        marker = self.root / 'escaped'
        payload = f"import time; from pathlib import Path; time.sleep(2); Path({str(marker)!r}).write_text('escaped')"
        parent = f"import subprocess,sys,time; subprocess.Popen([sys.executable,'-c',{payload!r}]); time.sleep(30)"
        d.prepare(job, [sys.executable, '-c', parent], self.root, .5)
        self.assertEqual(d.wait(job)['state'], 'timed_out')
        time.sleep(2)
        self.assertFalse(marker.exists())

    def test_active_clock_excludes_host_sleep(self):
        # Aqar 26 Nov 2026: two hours of Modern Standby timed out a gate that was frozen, not slow.
        now = [1000.0]
        clock = d.ActiveClock(now=lambda: now[0])
        for step in (0.25, 0.25, 7200.0, 0.25, -5.0, 0.25):
            now[0] += step
            clock.tick()
        self.assertAlmostEqual(clock.active, 1.0)
        self.assertAlmostEqual(clock.suspended, 7200.0)

    def test_receipt_records_keep_awake_and_no_suspension_when_awake(self):
        job = self.root / 'job'
        d.prepare(job, [sys.executable, '-c', 'import time; time.sleep(.6)'], self.root, 20)
        result = d.wait(job)
        self.assertEqual(result['state'], 'passed')
        self.assertEqual(result.get('keep_awake'), os.name == 'nt')
        self.assertNotIn('suspended_seconds', result)

    def test_supervisor_crash_is_interrupted_not_replayed(self):
        job = self.root / 'job'
        marker = self.root / 'escaped'
        payload = f"import time; from pathlib import Path; time.sleep(2); Path({str(marker)!r}).write_text('escaped')"
        d.prepare(job, [sys.executable, '-c', payload], self.root, 20)
        process = d.launch(job)
        until = time.time() + 10
        while time.time() < until:
            status = d.inspect(job)
            if status.get('child_pid'):
                break
            time.sleep(.05)
        self.assertIn('child_pid', status)
        process.kill()
        process.wait(timeout=10)
        self.assertEqual(d.wait(job)['state'], 'interrupted')
        if os.name == 'nt':
            time.sleep(2)
            self.assertFalse(marker.exists())
        else:
            # POSIX process-group cleanup on supervisor SIGKILL is NOT guaranteed.
            import signal
            os.killpg(status['child_pid'], signal.SIGKILL)

    def test_cancel_persists_and_identity_cannot_change(self):
        job = self.root / 'job'
        command = [sys.executable, '-c', 'import time; time.sleep(20)']
        d.prepare(job, command, self.root, 30)
        with self.assertRaises(ValueError):
            d.prepare(job, command, self.root, 31)
        self.assertEqual(d.wait(job, cancel=lambda: True)['state'], 'cancelled')
        self.assertEqual(d.wait(job)['state'], 'cancelled')

    def test_partial_temp_file_does_not_replace_last_checkpoint(self):
        path = self.root / 'checkpoint.json'
        d.write_json(path, {'head': 'accepted'})
        (self.root / 'checkpoint.json.partial.tmp').write_text('{')
        self.assertEqual(d.read_json(path), {'head': 'accepted'})
        path.write_text('{')
        with self.assertRaises(ValueError):
            d.read_json(path)

    def test_receipt_from_another_job_is_rejected(self):
        job = self.root / 'job'
        spec = d.prepare(job, [sys.executable, '-c', 'pass'], self.root, 10)
        d.write_json(job / 'result.json', {'state': 'passed', 'digest': spec['digest'], 'job_id': 'other-job'})
        with self.assertRaisesRegex(ValueError, 'identity'):
            d.wait(job)

    def test_prepared_spec_tampering_is_rejected_before_launch(self):
        job = self.root / 'job'
        marker = self.root / 'ran'
        d.prepare(job, [sys.executable, '-c', f"from pathlib import Path; Path({str(marker)!r}).write_text('ran')"],
                  self.root, 10, 'original prompt', 'plan')
        saved = d.read_json(job / 'spec.json')
        for key, value in (('input', 'changed prompt'), ('timeout', 30), ('login_mode', 'inherit')):
            tampered = dict(saved)
            tampered[key] = value
            d.write_json(job / 'spec.json', tampered)
            with self.subTest(field=key), self.assertRaisesRegex(ValueError, 'specification'):
                d.wait(job)
            self.assertFalse(marker.exists())
        d.write_json(job / 'spec.json', saved)
        self.assertEqual(d.wait(job)['state'], 'passed')
        self.assertTrue(marker.exists())

    def test_terminal_receipt_cannot_validate_tampered_spec(self):
        job = self.root / 'job'
        saved = d.prepare(job, [sys.executable, '-c', 'pass'], self.root, 10,
                          'original prompt', 'plan')
        d.write_json(job / 'result.json', {'state': 'passed', 'digest': saved['digest'], 'job_id': job.name})
        tampered = dict(saved, timeout=20)
        d.write_json(job / 'spec.json', tampered)
        with self.assertRaisesRegex(ValueError, 'specification'):
            d.inspect(job)


    def test_boot_identity_on_macos_uses_boot_session_then_boot_time(self):
        from unittest.mock import patch
        def fake(outputs):
            def run(argv, **kwargs):
                out = outputs.get(argv[-1])
                return subprocess.CompletedProcess(argv, 0 if out else 1, stdout=out or '', stderr='')
            return run
        with patch.object(d.os, 'name', 'posix'), patch.object(d.sys, 'platform', 'darwin'):
            with patch.object(d.subprocess, 'run', fake({'kern.bootsessionuuid': 'ABC-123\n'})):
                self.assertEqual(d.boot_identity(), 'ABC-123')
            with patch.object(d.subprocess, 'run', fake({'kern.boottime': '{ sec = 1794434341, usec = 241329 } Thu Nov 12 00:59:01 2026\n'})):
                self.assertEqual(d.boot_identity(), 'boottime:1794434341.241329')
            with patch.object(d.subprocess, 'run', fake({})):
                self.assertIsNone(d.boot_identity())

    @unittest.skipUnless(sys.platform == 'darwin', 'macOS only')
    def test_boot_identity_is_known_and_stable_on_this_mac(self):
        first = d.boot_identity()
        self.assertTrue(first)
        self.assertEqual(first, d.boot_identity())


if __name__ == '__main__':
    unittest.main()
