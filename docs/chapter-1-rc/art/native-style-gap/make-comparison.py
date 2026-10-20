from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
ROOT=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
# Fixed whole-image viewing scales per asset group, unchanged across00/23. No anatomy registration.
native=ROOT/'art/ruta-native-volume-front-proof-v1/renders/front-proof/front-proof/walk';raw=ROOT/'art/ruta-native-painted-sprites-v2/full48/painted-sheet-v1.png';canonical=ROOT/'public/assets/characters-v1/ruta-idle-pilot.png';panels=[];provenance=[]
for name,im,path,scale,rect in [('Canonical accepted appearance',Image.open(canonical),canonical,.45,None)]+[(f'Native front phase{i:02}',Image.open(native/f'{i:02}.png'),native/f'{i:02}.png',1,None)for i in [0,23]]+[(f'Painted v2 phase{i:02} (profile)',Image.open(raw).crop(((i%8)*162,30+(i//8)*200,(i%8+1)*162,30+(i//8+1)*200)),raw,2.4,[(i%8)*162,30+(i//8)*200,162,200])for i in [0,23]]:
 im=im.convert('RGBA');view=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);panel=Image.new('RGBA',(512,720),(233,227,212,255));panel.alpha_composite(view,((512-view.width)//2,70));d=ImageDraw.Draw(panel);d.text((12,12),name,fill=(30,25,20));d.text((12,34),f'ONE group scale {scale}; whole source, no fit',fill=(30,25,20));panels.append(panel);provenance.append({'label':name,'source':str(path.relative_to(ROOT)),'sourceSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'fixedViewingScale':scale,'sourceRectXYWH':rect,'wholeCanvasNoPerFrameFit':True})
full=Image.new('RGB',(512*len(panels),720))
for i,p in enumerate(panels):full.paste(p.convert('RGB'),(i*512,0))
full.save(O/'appearance-side-by-side.jpg',quality=95)
# Exact same fixed view comparison focused by a COMMON canvas crop of top area, never fitted by anatomy.
full.crop((0,70,2560,390)).save(O/'upper-body-common-view-crop.jpg',quality=95)
(O/'sources-and-view-transforms.json').write_text(json.dumps({'purpose':'view-only mechanicalcomparison; no sprite/model edits','sourceNativeProofCommit':'ac1aa06','nativeYaw':0,'paintedV2Yaw':'illustratedprofile, differsfromnativefront; notangle-equivalentlikenessmeasurement','canonicalPose':'acceptedstatic3quarterportrait, notmatchingwalkframe','groupScales':{'canonical':.45,'native00and23':1,'painted00and23':2.4},'panels':provenance},indent=2)+'\n')
