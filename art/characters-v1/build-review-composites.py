"""Generate explicitly labelled review composites; never production screenshots.
Usage: python3 art/characters-v1/build-review-composites.py /path/to/courtyard.png /path/to/layers
"""
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
import json,sys,hashlib
R=Path(__file__).resolve().parents[2];A=R/'public/assets/characters-v1';O=R/'docs/chapter-1-rc/characters/residents';O.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
res=json.loads((A/'residents-manifest.json').read_text());poses=json.loads((A/'poses-manifest.json').read_text());pilot=json.loads((A/'manifest.json').read_text())['characters']['ruta']
background=Path(sys.argv[1]);layers=Path(sys.argv[2]);base=Image.open(background).convert('RGBA');assert base.size==(1672,941)
foreground=Image.open(layers/'foreground-fixed.png').convert('RGBA');gate=Image.open(layers/'gate-closed.png').convert('RGBA')
def draw_actor(canvas,f,foot,scale):
 im=Image.open(A/f['image']).convert('RGBA');size=(round(im.width*scale),round(im.height*scale));im=im.resize(size,Image.Resampling.LANCZOS);ax,ay=f['footAnchor'];canvas.alpha_composite(im,(round(foot[0]-ax*scale),round(foot[1]-ay*scale)))
# Uniform shadows remain separate from character alpha assets.
def ground_shadow(canvas,foot,width):
 sh=Image.new('RGBA',canvas.size);d=ImageDraw.Draw(sh);x,y=foot;d.ellipse((x-width,y-3,x+width,y+4),fill=(54,37,20,48));canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
def finish(canvas):
 canvas.alpha_composite(foreground);canvas.alpha_composite(gate);return canvas
# Actual alpha-edge review on three independent backdrops, sprite and real bust.
for color,label in [('#fbfaf6','light'),('#17232b','dark'),('#7fb78b','green')]:
 sheet=Image.new('RGB',(1800,1000),color);d=ImageDraw.Draw(sheet)
 for i,(id,c) in enumerate(res['characters'].items()):
  x=i*300;d.text((x+10,10),c['speaker'],font=font,fill=('#fff' if label=='dark' else '#25251e'))
  for which,box in [('idle',(x+20,55,260,540)),('portrait',(x+15,620,270,330))]:
   im=Image.open(A/c['frames'][which]['image']).convert('RGBA');im.thumbnail(box[2:],Image.Resampling.LANCZOS);sheet.paste(im,(box[0]+(box[2]-im.width)//2,box[1]),im)
 sheet.save(O/f'alpha-{label}.jpg',quality=92)
# Compare relative scale in the accepted courtyard, with intact foreground masks.
line=base.copy();items=[('ruta',pilot['frames']['idle-pilot'],136/pilot['frames']['idle-pilot']['frameSize'][1])]+[(id,c['frames']['idle'],c['scale'])for id,c in res['characters'].items()]
for i,(id,f,scale) in enumerate(items):
 foot=(560+i*118,600);ground_shadow(line,foot,14);draw_actor(line,f,foot,scale)
finish(line).convert('RGB').save(O/'scale-in-accepted-courtyard.jpg',quality=94)
# Six separate semantic compositions. Orchard uses an explicitly recorded existing v8 background.
orchard=R/'public/assets/chapter-1/v8/02-orchard-open.jpg'
for st in poses['staging']:
 idx=st['frameIndex'];scene=Image.open(orchard).convert('RGBA') if st['scene']=='orchard' else base.copy()
 pose=st['pose'];f=pilot['frames']['idle-pilot'] if pose=='idle-pilot' else poses['frames'][pose];scale=136/f['frameSize'][1] if pose=='idle-pilot' else f['scale']
 ground_shadow(scene,st['foot'],15);draw_actor(scene,f,st['foot'],scale)
 if st['scene']!='orchard':finish(scene)
 # Review camera crops are applied to the entire scene/actor together.
 crop=st.get('cameraReviewCrop')
 if crop:scene=scene.crop((crop[0],crop[1],crop[0]+crop[2],crop[1]+crop[3])).resize((1672,941),Image.Resampling.LANCZOS)
 scene.convert('RGB').save(O/f'prologue-{idx+1:02}-scene-composite.jpg',quality=94)
# Pose identity comparison at common sheet scale, not per-pose height stretching.
sheet=Image.new('RGB',(2000,650),'#ece6d8');d=ImageDraw.Draw(sheet)
for i,id in enumerate(['accepted-idle','ruta-basket','ruta-adjust-satchel','ruta-surprised','ruta-crouch-basket']):
 f=pilot['frames']['idle-pilot'] if id=='accepted-idle' else poses['frames'][id];scale=.65*768/970 if id=='accepted-idle' else .65
 im=Image.open(A/f['image']);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);sheet.paste(im,(i*400+40,570-round(f['footAnchor'][1]*scale)),im);d.text((i*400+10,600),id,font=font,fill='#30281e')
sheet.save(O/'ruta-poses-scale-review.jpg',quality=94)
provenance={'type':'offline scene composites, not production screenshots','courtyardSource':str(background),'courtyardSHA256':hashlib.sha256(background.read_bytes()).hexdigest(),'foregroundSource':str(layers),'orchardSource':str(orchard),'notes':'No grid/solution integration claimed; final game staging belongs to #47/#46. Existing v8 orchard used pending new scene package.'}
(O/'composite-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
print('3 alpha sheets, courtyard scale review,6 semantic composites, pose scale review')
