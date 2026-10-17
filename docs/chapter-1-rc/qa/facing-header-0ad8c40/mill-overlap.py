import json,re
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
page=json.loads((OUT/'independent-edges.json').read_text())[1]['pages'][4];s=page['ruta'][0]['frame'];scale=.7566418703506907;offset=1.447396386822561
v={k:float(re.search(r' '+k+r'="([^"]+)"',s)[1]) for k in ['x','y','width','height']};box={k:((val-offset)/scale if k=='x' else val/scale) for k,val in v.items()}
ruta=Image.open(ROOT/'public/assets/characters-walk-v1/animated-v3/base-ne.webp').crop((0,432,144,648)).getchannel('A');ruta=ruta.resize((round(box['width']),round(box['height'])));mask=Image.new('L',(1672,941));mask.paste(ruta,(round(box['x']),round(box['y'])))
a=page['actors'][1];x,y=1330,405;ix,iy,w,h=map(float,a['image']);squirrel=Image.open(ROOT/'public/assets/characters-facing-v1/residents/squirrel-conversation-front.png').getchannel('A').resize((round(w),round(h)));other=Image.new('L',mask.size);other.paste(squirrel,(round(x+ix),round(y+iy)));overlap=ImageChops.multiply(mask,other).point(lambda v:255 if v>32 else 0);count=sum(1 for v in overlap.getdata() if v)
assert count>0
(OUT/'mill-overlap.json').write_text(json.dumps({'finding':'F1 real mill arrival Ruta obscures squirrel','viewport':[1280,720],'rutaDirection':'ne','rutaNativeBox':box,'rutaFeet':[box['x']+box['width']/2,box['y']+box['height']*192/216],'squirrelNativeBox':{'x':x+ix,'y':y+iy,'width':w,'height':h},'squirrelFeet':[x,y],'overlappingAlphaNativePixelsGt32':count,'overlapBBox':overlap.getbbox(),'method':'actual recorded runtime image coordinates plus decoded authored sprite alpha; rounded to native scene pixels; breathing subpixel scale excluded'},indent=2)+'\n');overlap.save(OUT/'mill-overlap-mask.png');print('F1 confirmed alpha overlap',count)
