"""Reuse accepted actual geometry auditors on41 fresh pivot poses, without source writes."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for name in ['arm','grip']:
 script=ROOT/f'scripts/mpfb-motion-{name}-check.py';text=script.read_text()
 original="OUT=ROOT/'art/characters-mpfb-v1/motion/pilot';bpy.ops.wm.open_mainfile(filepath=str(OUT/'mpfb-walk-technical.blend'))"
 replacement="OUT=ROOT/'art/characters-mpfb-v1/motion/pivot-study';bpy.ops.wm.open_mainfile(filepath=str(OUT/'mpfb-compact-pivot60-technical.blend'));pivot_meta=json.loads((OUT/'manifest.json').read_text())\nfor pivot_name,pivot_action in pivot_meta['turnActions'].items():bpy.data.objects[pivot_name].animation_data.action=bpy.data.actions[pivot_action]"
 assert original in text;text=text.replace(original,replacement).replace('range(1,25)','range(1,42)').replace('range(1,26)','range(1,42)')
 exec(compile(text,str(script),'exec'),{'__file__':str(script),'__name__':'__main__'})
