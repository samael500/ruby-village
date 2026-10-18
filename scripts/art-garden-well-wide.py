"""Register real builtin outpaint and apply painted decorative seam pixels only."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import json,sys,hashlib
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'art/chapter-1-v9';OWN=ART/'garden-well';OUT=OWN/'outpaint'
scene=sys.argv[1] if len(sys.argv)>1 else 'garden'
PUBLIC=ROOT/f'public/assets/chapter-1-garden-well/{scene}'
def register(source):
    im=Image.open(source).convert('RGB');scale=3272/im.width
    size=(3272,round(im.height*scale));im=im.resize(size,Image.Resampling.LANCZOS)
    assert im.height>=1200
    top=(im.height-1200)//2
    return im.crop((0,top,3272,top+1200)),{'sourceSize':list(Image.open(source).size),'uniformScale':scale,'scaledSize':list(size),'verticalCropStart':top}
generated,registration=register(OUT/f'{scene}-seam-painted-v1.png')
wide,base_registration=register(OUT/f'{scene}-wide-source-v1.png')
core=Image.open(OWN/f'{scene}-native-v1.png').convert('RGB')
wide.paste(core,(800,129))
layout=json.loads((ART/f'packages/{scene}/geometry.json').read_text())
guard=Image.new('L',core.size);d=ImageDraw.Draw(guard)
for cell in layout['cells']:
    if cell['terrain'] is None:d.polygon([(p['x'],p['y']) for p in cell['polygon']],fill=255)
guard=guard.filter(ImageFilter.MaxFilter(13))
if scene=='well':
    # Preserve complete original architecture, including roof/chimney high tips.
    d=ImageDraw.Draw(guard)
    d.rectangle((100,45,480,340),fill=255)
    d.rectangle((1190,45,1530,420),fill=255)
mask=Image.new('L',(3272,1200));p=mask.load()
for y in range(1200):
    for x in range(3272):
        a=x-800;b=y-129
        if 0<=a<1672 and 0<=b<941:
            distance=min(a,b,1671-a,940-b);t=max(0,1-distance/72)
            if guard.getpixel((a,b)):t=0
        else:
            distance=max(-a,a-1671,-b,b-940,0);t=min(1,max(0,(192-distance)/80))
        p[x,y]=round(255*t*t*(3-2*t))
result=Image.composite(generated,wide,mask)
delivered=result.crop((800,129,2472,1070))
diff=ImageChops.difference(core,delivered)
assert all(ImageChops.multiply(channel,guard).getbbox() is None for channel in diff.split())
assert diff.crop((72,72,1600,869)).getbbox() is None
if scene=='garden':
    for name in ['tree','table']:
        alpha=Image.open(OWN/f'layers/garden-{name}-v1.png').getchannel('A')
        assert all(ImageChops.multiply(c,alpha).getbbox() is None for c in diff.split())
result.save(OUT/f'{scene}-wide-painted-v1.png')
delivered.save(OUT/f'{scene}-native-painted-join-v1.png')
mask.save(OUT/f'{scene}-painted-join-mask.png')
PUBLIC.mkdir(parents=True,exist_ok=True)
result.save(PUBLIC/'wide.webp',lossless=True,method=6)
delivered.save(PUBLIC/'background.webp',lossless=True,method=6)
assert ImageChops.difference(Image.open(PUBLIC/'background.webp').convert('RGB'),Image.open(PUBLIC/'wide.webp').convert('RGB').crop((800,129,2472,1070))).getbbox() is None
overlay=result.copy();ImageDraw.Draw(overlay).rectangle((800,129,2471,1069),outline='#ff5060',width=2);overlay.save(OUT/f'{scene}-painted-registration-overlay.png')
manifest_path=PUBLIC.parent/f'{scene}-manifest.json';manifest=json.loads(manifest_path.read_text())
contract={'canvas':{'width':3272,'height':1200},'originalRect':{'x':800,'y':129,'width':1672,'height':941},'file':f'{scene}/wide.webp','registration':registration,'baseRegistration':base_registration,'joinBand':48,'paintedSeam':{'method':'builtin painted edit constrained to decorative source-pixel perimeter','coreBand':72,'outerAdjacency':192,'freePolygonGuard':6,'completeFreePolygonChangedPixels':0,'coreInteriorChangedPixels':0,'nativePropsChangedPixels':0,'wideOriginalRectBitExact':True},'status':'source-candidate-awaiting-actual-game'}
manifest['wide']=contract;manifest['status']='native-and-wide-awaiting-actual-game'
manifest['sourceBeforeJoin']=str((OWN/f'{scene}-native-v1.png').relative_to(ROOT))
manifest['source']=str((OUT/f'{scene}-native-painted-join-v1.png').relative_to(ROOT))
manifest['sourceSha256']=hashlib.sha256((OUT/f'{scene}-native-painted-join-v1.png').read_bytes()).hexdigest()
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(OUT/f'{scene}-painted-join-checks.json').write_text(json.dumps(contract,indent=2)+'\n')
print(json.dumps(contract))
