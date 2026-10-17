#!/usr/bin/env python3
"""Technical packing of near-front authored meeting poses; no drawing."""
from pathlib import Path
import json
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'public/assets/characters-facing-v1'
path=OUT/'residents-facing-manifest.json'
data=json.loads(path.read_text())
for name in ['teacher','squirrel']:
    item=data['characters'][name]
    native=item['nativeHeightPx']
    source=ROOT/f'art/characters-facing-v1/{name}-front-source-v1.png'
    im=Image.open(source).convert('RGBA')
    bbox=im.getchannel('A').point(lambda v:255 if v>=8 else 0).getbbox()
    assert bbox
    crop=im.crop(bbox);height=native-12
    crop=crop.resize((round(crop.width*height/crop.height),height),Image.Resampling.LANCZOS)
    feet=crop.getchannel('A').crop((0,round(height*.96),crop.width,height)).point(lambda v:255 if v>=32 else 0).getbbox()
    assert feet
    fx=(feet[0]+feet[2])/2
    anchor=max(item['frames']['conversation-left']['footAnchor'][0],round(fx)+4)
    left=round(anchor-fx)
    frame=Image.new('RGBA',(max(item['frames']['conversation-left']['frameSize'][0],left+crop.width+4),native))
    frame.alpha_composite(crop,(left,8));frame.save(OUT/f'residents/{name}-conversation-front.png')
    item['frames']['conversation-front']={'image':f'residents/{name}-conversation-front.png','source':str(source.relative_to(ROOT)),'sourceRect':[0,0,*frame.size],'frameSize':list(frame.size),'footAnchor':[anchor,native-4],'facing':'front-slight-right','mirrored':False,'packing':{'sourceSize':list(im.size),'measuredAlphaBBox':list(bbox),'uniformResizeHeight':height,'packedOffset':[left,8],'alphaPreserved':True}}
    item['meeting']['availableAuthoredFacings']=['right','left','front-slight-right']
    item['meeting']['arrivalFrame']='conversation-front'
    item['meeting']['arrivalUse']={'scene':'well' if name=='teacher' else 'mill','reason':'Ruta goal lies in front and slightly right of this placement'}
    print(name,frame.size,'footAnchor',[anchor,native-4],'sceneHeight',item['sceneHeightPx'])
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
