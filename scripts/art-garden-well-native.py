"""Source-preserving garden/well registration; no procedural bitmap illustration."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import json,re,subprocess
from collections import deque
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'art/chapter-1-v9';OUT=ART/'garden-well'
for folder in ['layers','review']: (OUT/folder).mkdir(parents=True,exist_ok=True)
SIZE=(1672,941)
def geometry(name):return json.loads((ART/f'packages/{name}/geometry.json').read_text())
def polygon_mask(scene,kind=None,free=False):
    mask=Image.new('L',SIZE);d=ImageDraw.Draw(mask)
    for c in geometry(scene)['cells']:
        if (free and c['terrain'] is None) or (not free and c['terrain']==kind):d.polygon([(p['x'],p['y']) for p in c['polygon']],fill=255)
    return mask
def intersects(alpha,mask):return sum(v>8 for v in ImageChops.multiply(alpha,mask).getdata())
def overlay(scene,base,name):
    canvas=base.convert('RGBA');marks=Image.new('RGBA',SIZE);d=ImageDraw.Draw(marks)
    for c in geometry(scene)['cells']:
        pts=[(p['x'],p['y']) for p in c['polygon']];color=(230,60,65,65) if c['terrain'] else (30,170,240,25)
        d.polygon(pts,fill=color);d.line(pts+[pts[0]],fill=(235,65,70,190) if c['terrain'] else (15,140,230,150),width=1)
    Image.alpha_composite(canvas,marks).save(OUT/f'review/{name}-geometry.png')
def garden():
    base=Image.open(ART/'candidates/garden-clear-v1.png').convert('RGBA')
    tree=Image.open(ART/'candidates/apple-tree-prop-v1.png').convert('RGBA')
    # Native alpha-only erosion removes generated colored fringe; whole source preserved.
    tree.putalpha(tree.getchannel('A').filter(ImageFilter.MinFilter(5)))
    tree=tree.resize((588,490),Image.Resampling.LANCZOS)
    tree_layer=Image.new('RGBA',SIZE);tree_layer.alpha_composite(tree,(580,100))
    tree_layer.save(OUT/'layers/garden-tree-v1.png')
    # Segment the original tiny prop crop: green backdrop becomes alpha,
    # connected painted furniture/fruit survives (including the central leg).
    source=Image.open(ART/'candidates/garden-map-v1.png').convert('RGBA').crop((1030,375,1310,530))
    pix=list(source.getdata());w,h=source.size
    foreground=[not(g>r*.9 and g>b*1.2) or (min(r,g,b)>150 and max(r,g,b)-min(r,g,b)<80) for r,g,b,a in pix]
    seen=set();components=[]
    for start in range(w*h):
        if not foreground[start] or start in seen:continue
        seen.add(start);q=deque([start]);component=[]
        while q:
            i=q.popleft();component.append(i);x=i%w;y=i//w
            for j in [i-1 if x else -1,i+1 if x<w-1 else -1,i-w if y else -1,i+w if y<h-1 else -1]:
                if j>=0 and foreground[j] and j not in seen:seen.add(j);q.append(j)
        components.append(component)
    keep=set(i for c in components if len(c)>100 and max(i%w for i in c)<260 and max(i//w for i in c)<144 for i in c)
    alpha=Image.new('L',(w,h));alpha.putdata([255 if i in keep else 0 for i in range(w*h)])
    source.putalpha(alpha)
    source.save(OUT/'layers/table-native-cutout.png')
    # Source-owned dark green contact shadow beneath furniture, never a drawn
    # ellipse. Keep painted RGB texture and soften the extraction alpha only.
    shadow=Image.open(ART/'candidates/garden-map-v1.png').convert('RGBA').crop((1030,375,1310,530))
    shadow_alpha=[]
    for i,(r,g,b,a) in enumerate(shadow.getdata()):
        x=i%w;y=i//w
        shadow_alpha.append(round(max(0,min(110,(105-g)*2))) if 65<y<145 and 12<x<270 and i not in keep and g>r*.9 and g>b*1.1 else 0)
    shadow_mask=Image.new('L',(w,h));shadow_mask.putdata(shadow_alpha);shadow.putalpha(shadow_mask.filter(ImageFilter.GaussianBlur(1)))
    shadow.save(OUT/'layers/table-source-contact-shadow.png')
    table=Image.alpha_composite(shadow,source).resize((168,93),Image.Resampling.LANCZOS)
    table_layer=Image.new('RGBA',SIZE);table_layer.alpha_composite(table,(1215,170));table_layer.save(OUT/'layers/garden-table-v1.png')
    base=Image.alpha_composite(base,tree_layer);base=Image.alpha_composite(base,table_layer)
    base.save(OUT/'garden-native-v1.png');overlay('garden',base,'garden-native-v1')
    # A real full-alpha resident overlay, not a box/feet-only clearance claim.
    resident=Image.open(ROOT/'public/assets/characters-facing-v1/residents/rabbit-conversation-left.png').convert('RGBA')
    scale=108/981;resident=resident.resize((round(resident.width*scale),108),Image.Resampling.LANCZOS)
    rabbit=Image.new('RGBA',SIZE);rabbit.alpha_composite(resident,(round(1295-302*scale),round(265-977*scale)))
    Image.alpha_composite(base,rabbit).save(OUT/'review/garden-native-v1-rabbit.png')
    free=polygon_mask('garden',free=True).filter(ImageFilter.MinFilter(3))
    ground=Image.new('L',SIZE);ImageDraw.Draw(ground).rectangle((0,520,1671,940),fill=255)
    checks={'candidate':'garden-native-v1','status':'review-pending','treeUniformTransform':{'source':[1374,1145],'target':[588,490],'offset':[580,100],'crownClipping':False,'nativeAlphaErosionRadius':2},'table':{'sourceRect':[1030,375,280,155],'targetRect':[1215,170,168,93],'scale':.6,'count':1,'backdropGreenRemoved':True},'rabbitFeet':[1295,265],'fullFreeInteriorTolerancePx':1,'treeFullAlphaFreeOverlap':intersects(tree_layer.getchannel('A'),free),'treeGroundAlphaFreeOverlap':intersects(tree_layer.getchannel('A'),ImageChops.multiply(free,ground)),'tableAlphaFreeOverlap':intersects(table_layer.getchannel('A'),free),'rabbitFullAlphaFreeOverlap':intersects(rabbit.getchannel('A'),free)}
    (OUT/'review/garden-native-v1-checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks))
if __name__=='__main__':garden()
