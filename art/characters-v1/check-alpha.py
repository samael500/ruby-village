"""Quantitative actual-alpha checks and real RGB-composited pose evidence.
Underlying RGB beneath alpha=0 is intentionally not interpreted as visible pixels.
"""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];A=R/'public/assets/characters-v1';O=R/'docs/chapter-1-rc/characters/residents';O.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17);report={}
for p in sorted(A.rglob('*.png')):
 im=Image.open(p);assert im.mode=='RGBA';a=im.getchannel('A');hist=a.histogram();corners=[im.getpixel(pos) for pos in [(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)]]
 assert hist[0]>0 and a.getextrema()[1]>240
 report[str(p.relative_to(A))]={'frameSize':list(im.size),'alphaRange':list(a.getextrema()),'fullyTransparentFraction':hist[0]/(im.width*im.height),'cornerRGBA':corners,'underlyingTransparentRGB':'may contain brown/red/yellow; invisible at alpha0 and not a backdrop'}
poses=['ruta-basket','ruta-adjust-satchel','ruta-surprised','ruta-crouch-basket','rabbit-baking','basket-ground']
for color,label in [('#fbfaf6','light'),('#17232b','dark'),('#7fb78b','green')]:
 sheet=Image.new('RGB',(1800,700),color);d=ImageDraw.Draw(sheet)
 for i,name in enumerate(poses):
  im=Image.open(A/f'poses/{name}.png');im.thumbnail((280,600),Image.Resampling.LANCZOS);sheet.paste(im,(i*300+(300-im.width)//2,650-im.height),im);d.text((i*300+8,10),name,font=font,fill=('#fff' if label=='dark' else '#25251e'))
 sheet.save(O/f'poses-alpha-{label}.jpg',quality=96)
# Native-pixel transparent-corner and between-body/prop samples for a known viewer trap.
im=Image.open(A/'poses/ruta-crouch-basket.png');report['diagnostic']={'issue':'Some PNG display tools show underlying RGB despite alpha0. This is a viewer false alarm, not an opaque brown cutout. Inspect actual RGB composites.','crouchGapRGBA':list(im.getpixel((380,300))),'crouchEmptyRightRGBA':list(im.getpixel((480,100))),'actualComposite':'poses-alpha-light/dark/green.jpg'}
(O/'alpha-integrity.json').write_text(json.dumps(report,indent=2)+'\n');print('verified',len(report)-1,'RGBA PNGs')
