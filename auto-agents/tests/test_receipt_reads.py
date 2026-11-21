import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('receipt_runtime', Path(__file__).resolve().parents[1] / 'durable.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)


class ReceiptReads(unittest.TestCase):
    def test_transient_windows_denial_recovers_read(self):
        with patch.object(d, 'os', SimpleNamespace(name='nt')), patch.object(
                Path, 'read_text', side_effect=[PermissionError('busy'), '{"state":"passed"}']) as read, patch.object(d.time, 'sleep'):
            self.assertEqual(d.read_json('result.json'), {'state': 'passed'})
            self.assertEqual(read.call_count, 2)

    def test_persistent_denial_remains_failure(self):
        with patch.object(d, 'os', SimpleNamespace(name='nt')), patch.object(
                Path, 'read_text', side_effect=PermissionError('denied')) as read, patch.object(d.time, 'sleep') as sleep:
            with self.assertRaises(PermissionError):
                d.read_json('result.json')
            self.assertEqual(read.call_count, d.SHARING_RETRIES)
            self.assertEqual(sleep.call_count, d.SHARING_RETRIES - 1)
            # The whole budget stays bounded (about 8 s) but well above the 0.3 s that killed a live job.
            total = sum(d.sharing_delay(a) for a in range(d.SHARING_RETRIES - 1))
            self.assertTrue(5 < total < 10, total)

    def test_denied_heartbeat_does_not_fail_the_job(self):
        # Aqar 18 Nov 2026: one denied heartbeat replace failed the job and killed the agent.
        with patch.object(d, 'os', SimpleNamespace(name='nt')), patch.object(
                d, 'write_json', side_effect=PermissionError('[WinError 5] Access is denied')) as write:
            self.assertFalse(d.write_heartbeat('result.json', {'state': 'running'}))
            self.assertEqual(write.call_count, 1)
        with patch.object(d, 'write_json') as write:
            self.assertTrue(d.write_heartbeat('result.json', {'state': 'running'}))
            write.assert_called_once()

    def test_non_windows_heartbeat_denial_still_raises(self):
        with patch.object(d, 'os', SimpleNamespace(name='posix')), patch.object(
                d, 'write_json', side_effect=PermissionError('denied')):
            with self.assertRaises(PermissionError):
                d.write_heartbeat('result.json', {'state': 'running'})

    def test_worker_loop_uses_best_effort_heartbeat(self):
        import inspect
        source = inspect.getsource(d)
        loop = source[source.index('while child.poll() is None:'):source.index('code = child.wait()')]
        self.assertIn('write_heartbeat(', loop)
        self.assertNotIn('write_json(', loop)

    def test_non_windows_denial_is_not_retried(self):
        with patch.object(d, 'os', SimpleNamespace(name='posix')), patch.object(
                Path, 'read_text', side_effect=PermissionError('denied')) as read, patch.object(d.time, 'sleep') as sleep:
            with self.assertRaises(PermissionError):
                d.read_json('result.json')
            self.assertEqual(read.call_count, 1)
            sleep.assert_not_called()

    def test_missing_and_corrupt_receipts_fail_without_retry(self):
        for failure in (FileNotFoundError('missing'), json.JSONDecodeError('invalid', '!', 0)):
            with self.subTest(error=type(failure).__name__), patch.object(
                    Path, 'read_text', side_effect=failure) as read, patch.object(d.time, 'sleep') as sleep:
                with self.assertRaises(type(failure)):
                    d.read_json('result.json')
                self.assertEqual(read.call_count, 1)
                sleep.assert_not_called()

    @unittest.skipUnless(os.name == 'nt', 'Windows receipt contention')
    def test_receipt_retry_does_not_relaunch_completed_job(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            job = root / 'job'
            marker = root / 'effect.txt'
            d.prepare(job, [sys.executable, '-c',
                f'from pathlib import Path; p=Path({str(marker)!r}); p.write_text(p.read_text()+"x" if p.exists() else "x")'], root, 10)
            self.assertEqual(d.wait(job)['state'], 'passed')
            original = Path.read_text
            denied = []
            def read(path, *args, **kwargs):
                if path.name == 'result.json' and not denied:
                    denied.append(True)
                    raise PermissionError('simulated transient sharing denial')
                return original(path, *args, **kwargs)
            with patch.object(Path, 'read_text', read), patch.object(d, 'launch') as launch:
                self.assertEqual(d.wait(job)['state'], 'passed')
                launch.assert_not_called()
            self.assertEqual(denied, [True])
            self.assertEqual(marker.read_text(), 'x')
