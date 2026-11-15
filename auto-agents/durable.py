#!/usr/bin/env python3
"""Local job supervisor. State is evidence, never authority to replay an action."""
import argparse
import ctypes
import hashlib
import json
import math
import os
import re
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import time
import uuid


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    with temp.open('w', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    # Windows readers/AV may briefly deny replacement while holding the old file.
    # Retry only this local replace, never the operation whose receipt it records.
    for attempt in range(8):
        try:
            os.replace(temp, path)
            break
        except PermissionError:
            if os.name != 'nt' or attempt == 7:
                raise
            time.sleep(0.01 * (attempt + 1))
    if os.name != 'nt':
        fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def read_json(path):
    # Corruption is an explicit failure, not an empty/finished run.
    return json.loads(Path(path).read_text(encoding='utf-8'))


class Busy(RuntimeError):
    pass


class Lease:
    """Kernel-owned lock: automatically released on process death, no PID stealing.

    Keep the lock file permanently. Unlinking a locked file permits a second inode
    and therefore a second owner on POSIX. A separate marker supports old updaters.
    """
    def __init__(self, path):
        self.path = Path(path)
        self.file = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.file = self.path.open('a+b')
        if self.path.stat().st_size == 0:
            self.file.write(b'0')
            self.file.flush()
        self.file.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(self.file.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            self.file.close()
            self.file = None
            raise Busy(str(self.path)) from error
        return self

    def __exit__(self, *_):
        if self.file is not None:
            if os.name == 'nt':
                import msvcrt
                self.file.seek(0)
                msvcrt.locking(self.file.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.file, fcntl.LOCK_UN)
            self.file.close()
            self.file = None


def held(path):
    try:
        with Lease(path):
            return False
    except Busy:
        return True


def detached(argv, cwd, log):
    kwargs = {'start_new_session': True} if os.name != 'nt' else {
        'creationflags': subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
        'startupinfo': subprocess.STARTUPINFO(),
    }
    if os.name == 'nt':
        kwargs['startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW
        kwargs['startupinfo'].wShowWindow = subprocess.SW_HIDE
    with Path(log).open('ab', buffering=0) as output:
        return subprocess.Popen(argv, cwd=cwd, stdin=subprocess.DEVNULL,
                                stdout=output, stderr=subprocess.STDOUT,
                                close_fds=True, **kwargs)


def windows_job():
    """Put this dedicated supervisor in a kill-on-close job BEFORE spawning work.

    The non-inherited handle lives until this process exits. Descendants cannot
    break away. If nested assignment is unavailable, fail before executing work.
    """
    from ctypes import wintypes as w
    class Basic(ctypes.Structure):
        _fields_ = [('PerProcessUserTimeLimit', ctypes.c_longlong),
                    ('PerJobUserTimeLimit', ctypes.c_longlong), ('LimitFlags', w.DWORD),
                    ('MinimumWorkingSetSize', ctypes.c_size_t),
                    ('MaximumWorkingSetSize', ctypes.c_size_t), ('ActiveProcessLimit', w.DWORD),
                    ('Affinity', ctypes.c_size_t), ('PriorityClass', w.DWORD),
                    ('SchedulingClass', w.DWORD)]
    class IO(ctypes.Structure):
        _fields_ = [(name, ctypes.c_ulonglong) for name in
                    ('ReadOperationCount', 'WriteOperationCount', 'OtherOperationCount',
                     'ReadTransferCount', 'WriteTransferCount', 'OtherTransferCount')]
    class Extended(ctypes.Structure):
        _fields_ = [('BasicLimitInformation', Basic), ('IoInfo', IO),
                    ('ProcessMemoryLimit', ctypes.c_size_t), ('JobMemoryLimit', ctypes.c_size_t),
                    ('PeakProcessMemoryUsed', ctypes.c_size_t), ('PeakJobMemoryUsed', ctypes.c_size_t)]
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, w.LPCWSTR]
    kernel.CreateJobObjectW.restype = w.HANDLE
    kernel.SetInformationJobObject.argtypes = [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD]
    kernel.SetInformationJobObject.restype = w.BOOL
    kernel.GetCurrentProcess.restype = w.HANDLE
    kernel.AssignProcessToJobObject.argtypes = [w.HANDLE, w.HANDLE]
    kernel.AssignProcessToJobObject.restype = w.BOOL
    handle = kernel.CreateJobObjectW(None, None)
    info = Extended()
    info.BasicLimitInformation.LimitFlags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    if not handle or not kernel.SetInformationJobObject(handle, 9, ctypes.byref(info), ctypes.sizeof(info)):
        raise ctypes.WinError(ctypes.get_last_error())
    if not kernel.AssignProcessToJobObject(handle, kernel.GetCurrentProcess()):
        raise ctypes.WinError(ctypes.get_last_error())
    return handle  # Deliberately not closed until supervisor process exit.


def tail(path, limit=4000):
    try:
        with Path(path).open('rb') as stream:
            stream.seek(0, os.SEEK_END)
            stream.seek(max(0, stream.tell() - limit))
            return stream.read(limit).decode('utf-8', errors='replace')
    except FileNotFoundError:
        return ''


def boot_identity():
    """Evidence for restart reconciliation, not a claim about service/data freshness."""
    if os.name == 'nt':
        try:
            result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                '(Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToUniversalTime().ToString("o")'],
                capture_output=True, text=True, timeout=15, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass
    elif sys.platform == 'darwin' or 'bsd' in sys.platform:
        # macOS: kern.bootsessionuuid is unique per boot; BSDs (and older macOS) fall back to kern.boottime.
        for key in ('kern.bootsessionuuid', 'kern.boottime'):
            try:
                result = subprocess.run(['sysctl', '-n', key], capture_output=True, text=True, timeout=15)
            except (OSError, subprocess.TimeoutExpired):
                continue
            value = result.stdout.strip() if result.returncode == 0 else ''
            if not value:
                continue
            if key == 'kern.bootsessionuuid':
                return value
            seconds = re.search(r'sec\s*=\s*(\d+)', value)
            micros = re.search(r'usec\s*=\s*(\d+)', value)
            if seconds:
                return f"boottime:{seconds.group(1)}.{micros.group(1) if micros else '0'}"
    else:
        try:
            return Path('/proc/sys/kernel/random/boot_id').read_text().strip()
        except OSError:
            pass
    return None


def prepare(folder, argv, cwd, timeout, input_text=None, login_mode='inherit'):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    spec = {'job_id': folder.name, 'argv': argv, 'cwd': str(Path(cwd).resolve()), 'timeout': timeout,
            'input': input_text, 'login_mode': login_mode}
    spec['digest'] = spec_digest(spec)
    path = folder / 'spec.json'
    if path.exists():
        if read_spec(folder) != spec:
            raise ValueError('Job identity reused with different command, input or configuration')
    else:
        write_json(path, spec)
    return spec


def spec_digest(spec):
    """Hash every immutable execution field, excluding only the stored digest."""
    payload = {key: value for key, value in spec.items() if key != 'digest'}
    encoded = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def read_spec(folder):
    """Load and validate the job identity before trusting it for execution."""
    folder = Path(folder)
    spec = read_json(folder / 'spec.json')
    expected = {'job_id', 'argv', 'cwd', 'timeout', 'input', 'login_mode', 'digest'}
    if not isinstance(spec, dict) or set(spec) != expected:
        raise ValueError('Job specification has an invalid shape: ' + str(folder))
    if (spec['job_id'] != folder.name or not isinstance(spec['argv'], list) or
            not spec['argv'] or not isinstance(spec['argv'][0], str) or not spec['argv'][0] or
            not all(isinstance(arg, str) for arg in spec['argv']) or
            not isinstance(spec['cwd'], str) or not Path(spec['cwd']).is_absolute() or
            type(spec['timeout']) not in (int, float) or not math.isfinite(spec['timeout']) or
            spec['timeout'] <= 0 or (spec['input'] is not None and not isinstance(spec['input'], str)) or
            spec['login_mode'] not in ('inherit', 'plan') or not isinstance(spec['digest'], str) or
            spec['digest'] != spec_digest(spec)):
        raise ValueError('Job specification identity or fields are invalid: ' + str(folder))
    return spec


def launch(folder):
    folder = Path(folder).resolve()
    return detached([sys.executable, '-B', str(Path(__file__).resolve()), 'worker', str(folder)],
                    folder, folder / 'supervisor.log')


def inspect(folder):
    folder = Path(folder)
    spec = read_spec(folder)
    def snapshot():
        return read_json(folder / 'result.json') if (folder / 'result.json').exists() else {'state': 'prepared'}
    try:
        with Lease(folder / 'job.mutex'):
            status = snapshot()
            active = False
    except Busy:
        status = snapshot()
        active = True
    if status['state'] != 'prepared':
        if status.get('digest') != spec.get('digest') or status.get('job_id') != folder.name:
            raise ValueError('Job receipt identity does not match its specification: ' + str(folder))
    status['supervisor_active'] = active
    if not active and status['state'] == 'running':
        status = {**status, 'state': 'interrupted', 'reason': 'Supervisor exited without a terminal receipt; reconcile before replay.'}
    status['log'] = str(folder / 'output.log')
    if (folder / 'output.log').exists():
        status['output_bytes'] = (folder / 'output.log').stat().st_size
        status['last_output_at'] = (folder / 'output.log').stat().st_mtime
    return status


def wait(folder, observe=None, cancel=None, poll=0.25):
    """Reattach to a durable job; callers may disappear without terminating it."""
    folder = Path(folder)
    # A prepared job has no side effects until the worker holds its kernel lease.
    # Concurrent launches race on that lease and re-read the terminal receipt.
    status = inspect(folder)
    process = launch(folder) if status['state'] == 'prepared' else None
    while True:
        status = inspect(folder)
        if observe:
            observe(status)
        if cancel and cancel():
            (folder / 'CANCEL').touch()
        if status['state'] in ('passed', 'failed', 'cancelled', 'timed_out', 'interrupted'):
            # Wait for supervisor exit so the Windows job has killed any surviving children.
            if not status['supervisor_active']:
                if process is not None:
                    process.wait(timeout=10)
                return status
        if process is not None and process.poll() is not None and status['state'] == 'prepared':
            raise RuntimeError('Supervisor could not start; inspect ' + str(folder / 'supervisor.log'))
        time.sleep(poll)


def worker(folder):
    folder = Path(folder)
    # An inspector briefly holds the same lease to read a consistent terminal
    # snapshot. Do not mistake that reader for an already-started supervisor.
    until = time.monotonic() + 5
    while True:
        try:
            lease = Lease(folder / 'job.mutex').__enter__()
            break
        except Busy:
            if (folder / 'result.json').exists():
                return 0
            if time.monotonic() >= until:
                return 2
            time.sleep(.05)
    # Hold lease through process exit: terminal receipt alone is insufficient while
    # the Windows job may still have live descendants.
    try:
        if (folder / 'result.json').exists():
            return 0  # Never replay an interrupted/finished job under the same identity.
        spec = read_spec(folder)
        started = time.time()
        state = {'state': 'running', 'job_id': folder.name, 'started_at': started, 'heartbeat_at': started,
                 'pid': os.getpid(), 'digest': spec['digest']}
        write_json(folder / 'result.json', state)
        if (folder / 'CANCEL').exists():
            state.update(state='cancelled', exit_code=None, finished_at=time.time())
            write_json(folder / 'result.json', state)
            return 0
        job_handle = windows_job() if os.name == 'nt' else None
        env = os.environ.copy()
        if spec['login_mode'] == 'plan':
            for key in ('OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN'):
                env.pop(key, None)
        # File stdin avoids pipe deadlocks and survives the launching client's exit.
        input_path = folder / 'stdin.txt'
        input_path.write_text(spec.get('input') or '', encoding='utf-8')
        with input_path.open('rb') as source, (folder / 'output.log').open('ab', buffering=0) as output:
            command = list(spec['argv'])
            command[0] = shutil.which(command[0]) or command[0]
            child = subprocess.Popen(command, cwd=spec['cwd'], stdin=source,
                                     stdout=output, stderr=subprocess.STDOUT, env=env,
                                     start_new_session=(os.name != 'nt'))
            state['child_pid'] = child.pid
            terminal = None
            while child.poll() is None:
                if (folder / 'CANCEL').exists():
                    terminal = 'cancelled'
                elif time.time() - started >= spec['timeout']:
                    terminal = 'timed_out'
                if terminal:
                    child.kill()
                    break
                state['heartbeat_at'] = time.time()
                write_json(folder / 'result.json', state)
                time.sleep(0.25)
            code = child.wait()
            if os.name != 'nt':
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            state.update(state=terminal or ('passed' if code == 0 else 'failed'), exit_code=code,
                         finished_at=time.time(), heartbeat_at=time.time())
            write_json(folder / 'result.json', state)
        return 0
    except Exception as error:
        write_json(folder / 'result.json', {'state': 'failed', 'exit_code': None,
                   'job_id': folder.name, 'digest': locals().get('spec', {}).get('digest'),
                   'reason': str(error), 'finished_at': time.time()})
        return 2
    finally:
        # Do not release early: on Windows the OS closes the job and lock handles
        # together when this standalone process exits.
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['worker', 'status'])
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    if args.action == 'worker':
        sys.exit(worker(args.folder))
    print(json.dumps(inspect(args.folder), indent=2))
