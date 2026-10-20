"""Pack only actual complete whole-canvas renders. No crop/origin fit.
python THIS --contract art/.../source-contract.json
"""
import argparse,hashlib,json,math
from pathlib import Path
from PIL import Image,features
p=argparse.ArgumentParser();p.add_argument('--contract',required=True);args=p.parse_args();path=Path(args.contract).resolve();root=path.parent;contract=json.loads(path.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert contract['renderedFrameCount']>0 and contract['sourceUnchanged'];assert contract['frameSize']==[512,640];assert features.check('webp')
manifest={'schemaVersion':1,'status':'WHOLE-SPRITE-DELIVERY-CANDIDATE-NOT-ART-OR-GAME-ACCEPTANCE','productionEnabled':False,'sourceContract':path.name,'sourceContractSha256':sha(path),'sourceBlend':contract['source'],'sourceSha256':contract['sourceSha256'],'headingContractSha256':contract['headingContractSha256'],'actionHashes':contract['actionHashes'],'sourceFrameSize':[512,640],'frameSize':[256,320],'deliveryTransform':{'wholeCanvasUniformScale':.5,'resample':'Pillow LANCZOS RGBA','perFrameCrop':False,'perFrameTranslate':False,'perFrameScaleFit':False,'perDirectionScaleFit':False},'cameraVariants':{},'files':[]};audit=[];count=0
for variant,spec in contract['cameraVariants'].items():
 dest={'gameCamera':spec['gameCamera'],'scenes':spec['scenes'],'fixedRenderCamera':spec['fixedRenderCamera'],'directions':{}};manifest['cameraVariants'][variant]=dest
 for direction,d in spec['directions'].items():
  dr={'heading':d['heading'],'nativeHeightPx':d['nativeHeightPx']*.5,'visibleRestHeightMeters':d['visibleRestHeightMeters'],'footAnchor':[x*.5 for x in spec['fixedRenderCamera']['worldOriginAnchorPx']],'clips':{}};dest['directions'][direction]=dr
  for clip,c in d['clips'].items():
   n=contract['phaseCount'];assert len(c['frames'])==n and [r['index']for r in c['frames']]==list(range(n));assert c['loopEndpointMaxUsedVertexErrorMeters']<1e-5,'endpoint geometry seam: explicit review required'
   atlas=Image.new('RGBA',(256*6,320*math.ceil(n/6)));frames=[]
   for i,row in enumerate(c['frames']):
    file=root/row['file'];assert sha(file)==row['sha256'];im=Image.open(file);assert im.size==(512,640) and im.mode=='RGBA';box=im.getchannel('A').getbbox();assert box is not None;assert box[0]>0 and box[1]>0 and box[2]<512 and box[3]<640,('clipped source alpha',file,box)
    whole=im.resize((256,320),Image.Resampling.LANCZOS);box2=whole.getchannel('A').getbbox();assert box2 and box2[0]>0 and box2[1]>0 and box2[2]<256 and box2[3]<320,('clipped delivery alpha',file,box2);x=(i%6)*256;y=(i//6)*320;atlas.paste(whole,(x,y));frames.append({'index':i,'rect':[x,y,256,320],'sourceFrame':row['sourceFrame'],'sourcePng':row['file'],'sourcePngSha256':row['sha256']});audit.append({'source':row['file'],'sourceAlphaBounds':box,'deliveryAlphaBounds':box2,'fixedAnchor':dr['footAnchor'],'geometryInsideCanvas':row['geometryInsideCanvas']});count+=1
   atlaspath=root/'atlases'/f'{variant}-{direction}-{clip}.webp';atlaspath.parent.mkdir(exist_ok=True);atlas.save(atlaspath,format='WEBP',lossless=True,quality=100,method=6,exact=True)
   with Image.open(atlaspath)as reread:assert reread.convert('RGBA').tobytes()==atlas.tobytes(),'lossless atlas mismatch'
   dr['clips'][clip]={'atlas':atlaspath.relative_to(root).as_posix(),'frames':frames,'durationSeconds':c['durationSeconds'],'loop':True,'sourceAction':c['sourceAction'],'loopEndpointMaxUsedVertexErrorMeters':c['loopEndpointMaxUsedVertexErrorMeters']};manifest['files'].append({'path':atlaspath.relative_to(root).as_posix(),'sha256':sha(atlaspath),'bytes':atlaspath.stat().st_size,'size':list(atlas.size),'decodedRGBABytes':atlas.width*atlas.height*4})
assert count==contract['renderedFrameCount'];manifest['packedFrameCount']=count;manifest['limitations']=contract['limitations'];(root/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(root/'containment-audit.json').write_text(json.dumps({'actualAlphaCheckedFrames':count,'rows':audit,'physicalPhone':'NOT RUN','artAcceptance':'NOT CLAIMED','sourceAndRuntimeUnchanged':True},indent=2)+'\n');print('PACKED',count,'whole frames',len(manifest['files']),'lossless atlases')
