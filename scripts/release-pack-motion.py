"""Deterministic RGB delivery experiment; source atlas geometry stays exact."""
from pathlib import Path
from PIL import Image,ImageChops,ImageStat
import json,hashlib,copy,math
R=Path(__file__).resolve().parents[1];S=R/'public/assets/characters-walk-v1/animated-v2';D=R/'public/assets/characters-walk-v1/animated-v3';E=R/'docs/chapter-1-rc/release-motion-delivery';D.mkdir(exist_ok=True);E.mkdir(parents=True,exist_ok=True)
report={'sourceVersion':'animated-v2','quality':94,'alphaQuality':100,'method':6,'images':[],'frameAudit':[]};total=0
for p in sorted(S.glob('*.webp')):
 im=Image.open(p).convert('RGBA');row={'file':p.name,'sourceBytes':p.stat().st_size,'size':list(im.size),'sourceSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'experiments':{}}
 for q in [92,94]:
  out=D/p.name if q==94 else Path('/tmp')/('ruby-motion-q92-'+p.name);im.save(out,'WEBP',quality=q,alpha_quality=100,method=6,exact=True);got=Image.open(out).convert('RGBA');diff=ImageChops.difference(im,got);alphaExact=diff.getchannel('A').getbbox()is None;assert alphaExact
  # Error measured only where source is visible, because transparent RGB is irrelevant.
  mask=im.getchannel('A').point(lambda a:255 if a else 0);stat=ImageStat.Stat(diff.convert('RGB'),mask);mse=sum(x*x for x in stat.rms)/3
  row['experiments'][str(q)]={'bytes':out.stat().st_size,'alphaExact':alphaExact,'visibleRGBmae':sum(stat.mean)/3,'visibleRGBpsnr':10*math.log10(255**2/mse)if mse else None}
 report['images'].append(row);total+=p.stat().st_size
m=json.loads((S/'manifest.json').read_text());original=copy.deepcopy(m)
sourceImages={p.name:Image.open(p).convert('RGBA')for p in S.glob('*.webp')};deliveryImages={p.name:Image.open(p).convert('RGBA')for p in D.glob('*.webp')}
def visit(o):
 if isinstance(o,dict):
  if 'sourceRect'in o and 'file'in o:
   a=sourceImages[Path(o['file']).name];rect=o['sourceRect'];box=(rect[0],rect[1],rect[0]+rect[2],rect[1]+rect[3]);b=deliveryImages[Path(o['file']).name];assert a.crop(box).getchannel('A').tobytes()==b.crop(box).getchannel('A').tobytes();report['frameAudit'].append({'file':Path(o['file']).name,'sourceRect':rect,'footAnchor':o['footAnchor'],'alphaExact':True})
  for k,v in list(o.items()):
   if isinstance(v,str)and'animated-v2/'in v:o[k]=v.replace('animated-v2/','animated-v3/')
   else:visit(v)
 elif isinstance(o,list):
  for v in o:visit(v)
visit(m)
for name,meta in m['files'].items():
 p=D/name;meta['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();meta['bytes']=p.stat().st_size
# All non-delivery properties remain byte-for-byte equivalent as JSON values.
normalized=copy.deepcopy(m)
normalized['files']=original['files']
def sourcePaths(o):
 if isinstance(o,dict):return{k:sourcePaths(v)for k,v in o.items()}
 if isinstance(o,list):return[sourcePaths(v)for v in o]
 return o.replace('animated-v3/','animated-v2/')if isinstance(o,str)else o
assert sourcePaths(normalized)==original
report['semanticManifestEquality']=True
m['status']='optimized-delivery-of-source-v2';m['sourceStatus']=original['status'];m['deliveryEncoding']={'format':'WebP','quality':94,'alphaQuality':100,'sourceManifest':'assets/characters-walk-v1/animated-v2/manifest.json','geometryUnchanged':True};m['compressedBytes']=sum(p.stat().st_size for p in D.glob('*.webp'));(D/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');report.update(sourceBytes=total,deliveryBytes=m['compressedBytes'],decodedRGBABytes=sum(x['size'][0]*x['size'][1]*4 for x in report['images']),maxTextureSide=max(max(x['size'])for x in report['images']),framesAudited=len(report['frameAudit']));(E/'encoding-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['images','frameAudit']},indent=2))
