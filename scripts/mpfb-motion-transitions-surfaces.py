"""Fresh transition bundle playback with the accepted actual-geometry auditors."""
from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/transitions'
manifest=json.loads((OUT/'manifest.json').read_text())
# Execute unchanged measurement algorithms with explicit source/output/frame substitutions.
for label,source in [('grip','mpfb-motion-grip-check.py'),('arm','mpfb-motion-arm-check.py')]:
 code=(ROOT/'scripts'/source).read_text().replace("motion/pilot'","motion/transitions'").replace("mpfb-walk-technical.blend","mpfb-start-stop-technical.blend").replace('range(1,26)','range(1,56)').replace('range(1,25)','range(1,56)')
 for side in ['L','R']:
  insertion="\nfor object_name,action_name in "+repr(manifest['demos'][side]['actionBundle'])+".items():\n bpy.data.objects[object_name].animation_data.action=bpy.data.actions[action_name]\n"
  marker="body=bpy.data.objects"
  at=code.index(marker);run=code[:at]+insertion+code[at:]
  run=run.replace("'grip-torso-check.json'",repr('demo-'+side+'-grip-check.json')).replace("'arm-satchel-check.json'",repr('demo-'+side+'-arm-check.json'))
  exec(compile(run,str(ROOT/'scripts'/source),'exec'),{'__file__':str(ROOT/'scripts'/source),'__name__':'__main__'})
