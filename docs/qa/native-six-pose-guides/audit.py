from pathlib import Path
from PIL import Image
import json,hashlib
R=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style');B=R/'art/ruta-native-six-pose-guides-v1';O=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected='bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706'
assert sha(R/'art/ruta-native-layered-style-v2/ruta-native-style.blend')==expected
head=json.loads((R/'art/ready-character-walk-v1/heading-contract.json').read_text());rows=[];shared=None
for d in ['e','se','sw','w','nw','ne']:
 D=R/'art/ruta-native-layered-walk48-v2' if d=='e' else B/d;m=json.loads((D/'manifest.json').read_text());c=json.loads((D/m['sourceContract']).read_text());assert sha(D/m['sourceContract'])==m['sourceContractSha256'];assert m['sourceSha256']==c['sourceSha256']==expected;assert c['sourceSha256After']==expected and c['sourceUnchanged'];assert m['sourceFrameSize']==[512,640] and m['frameSize']==[256,320];assert c['actorTransform']=='Rz(contractYaw) @ T(-RootRestGround)' and c['cameraAngleAlreadyInHeadingYaw'];v=c['cameraVariants']['base'];dd=v['directions'][d];clip=dd['clips']['walk'];frames=clip['frames'];assert len(frames)==48;assert clip['durationSeconds']==40/24;assert clip['loopEndpointMaxUsedVertexErrorMeters']==0;assert max(abs(x) for x in dd['rootGroundReferenceWorld'])<1e-7
 assert dd['heading']==head['variants']['base']['directions'][d]
 contract={k:c[k]for k in ['sourceSha256','frameSize','deliveryUniformScale','rootRestGroundNative','actorTransform','actionHashes','headingContractSha256']};contract['camera']=v['fixedRenderCamera'];contract['nativeHeightPx']=dd['nativeHeightPx']
 if shared is None:shared=contract
 else:assert contract==shared
 mins=[512,640,512,640]
 for f in frames:
  p=D/f['file'];assert sha(p)==f['sha256'];im=Image.open(p).convert('RGBA');assert im.size==(512,640);bbox=im.getchannel('A').getbbox();assert bbox and bbox[0]>0 and bbox[1]>0 and bbox[2]<512 and bbox[3]<640;mins=[min(mins[0],bbox[0]),min(mins[1],bbox[1]),min(mins[2],512-bbox[2]),min(mins[3],640-bbox[3])];assert f['worldOriginAnchorPx']==v['fixedRenderCamera']['worldOriginAnchorPx'];assert f['geometryInsideCanvas']
 atlas=D/m['files'][0]['path'];assert sha(atlas)==m['files'][0]['sha256'];a=Image.open(atlas).convert('RGBA');assert a.size==(1536,2560)
 for i in [0,11,24,47]:
  raw=Image.open(D/frames[i]['file']).convert('RGBA').resize((256,320),Image.Resampling.LANCZOS);cell=a.crop((i%6*256,i//6*320,(i%6+1)*256,(i//6+1)*320));assert raw.tobytes()==cell.tobytes()
 rows.append({'direction':d,'manifestSha256':sha(D/'manifest.json'),'sourceContractSha256':sha(D/m['sourceContract']),'atlasSha256':sha(atlas),'PNGhashesVerified':48,'decodedAtlasSamplesExact':[0,11,24,47],'nativeAlphaMinMarginsLTRB':mins,'heading':dd['heading']})
(O/'results.json').write_text(json.dumps({'status':'PASS-scoped-technical-guide-readback','rootCheckpoint':'b37e0a9','sourceSha256':expected,'commonContract':shared,'directions':rows},indent=2)+'\n')

sheets=json.loads((B/'pose-guide-sheets.json').read_text())
for sheet in sheets['sheets']:
 p=B/sheet['path'];assert sha(p)==sheet['sha256'];im=Image.open(p).convert('RGBA');assert im.size==(2048,1920);assert len(sheet['frames'])==48
 for f in sheet['frames']:
  assert sha(B/f['sourcePng'])==f['sourcePngSha256']
 for i in [0,11,24,47]:
  f=sheet['frames'][i];x,y,w,h=f['rect'];raw=Image.open(B/f['sourcePng']).convert('RGBA').resize((256,320),Image.Resampling.LANCZOS);assert raw.tobytes()==im.crop((x,y,x+w,y+h)).tobytes()
(O/'sheet-checks.json').write_text(json.dumps({'sheets':5,'allSheetHashes':'PASS','all240MappedPNGhashes':'PASS','sampleDecodedCellsPerSheet':[0,11,24,47],'headingContractAllSix':'exact match'},indent=2)+'\n')
