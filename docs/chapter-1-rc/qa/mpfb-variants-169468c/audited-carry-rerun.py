from pathlib import Path
import json,hashlib
R=Path('/tmp/ruby-qa-turn-variants');O=R/'docs/chapter-1-rc/qa/mpfb-variants-169468c/pivot';source=R/'art/characters-mpfb-v1/motion/pivot-study/mpfb-compact-pivot60-technical.blend';before=hashlib.sha256(source.read_bytes()).hexdigest()
for kind in ['arm','grip']:
 p=R/f'scripts/mpfb-motion-{kind}-check.py';text=p.read_text().replace("ROOT=Path(__file__).resolve().parents[1]","ROOT=Path('/tmp/ruby-qa-turn-variants')")
 old="OUT=ROOT/'art/characters-mpfb-v1/motion/pilot';bpy.ops.wm.open_mainfile(filepath=str(OUT/'mpfb-walk-technical.blend'))"
 new="""SOURCE=ROOT/'art/characters-mpfb-v1/motion/pivot-study';bpy.ops.wm.open_mainfile(filepath=str(SOURCE/'mpfb-compact-pivot60-technical.blend'));pivot=json.loads((SOURCE/'manifest.json').read_text())
for n,a in pivot['turnActions'].items():bpy.data.objects[n].animation_data.action=bpy.data.actions[a]
OUT=ROOT/'docs/chapter-1-rc/qa/mpfb-variants-169468c/pivot'"""
 assert old in text;text=text.replace(old,new).replace('range(1,25)','range(1,42)').replace('range(1,26)','range(1,42)');exec(compile(text,str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
print('SOURCE_UNCHANGED',before)
