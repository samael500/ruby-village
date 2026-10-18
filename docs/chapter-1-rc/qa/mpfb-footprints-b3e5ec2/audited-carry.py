from pathlib import Path
import json,hashlib
import os
V=os.environ.get('RUBY_MPFB_PIVOT_VARIANT','right60');R=Path('/tmp/ruby-qa-pivot-footprints');O=R/'docs/chapter-1-rc/qa/mpfb-footprints-b3e5ec2'/V;source=R/'art/characters-mpfb-v1/motion/pivot-variants'/V/'mpfb-compact-pivot-technical.blend';before=hashlib.sha256(source.read_bytes()).hexdigest();count=41 if V=='right60'else 81
for kind in ['arm','grip']:
 p=R/f'scripts/mpfb-motion-{kind}-check.py';text=p.read_text().replace("ROOT=Path(__file__).resolve().parents[1]","ROOT=Path('/tmp/ruby-qa-pivot-footprints')")
 old="OUT=ROOT/'art/characters-mpfb-v1/motion/pilot';bpy.ops.wm.open_mainfile(filepath=str(OUT/'mpfb-walk-technical.blend'))"
 new=f"""SOURCE=ROOT/'art/characters-mpfb-v1/motion/pivot-variants/{V}';bpy.ops.wm.open_mainfile(filepath=str(SOURCE/'mpfb-compact-pivot-technical.blend'));pivot=json.loads((SOURCE/'manifest.json').read_text())
for n,a in pivot['turnActions'].items():bpy.data.objects[n].animation_data.action=bpy.data.actions[a]
OUT=ROOT/'docs/chapter-1-rc/qa/mpfb-footprints-b3e5ec2/{V}'"""
 assert old in text;text=text.replace(old,new).replace('range(1,25)',f'range(1,{count+1})').replace('range(1,26)',f'range(1,{count+1})');exec(compile(text,str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
print('SOURCE_UNCHANGED',before)
