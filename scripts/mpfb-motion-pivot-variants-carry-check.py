"""Reuse accepted actual geometry auditors on41 fresh pivot poses, without source writes."""
from pathlib import Path
import hashlib,json,os
ROOT=Path(__file__).resolve().parents[1];VARIANT=os.environ.get('RUBY_MPFB_PIVOT_VARIANT','right60');assert VARIANT in ['right60','left120','right120'];PIVOT=ROOT/'art/characters-mpfb-v1/motion/pivot-variants'/VARIANT;SOURCE=PIVOT/'mpfb-compact-pivot-technical.blend';BEFORE=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
duration=json.loads((PIVOT/'manifest.json').read_text())['durationMs'];count=int(duration/30)+1
for name in ['arm','grip']:
 script=ROOT/f'scripts/mpfb-motion-{name}-check.py';text=script.read_text()
 original="OUT=ROOT/'art/characters-mpfb-v1/motion/pilot';bpy.ops.wm.open_mainfile(filepath=str(OUT/'mpfb-walk-technical.blend'))"
 replacement=f"OUT=ROOT/'art/characters-mpfb-v1/motion/pivot-variants/{VARIANT}';bpy.ops.wm.open_mainfile(filepath=str(OUT/'mpfb-compact-pivot-technical.blend'));pivot_meta=json.loads((OUT/'manifest.json').read_text())\nfor pivot_name,pivot_action in pivot_meta['turnActions'].items():bpy.data.objects[pivot_name].animation_data.action=bpy.data.actions[pivot_action]"
 assert original in text;text=text.replace(original,replacement).replace('range(1,25)',f'range(1,{count+1})').replace('range(1,26)',f'range(1,{count+1})').replace("'worldHeadRotationExcursionDegrees'","'rigLocalHeadRotationExcursionDegrees'")
 exec(compile(text,str(script),'exec'),{'__file__':str(script),'__name__':'__main__'})

arm=json.loads((PIVOT/'arm-satchel-check.json').read_text());grip=json.loads((PIVOT/'grip-torso-check.json').read_text());passed=max(arm['summary']['maxTrianglePairs'].values())==0 and max(grip['summary']['gripMaxTriangleIntersections'].values())==0
result={'sourceSha256Before':BEFORE,'sourceSha256After':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'actualPoseSamples':count,'armBagAndGripPass':passed,'armBag':arm['summary'],'grip':grip['summary']};assert result['sourceSha256After']==BEFORE;(PIVOT/'carry-check.json').write_text(json.dumps(result,indent=2)+'\n');print('PIVOT_CARRY_CHECK',passed)
