"""Rebuild chosen Kenney CC0 effects and deterministic original ambient masters. ffmpeg required."""
import json,math,random,wave,struct,subprocess,hashlib,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]; originals=root/'art/audio/sfx/originals'; out=root/'public/assets/audio/sfx'
originals.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
# Downloads are deliberately outside Git; commit only selected untouched originals plus their licenses.
source=Path('/tmp/ruby-audio-download')
choices={'click':('interface','click_004'),'modal':('interface','open_001'),'dialog':('interface','switch_001'),'select':('impact','impactSoft_medium_000'),'place':('impact','impactGeneric_light_000'),'rotate':('interface','pluck_002'),'return':('impact','impactWood_light_000'),'reject':('impact','impactSoft_medium_002'),'gate':('impact','impactWood_medium_000'),'paper':('interface','scratch_004'),'basket':('impact','impactSoft_medium_001')}
for i in range(1,3):choices[f'place-{i}']=('impact',f'impactGeneric_light_{i:03}')
# Concrete/grass/wood get three real recorded variants.
for surface,material in [('stone','concrete'),('earth','grass'),('wood','wood')]:
 for i in range(3):choices[f'foot-{surface}-{i}']=('impact',f'footstep_{material}_{i:03}')
for name,(pack,file) in choices.items():
 path=originals/f'{file}.ogg'
 if not path.exists():shutil.copyfile(source/pack/'Audio'/f'{file}.ogg',path)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(path),'-af','highpass=f=90,lowpass=f=6500,alimiter=limit=0.7:level=false,volume=0.7,afade=t=in:d=0.005,areverse,afade=t=in:d=0.025,areverse','-ar','24000','-ac','1','-c:a','libvorbis','-q:a','3',str(out/f'{name}.ogg')],check=True)
for pack in ['impact','interface']:
 if (source/pack/'License.txt').exists():shutil.copyfile(source/pack/'License.txt',originals/f'Kenney-{pack}-License.txt')
rate=24000
for name,seconds in [('chime',1.1),('victory',2.0),('leaves',12),('village',12),('bakery',12),('water',12),('forest',12)]:
 rng=random.Random(51050); n=int(seconds*rate);values=[]
 for i in range(n):
  t=i/rate
  if seconds<3:
   notes=[523.25,659.25,783.99] if name=='victory' else [783.99,1174.66]
   x=sum(math.sin(2*math.pi*f*t)*math.exp(-3*max(0,t-j*.16))*(t>=j*.16) for j,f in enumerate(notes))*.15
   x*=min(1,t/.01,(seconds-t)/.08)
  else:
   # Periodic oscillators and enveloped deterministic noise; endpoints are faded to zero.
   bed=(rng.random()*2-1)*(.025 if name=='water' else .008)
   flow=sum(math.sin(2*math.pi*k*t/seconds+p)*a for k,p,a in [(1101,0,.008),(1607,1,.004),(2303,2,.003)])
   bird=0
   if name in ['leaves','forest','village']:
    for at in [1.5,5.8,9.4]:
     dt=t-at
     if 0<dt<.35:bird+=math.sin(2*math.pi*(1600*dt+600*dt*dt))*math.sin(math.pi*dt/.35)**2*.035
   if name=='bakery':flow=math.sin(2*math.pi*61*t)*.004
   x=(bed+flow+bird)*min(1,t/.3,(seconds-t)/.3)
  values.append(struct.pack('<h',int(max(-.8,min(.8,x))*32767)))
 path=originals/f'original-{name}.wav'
 with wave.open(str(path),'wb') as w:w.setparams((1,2,rate,n,'NONE','not compressed'));w.writeframes(b''.join(values))
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(path),'-c:a','libvorbis','-q:a','3',str(out/f'{name}.ogg')],check=True)
events={}
def event(name,files,gain=.5,interval=70):events[name]={'variants':[f'{f}.ogg' for f in files],'gain':gain,'minIntervalMs':interval,'loop':False,'license':'CC0-1.0','author':'Kenney' if all(f in choices for f in files) else 'Ruby Village contributors','sourceUrl':'https://kenney.nl/assets/impact-sounds' if files[0] in choices and choices[files[0]][0]=='impact' else 'https://kenney.nl/assets/interface-sounds' if files[0] in choices else 'scripts/audio-effects-build.py'}
for name,file in [('ui-click','click'),('modal','modal'),('dialog','dialog'),('tile-select','select'),('tile-place','place'),('tile-rotate','rotate'),('tile-return','return'),('tile-reject','reject'),('check-incomplete','reject'),('path-connected','chime'),('victory','victory'),('gate-open','gate'),('paper','paper'),('basket','basket'),('stone','chime')]:event(name,[file],.4 if name!='victory' else .55)
events['tile-place']['variants']=['place.ogg','place-1.ogg','place-2.ogg']
for s in ['earth','stone','wood']:event(f'foot-{s}',[f'foot-{s}-{i}' for i in range(3)],.28,160)
manifest={'version':1,'events':events,'ambiences':{k:{'file':v+'.ogg','gain':.65,'loop':True,'license':'CC0-1.0','author':'Ruby Village contributors','sourceUrl':'scripts/audio-effects-build.py'} for k,v in {'gate':'leaves','garden':'leaves','well':'village','bakery':'bakery','stream':'water','mill':'water','post':'village','forest':'forest'}.items()},'files':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(out.glob('*.ogg'))}}
(root/'src/sound-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
