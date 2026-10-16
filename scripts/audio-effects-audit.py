"""Decode every delivered file, verify manifest hashes, no clipping and smooth ambience edges."""
import hashlib,json,math,struct,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'src/sound-manifest.json').read_text());results=[]
for name,record in manifest['files'].items():
 path=root/'public/assets/audio/sfx'/name
 assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256']
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','s16le','-ac','1','-ar','24000','-'])
 samples=struct.unpack('<'+'h'*(len(raw)//2),raw);peak=max(abs(x) for x in samples)/32768;rms=math.sqrt(sum(x*x for x in samples)/len(samples))/32768
 assert peak<.999,(name,peak)
 if name in ['water.ogg','leaves.ogg','village.ogg','forest.ogg','bakery.ogg']:assert max(abs(samples[0]),abs(samples[-1]))<50,(name,samples[0],samples[-1])
 results.append({'file':name,'duration':round(len(samples)/24000,3),'peakDbFS':round(20*math.log10(peak),2),'rmsDbFS':round(20*math.log10(rms),2),'edgeSamples':[samples[0],samples[-1]]})
(root/'docs/chapter-1-rc/audio-effects/asset-audit.json').write_text(json.dumps(results,indent=2)+'\n')
print(f'{len(results)} files: hashes/decode/no clipping/ambient edge checks pass')
