"""Asset transparency and source IK stance audit. Does not certify artistic acceptance."""
from pathlib import Path
from PIL import Image
import json,math,hashlib
r=Path(__file__).resolve().parents[1];folder=r/'art/characters-walk-v1/mesh-pilot';poses=json.loads((folder/'evaluated-rig-joints.json').read_text());records=[]
for f in range(1,17):
 p=folder/f'renders/e-{f:02}.png';im=Image.open(p);assert im.size==(320,320) and im.mode=='RGBA';alpha=im.getchannel('A');assert alpha.getextrema()==(0,255);assert alpha.getpixel((0,0))==0;bounds=alpha.point(lambda x:255 if x>96 else 0).getbbox();assert bounds and all([bounds[0]>0,bounds[1]>0,bounds[2]<320,bounds[3]<320]);records.append({'frame':f,'bounds':bounds,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
scale=136/210;expected=(.72*256/2.65)*scale/.8
plant=[(poses[str(f+1)]['foot.L'][0][0]-poses[str(f)]['foot.L'][0][0])*scale/.05 for f in range(1,8)];error=max(abs(abs(speed)-expected) for speed in plant);assert error<.01,error
assert poses['1']['foot.L'][0][0]>poses['1']['foot.R'][0][0];assert poses['9']['foot.L'][0][0]<poses['9']['foot.R'][0][0]
result={'status':'technical-pilot-checks-pass-not-artistic-acceptance','renderedFrames':records,'actualRigStanceExchange':True,'stanceVelocityPixelsPerSecond':plant,'expectedEastVelocityPixelsPerSecond':expected,'maxStanceVelocityError':error,'sourceStrideWorldUnits':.72,'durationMs':800,'targetDisplayHeightPx':136,'projectedStrideAtDisplay136':{'e':expected*.8,'w':expected*.8,'se':21.662,'sw':21.662,'nw':21.662,'ne':21.662},'notCertified':['painted knee/cuff seams','hidden-side boot anatomy','all six final directions','production occlusion','idle/turn/start-stop','human artistic acceptance']}
(r/'docs/chapter-1-rc/painted-motion/mesh-audit.json').write_text(json.dumps(result,indent=2)+'\n');print('16 transparent frames + actual IK stance exchange/stride pass; art remains review')
