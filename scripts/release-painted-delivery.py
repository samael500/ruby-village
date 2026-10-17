"""Read-only delivery experiment; source paintings stay unchanged, no activation."""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image
import numpy as np
root=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=Path('/tmp/ruby-painted-delivery'));parser.add_argument('--quality',type=int,default=92);args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True);records=[]
for scene in ['gate','bakery','post','forest']:
 for name in ['background','wide']:
  source=root/f'public/assets/chapter-1-map-match/{scene}/{name}.webp';image=Image.open(source).convert('RGBA');target=args.out/f'{scene}-{name}-q{args.quality}.webp';image.save(target,'WEBP',quality=args.quality,method=6,exact=True)
  decoded=Image.open(target).convert('RGBA');a=np.asarray(image).astype(float);b=np.asarray(decoded).astype(float);mse=float(np.mean((a[:,:,:3]-b[:,:,:3])**2));records.append({'scene':scene,'file':name,'sourceBytes':source.stat().st_size,'q92Bytes':target.stat().st_size,'alphaExact':bool(np.array_equal(a[:,:,3],b[:,:,3])),'psnrDb':round(float(10*np.log10(255**2/mse)),2),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scope':'delivery compression experiment only; not active or visually accepted'})
assert all(r['alphaExact'] for r in records)
(args.out/'report.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps({'sourceBytes':sum(r['sourceBytes'] for r in records),'deliveryBytes':sum(r['q92Bytes'] for r in records),'quality':args.quality,'active':False}))
