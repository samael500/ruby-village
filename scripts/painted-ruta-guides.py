"""Deterministic transparent pose sheets; no artistic pixel modification."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/painted-ruta-guides-v1';OUT.mkdir(exist_ok=True)
SOURCE=ROOT/'art/ready-character-six-v1/assets/base-e.webp'
atlas=Image.open(SOURCE).convert('RGBA');keys=list(range(0,24,3));anchor=[128.,258.42965602874756]
full=atlas.crop((0,0,1536,1280));full.save(OUT/'walk-e24-guide.png')
key=Image.new('RGBA',(1536,960));rows=[]
for slot,i in enumerate(keys):
 rect=[i%6*256,i//6*320,256,320];frame=atlas.crop((rect[0],rect[1],rect[0]+256,rect[1]+320));origin=[slot%4*384,slot//4*480]
 key.paste(frame.resize((384,480),Image.Resampling.LANCZOS),tuple(origin))
 rows.append({'slot':slot,'walkFrameIndex':i,'sourceFrame':40*i/24,'sourceAtlasRect':rect,'keyCellOrigin':origin,'rootKeySheet':[origin[0]+192,origin[1]+anchor[1]*1.5]})
key.save(OUT/'walk-e8-key-guide.png')
report={'status':'pose-guides-only-not-painted-Ruta','sourceAtlas':str(SOURCE.relative_to(ROOT)),'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'sourceAction':'Walk','cycleDurationMs':1666.6666666666667,'frameCount':24,'frameSize':[256,320],'rootLocal':anchor,'fullSheet':{'file':'walk-e24-guide.png','size':[1536,1280],'columns':6,'rows':4},'keySheet':{'file':'walk-e8-key-guide.png','size':[1536,960],'cellSize':[384,480],'columns':4,'rows':2,'uniformScale':1.5,'rootLocal':[192,anchor[1]*1.5],'resampler':'Pillow LANCZOS'},'frames':rows,'perFrameCropOrTranslation':False,'artisticModification':False,'checks':{}}
for name in ['walk-e24-guide.png','walk-e8-key-guide.png']:
 im=Image.open(OUT/name);assert im.mode=='RGBA';assert im.getextrema()[3][0]==0
 report['checks'][name]={'sha256':hashlib.sha256((OUT/name).read_bytes()).hexdigest(),'alphaBBox':im.getbbox(),'transparentPixelCount':sum(v==0 for v in im.getchannel('A').getdata())}
for i in range(24):
 x=i%6*256;y=i//6*320
 assert full.crop((x,y,x+256,y+320)).tobytes()==atlas.crop((x,y,x+256,y+320)).tobytes()
report['checks']['walk24ExactAtlasRGBAEquality']=True
(OUT/'guide-contract.json').write_text(json.dumps(report,indent=2)+'\n')
