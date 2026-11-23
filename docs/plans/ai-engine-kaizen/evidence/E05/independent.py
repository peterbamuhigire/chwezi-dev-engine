"""Independent process-level K3 checks. Pass a directory containing cli.py and legacy_fixture.sql."""
from pathlib import Path
from contextlib import closing
import argparse
import json
import sqlite3
import subprocess
import sys
import tempfile

def evaluate(example, variant):
    with tempfile.TemporaryDirectory() as scratch:
        db=Path(scratch)/'ticket.db'
        with closing(sqlite3.connect(db)) as conn:
            conn.executescript((example/'legacy_fixture.sql').read_text(encoding='utf-8-sig'))
        def rows():
            with closing(sqlite3.connect(db)) as conn:
                return conn.execute("SELECT ticket_id,status,source_event_id FROM history ORDER BY history_id").fetchall()
        def send(event,status,*extra):
            return subprocess.run([sys.executable,'-B',str(example/'cli.py'),'--db',str(db),
                '--event',event,'--ticket','T1','--status',status,'--implementation',variant,*extra],
                capture_output=True,text=True)
        original=rows()
        assert original==[('T1','open',None)]
        first=send('E7','review')
        first_history=rows()
        retry=send('E7','review')
        retry_history=rows()
        second=send('E8','closed')
        second_history=rows()
        conflict=send('E7','closed')
        conflict_history=rows()
        interrupted=send('E9','open','--fail-before-history')
        failed_history=rows()
        recovered=send('E9','open')
        final_history=rows()
        with closing(sqlite3.connect(db)) as conn:
            final_status=conn.execute("SELECT status FROM tickets WHERE ticket_id='T1'").fetchone()[0]
        return {
            'legacy_preserved':final_history[:1]==original,
            'first_applied':first.returncode==0 and first_history==original+[('T1','review','E7')],
            'retry_once':retry.returncode==0 and retry_history==original+[('T1','review','E7')],
            'distinct_applied':second.returncode==0 and second_history==original+[('T1','review','E7'),('T1','closed','E8')],
            'conflict_rejected':conflict.returncode!=0 and conflict_history==second_history,
            'failure_atomic':interrupted.returncode!=0 and failed_history==second_history,
            'retry_recovers':recovered.returncode==0 and final_history==second_history+[('T1','open','E9')] and final_status=='open'
        }

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('example',type=Path)
    args=p.parse_args()
    result={name:evaluate(args.example,name) for name in ('baseline','ticket-level-dedupe','fixed')}
    print(json.dumps(result,indent=2))
    sys.exit(0 if not result['baseline']['retry_once'] and not result['ticket-level-dedupe']['distinct_applied'] and all(result['fixed'].values()) else 1)
