#!/usr/bin/env python3
"""Decode the actual game assets; compare seams against ordinary sample steps.
Produces two-cycle analysis, boundary montage, and SHA256 provenance.
This measures signal integrity; it does not claim human listening approval.
"""
import subprocess,json,array,math,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]; game=R/'public/assets/audio/music'; out=R/'docs/chapter-1-rc/music'; report={}
for p in sorted(game.glob('*.ogg')):
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ar','32000','-ac','2','-'])
 n=len(data)//4
 edge=array.array('f'); edge.frombytes(data[:8]+data[-8:])
 seam=max(abs(edge[2]-edge[0]),abs(edge[3]-edge[1]))
 stats=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-af','astats=metadata=0:reset=0','-f','null','-'],capture_output=True,text=True,check=True).stderr
 import re
 def metric(label):
  return [float(x) for x in re.findall(re.escape(label)+r': ([-+0-9.einf]+)',stats)]
 peak=max(metric('Peak level dB')); rms=metric('RMS level dB')[-1]; largest=max(metric('Max difference'))
 report[p.stem]={'seconds':n/2/32000,'bytes':p.stat().st_size,'peakDbFS':peak,'rmsDbFS':rms,'boundaryMaxStep':seam,'ordinaryMaxStep':largest,'boundaryToMaxRatio':seam/max(largest,1e-9),'twoBoundariesAnalyzed':p.stem!='ending','finite':not any(metric('Number of NaNs')+metric('Number of Infs')),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if p.stem!='ending':
  subprocess.run(['ffmpeg','-v','error','-y','-stream_loop','2','-i',str(p),'-ss',str(n/2/32000-7),'-t','14','-c:a','libmp3lame','-b:a','128k',str(out/f'{p.stem}-seam-preview.mp3')],check=True)
(out/'analysis.json').write_text(json.dumps(report,indent=2)+'\n')
paths=sorted((R/'art/audio/music').rglob('*'))+sorted(game.rglob('*'))
(out/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n' for p in paths if p.is_file()))
print(json.dumps(report,indent=2))
# Compact, ordered audition of the single recommended suite.
parts=[]
for cue in ['village','day','water','evening','ending']:
 part=Path('/tmp')/f'ruby-music-{cue}.wav'; parts.append(part)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(game/f'{cue}.ogg'),'-t','12','-c:a','pcm_s16le',str(part)],check=True)
concat=Path('/tmp/ruby-music-concat.txt'); concat.write_text(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-c:a','libmp3lame','-b:a','128k',str(out/'recommended-suite-preview.mp3')],check=True)
