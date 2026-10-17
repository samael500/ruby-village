"""Fresh Blender-process reopen and actual weighted deformation check; not artistic or gait QA."""
from pathlib import Path
import bpy,json,math
r=Path(__file__).resolve().parents[1];p=r/'art/characters-mpfb-v1/smoke';bpy.ops.wm.open_mainfile(filepath=str(p/'ruta-mpfb-smoke.blend'));human=bpy.data.objects['Ruta.MPFB.Body'];rig=bpy.data.objects['Ruta.MPFB.StandardRig'];deps=bpy.context.evaluated_depsgraph_get()
def positions():
 bpy.context.view_layer.update();return [v.co.copy()for v in human.evaluated_get(deps).data.vertices]
a=positions();bone=rig.pose.bones['lowerleg01.L'];old=bone.rotation_euler.copy();bone.rotation_euler.x=.2;b=positions();changes=[(x-y).length for x,y in zip(a,b)];bone.rotation_euler=old;bpy.context.view_layer.update();assert max(changes)>.001
report={'reopen':'PASS','standardRigBones':len(rig.data.bones),'armatureModifier':any(m.type=='ARMATURE'and m.object==rig for m in human.modifiers),'actualPoseProbe':{'bone':'lowerleg01.L','rotationRadians':.2,'deformedVisibleVertices':sum(d>1e-6 for d in changes),'maximumDisplacementMeters':max(changes)},'restPoseRestoredInMemory':True,'originalBlendNotOverwritten':True,'artisticAppearance':'NOT_TESTED','gait':'NOT_TESTED'}
assert report['armatureModifier'];(p/'reopen-check.json').write_text(json.dumps(report,indent=2)+'\n');print('RUBY_MPFB_REOPEN',json.dumps(report))
