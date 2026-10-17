#!/usr/bin/env python3
"""Technical alpha crop/uniform resize/packing only. No drawing or mirroring."""
from pathlib import Path
import json
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'art/characters-facing-v1/rabbit-left-source-v3.png'
OUT=ROOT/'public/assets/characters-facing-v1'
im=Image.open(SOURCE).convert('RGBA')
a=im.getchannel('A')
# Ignore only near-invisible generated fringe for measurement, preserve original alpha.
bbox=a.point(lambda x:255 if x>=8 else 0).getbbox()
assert bbox
crop=im.crop(bbox)
# Same native height and foot coordinate system as approved idle (981 / 977).
height=969
crop=crop.resize((round(crop.width*height/crop.height),height),Image.Resampling.LANCZOS)
# Foot midpoint measured from the bottom 6% silhouette, avoiding airborne apron/tail.
feet=crop.getchannel('A').crop((0,round(height*.94),crop.width,height)).point(lambda x:255 if x>=32 else 0).getbbox()
assert feet
foot_x=(feet[0]+feet[2])/2
left=round(302-foot_x)
assert left>=0, 'needs wider canonical anchor contract, do not shift existing anchor'
frame=Image.new('RGBA',(max(604,left+crop.width+4),981))
frame.alpha_composite(crop,(left,8))
(OUT/'residents').mkdir(parents=True,exist_ok=True)
frame.save(OUT/'residents/rabbit-conversation-left.png')
manifest={'schemaVersion':1,'version':'residents-facing-pilot-v1','status':'pilot-awaiting-actual-scene-review','baseManifest':'characters-v1/residents-manifest.json','characters':{'rabbit':{'speaker':'Кролик','nativeHeightPx':981,'sceneHeightPx':108,'scale':108/981,'frames':{'conversation-left':{'image':'residents/rabbit-conversation-left.png','source':'art/characters-facing-v1/rabbit-left-source-v3.png','sourceRect':[0,0,*frame.size],'frameSize':list(frame.size),'footAnchor':[302,977],'facing':'left','mirrored':False}},'policy':{'idle':'retain-approved-characters-v1-idle','conversation':'choose-on-encounter-not-per-frame','productionApproved':False}}},'packing':{'sourceSize':list(im.size),'measuredAlphaBBox':list(bbox),'uniformResizeHeight':height,'packedOffset':[left,8],'alphaPreserved':True}}
(OUT/'residents-facing-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest['packing']))
print('output',frame.size,'alpha',frame.getchannel('A').getextrema())
