"""Seven disjoint RGBA crops from one painted charoite progress source."""
from pathlib import Path
from PIL import Image,ImageChops
import json,math,hashlib
R=Path(__file__).resolve().parents[1];A=R/'art/chapter-map-v2';D=R/'public/assets/chapter-map-v2';E=R/'docs/chapter-1-rc/art/map-paving';base=Image.open(A/'map-base-candidate.png').convert('RGBA');paint=Image.open(A/'generated-charoite-03.png').convert('RGBA').resize((1000,400),Image.Resampling.LANCZOS);mask=Image.open(A/'painted-paving-and-grass-mask.png');protect=Image.open(A/'protected-landmarks.png');routes=json.loads((A/'routes.json').read_text())['routes'];samples=[r['samples'][::5]+[r['end']]for r in routes]
# Actual bank/causeway painting, while immutable original endpoints stay fixed.
line=[(932,292),(910,277),(886,274),(835,270),(786,273),(750,283),(728,299),(696,308),(663,319),(626,324)];samples[4]=[]
for a,b in zip(line,line[1:]):
 count=max(1,round(math.dist(a,b)/4))
 samples[4]+=[(a[0]+(b[0]-a[0])*i/count,a[1]+(b[1]-a[1])*i/count)for i in range(count)]
samples[4].append(line[-1]);alphas=[Image.new('L',(1000,400))for _ in routes];loads=[a.load()for a in alphas];ma=mask.load()
for y in range(400):
 for x in range(1000):
  alpha=ma[x,y]
  if alpha:
   owner=min(range(7),key=lambda i:min((x-p[0])**2+(y-p[1])**2 for p in samples[i]));loads[owner][x,y]=alpha
complete=base.copy();partial=base.copy();entries={};seen=Image.new('L',(1000,400))
for i,(route,alpha)in enumerate(zip(routes,alphas)):
 assert ImageChops.multiply(alpha,protect).getbbox()is None;assert ImageChops.multiply(alpha,seen).getbbox()is None;seen=ImageChops.lighter(seen,alpha);patch=paint.copy();patch.putalpha(alpha);zero=Image.new('RGBA',patch.size);binary=alpha.point(lambda a:255 if a else 0);patch=Image.composite(patch,zero,binary);file='completed-'+route['id']+'.webp';patch.save(D/file,'WEBP',lossless=True,method=6);assert Image.open(D/file).getchannel('A').tobytes()==alpha.tobytes();patch.save(A/('completed-'+route['id']+'.png'));complete=Image.alpha_composite(complete,patch)
 if i<3:partial=Image.alpha_composite(partial,patch)
 entries[route['id']]={'file':file,'canvas':[1000,400],'alphaBBox':alpha.getbbox(),'bytes':(D/file).stat().st_size,'sha256':hashlib.sha256((D/file).read_bytes()).hexdigest(),'source':'art/chapter-map-v2/generated-charoite-03.png','overlapWithOtherRoutePixels':0}
assert seen.tobytes()==mask.tobytes();complete.convert('RGB').save(A/'map-completed-candidate.png');partial.convert('RGB').save(A/'map-partial-candidate.png');complete.convert('RGB').save(E/'map-completed.jpg',quality=96);partial.convert('RGB').save(E/'map-partial.jpg',quality=96);base.convert('RGB').save(E/'map-new.jpg',quality=96)
m=json.loads((D/'manifest.json').read_text());m['layers']['completedRoads']=entries;m['checks'].update(progressPatchCount=7,progressPatchAlphaExact=True,progressPatchOverlaps=0,protectedLandmarkProgressPixelsChanged=0);m['charoiteSourceSha256']=hashlib.sha256((A/'generated-charoite-03.png').read_bytes()).hexdigest();m['completedState']='single painted source, spatially partitioned; no SVG paving shapes';(D/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('7 exact-alpha disjoint progress patches; all-state composition ready')
