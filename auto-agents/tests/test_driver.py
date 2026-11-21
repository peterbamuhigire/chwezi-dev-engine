import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

DRIVER = Path(__file__).resolve().parents[1] / 'driver.py'

def git(root, *args):
    return subprocess.run(['git',*args],cwd=root,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True).stdout.strip()

class DriverTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)/'repo'; self.root.mkdir()
        git(self.root,'init','-q'); git(self.root,'config','user.email','fixture@example.test'); git(self.root,'config','user.name','Fixture')
        (self.root/'auto-agents').mkdir()
        (self.root/'auto-agents'/'PLAN.md').write_text('# Plan\n',encoding='utf8')
        git(self.root,'add','.'); git(self.root,'commit','-qm','initial')
        spec=importlib.util.spec_from_file_location('driver_fixture',DRIVER)
        self.d=importlib.util.module_from_spec(spec); spec.loader.exec_module(self.d)
        self.d.ROOT=self.root
        self.base=self.root/'.git'/'auto-agents'
        self.fake=self.root.parent/'fake.py'
        self.fake.write_text('''import pathlib,subprocess,sys\nsys.stdin.read()\np=pathlib.Path("auto-agents/PLAN.md")\np.write_text("STATUS: DONE\\n",encoding="utf8")\nsubprocess.run(["git","add",str(p)],check=True)\nsubprocess.run(["git","commit","-qm","finish slice"],check=True)\n''',encoding='utf8')
        self.d.agent_command=lambda cfg:[sys.executable,str(self.fake)]
        self.cfg={'runner':'codex','plan':'auto-agents/PLAN.md','verify':[[sys.executable,'-c','pass']],'session_timeout_seconds':20,'max_hours':1,'max_sessions':2,'publish':False,'remote':'origin','target_branch':'main'}
    def tearDown(self):
        # A failed assertion must not leave a disposable supervisor running while
        # TemporaryDirectory removes its files. Never start prepared jobs here.
        import durable
        jobs=self.base/'jobs'
        if jobs.exists():
            assert jobs.resolve().is_relative_to(Path(self.tmp.name).resolve())
            for job in jobs.iterdir():
                if job.is_dir() and durable.held(job/'job.mutex'):
                    (job/'CANCEL').touch()
                    until=time.monotonic()+10
                    while durable.held(job/'job.mutex') and time.monotonic()<until:
                        time.sleep(.05)
        self.tmp.cleanup()
    def crlf_fixture(self):
        # Store this one file byte-for-byte (no EOL conversion) whatever core.autocrlf says.
        (self.root/'.gitattributes').write_text('menu.php -text\n',encoding='utf8')
        (self.root/'menu.php').write_bytes(b'<?php\r\necho 1;\r\n')
        git(self.root,'add','.gitattributes','menu.php'); git(self.root,'commit','-qm','crlf file')
    def test_line_ending_only_leftover_is_restored_not_blocking(self):
        # Garage 18 Nov 2026: "agent left uncommitted changes" while git diff was empty.
        self.crlf_fixture()
        self.fake.write_text('''import pathlib,subprocess,sys\nsys.stdin.read()\np=pathlib.Path("auto-agents/PLAN.md")\np.write_text("STATUS: DONE\\n",encoding="utf8")\nsubprocess.run(["git","add",str(p)],check=True)\nsubprocess.run(["git","commit","-qm","finish slice"],check=True)\npathlib.Path("menu.php").write_bytes(b"<?php\\necho 1;\\n")\n''',encoding='utf8')
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        self.assertEqual(json.loads((self.base/'status.json').read_text())['state'],'done')
        self.assertIn('eol_restored',(self.base/'events.jsonl').read_text())
        self.assertEqual((self.base/'worktrees'/'codex'/'menu.php').read_bytes(),b'<?php\r\necho 1;\r\n')
    def test_ansi_byte_in_plan_does_not_block(self):
        # Garage 19 Nov 2026: an agent rewrote PLAN.md via PowerShell 5.1 (ANSI); byte 0x97 blocked the run.
        self.fake.write_text('''import pathlib,subprocess,sys\nsys.stdin.read()\np=pathlib.Path("auto-agents/PLAN.md")\np.write_bytes(b"STATUS: DONE\\n| step \\x97 complete |\\n")\nsubprocess.run(["git","add",str(p)],check=True)\nsubprocess.run(["git","commit","-qm","finish slice"],check=True)\n''',encoding='utf8')
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        self.assertEqual(json.loads((self.base/'status.json').read_text())['state'],'done')
    def capture_prompt(self, cfg):
        seen=self.root.parent/'prompt.txt'
        self.fake.write_text(f'''import pathlib,subprocess,sys\npathlib.Path({str(seen)!r}).write_text(sys.stdin.read(),encoding="utf8")\np=pathlib.Path("auto-agents/PLAN.md")\np.write_text("STATUS: DONE\\n",encoding="utf8")\nsubprocess.run(["git","add",str(p)],check=True)\nsubprocess.run(["git","commit","-qm","finish slice"],check=True)\n''',encoding='utf8')
        self.assertEqual(self.d.run(cfg,self.base),0)
        return seen.read_text(encoding='utf8')
    def test_prompt_points_to_on_demand_skill_finder(self):
        # 19 Nov 2026 Kaizen: runner sessions no longer preload ~285 plugin skill descriptions.
        import execution
        self.assertIn(str(Path(execution.__file__).resolve().parent/'find_skill.py'),self.capture_prompt(self.cfg))
    def test_preload_mode_omits_skill_finder(self):
        self.assertNotIn('find_skill.py',self.capture_prompt({**self.cfg,'skills':'preload'}))
    def test_research_status_reports_missing_and_present_clone(self):
        # 20 Nov 2026: check tells whether this PC contributes to the private efficiency study. Never blocks.
        old=os.environ.get('CHWEZI_RESEARCH_REPO')
        try:
            os.environ['CHWEZI_RESEARCH_REPO']=str(self.root.parent/'no-such-repo')
            real=self.d.ROOT; self.d.ROOT=self.root.parent/'isolated'/'repo'
            try:
                if not (Path(r'C:\wamp64\www')/self.d.RESEARCH_REPO/'collect'/'sync.py').is_file():
                    self.assertIn('not set up',self.d.research_status())
                repo=self.root.parent/'research'; (repo/'collect').mkdir(parents=True); (repo/'collect'/'sync.py').write_text('',encoding='utf8')
                os.environ['CHWEZI_RESEARCH_REPO']=str(repo)
                line=self.d.research_status()
                self.assertTrue(line.startswith('RESEARCH: '+str(repo)),line)
                self.assertIn('remote',line)
            finally:
                self.d.ROOT=real
        finally:
            if old is None: os.environ.pop('CHWEZI_RESEARCH_REPO',None)
            else: os.environ['CHWEZI_RESEARCH_REPO']=old
    def test_skills_mode_is_validated(self):
        (self.root/'auto-agents'/'config.json').write_text(json.dumps({**self.cfg,'skills':'all'}),encoding='utf8')
        self.d.CFG=self.root/'auto-agents'/'config.json'
        with self.assertRaisesRegex(self.d.Stop,'skills must be'): self.d.config()
    def test_subagents_mode_is_validated(self):
        (self.root/'auto-agents'/'config.json').write_text(json.dumps({**self.cfg,'subagents':'cheap'}),encoding='utf8')
        self.d.CFG=self.root/'auto-agents'/'config.json'
        with self.assertRaisesRegex(self.d.Stop,'subagents must be'): self.d.config()
    def test_economy_subagent_file_pins_read_only_explore_to_haiku(self):
        # 20 Nov 2026 Kaizen (model class M): file discovery runs on Haiku, never on the session's model.
        args=self.d.subagent_args({**self.cfg,'runner':'claude'},write=True)
        self.assertEqual(args[0],'--agents')
        spec=json.loads(Path(args[1]).read_text(encoding='utf8'))
        self.assertEqual(list(spec),['Explore'])
        self.assertEqual(spec['Explore']['model'],'haiku')
        self.assertEqual(spec['Explore']['tools'],['Read','Grep','Glob'])
        self.assertEqual(self.d.subagent_args({**self.cfg,'runner':'codex'},write=True),[])
        self.assertEqual(self.d.subagent_args({**self.cfg,'runner':'claude','subagents':'inherit'},write=True),[])
    EXPLORE_LINE='delegate it to the Explore subagent'
    def test_prompt_mentions_explore_for_claude_economy(self):
        self.assertIn(self.EXPLORE_LINE,self.capture_prompt({**self.cfg,'runner':'claude'}))
    def test_prompt_omits_explore_when_subagents_inherit(self):
        self.assertNotIn(self.EXPLORE_LINE,self.capture_prompt({**self.cfg,'runner':'claude','subagents':'inherit'}))
    def test_prompt_omits_explore_for_codex(self):
        self.assertNotIn(self.EXPLORE_LINE,self.capture_prompt({**self.cfg,'runner':'codex'}))
    def test_on_demand_profiles_disable_enabled_plugins(self):
        import tomllib
        home=self.root.parent/'home'; (home/'.claude').mkdir(parents=True); (home/'.codex').mkdir()
        (home/'.claude'/'settings.json').write_text(json.dumps({'enabledPlugins':{'big@m':True,'off@m':False,'proj@m':True}}),encoding='utf8')
        (self.root/'.claude').mkdir(); (self.root/'.claude'/'settings.json').write_text(json.dumps({'enabledPlugins':{'proj@m':False,'extra@m':True}}),encoding='utf8')
        (home/'.codex'/'config.toml').write_text('[plugins."a@x"]\nenabled = true\n\n[plugins."b@x"]\nenabled = false\n',encoding='utf8')
        old=os.environ.get('CODEX_HOME'); os.environ['CODEX_HOME']=str(home/'.codex')
        real_home=Path.home
        try:
            Path.home=staticmethod(lambda: home)
            args=self.d.skill_args({**self.cfg,'runner':'claude'},write=True)
            self.assertEqual(args[0],'--settings')
            self.assertEqual(json.loads(Path(args[1]).read_text(encoding='utf8')),{'enabledPlugins':{'big@m':False,'extra@m':False}})
            self.assertEqual(self.d.skill_args(self.cfg,write=True),['-p',self.d.CODEX_SKILL_PROFILE])
            profile=tomllib.loads((home/'.codex'/(self.d.CODEX_SKILL_PROFILE+'.config.toml')).read_text(encoding='utf8'))
            self.assertEqual(profile,{'plugins':{'a@x':{'enabled':False}}})
            self.assertEqual(self.d.skill_args({**self.cfg,'skills':'preload'},write=True),[])
        finally:
            Path.home=real_home
            if old is None: os.environ.pop('CODEX_HOME',None)
            else: os.environ['CODEX_HOME']=old
    def test_prompt_asks_for_utf8_files(self):
        import execution
        self.assertIn('Write text files as UTF-8', execution.Execution.prompt.__code__.co_consts.__str__())
    def test_real_leftover_change_still_blocks(self):
        self.crlf_fixture()
        self.fake.write_text('''import pathlib,subprocess,sys\nsys.stdin.read()\np=pathlib.Path("auto-agents/PLAN.md")\np.write_text("STATUS: DONE\\n",encoding="utf8")\nsubprocess.run(["git","add",str(p)],check=True)\nsubprocess.run(["git","commit","-qm","finish slice"],check=True)\npathlib.Path("menu.php").write_bytes(b"<?php\\necho 2;\\n")\n''',encoding='utf8')
        self.assertEqual(self.d.run(self.cfg,self.base),2)
        s=json.loads((self.base/'status.json').read_text())
        self.assertEqual(s['state'],'blocked'); self.assertIn('uncommitted',s['reason'])
        self.assertNotIn('eol_restored',(self.base/'events.jsonl').read_text())
    def test_accepts_committed_slice_and_completes(self):
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        self.assertEqual(json.loads((self.base/'status.json').read_text())['state'],'done')
        self.assertEqual((self.root/'auto-agents'/'PLAN.md').read_text(),'# Plan\n')
    def test_failed_gate_blocks_and_does_not_publish(self):
        self.cfg['verify']=[[sys.executable,'-c','import sys;sys.exit(7)']]
        self.cfg['max_sessions']=1
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        s=json.loads((self.base/'status.json').read_text())
        self.assertEqual(s['state'],'stopped')
        events=(self.base/'events.jsonl').read_text(); self.assertNotIn('published',events)
        self.cfg['verify']=[[sys.executable,'-c','pass']]
        self.assertEqual(self.d.run(self.cfg,self.base),2)
        s=json.loads((self.base/'status.json').read_text())
        self.assertNotEqual(s['state'],'done')
    def test_failed_gate_can_be_repaired_in_next_session(self):
        self.fake.write_text('''import pathlib,subprocess,sys\nsys.stdin.read()\np=pathlib.Path("auto-agents/PLAN.md")\np.write_text("STATUS: DONE\\n",encoding="utf8")\nf=pathlib.Path("fixed.txt")\nif f.exists(): f.write_text("yes",encoding="utf8")\nelse: f.write_text("no",encoding="utf8")\nsubprocess.run(["git","add",str(p),str(f)],check=True)\nsubprocess.run(["git","commit","-qm","slice or repair"],check=True)\n''',encoding='utf8')
        self.cfg['max_sessions']=3
        self.cfg['verify']=[[sys.executable,'-c','from pathlib import Path; import sys; sys.exit(0 if Path("fixed.txt").read_text()=="yes" else 1)']]
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        s=json.loads((self.base/'status.json').read_text())
        self.assertEqual(s['state'],'done')
        self.assertFalse((self.base/'pending-codex.json').exists())
    def test_stop_and_lock_block_execution(self):
        self.base.mkdir(parents=True); (self.base/'STOP').write_text('stop')
        self.assertEqual(self.d.run(self.cfg,self.base),2)
        self.assertFalse((self.base/'run.lock').exists())
        (self.base/'run.lock').write_text('existing')
        with self.assertRaises(self.d.Stop): self.d.run(self.cfg,self.base)
        self.assertEqual((self.base/'run.lock').read_text(),'existing')
    def test_verified_push_to_local_remote(self):
        remote=self.root.parent/'remote.git'
        subprocess.run(['git','init','--bare','-q',str(remote)],check=True)
        git(self.root,'remote','add','origin',str(remote))
        self.cfg['publish']=True
        self.cfg['target_branch']='delivery'
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        sent=git(remote,'rev-parse','refs/heads/delivery')
        worker=self.base/'worktrees'/'codex'
        self.assertEqual(sent,git(worker,'rev-parse','HEAD'))
        self.assertIn('published',(self.base/'events.jsonl').read_text())
    def test_claude_cli_limit_wording_waits_instead_of_blocking(self):
        marker=self.root.parent/'attempted'
        self.fake.write_text('''import pathlib,subprocess,sys\nsys.stdin.read()\nm=pathlib.Path(%r)\nif not m.exists():\n m.write_text('once')\n print("You've hit your 5-hour limit - resets 7:10am (Africa/Kampala)")\n sys.exit(1)\np=pathlib.Path('auto-agents/PLAN.md')\np.write_text('STATUS: DONE\\n',encoding='utf8')\nsubprocess.run(['git','add',str(p)],check=True)\nsubprocess.run(['git','commit','-qm','finish'],check=True)\n''' % str(marker),encoding='utf8')
        self.cfg.update(max_sessions=3,usage_wait_seconds=0.01,max_rate_retries=2)
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        self.assertEqual(json.loads((self.base/'status.json').read_text())['state'],'done')
        self.assertIn('rate_wait',(self.base/'events.jsonl').read_text())
    def test_network_failure_retries_fresh_session(self):
        marker=self.root.parent/'attempted'
        self.fake.write_text('''import pathlib,subprocess,sys\nsys.stdin.read()\nm=pathlib.Path(%r)\nif not m.exists():\n m.write_text('once')\n print("API Error: Can't reach the API server (ENOTFOUND)")\n sys.exit(1)\np=pathlib.Path('auto-agents/PLAN.md')\np.write_text('STATUS: DONE\\n',encoding='utf8')\nsubprocess.run(['git','add',str(p)],check=True)\nsubprocess.run(['git','commit','-qm','finish'],check=True)\n''' % str(marker),encoding='utf8')
        self.cfg.update(max_sessions=3,network_retry_seconds=0.01,max_network_retries=2)
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        self.assertEqual(json.loads((self.base/'status.json').read_text())['state'],'done')
        self.assertIn('network_wait',(self.base/'events.jsonl').read_text())
    def test_network_retry_is_bounded(self):
        self.fake.write_text('''import sys\nsys.stdin.read()\nprint('ENOTFOUND')\nsys.exit(1)\n''',encoding='utf8')
        self.cfg.update(max_sessions=5,network_retry_seconds=0.01,max_network_retries=1)
        self.assertEqual(self.d.run(self.cfg,self.base),2)
        s=json.loads((self.base/'status.json').read_text())
        self.assertEqual(s['state'],'blocked')
        self.assertEqual((self.base/'events.jsonl').read_text().count('network_wait'),1)
    def test_unreachable_remote_push_retries_then_blocks(self):
        git(self.root,'remote','add','origin',str(self.root.parent/'missing-remote.git'))
        self.cfg.update(publish=True,target_branch='delivery',publish_retry_seconds=0.01,max_publish_retries=2)
        self.assertEqual(self.d.run(self.cfg,self.base),2)
        s=json.loads((self.base/'status.json').read_text())
        self.assertEqual(s['state'],'blocked')
        self.assertIn('push failed',s['reason'])
        self.assertEqual((self.base/'events.jsonl').read_text().count('"publish_retry"'),2)
    def test_rejected_push_is_not_retried(self):
        remote=self.root.parent/'remote.git'
        subprocess.run(['git','init','--bare','-q',str(remote)],check=True)
        git(self.root,'remote','add','origin',str(remote))
        other=self.root.parent/'other'
        subprocess.run(['git','clone','-q',str(remote),str(other)],check=True)
        git(other,'config','user.email','o@example.test'); git(other,'config','user.name','O')
        (other/'x.txt').write_text('x',encoding='utf8'); git(other,'add','.'); git(other,'commit','-qm','elsewhere')
        git(other,'push','-q','origin','HEAD:refs/heads/delivery')
        self.cfg.update(publish=True,target_branch='delivery',publish_retry_seconds=0.01,max_publish_retries=5)
        self.assertEqual(self.d.run(self.cfg,self.base),2)
        self.assertNotIn('publish_retry',(self.base/'events.jsonl').read_text())
    def test_check_warns_when_worktree_is_inside_git(self):
        import contextlib,io
        (self.root/'auto-agents'/'PLAN.md').write_text('STATUS: ACTIVE\n',encoding='utf8')
        git(self.root,'commit','-qam','plan')
        out=io.StringIO()
        with contextlib.redirect_stdout(out): self.d.preflight(self.cfg)
        self.assertIn('WARNING: the runner worktree',out.getvalue())
        out=io.StringIO()
        with contextlib.redirect_stdout(out): self.d.preflight({**self.cfg,'worktree_root':'../repo-autorun'})
        self.assertNotIn('WARNING',out.getvalue())
    def test_invalid_location_and_retry_settings_are_rejected(self):
        p=self.root/'auto-agents'/'config.json'
        self.d.CFG=p
        base={**self.cfg,'verify':[['python','-c','pass']]}
        p.write_text(json.dumps({**base,'worktree_root':'../repo-autorun','max_publish_retries':0}),encoding='utf8')
        self.assertEqual(self.d.config()['worktree_root'],'../repo-autorun')
        for bad in ({'worktree_root':''},{'worktree_root':3},{'network_retry_seconds':0},{'max_publish_retries':-1}):
            p.write_text(json.dumps({**base,**bad}),encoding='utf8')
            with self.assertRaises(self.d.Stop): self.d.config()
    def test_rate_limit_retries_without_changes(self):
        marker=self.root.parent/'attempted'
        self.fake.write_text('''import pathlib,subprocess,sys\nsys.stdin.read()\nm=pathlib.Path(%r)\nif not m.exists():\n m.write_text('once')\n print('usage limit')\n sys.exit(1)\np=pathlib.Path('auto-agents/PLAN.md')\np.write_text('STATUS: DONE\\n',encoding='utf8')\nsubprocess.run(['git','add',str(p)],check=True)\nsubprocess.run(['git','commit','-qm','finish'],check=True)\n''' % str(marker),encoding='utf8')
        self.cfg.update(max_sessions=3,initial_backoff_seconds=0.01,max_backoff_seconds=0.01,usage_wait_seconds=0.01,max_rate_retries=2)
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        self.assertEqual(json.loads((self.base/'status.json').read_text())['state'],'done')
        self.assertIn('rate_wait',(self.base/'events.jsonl').read_text())
    def test_verification_must_not_commit_a_different_revision(self):
        remote=self.root.parent/'remote.git'
        subprocess.run(['git','init','--bare','-q',str(remote)],check=True)
        git(self.root,'remote','add','origin',str(remote))
        self.cfg.update(publish=True,target_branch='delivery')
        self.cfg['verify']=[[sys.executable,'-c',
            "from pathlib import Path; import subprocess; Path('extra.txt').write_text('unexpected'); subprocess.run(['git','add','extra.txt'],check=True); subprocess.run(['git','commit','-qm','gate mutation'],check=True)"]]
        self.assertEqual(self.d.run(self.cfg,self.base),2)
        self.assertIn('verification changed HEAD',json.loads((self.base/'status.json').read_text())['reason'])
        self.assertNotIn('published',(self.base/'events.jsonl').read_text())
        self.assertNotEqual(subprocess.run(['git','show-ref','--verify','--quiet','refs/heads/delivery'],cwd=remote).returncode,0)
    def test_verification_must_not_switch_branch(self):
        self.cfg['verify']=[[sys.executable,'-c',"import subprocess; subprocess.run(['git','switch','-c','changed'],check=True)"]]
        self.assertEqual(self.d.run(self.cfg,self.base),2)
        self.assertIn('verification changed HEAD or branch',json.loads((self.base/'status.json').read_text())['reason'])
    def test_nonfinite_limits_rejected(self):
        self.d.CFG=self.root/'auto-agents'/'config.json'
        for key in ('max_hours','session_timeout_seconds','initial_backoff_seconds'):
            bad=dict(self.cfg); bad[key]=float('nan')
            self.d.CFG.write_text(json.dumps(bad),encoding='utf8')
            with self.assertRaises(self.d.Stop): self.d.config()
    def test_empty_verify_rejected(self):
        self.cfg['verify']=[]; self.d.CFG=self.root/'auto-agents'/'config.json'
        self.d.CFG.write_text(json.dumps(self.cfg),encoding='utf8')
        with self.assertRaises(self.d.Stop): self.d.config()

if __name__=='__main__': unittest.main()
