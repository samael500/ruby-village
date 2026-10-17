#!/usr/bin/env python3
"""Original Ruby Village score. GPL-2.0-only; deterministic MIDI + FluidSynth renders.
Run python3 scripts/music-compose.py; requires libfluidsynth.so.3 and ffmpeg.
"""
import ctypes as C, struct, subprocess, json, hashlib, math, os
from pathlib import Path
R=Path(__file__).resolve().parents[1]; OUT=R/'art/audio/music'; GAME=R/'public/assets/audio/music'
SR=32000; BPM=108; SPB=60/BPM; BARS=64; BEATS=BARS*3
# D major / B minor family. Each pair of bars forms a breath, not an ostinato lead.
PHRASES=[[(0,74,1),(1,78,.5),(1.5,81,1),(3,78,1),(4,76,1.5)],[(0,74,.75),(1,76,.75),(2,78,1),(3,81,1),(4,83,.5),(4.5,81,1)],[(0,79,1.5),(2,78,.75),(3,76,1),(4,74,1.5)],[(0,73,1),(1.5,76,1),(3,74,2.5)],[(0,78,1),(1,81,1),(3,85,1),(4,83,1.5)],[(0,83,1.5),(2,81,.75),(3,78,1),(4,76,1.5)],[(0,79,1),(1.5,78,1),(3,76,1),(4,73,1.5)],[(0,76,1),(1,73,1),(3,74,2.5)]]
CHORDS=[(50,54,57),(47,50,54),(43,47,50),(45,49,52),(50,54,57),(54,57,61),(43,47,50),(45,49,52)]
CONFIG={'village':(73,24,46,0,1.0),'day':(73,24,11,0,.78),'water':(75,46,8,12,.72),'evening':(71,24,10,0,.68),'ending':(73,46,8,0,.85)}
def score(cue):
 lead,pluck,bell,shift,vel=CONFIG[cue]; ending=cue=='ending'; bars=8 if ending else BARS; ev=[]
 def note(ch,p,start,dur,v):
  if ending and start>=21 and start!=21: return
  ev.extend([(round(start*SPB*SR),1,ch,p,max(1,int(v*vel))),(round((start+dur)*SPB*SR),0,ch,p,0)])
 for bar in range(bars):
  section=bar//16; chord=CHORDS[(bar//2)%8]
  if cue=='evening': chord=CHORDS[(bar//2+1)%8]
  root=chord[0]; base=bar*3
  note(1,root,base,2.6,42)
  # Warm six-note arpeggio with alternating inversions and dynamic breathing.
  for k in range(6):
   p=chord[[0,1,2,1,2,1][k]]+12
   note(2,p,base+k*.5,.42,34+(k%3)*4)
  if bar%4==0: note(3,chord[2]+24,base+.03,2,25)
  if section in [1,3] or ending:
   for p in chord: note(4,p+12,base,2.85,18)
  if bar%2==0 and (cue!='day' or bar%8<6):
   phrase=PHRASES[(bar//2 + (2 if cue=='water' else 0))%8]
   for offset,p,dur in phrase:
    if base+offset>=bars*3: continue
    # B section answer lowers phrase, last 16 bars return softly.
    trans=-12 if section==2 else 0
    note(0,p+trans+(0 if cue!='evening' else -12),base+offset,dur,57+((bar//2)%3)*3)
 if ending:
  # Complete tonic cadence, then natural decay to silence.
  ev=[e for e in ev if e[0]<round(21*SPB*SR) or e[1]==0]
  for p in [50,57,62,66,74]: note(0 if p==74 else 4,p,21,2.5,42)
 duration=round((bars*3*SPB+(4 if ending else 0))*SR)
 return sorted(ev),duration,[lead,32,pluck,bell,48]
def vlq(n):
 b=[n&127]; n>>=7
 while n: b.insert(0,(n&127)|128); n>>=7
 return bytes(b)
def midi(cue,ev,programs):
 events=[(0,bytes([0xc0+ch,p])) for ch,p in enumerate(programs)]
 for t,on,ch,p,v in ev: events.append((round(t/SR/SPB*480),bytes([(0x90 if on else 0x80)+ch,p,v])))
 data=b'\x00\xff\x51\x03'+int(SPB*1e6).to_bytes(3,'big'); last=0
 for tick,msg in sorted(events,key=lambda e:e[0]): data+=vlq(tick-last)+msg; last=tick
 data+=b'\x00\xff\x2f\x00'; (OUT/f'{cue}.mid').write_bytes(b'MThd'+struct.pack('>IHHH',6,0,1,480)+b'MTrk'+struct.pack('>I',len(data))+data)
F=C.CDLL('libfluidsynth.so.3')
def bind(name,restype,args):
 f=getattr(F,name); f.restype=restype; f.argtypes=args; return f
ptr=C.c_void_p; I=C.c_int; S=C.c_char_p
settings=bind('new_fluid_settings',ptr,[])(); bind('fluid_settings_setnum',I,[ptr,S,C.c_double])(settings,b'synth.sample-rate',SR)
bind('fluid_settings_setnum',I,[ptr,S,C.c_double])(settings,b'synth.gain',.55)
bind('fluid_settings_setint',I,[ptr,S,I])(settings,b'synth.cpu-cores',1)
new=bind('new_fluid_synth',ptr,[ptr]); load=bind('fluid_synth_sfload',I,[ptr,S,I]); program=bind('fluid_synth_program_change',I,[ptr,I,I]); on=bind('fluid_synth_noteon',I,[ptr,I,I,I]); off=bind('fluid_synth_noteoff',I,[ptr,I,I]); write=bind('fluid_synth_write_float',I,[ptr,I,ptr,I,I,ptr,I,I]); delete=bind('delete_fluid_synth',None,[ptr])
manifest={'version':1,'cues':{}}
for cue in CONFIG:
 if os.environ.get('MUSIC_CUES') and cue not in os.environ['MUSIC_CUES'].split(','): continue
 ev,duration,programs=score(cue); midi(cue,ev,programs); synth=new(settings); load(synth,str(OUT/'TimGM6mb.sf2').encode(),1)
 for ch,p in enumerate(programs): program(synth,ch,p)
 for ch,pan in enumerate([68,64,48,83,64]): bind('fluid_synth_cc',I,[ptr,I,I,I])(synth,ch,10,pan)
 # Render three complete cycles. The third contains the preceding reverb tail.
 cycles=1 if cue=='ending' else 3; raw=OUT/f'{cue}.f32'; buf=(C.c_float*(4096*2))()
 with raw.open('wb') as out:
  def render(n,save):
   while n:
    count=min(n,4096); write(synth,count,buf,0,2,buf,1,2)
    if save: out.write(bytes(buf)[:count*8])
    n-=count
  for cycle in range(cycles):
   cursor=0
   for t,is_on,ch,p,v in ev:
    render(t-cursor,cycle==cycles-1); cursor=t
    on(synth,ch,p,v) if is_on else off(synth,ch,p)
   render(max(0,duration-cursor),cycle==cycles-1)
 delete(synth)
 master=OUT/f'{cue}-master.flac'
 subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i',str(raw),'-af','volume=0.8','-sample_fmt','s16',str(master)],check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(master),'-c:a','libvorbis','-q:a','3',str(GAME/f'{cue}.ogg')],check=True)
 raw.unlink(); manifest['cues'][cue]={'file':f'{cue}.ogg','gain':.65,'loop':cue!='ending'}
 print(cue,duration/SR,flush=True)
if os.environ.get('MUSIC_CUES') and (GAME/'manifest.json').exists():
 old=json.loads((GAME/'manifest.json').read_text()); old['cues'].update(manifest['cues']); manifest=old
(GAME/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
