"""Frozen source technical guide batch; calls unchanged verified tools sequentially."""
from pathlib import Path
import subprocess,json,hashlib,time,datetime,os,sys
O=Path(__file__).resolve().parent;R=O.parents[1];SOURCE=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-layered-style-v2/ruta-native-style.blend');EXPECTED='bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(SOURCE)==EXPECTED
exporter=R/'scripts/ruta-ready-sprite-export.py';packer=R/'scripts/ruta-ready-sprite-pack.py';baseline=json.loads((R/'art/ruta-native-layered-walk48-v2/source-contract.json').read_text());assert baseline['parameters']['variants']==['base'] and baseline['parameters']['directions']==['e'] and baseline['parameters']['frameCount']==48;assert sha(exporter)==baseline['exporterSha256'];assert sha(R/baseline['headingContract'])==baseline['headingContractSha256']
report={'scope':'technical native pose guides, NOT final painted artwork/runtime or new art acceptance','baseCommit':'b33addd','source':str(SOURCE),'sourceSha256':EXPECTED,'exporterSha256':sha(exporter),'packerSha256':sha(packer),'parameters':{'variant':'base','directions':['se','sw','w','nw','ne'],'clip':'walk','frameCountPerDirection':48,'existingENotRepeated':'art/ruta-native-layered-walk48-v2'},'startedUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'batchPid':os.getpid(),'status':'RUNNING','checkpoints':[]}
def save():(O/'batch-report.json').write_text(json.dumps(report,indent=2)+'\n')
resume='--resume-verified-se' in sys.argv
previous=None
if resume:
 previous=json.loads((O/'batch-report.json').read_text());assert previous['status']=='STOPPED-ERROR' and previous['checkpoints'][-1]['direction']=='se' and previous['checkpoints'][-1]['renderExitCode']==0
 (O/'initial-attempt-report.json').write_text(json.dumps(previous,indent=2)+'\n')
 report['recovery']='Initial controller checked frames/ instead of actual renders/ after successful SE export; stopped fail-closed. Existing SE is explicitly reverified and packed, never rerendered.'
save()
try:
 for direction in report['parameters']['directions']:
  assert sha(SOURCE)==EXPECTED;out=O/direction;reuse=resume and direction=='se'
  if reuse:assert out.exists() and (out/'source-contract.json').exists()
  else:assert not out.exists(),'New output must not overwrite artifacts';out.mkdir()
  cmd=['/tmp/blender-4.5.3-linux-x64/blender','--background','--threads','2','--disable-autoexec','--python-exit-code','1','--python',str(exporter),'--','--source',str(SOURCE),'--out',str(out),'--variants','base','--directions',direction,'--clips','walk','--frame-count','48','--allow-batch'];t=time.perf_counter();checkpoint={'direction':direction,'command':cmd,'startedUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'RENDERING'};report['checkpoints'].append(checkpoint);save()
  if reuse:
   code=0;checkpoint['renderReusedFromFirstAttempt']=True;checkpoint['originalRenderSeconds']=previous['checkpoints'][-1]['renderSeconds']
  else:
   with(out/'render-process.log').open('w')as f:
    proc=subprocess.Popen(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT);checkpoint['blenderPid']=proc.pid;save();code=proc.wait()
  checkpoint['renderSeconds']=time.perf_counter()-t;checkpoint['renderExitCode']=code;assert code==0
  contract=json.loads((out/'source-contract.json').read_text());assert contract['sourceSha256']==EXPECTED and contract['renderedFrameCount']==48;assert contract['parameters']=={'variants':['base'],'directions':[direction],'clips':['walk'],'frameCount':48,'contractOnly':False};assert len(list((out/'renders').rglob('*.png')))==48
  cmdpack=['/tmp/ruby-rc-tools/bin/python',str(packer),'--contract',str(out/'source-contract.json')];checkpoint['packCommand']=cmdpack;t=time.perf_counter()
  with(out/'pack-process.log').open('w')as f:subprocess.run(cmdpack,cwd=R,stdout=f,stderr=subprocess.STDOUT,check=True)
  checkpoint['packSeconds']=time.perf_counter()-t;manifest=json.loads((out/'manifest.json').read_text());audit=json.loads((out/'containment-audit.json').read_text());assert manifest['packedFrameCount']==48 and audit['actualAlphaCheckedFrames']==48;assert sha(SOURCE)==EXPECTED;checkpoint['status']='PASS';checkpoint['actualPngCount']=48;checkpoint['packedFrameCount']=48;checkpoint['sourceSha256After']=sha(SOURCE);checkpoint['checks']='exporter geometry/projection/seam + pack actual alpha containment and decoded losslessWebP byte equality';checkpoint['finishedUtc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save();print('CHECKPOINT',direction,'48PNG+lossless atlas PASS',flush=True)
 report['status']='COMPLETE-TECHNICAL-GUIDES-NOT-FINAL-ART';report['newPngCount']=240;report['sourceSha256After']=sha(SOURCE);save()
except BaseException as e:
 report['status']='STOPPED-ERROR';report['error']=repr(e);save();raise
