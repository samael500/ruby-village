"""Run via isolated Blender4.5: genuine MPFB human, weighted standard rig, saved blend. Not final art."""
import sys,os,json,hashlib
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/smoke';OUT.mkdir(parents=True,exist_ok=True)
MPFB_SRC=Path(os.environ.get('RUBY_MPFB_SRC','/home/mskorokhod/life/_tools/mpfb2-v2.0.18/src'))
OWN=Path('/tmp/ruby-mpfb-config/data');OWN.mkdir(parents=True,exist_ok=True)
# Source checkout isn't a bl_ext namespace. Scoped API adapter maps only MPFB's extension home.
_original=bpy.utils.extension_path_user
bpy.utils.extension_path_user=lambda package,*a,**kw:str(OWN) if package=='mpfb'else _original(package,*a,**kw)
sys.path.insert(0,str(MPFB_SRC));import mpfb
bpy.context.preferences.addons.new().module='mpfb'
mpfb.register()
from mpfb.services import HumanService,TargetService,LocationService
assert str(LocationService.get_user_home()).startswith('/tmp/ruby-mpfb-config/')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
macro=TargetService.get_default_macro_info_dict();macro.update(gender=0.,age=.1875,muscle=.3,weight=.45,proportions=.35,height=.5);macro['race']={'asian':.15,'caucasian':.85,'african':0.}
human=HumanService.create_human(scale=.1,macro_detail_dict=macro,feet_on_ground=True);human.name='Ruta.MPFB.Body'
rig=HumanService.add_builtin_rig(human,'default');rig.name='Ruta.MPFB.StandardRig'
assert rig.type=='ARMATURE'and len(rig.data.bones)>50
assert any(m.type=='ARMATURE'for m in human.modifiers)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-mpfb-smoke.blend'))
report={'status':'technical-smoke-not-final-art','blender':bpy.app.version_string,'mpfbVersion':list(mpfb.VERSION),'mpfbSource':str(MPFB_SRC),'macro':macro,'meshVertices':len(human.data.vertices),'meshFaces':len(human.data.polygons),'rigType':'default','boneCount':len(rig.data.bones),'bones':[b.name for b in rig.data.bones],'armatureModifier':True,'userData':str(LocationService.get_user_home()),'bodyHeightMeters':human.dimensions.z,'productionEnabled':False}
(OUT/'smoke.json').write_text(json.dumps(report,indent=2)+'\n');print('RUBY_MPFB_SMOKE',json.dumps(report))
