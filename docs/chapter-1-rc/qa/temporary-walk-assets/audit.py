from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,subprocess,numpy as np
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;REV='e32cad43a8b4061dec2f95a09e3669ac4537f405';mp='public/assets/characters-walk-v1/animated-v3/manifest.json';raw=subprocess.check_output(['git','show',REV+':'+mp],cwd=R);m=json.loads(raw);assert hashlib.sha256((R/mp).read_bytes()).hexdigest()==hashlib.sha256(raw).hexdigest();rows=[];selected={};sheet=Image.new('RGBA',(4*288,2*472),(235,229,213,255));draw=ImageDraw.Draw(sheet)
for name,spec in m['cameraVariants'].items():
 for direction,d in spec['directions'].items():
  clip=d['clips']['walk'];frames=[];hashes=[];rects=[]
  for f in clip['frames']:
   p=R/'public'/f['file'];blob=subprocess.check_output(['git','show',REV+':public/'+f['file']],cwd=R);assert hashlib.sha256(blob).hexdigest()==hashlib.sha256(p.read_bytes()).hexdigest();x,y,w,h=f['sourceRect'];im=Image.open(p).convert('RGBA').crop((x,y,x+w,y+h));frames.append(np.array(im));hashes.append(hashlib.sha256(im.tobytes()).hexdigest());rects.append(f['sourceRect'])
  deltas=[int(np.any(frames[i]!=frames[(i+1)%len(frames)],axis=2).sum())for i in range(len(frames))];visibleDeltas=[int((np.any(abs(frames[i].astype(int)-frames[(i+1)%len(frames)].astype(int))>25,axis=2)&((frames[i][:,:,3]>128)|(frames[(i+1)%len(frames)][:,:,3]>128))).sum())for i in range(len(frames))];rows.append({'visibleUnionAdjacentPixelsChangingAbove25RGBAIncludingLoopSeam':visibleDeltas,'camera':name,'direction':direction,'frameCount':len(frames),'uniqueRGBAFrames':len(set(hashes)),'cycleMs':sum(f['durationMs']for f in clip['frames']),'frameHashes':hashes,'adjacentChangedPixelCountsIncludingLoopSeam':deltas,'allAssetsMatchIntegrationCommit':True})
  if name=='base'and direction in ['e','se']:
   row=0 if direction=='e' else 1
   for j,i in enumerate([0,4,8,12]):
    im=Image.fromarray(frames[i]).resize((288,432),Image.Resampling.NEAREST);sheet.alpha_composite(im,(288*j,row*472+36));draw.text((288*j+8,row*472+8),f'{direction} phase{i}/16 · {i*50}ms',fill=(25,20,15))
   selected[direction]={'phaseIndices':[0,4,8,12],'sourceRects':[rects[i]for i in [0,4,8,12]]}
sheet.convert('RGB').save(O/'animated-v3-two-directions-four-poses.jpg',quality=95);alternatives=[]
for rel in ['public/assets/characters-walk-v1/manifest.json','public/assets/characters-walk-v1/animated-v2/manifest.json','public/assets/characters-walk-v1/east-mesh-pilot/manifest.json']:
 p=R/rel
 if not p.exists():continue
 q=json.load(open(p));dirs=q.get('directions',{});alternatives.append({'path':rel,'cameraVariants':list(q.get('cameraVariants',{})),'directionKeys':list(dirs),'walkFrameCounts':{d:len(v.get('clips',{}).get('walk',{}).get('frames',[]))for d,v in dirs.items()},'frameSize':q.get('frameSize'),'status':q.get('status')})
r={'integrationCommit':REV,'manifestSHA256':hashlib.sha256(raw).hexdigest(),'scope':'read-onlyactualatlases; notbrowser/inputQA','selectedContactSheet':selected,'actualV3':rows,'alternatives':alternatives,'recommendation':'KEEPexistinganimated-v3temporary; no newmodel/renderer/style/controller'};(O/'audit.json').write_text(json.dumps(r,indent=2)+'\n');print([(x['camera'],x['direction'],x['uniqueRGBAFrames'],min(x['adjacentChangedPixelCountsIncludingLoopSeam']))for x in rows]);print(alternatives)
