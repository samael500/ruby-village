#!/usr/bin/env python3
"""Match each lossless master to -24.5 dBFS mean level, then re-encode Vorbis."""
from pathlib import Path
import subprocess,re
R=Path(__file__).resolve().parents[1]
for master in sorted((R/'art/audio/music').glob('*-master.flac')):
 stats=subprocess.run(['ffmpeg','-hide_banner','-i',str(master),'-af','volumedetect','-f','null','-'],capture_output=True,text=True,check=True).stderr
 mean=float(re.search(r'mean_volume: ([-.0-9]+)',stats)[1]); peak=float(re.search(r'max_volume: ([-.0-9]+)',stats)[1])
 gain=min(-24.5-mean,-3-peak)
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(master)],text=True))
 filters=f'volume={gain}dB'
 if 'ending' not in master.name: filters+=f',afade=t=in:d=0.004,afade=t=out:st={duration-0.004}:d=0.004'
 temp=master.with_name(master.stem+'-normalized.flac')
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(master),'-af',filters,'-sample_fmt','s16',str(temp)],check=True); temp.replace(master)
 cue=master.stem.replace('-master','')
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(master),'-c:a','libvorbis','-q:a','3',str(R/f'public/assets/audio/music/{cue}.ogg')],check=True)
 print(cue,'gain',gain)
