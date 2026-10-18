"""Actual body/sole joins for180deg source recipes; no new blend or raster batch."""
from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];MOTION=ROOT/'art/characters-mpfb-v1/motion';OUT=MOTION/'pivot-variants'
registry={'left60':(MOTION/'pivot-study','mpfb-compact-pivot60-technical.blend')}
registry.update({v:(OUT/v,'mpfb-compact-pivot-technical.blend') for v in ['right60','left120','right120']})
def read(variant,f,externalYaw=0,idle=False):
 folder,name=registry[variant];meta=json.loads((folder/'manifest.json').read_text());source=folder/name;sha=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(source));rig=bpy.data.objects['Ruta.MPFB.StandardRig'];shoe=bpy.data.objects['Ruta.shoes01'];measure=shoe.copy();measure.data=shoe.data.copy();bpy.context.scene.collection.objects.link(measure)
 for mod in measure.modifiers:
  if mod.type=='SUBSURF':mod.show_viewport=False
 bundle=meta['idleActions'] if idle else meta['turnActions']
 for n,a in bundle.items():bpy.data.objects[n].animation_data.action=bpy.data.actions[a]
 bpy.context.scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();rig.rotation_euler.z+=externalYaw;bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();r=rig.evaluated_get(deps);s=measure.evaluated_get(deps);soles={}
 for side,sign in [('L',1),('R',-1)]:
  vs=[v for v in measure.data.vertices if v.co.x*sign>0];z=min(v.co.z for v in vs);ids=[v.index for v in vs if v.co.z<z+.008];soles[side]=[list(s.matrix_world@s.data.vertices[i].co) for i in ids]
 assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
 return {'sourceSha256':sha,'root':list(rig.matrix_world.translation),'yaw':rig.rotation_euler.z,'bones':{b.name:[list(row) for row in r.matrix_world@b.matrix] for b in r.pose.bones},'soles':soles}
def compare(a,b):return {'bodyWorldMatrixMaxElementError':max(abs(x-y) for n,rows in a['bones'].items() for ra,rb in zip(rows,b['bones'][n]) for x,y in zip(ra,rb)),'actualSoleVertexWorldMaxErrorMeters':max((Vector(x)-Vector(y)).length for s in ['L','R'] for x,y in zip(a['soles'][s],b['soles'][s]))}
results={}
for side in ['left','right']:
 first=read(side+'60',41);join=read(side+'120',1,first['yaw']);end=read(side+'120',81,first['yaw']);idle=read(side+'60',1,end['yaw'],True);checks={'internal60To120':compare(first,join),'exit180ToIdle':compare(end,idle)};assert max(r['bodyWorldMatrixMaxElementError'] for r in checks.values())<.0001 and max(r['actualSoleVertexWorldMaxErrorMeters'] for r in checks.values())<.0001
 results[side+'180']={'nativeYawRadiansActual':end['yaw'],'rootDeltaMetersActual':end['root'],'durationMs':3600,'clips':[side+'60',side+'120'],'sources':[first['sourceSha256'],end['sourceSha256']],'actualJoins':checks,'rasterStatus':'Not rendered as180. Actual source joins measured; source60/120 contact/BVH checks are separate. No complete360 loop claim.'}
recipes={0:{'clips':[],'durationMs':0,'nativeYawRadians':0},60:{'clips':['right60'],'durationMs':1200,'nativeYawRadians':-math.pi/3},120:{'clips':['right120'],'durationMs':2400,'nativeYawRadians':-2*math.pi/3},180:{'alternatives':['left180','right180'],'durationMs':3600},240:{'clips':['left120'],'durationMs':2400,'nativeYawRadians':2*math.pi/3},300:{'clips':['left60'],'durationMs':1200,'nativeYawRadians':math.pi/3}}
for recipe in recipes.values():
 if 'clips' in recipe:recipe['footprintStates']=['pivot-'+name for name in recipe['clips']]
 if recipe.get('clips'):
  folder,_=registry[recipe['clips'][-1]];native=json.loads((folder/'native-contact-join-check.json').read_text());recipe['nativeYawRadiansActual']=native['records'][-1]['heading']
for recipe in results.values():recipe['footprintStates']=['pivot-'+name for name in recipe['clips']]
result={'status':'TECHNICAL NATIVE IDLE-BOUNDARY RECIPES; NO RUNTIME OR ROUTE CLEARANCE CERTIFICATE','footprintManifest':'../footprints-native-v1/manifest.json','headingBasis':'keys are relative base-grid heading change degrees modulo360, not screen angles','recipesByGridHeadingDeltaDegrees':recipes,'actual180RecipeJoins':results,'entryExit':'flat idle at root0 before/after each complete pivot. Requires stop360+settle180 before and start360 after; plus heel-strike queue≤360ms.','rootBound':'Each root curve≤.03000001m about pivot origin, zero terminal root displacement; rigid placements preserve this. Body/bag swept clearance separately required.','appearance':'rejected generic technical mannequin; final shoes/source require renewed footprints and source checks'};(OUT/'heading-recipes.json').write_text(json.dumps(result,indent=2)+'\n');print('ACTUAL_180_IDLE_RECIPE_JOINS_PASS; no new raster')
