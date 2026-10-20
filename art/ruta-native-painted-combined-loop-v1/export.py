"""Pinned whole-sprite export launcher. Default prints command, never renders."""
from pathlib import Path
import argparse,hashlib,json,subprocess,time
O=Path(__file__).resolve().parent;ROOT=O.parents[1]
p=argparse.ArgumentParser();p.add_argument('--render',action='store_true');p.add_argument('--contract-only',action='store_true');a=p.parse_args();assert not(a.render and a.contract_only)
s=ROOT/'art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend';expected='b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(s)==expected
cmd=['/tmp/blender-4.5.3-linux-x64/blender','--background','--threads','2','--disable-autoexec','--python-exit-code','1','--python',str(ROOT/'scripts/ruta-ready-sprite-export.py'),'--','--source',str(s),'--out',str(O),'--variants','base','--directions','e','--clips','walk','--frame-count','48']
if a.contract_only:cmd+=['--contract-only']
print(' '.join(cmd),flush=True)
if a.render or a.contract_only:
 start=time.monotonic()
 with (O/('render-process.log'if a.render else 'smoke-process.log')).open('w')as log:subprocess.run(cmd,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
 assert sha(s)==expected
 (O/('render-run.json'if a.render else 'smoke-run.json')).write_text(json.dumps({'command':cmd,'sourceSha256':expected,'seconds':time.monotonic()-start,'rendered':a.render},indent=2)+'\n')
