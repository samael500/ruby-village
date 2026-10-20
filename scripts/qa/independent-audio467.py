"""Observe native WebAudio nodes/params, and compare exact source/delivery bytes."""
import json,hashlib,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/qa/residents-bridge-audio-467';OUT.mkdir(parents=True,exist_ok=True)
init='''const Native=window.AudioContext;window.qaAudio={contexts:[],voices:[],ramps:[]};const conn=AudioNode.prototype.connect,start=AudioBufferSourceNode.prototype.start,stop=AudioBufferSourceNode.prototype.stop,ramp=AudioParam.prototype.setTargetAtTime;AudioNode.prototype.connect=function(dest,...args){const r=conn.call(this,dest,...args);if(dest===this.context.destination)this.context.qaMaster=this;return r};AudioParam.prototype.setTargetAtTime=function(value,time,constant){qaAudio.ramps.push({master:qaAudio.contexts.some(c=>c.qaMaster?.gain===this),value,time});return ramp.call(this,value,time,constant)};AudioBufferSourceNode.prototype.start=function(...args){const r=start.apply(this,args);const v={source:this,context:this.context,ended:false};qaAudio.voices.push(v);this.addEventListener('ended',()=>v.ended=true);return r};AudioBufferSourceNode.prototype.stop=function(...args){const r=stop.apply(this,args);const v=qaAudio.voices.find(v=>v.source===this);if(v)v.stopAt=args[0]??this.context.currentTime;return r};window.AudioContext=new Proxy(Native,{construct(T,args){const c=new T(...args);qaAudio.contexts.push(c);return c}});window.qaAudioSnapshot=()=>({contexts:qaAudio.contexts.length,states:qaAudio.contexts.map(c=>c.state),masterValues:qaAudio.contexts.map(c=>c.qaMaster?.gain.value),activeLoops:qaAudio.voices.filter(v=>v.source.loop&&!v.ended&&(v.stopAt===undefined||v.stopAt>v.context.currentTime)).map(v=>({duration:v.source.buffer.duration,channels:v.source.buffer.numberOfChannels})),masterTargets:qaAudio.ramps.filter(r=>r.master).map(r=>r.value)});'''
with sync_playwright() as p:
 b=p.chromium.launch();q=b.new_page(viewport={'width':844,'height':390},has_touch=True,is_mobile=True);q.add_init_script(init);bad=[];q.on('response',lambda r:bad.append({'url':r.url,'status':r.status})if r.status>=400 else None);q.goto('http://127.0.0.1:5297/ruby-village/');before=q.evaluate('qaAudioSnapshot()');assert before['contexts']==0;q.locator('#continue-game').tap();q.locator('#prologue-skip').tap()
 while q.locator('#story[open]').count():q.locator('#story-action').tap()
 q.wait_for_timeout(1200);playing=q.evaluate('qaAudioSnapshot()');assert playing['contexts']==1 and len(playing['activeLoops'])==2,playing
 q.locator('#settings-open').tap();q.wait_for_timeout(400);paused=q.evaluate('qaAudioSnapshot()');assert len(paused['activeLoops'])==0
 q.locator('#pause-continue').tap();q.wait_for_timeout(1200);resumed=q.evaluate('qaAudioSnapshot()');assert len(resumed['activeLoops'])==2,resumed
 q.locator('#settings-open').tap();q.locator('#pause-settings').tap();q.locator('#audio-muted').check();q.wait_for_timeout(200);muted=q.evaluate('qaAudioSnapshot()');q.locator('#audio-muted').uncheck();q.wait_for_timeout(300);unmuted=q.evaluate('qaAudioSnapshot()');assert muted['masterTargets'][-1]==0 and unmuted['masterTargets'][-1]==.7
 # Real native keyboard adjusts sliders, restores defaults, and checks persisted independent buses.
 q.locator('#audio-music').focus();q.keyboard.press('Home');q.locator('#audio-sfx').focus();q.keyboard.press('Home');prefs=q.evaluate('JSON.parse(localStorage.getItem("ruby-village:audio:v1"))');assert prefs['music']==0 and prefs['sfx']==0 and prefs['muted']==False,prefs
 for ident,count in [('audio-music',7),('audio-sfx',13)]:
  q.locator('#'+ident).focus()
  for _ in range(count):q.keyboard.press('ArrowRight')
 q.locator('#settings-close').tap();q.wait_for_timeout(700);restored=q.evaluate('qaAudioSnapshot()');assert restored['contexts']==1 and len(restored['activeLoops'])==2
 report={'baseline':'467eab2','nativeAudioContext':'observed, not replaced with fake','beforeGesture':before,'playing':playing,'paused':paused,'resumed':resumed,'muted':muted,'unmuted':unmuted,'zeroVolumePreferences':prefs,'restored':restored,'httpErrors':bad,'subjectiveListening':'NOT RUN'};assert not bad;q.close();b.close()
# Compare music/effects/master before noise-only edit; five ambience files intentionally differ.
base='51e15d5^';hashes=[];ambience={'bakery.ogg','forest.ogg','leaves.ogg','village.ogg','water.ogg'}
for prefix in ['public/assets/audio/music','public/assets/audio/sfx','art/audio/music']:
 for p in (ROOT/prefix).rglob('*'):
  if not p.is_file() or p.name in ambience:continue
  rel=str(p.relative_to(ROOT));old=subprocess.run(['git','show',base+':'+rel],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
  if old.returncode==0:
   oldhash=hashlib.sha256(old.stdout).hexdigest();newhash=hashlib.sha256(p.read_bytes()).hexdigest();hashes.append({'file':rel,'before':oldhash,'after':newhash,'equal':oldhash==newhash})
assert all(x['equal']for x in hashes)
oldaudio=subprocess.check_output(['git','show',base+':src/audio.ts'],cwd=ROOT);assert oldaudio==(ROOT/'src/audio.ts').read_bytes()
originals=[]
for name in ['bakery','forest','leaves','village','water']:
 oldpath='art/audio/sfx/originals/original-'+name+'.wav';old=subprocess.check_output(['git','show',base+':'+oldpath],cwd=ROOT);saved=ROOT/'art/audio/sfx/noise-review-before'/('original-'+name+'.wav');originals.append({'file':str(saved.relative_to(ROOT)),'archivedOriginalMatchesBefore':saved.read_bytes()==old});assert saved.read_bytes()==old
exports=json.loads((ROOT/'dist/export-assets.json').read_text());sourcechecks=[]
for item in exports['removed']:
 src=ROOT/'public'/item['file'];sourcechecks.append({'file':item['file'],'sourceExists':src.is_file(),'sourceBytes':src.stat().st_size if src.exists()else None,'excludedBytes':item['bytes']})
assert all(x['sourceExists']and x['sourceBytes']==x['excludedBytes']for x in sourcechecks)
report.update({'unchangedAudioBytes':hashes,'audioModuleByteIdentical':True,'oldAmbienceOriginalsArchivedIntact':originals,'excludedSourcesStillPresent':sourcechecks,'exportKeptBytes':exports['keptBytes'],'exportRemovedBytes':exports['removedBytes']})
(OUT/'audio-and-source-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS native audio, unchanged music/effects/master, preserved source originals')
