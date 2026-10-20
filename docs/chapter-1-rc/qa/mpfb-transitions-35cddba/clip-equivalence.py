import bpy,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent;SRC=ROOT/'art/characters-mpfb-v1/motion/transitions';meta=json.loads((SRC/'manifest.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(SRC/'mpfb-start-stop-technical.blend'));rig=bpy.data.objects['Ruta.MPFB.StandardRig'];scene=bpy.context.scene

def sample(bundle,f):
 for name,action in bundle.items():bpy.data.objects[name].animation_data.action=bpy.data.actions[action]
 scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();r=rig.evaluated_get(bpy.context.evaluated_depsgraph_get());return {'pose':[v for b in r.pose.bones for row in b.matrix for v in row],'controls':[v for name in bundle if name!=rig.name for v in bpy.data.objects[name].location],'root':list(r.matrix_world.translation)}
results=[]
for lead in ['L','R']:
 for kind,n,start in [('start',49,1),('stop',49,37),('settle',25,49)]:
  key=kind+'-'+lead if kind!='settle'else'settle';errors=[];controls=[];offsets=[]
  for i in range(n):
   f=1+i/4;a=sample(meta['clips'][key]['actionBundle'],f);b=sample(meta['demos'][lead]['actionBundle'],start+i/4);errors.append(max(abs(x-y)for x,y in zip(a['pose'],b['pose'])));controls.append(max(abs(x-y)for x,y in zip(a['controls'],b['controls'])));offsets.append([y-x for x,y in zip(a['root'],b['root'])])
  variation=max(abs(row[k]-offsets[0][k])for row in offsets for k in range(3));assert max(errors)<1e-4 and max(controls)<1e-5 and variation<1e-6
  results.append({'lead':lead,'clip':key,'actualQuarterSamples':n,'maxRootRelativeBoneMatrixDeltaFromDemo':max(errors),'maxHelperLocalDeltaFromDemo':max(controls),'constantWorldRootOffset':offsets[0],'maxRootOffsetVariation':variation})
idle=[sample(meta['clips']['idle']['actionBundle'],1+i/4)for i in range(25)];idleError=max(abs(x-y)for row in idle for x,y in zip(row['pose'],idle[0]['pose']));assert idleError<1e-7
(OUT/'clip-equivalence.json').write_text(json.dumps({'method':'All saved standalone start/stop/settle quarter-samples compared to actual bundled demo sections, allowing only constant global root translation. All three actions including both thumb controls activated; source pose/action data not rebuilt.','clips':results,'idleQuarterSamples':25,'idleBoneMatrixVariation':idleError,'sourceActionsPresent':all(a in bpy.data.actions for a in meta['sourceActions'].values())},indent=2)+'\n');print('PASS allstandaloneclipinteriors match demos withconstantroot offsets, idle stable')
