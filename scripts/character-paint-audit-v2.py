"""Audit actual evaluated source foot planting and camera/stride contracts; not an art approval."""
from pathlib import Path
import math,json,argparse,hashlib
from PIL import Image
root=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--input',default='art/characters-walk-v1/export-v2');args=parser.parse_args();source=root/args.input
manifest=json.loads((source/'manifest.json').read_text());poses=json.loads((source/'evaluated-joints.json').read_text());report={'source':args.input,'views':{},'physicalPhone':'not-run','familyTest':'not-run','artisticAcceptance':'pending'}
for variant,v in manifest['cameraVariants'].items():
 for direction,spec in v['directions'].items():
  view=direction if variant=='base' else variant+'-'+direction;angle=spec['screenAngleRadians'];stride=spec['projectedStridePixels'];dx=math.cos(angle)*stride*210/136;dy=math.sin(angle)*stride*210/136;checks={}
  for name,frames,side,distance in [('walk-L',range(1,9),'L',lambda f:(f-1)/16),('walk-R',range(9,17),'R',lambda f:(f-1)/16),('start',range(201,210),'R',lambda f:.25*((f-201)/8)**2),('stop-L',range(301,310),'L',lambda f:.25*(2*(f-301)/8-((f-301)/8)**2)),('stop-R',range(401,410),'R',lambda f:.25*(2*(f-401)/8-((f-401)/8)**2))]:
   positions=[]
   for f in frames:
    ankle=poses[view][str(f)]['foot.'+side][0];t=distance(f);positions.append([ankle[0]+dx*t,ankle[1]+dy*t])
   drift=max(math.dist(p,positions[0]) for p in positions);assert drift<.01,(view,name,drift);checks[name]=round(drift,7)
  camera=v['camera'];i=['e','se','sw','w','nw','ne'].index(direction);logical=i*math.pi/3+camera['angle'];expected=math.atan2(camera['groundScale']*math.sin(logical),math.cos(logical));assert abs(math.atan2(math.sin(angle-expected),math.cos(angle-expected)))<1e-8
  count=0
  for clip in spec['clips'].values():
   for frame in clip['frames']:
    path=root/frame['file'];im=Image.open(path);assert im.mode=='RGBA' and im.size==(320,320),(path,im.mode,im.size);assert im.getchannel('A').getbbox();count+=1
  hashes={hashlib.sha256((root/f['file']).read_bytes()).hexdigest() for f in spec['clips']['walk']['frames']};assert len(hashes)>=12,(view,'insufficient distinct walk phases',len(hashes))
  report['views'][view]={'distinctWalkFrames':len(hashes),'stridePixelsAtDisplay136':stride,'screenAngleRadians':angle,'maxPlantedFootDriftSourcePx':checks,'rgbaFrames':count}
report['result']='passed';target=root/'docs/chapter-1-rc/painted-motion/v2-technical-audit.json';target.write_text(json.dumps(report,indent=2)+'\n');print('All camera/stride/stance/source RGBA assertions passed:',len(report['views']),'views')
