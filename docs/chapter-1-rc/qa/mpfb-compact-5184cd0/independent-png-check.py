from pathlib import Path
from PIL import Image,ImageChops,ImageStat
import json,hashlib,math
R=Path('/tmp/ruby-qa-compact-view');D=R/'art/characters-mpfb-v1/motion/sixview-proof';O=R/'docs/chapter-1-rc/qa/mpfb-compact-5184cd0';rows=[]
for p in sorted(D.glob('*/*/*.png')):
 im=Image.open(p).convert('RGBA');a=im.getchannel('A');box=a.getbbox();assert im.size==(384,384);assert box and min(box[:2])>1 and max(box[2:])<383
 rows.append(dict(path=str(p.relative_to(D)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bounds=box,height=box[3]-box[1]))
assert len(rows)==24 and len({r['sha256']for r in rows})==24
# Verify E/W pixels are not simple mirrored derivatives, including asymmetrical satchel.
mirrors=[]
for g in ['base','calibrated-1']:
 for f in ['01','13']:
  e=Image.open(D/g/'e'/f'{f}.png').convert('RGBA');w=Image.open(D/g/'w'/f'{f}.png').convert('RGBA');diff=ImageChops.difference(e.transpose(Image.Transpose.FLIP_LEFT_RIGHT),w);mirrors.append(dict(group=g,frame=f,mirroredEqual=diff.getbbox() is None));assert diff.getbbox() is not None
(O/'independent-png-check.json').write_text(json.dumps(dict(records=rows,mirrorChecks=mirrors),indent=2)+'\n')
print('PNG PASS',len(rows),'height',min(r['height']for r in rows),max(r['height']for r in rows))
