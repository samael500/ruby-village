"""Package reviewed rig renders into compact lossless atlases; deterministic common crop/scale.
Sources remain full320px with packed .blend. No per-frame realignment or asymmetric mirroring.
"""
from pathlib import Path
from PIL import Image
import argparse,json,math,hashlib
root=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--input',default='art/characters-walk-v1/export-v2');parser.add_argument('--output',default='public/assets/characters-walk-v1/animated-v2');parser.add_argument('--scale',type=float,default=.75);args=parser.parse_args();source=root/args.input;out=root/args.output;out.mkdir(parents=True,exist_ok=True);manifest=json.loads((source/'manifest.json').read_text());crop=(64,0,256,288);width=round((crop[2]-crop[0])*args.scale);height=round((crop[3]-crop[1])*args.scale);anchor=[(160-crop[0])*args.scale,(256-crop[1])*args.scale];files={}
variants=manifest.get('cameraVariants',{'base':{'directions':manifest['directions']}})
for variant,variant_spec in variants.items():
 for direction,spec in variant_spec['directions'].items():
  frames=[f for clip in spec['clips'].values() for f in clip['frames']];rows=math.ceil(len(frames)/8);atlas=Image.new('RGBA',(width*8,height*rows));cells={}
  for index,frame in enumerate(frames):
   path=root/frame['file'];im=Image.open(path).convert('RGBA');alpha=im.getchannel('A').point(lambda a:255 if a>16 else 0);bounds=alpha.getbbox();assert bounds and bounds[0]>=crop[0] and bounds[1]>=crop[1] and bounds[2]<=crop[2] and bounds[3]<=crop[3],(direction,path,bounds,'common crop would lose painted pixels')
   patch=im.crop(crop).resize((width,height),Image.Resampling.LANCZOS);x=(index%8)*width;y=(index//8)*height;atlas.alpha_composite(patch,(x,y));frame.update(sourceFile=frame['file'],file=f'assets/characters-walk-v1/animated-v2/{variant}-{direction}.webp',sourceRect=[x,y,width,height],frameSize=[width,height],footAnchor=anchor)
  path=out/f'{variant}-{direction}.webp';atlas.save(path,'WEBP',lossless=True,method=6);files[path.name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,'atlasSize':list(atlas.size),'decodedRGBABytes':atlas.width*atlas.height*4}
manifest['cameraVariants']=variants;manifest['directions']=variants.get('base',next(iter(variants.values())))['directions']
manifest.update(status='full-set-candidate-requires-artistic-runtime-review',productionEnabled=False,frameSize=[width,height],footAnchor=anchor,nativeHeightPx=224*args.scale,sourceFrameSize=[320,320],sourceFootAnchor=[160,256],deliveryTransform={'crop':list(crop),'uniformScale':args.scale,'method':'one common crop and scale for ALL directions/states; lossless WebP atlas; originals retained'},files=files,decodedRGBABytes=sum(f['decodedRGBABytes'] for f in files.values()),compressedBytes=sum(f['bytes'] for f in files.values()))
for previous in out.glob('*.webp'):
 if previous.name not in files:previous.unlink()
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(f'{len(files)} direction atlases; {manifest["compressedBytes"]} compressed bytes, {manifest["decodedRGBABytes"]} decoded bytes')
