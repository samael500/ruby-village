"""One uniform painted-source registration; no runtime/CSS adjustment."""
from pathlib import Path
from PIL import Image,ImageChops,ImageStat
import json,hashlib
root=Path(__file__).resolve().parents[1];base=root/'art/chapter-1-v9';out=base/'layers/water/mill-pilot'
source=base/'candidates/mill-wide-generated-v2.png'
wide=Image.open(source).convert('RGB')
reference=out/'native-registration-reference.png'
native=Image.open(reference if reference.exists() else out/'native-background.png').convert('RGB')
def error(a,b):return sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)
small=native.resize((209,118));best=(float('inf'),None)
for n in range(84,109,2):
    scale=n/100;candidate=wide.resize((round(512*scale),round(200*scale)))
    for y in range(18,60,2):
        for x in range(108,175,2):
            value=error(small,candidate.crop((x,y,x+209,y+118)))
            if value<best[0]:best=(value,(scale,x,y))
scale,cx,cy=best[1]
quarter=native.resize((418,235));fine=(float('inf'),None)
for n in range(round(scale*200)-4,round(scale*200)+5):
    scale=n/200;candidate=wide.resize((round(1024*scale),round(400*scale)))
    for y in range(cy*2-8,cy*2+9):
        for x in range(cx*2-8,cx*2+9):
            value=error(quarter,candidate.crop((x,y,x+418,y+235)))
            if value<fine[0]:fine=(value,(scale,x,y))
scale,x,y=fine[1];translation=[1212-4*x,329-4*y]
delivery=[round(4096*scale),round(1600*scale)]
assert translation[0]<=412 and translation[1]<=200
assert translation[0]+delivery[0]>=3684 and translation[1]+delivery[1]>=1400
fit={'method':'single uniform source-level affine fitted to nativecore at1/4 scale; exact native board and building restored bydeliverybuilder; join/art/game review pending','source':str(source.relative_to(root)),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceNativeSize':list(wide.size),'rgbMeanAbsoluteError':fine[0]/3,'scale':scale,'sourceCoreXAtQuarter':x,'sourceCoreYAtQuarter':y,'translation':translation,'registeredPaintSize':delivery,'coverage':'entire3272x1200crop covered by painted source; no blank fill/reflection/repeated edge strips'}
(out/'wide-registration-fit.json').write_text(json.dumps(fit,indent=2)+'\n')
print(json.dumps(fit,indent=2))
