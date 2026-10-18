from pathlib import Path
from PIL import Image,ImageChops,ImageStat
import json,hashlib,math
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;M=R/'art/characters-mpfb-v1/motion';fm=json.loads((M/'footprints-native-v1/manifest.json').read_text());recipes=json.loads((M/'pivot-variants/heading-recipes.json').read_text());fresh=json.loads((O/'fresh-180-recipes.json').read_text());images=[];gates={}
for key,row in recipes['recipesByGridHeadingDeltaDegrees'].items():
 if key=='180':continue
 assert row['footprintStates']==['pivot-'+n for n in row['clips']];assert all(n in fm['states']for n in row['footprintStates']);assert sum(json.loads((M/'footprints-native-v1'/fm['states'][n]['file']).read_text())['durationMs']for n in row['footprintStates'])==row['durationMs']
for key,row in recipes['actual180RecipeJoins'].items():
 assert row['footprintStates']==['pivot-'+n for n in row['clips']];assert row['sources']==[fm['states'][state]['sourceSha256']for state in row['footprintStates']];actual=fresh['actual180RecipeJoins'][key];assert row['sources']==actual['sources'] and row['durationMs']==3600 and math.dist(row['rootDeltaMetersActual'],[0,0,0])<1e-6
 for label,c in actual['actualJoins'].items():assert c['bodyWorldMatrixMaxElementError']<1e-4 and c['actualSoleVertexWorldMaxErrorMeters']<1e-4
for v in ['right60','left120','right120']:
 D=M/'pivot-variants'/v;meta=json.loads((D/'raster-path-metadata.json').read_text())
 for rec in meta['renderedFrames']:
  p=D/'E'/f'{rec["frame"]:02}.png';im=Image.open(p);box=im.getchannel('A').getbbox();assert im.size==(384,384)and min(box[:2])>1 and max(box[2:])<383;assert hashlib.sha256(p.read_bytes()).hexdigest()==rec['sha256'];images.append(dict(variant=v,frame=rec['frame'],bounds=box))
 assert len(meta['renderedFrames'])==12
 a=json.loads((O/v/'arm-satchel-check.json').read_text());g=json.loads((O/v/'grip-torso-check.json').read_text());pres=json.loads((O/v/'baseline-preservation.json').read_text());expected=41 if v=='right60'else 81;assert len(a['records'])==len(g['records'])==expected;assert all(min(r['evaluatedSelectedVertices'].values())>0 and max(r['intersections'].values())==0 for r in a['records']);assert all(all(x['selectedVertices']>0 and x['surfaceTriangleIntersections']==0 for x in r['grasp'].values())for r in g['records']);assert all(pres[k]for k in ['retainedActionsUnchanged','rigRestConstraintsAndShoeWeightsUnchanged','allAsymmetricMeshGeometryWeightsUnchanged']);gates[v]=dict(carryActualSamples=expected,carryArmTriangleMax=0,carryStrapTriangleMax=0,allSetsNonempty=True,preservedNativeActionsAndAsymmetricGeometry=True)
a=Image.open(O/'right120/independent-render.png').convert('RGBA');b=Image.open(M/'pivot-variants/right120/E/57.png').convert('RGBA');rms=ImageStat.Stat(ImageChops.difference(a,b)).rms;assert max(rms)==0
(O/'metadata-check.json').write_text(json.dumps(dict(actualRecordCount=fm['recordCount'],actualStateCount=len(fm['states']),allRecipeFootprintSourceLinksCorrect=True,fresh180Joins=fresh['actual180RecipeJoins'],diagnosticImageCount=len(images),images=images,nativeCarryPreservation=gates,right120Frame57RepeatRms=rms),indent=2)+'\n');print('METADATA PASS335/11,36PNG,41/81/81carry,180recipes')
