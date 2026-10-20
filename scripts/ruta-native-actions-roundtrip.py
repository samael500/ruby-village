"""Cold-open saved assets: both motion copies must actually survive serialization."""
from pathlib import Path
import bpy,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
rows=[]
def ah(a):
    values=[(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves]
    return hashlib.sha256(repr(values).encode()).hexdigest()
for folder in ['art/ruta-native-proportions-v1','art/ruta-native-proportions-study-v2/a-neutral','art/ruta-native-proportions-study-v2/b-neutral']:
    path=ROOT/folder/'ruta-proportion-proposal.blend'
    contract=json.loads((path.parent/'rest-transform-contract.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(path))
    actions={a.name:a for a in bpy.data.actions}
    required={**contract['originalActionsHashes'],**{v['action']:v['hash']for v in contract['retargetedActions'].values()}}
    assert set(required)<=set(actions),f'Missing saved actions: {set(required)-set(actions)}'
    assert all(ah(actions[n])==h for n,h in required.items()),'Saved curves changed'
    assert all(actions[v['action']].use_fake_user for v in contract['retargetedActions'].values()),'Unretained motion copy'
    rows.append({'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'requiredActionCount':len(required),'allRequiredActionsPresent':True,'allRequiredCurveHashesMatch':True,'retargetedActions':{v['action']:{'fakeUser':actions[v['action']].use_fake_user,'users':actions[v['action']].users,'sha256':ah(actions[v['action']])}for v in contract['retargetedActions'].values()}})
out=ROOT/'art/ruta-native-proportions-study-v2/saved-actions-roundtrip.json'
out.write_text(json.dumps({'status':'saved-action-preservation-PASS-not-gait-or-art-acceptance','files':rows},indent=2)+'\n')
print('SAVED_ACTION_ROUNDTRIP_PASS',len(rows))
