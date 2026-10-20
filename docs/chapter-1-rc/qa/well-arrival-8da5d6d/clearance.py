from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFilter
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;g=json.loads((R/'art/chapter-1-v9/packages/well/geometry.json').read_text());free=Image.new('L',(1672,941));d=ImageDraw.Draw(free)
for c in g['cells']:
 if c['terrain']is None or c['terrain']=='water':d.polygon([(p['x'],p['y'])for p in c['polygon']],fill=255)
fm=json.loads((R/'public/assets/characters-facing-v1/residents-facing-manifest.json').read_text())['characters']['teacher'];resident=json.loads((R/'public/assets/characters-v1/residents-manifest.json').read_text())['characters']['teacher'];checks=[]
for name,f in fm['frames'].items():
 scale=resident['sceneHeightPx']/f['frameSize'][1];im=Image.open(R/'public/assets/characters-facing-v1'/f['image']).getchannel('A');im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);alpha=Image.new('L',free.size);alpha.paste(im,(round(1320-f['footAnchor'][0]*scale),round(405-f['footAnchor'][1]*scale)));overlap=sum(v>0 for v in ImageChops.multiply(alpha,free).get_flattened_data());assert overlap==0;checks.append({'view':name,'feet':[1320,405],'fullNonzeroAlphaOverPlayableGroundWater':overlap})
flowers=Image.open(R/'art/chapter-1-v9/garden-well/layers/well-flowers-v1.png').getchannel('A');fc={c['id']:flowers.getpixel((round(c['center']['x']),round(c['center']['y'])))for c in g['cells']if c['terrain']=='flower'};assert len(fc)==14 and all(v>0 for v in fc.values());floweroverlap=sum(v>0 for v in ImageChops.multiply(flowers,free).get_flattened_data());flowerinterior=sum(v>0 for v in ImageChops.multiply(flowers,free.filter(ImageFilter.MinFilter(3))).get_flattened_data());assert flowerinterior==0
native=Image.open(R/'public/assets/chapter-1/v9/well/background.webp').convert('RGB');wide=Image.open(R/'public/assets/chapter-1/v9/well/wide.webp').convert('RGB');assert wide.crop((800,129,2472,1070)).tobytes()==native.tobytes()
unchanged={}
for path in ['art/blender/chapter-layouts/layout-adjustments.json','src/art-solutions.json','art/chapter-1-v9/packages/well/geometry.json']:
 old=subprocess.check_output(['git','show','d831f52:'+path],cwd=R);new=(R/path).read_bytes();assert old==new;unchanged[path]=hashlib.sha256(new).hexdigest()
(O/'clearance.json').write_text(json.dumps({'teacherActualViews':checks,'teacherViewCount':len(checks),'flower14CenterAlpha':fc,'flowerFullNonzeroAlphaOverRasterFreeWater':floweroverlap,'flowerFullNonzeroAlphaBeyond1pxFreeInterior':flowerinterior,'wideNativePixelExact':True,'nativeSize':native.size,'wideSize':wide.size,'unchangedFromPreAnchorFix':unchanged},indent=2)+'\n');print('PASS',len(checks),'actual teacher-view alphas,14flowers,widecrop,immutablegeometry')
