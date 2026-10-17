#!/usr/bin/env python3
"""Pack generated whole PNGs; preserve world-foot contract via frame metadata."""
from pathlib import Path
import json, sys
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'public/assets/characters-facing-v1'
BASE=json.loads((ROOT/'public/assets/characters-v1/residents-manifest.json').read_text())
MANIFEST=OUT/'residents-facing-manifest.json'
data=json.loads(MANIFEST.read_text())
activities={
    'rabbit': [('garden','garden-table')],
    'teacher': [('well','well-and-flowerbed')],
    'baker': [('bakery','bakery-work')],
    'squirrel': [('stream','stream-bank'),('mill','miller-meeting')],
    'miller': [('mill','mill-work')],
    'hedgehog': [('post','postal-work')],
}
for name in sys.argv[1:]:
    original=BASE['characters'][name]
    source=ROOT/f'art/characters-facing-v1/{name}-left-source-v1.png'
    im=Image.open(source).convert('RGBA')
    bbox=im.getchannel('A').point(lambda v:255 if v>=8 else 0).getbbox()
    assert bbox
    crop=im.crop(bbox)
    native=original['nativeHeightPx']
    height=native-12
    crop=crop.resize((round(crop.width*height/crop.height),height),Image.Resampling.LANCZOS)
    feet=crop.getchannel('A').crop((0,round(height*.96),crop.width,height)).point(lambda v:255 if v>=32 else 0).getbbox()
    assert feet
    foot_x=(feet[0]+feet[2])/2
    old_anchor=original['frames']['idle']['footAnchor']
    # If the new silhouette needs room left of old pixel anchor, enlarge frame
    # and anchor together. Runtime's world foot stays exactly where caller put it.
    anchor_x=max(old_anchor[0],round(foot_x)+4)
    left=round(anchor_x-foot_x)
    frame=Image.new('RGBA',(max(original['frames']['idle']['frameSize'][0],left+crop.width+4),native))
    frame.alpha_composite(crop,(left,8))
    frame.save(OUT/f'residents/{name}-conversation-left.png')
    data['characters'][name]={
        'speaker':original['speaker'],'nativeHeightPx':native,
        'sceneHeightPx':original['sceneHeightPx'],'scale':original['sceneHeightPx']/native,
        'frames':{'conversation-left':{
            'image':f'residents/{name}-conversation-left.png','source':str(source.relative_to(ROOT)),
            'sourceRect':[0,0,*frame.size],'frameSize':list(frame.size),
            'footAnchor':[anchor_x,native-4],'facing':'left','mirrored':False}},
        'policy':{'idle':'retain-approved-characters-v1-idle','conversation':'choose-on-encounter-not-per-frame','productionApproved':False},
        'packing':{'sourceSize':list(im.size),'measuredAlphaBBox':list(bbox),'uniformResizeHeight':height,'packedOffset':[left,8],'alphaPreserved':True}}
    print(name,frame.size,'anchor',(anchor_x,native-4),'sceneHeight',original['sceneHeightPx'])
for name,resident in data['characters'].items():
    resident['activity']=[{'scene':scene,'focus':focus,'idleFacing':'right','idleAsset':f'characters-v1/residents/{name}-idle.png'} for scene,focus in activities[name]]
    resident['meeting']={'availableAuthoredFacings':['right','left'],'conversationFrame':'conversation-left','selectOn':['encounter','dialogue-entry'],'continuousTracking':False,'mirrorAllowed':False,'worldFeet':'retain-caller-placement'}
data['status']='authored-views-awaiting-actual-scene-review'
MANIFEST.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
