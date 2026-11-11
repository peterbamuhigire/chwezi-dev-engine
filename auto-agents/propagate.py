#!/usr/bin/env python3
"""Preview or apply a verified tool update to one or more project checkouts."""
import argparse
import json
from pathlib import Path
import sys
from upgrade import upgrade, UpgradeError

SOURCE=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('repositories',nargs='+',help='repository roots containing auto-agents')
    p.add_argument('--apply',action='store_true')
    args=p.parse_args()
    failed=False
    for name in args.repositories:
        target=Path(name)/'auto-agents'
        try: print(json.dumps({'repository':name,**upgrade(SOURCE,target,args.apply)}))
        except (OSError,ValueError,UpgradeError) as e:
            failed=True;print(json.dumps({'repository':name,'error':str(e)}),file=sys.stderr)
    return 2 if failed else 0

if __name__=='__main__':sys.exit(main())
