"""Separate stems and equal-RMS comparisons; objective analysis, not human listening."""
import json,subprocess,hashlib
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[2];out=root/'docs/chapter-1-rc/audio-noise';out.mkdir(parents=True,exist_ok=True);rate=24000

def decode(p,channels=2):
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ar',str(rate),'-ac',str(channels),'-f','f32le','-']);return np.frombuffer(data,dtype='<f4').reshape(-1,channels).copy()
def db(value):return round(float(20*np.log10(max(value,1e-9))),3)
def metrics(x):
 frames=x.reshape(-1);window=rate//10;mono=x.mean(axis=1);energy=np.sqrt(np.mean(mono[:len(mono)//window*window].reshape(-1,window)**2,axis=1));return {'peakDbFS':db(np.max(np.abs(frames))),'rmsDbFS':db(np.sqrt(np.mean(frames**2))),'quiet100msPercentile10DbFS':db(np.percentile(energy,10)),'nearSilentWindowsPercent':round(float(np.mean(energy<1e-5)*100),2),'loopEdgeDelta':float(np.max(np.abs(x[-1]-x[0])))}
def encode(name,x):
 subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(rate),'-ac','2','-i','-','-c:a','flac',str(out/name)],input=x.astype('<f4').tobytes(),check=True)
report={'scope':'Objective decoded-stem and equal-RMS comparisons, no human listening claim. Music and SFX bytes unchanged. Final real browser mix capture follows integration.','ambiences':[],'mixes':[]}
for scene in ['leaves','village','bakery','water','forest']:
 before=root/f'art/audio/sfx/noise-review-before/{scene}.ogg';after=root/f'public/assets/audio/sfx/{scene}.ogg';b=decode(before);a=decode(after);report['ambiences'].append({'scene':scene,'before':metrics(b),'after':metrics(a),'beforeSha256':hashlib.sha256(before.read_bytes()).hexdigest(),'afterSha256':hashlib.sha256(after.read_bytes()).hexdigest()})
for cue,amb in [('village','leaves'),('water','water')]:
 music=decode(root/f'public/assets/audio/music/{cue}.ogg');count=24*rate;indices=(np.arange(count)+len(music)-6*rate)%len(music);excerpt=music[indices];encode(f'{cue}-music-only.flac',excerpt)
 for state,path in [('before',root/f'art/audio/sfx/noise-review-before/{amb}.ogg'),('after',root/f'public/assets/audio/sfx/{amb}.ogg')]:
  ambience=decode(path);stem=ambience[np.arange(count)%len(ambience)];mix=(excerpt+stem)*.65*.7*.35
  gain=.06/max(float(np.sqrt(np.mean(mix**2))),1e-9);normalized=mix*gain;assert np.max(np.abs(normalized))<.99
  encode(f'{cue}-{state}-equal-rms.flac',normalized);encode(f'{cue}-{state}-ambience-only.flac',stem)
  report['mixes'].append({'cue':cue,'state':state,'musicExcerpt':'six seconds before loop edge through18 seconds after','sameMasterAndCueGain':True,'comparisonRmsTargetDbFS':db(.06),'normalizationGain':gain,'metrics':metrics(normalized)})
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS stem decode, comparison encode, same RMS and no clipping; subjective listening NOT RUN')
