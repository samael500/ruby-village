"""Uniform whole-frame delivery packing and native/delivery alpha contracts."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/ready-character-six-v1';ASSETS=OUT/'assets';ASSETS.mkdir(exist_ok=True)
parts=[json.loads((OUT/f'source-contract.{v}.json').read_text())for v in ['base','calibrated-1']];source=parts[0];source['cameraVariants'].update(parts[1]['cameraVariants']);ref=json.loads((OUT/'static-origin-checks.json').read_text());reference=ref['bodyReference'];anchor=[v*.5 for v in ref['commonFootAnchor']];height=reference['deliveryNativeHeightPx'];motion=json.loads((ROOT/'art/ready-character-walk-v1/motion-checks.json').read_text());old=json.loads((ROOT/'public/assets/characters-walk-v1/animated-v3/manifest.json').read_text())
manifest={'schemaVersion':3,'status':'native-ready-part-source-candidate-not-approved-Ruta-or-runtime','productionEnabled':False,'frameSize':[256,320],'footAnchor':anchor,'nativeHeightPx':height,'nativeBodyReference':reference,'targetDisplayHeightPx':136,'sourceFrameSize':[512,640],'sourceFootAnchor':ref['commonFootAnchor'],'deliveryTransform':{'uniformScale':.5,'perFrameCrop':False,'perFrameTranslate':False,'perDirectionScale':False,'note':'one fixed half-resolution resize of every entire camera canvas'},'sourceRig':source['source'],'sourceSha256':source['sourceSha256'],'sourceActionHashes':source['actionHashes'],'loopEndpointChecks':'loop-seam-checks.json','originNormalization':source['originNormalization'],'framesAlreadyProjected':True,'applyGroundTransformToSpritePixels':False,'cycleDurationMs':40/24*1000,'sourceStrideMetersPerCycle':motion['suggestedStrideMetersPerCycle'],'sourceTravelSpeedMetersPerSecond':motion['suggestedTravelSpeedMetersPerSecond'],'sourceStanceSpeedResidualRmsMetersPerSecond':motion['stanceSpeedResidualRmsMetersPerSecond'],'strideUnits':'native model meters; convert through measured camera pixels and body display scale, never treat as game hex cells','headingContract':'../ready-character-walk-v1/heading-contract.json','sceneCameraVariant':old['sceneCameraVariant'],'cameraVariants':{},'spriteCameraFields':['groundScale','angle'],'cameraOriginAndRadiusAreRouteMetadataOnly':True,'runtimeInstallation':'none; root owns URL placement, stage review and runtime adapter','limitations':['adult stock likeness not approved Ruta','no start/stop clips or turn transitions authored','existing Walk and Idle_Neutral source actions; no invented joint motion','stance/contact residual and visual bag grazing remain disclosed in source pilot checks']}
audit=[];files=[];walkpreviews={}
for variant,spec in source['cameraVariants'].items():
 directions={};walkpreviews[variant]={}
 for name,ds in spec['directions'].items():
  atlas=Image.new('RGBA',(6*256,8*320));clips={};walkpreviews[variant][name]=[]
  for clip_index,clip in enumerate(['walk','idle']):
   cs=ds['clips'][clip];assert len(cs['frames'])==24;frames=[];hashes=[]
   for i,row in enumerate(cs['frames']):
    p=OUT/row['file'];im=Image.open(p).convert('RGBA');assert im.size==(512,640);b=im.getchannel('A').getbbox();assert b and b[0]>0 and b[1]>0 and b[2]<512 and b[3]<640,(variant,name,clip,i,b)
    scaled=im.resize((256,320),Image.Resampling.LANCZOS);db=scaled.getchannel('A').getbbox();assert db and db[0]>0 and db[1]>0 and db[2]<256 and db[3]<320;x=(i%6)*256;y=(i//6+clip_index*4)*320;atlas.alpha_composite(scaled,(x,y));h=hashlib.sha256(p.read_bytes()).hexdigest();hashes.append(h)
    frames.append({'file':f'assets/{variant}-{name}.webp','sourceRect':[x,y,256,320],'frameSize':[256,320],'footAnchor':anchor,'durationMs':cs['cycleDurationMs']/24,'motionFraction':i/24 if clip=='walk' else 0,'sourceFrame':row['sourceFrame'],'sourceFile':row['file']})
    audit.append({'variant':variant,'direction':name,'clip':clip,'index':i,'sourceSha256':h,'sourceAlphaBounds':list(b),'deliveryAlphaBounds':list(db)})
    if clip=='walk':walkpreviews[variant][name].append(scaled)
   if clip=='walk':assert len(set(hashes))>=20,(variant,name,clip,'insufficient distinct walk renders')
   clips[clip]={'loop':True,'sourceAction':cs['sourceAction'],'cycleDurationMs':cs['cycleDurationMs'],'frames':frames,'uniqueSourceFrames':len(set(hashes))}
  path=ASSETS/f'{variant}-{name}.webp';atlas.save(path,lossless=True,method=6,exact=True);decoded=Image.open(path).convert('RGBA');assert decoded.tobytes()==atlas.tobytes();files.append({'file':str(path.relative_to(OUT)),'sizeBytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'decodedRGBABytes':atlas.width*atlas.height*4})
  yaw=ds['stockForwardMinusYBlenderYawRadians'];stride=motion['suggestedStrideMetersPerCycle']*reference['nativeHorizontalPixelsPerMeter']*.5*math.hypot(math.sin(yaw),.65*math.cos(yaw));directions[name]={'screenAngleRadians':ds['acceptedScreenAngleRadians'],'sourceYawRadians':yaw,'projectedStridePixels':stride,'projectedStrideDisplayPixelsAt136':stride*136/height,'normalizedRootGroundWorld':ds['normalizedRootGroundWorld'],'clips':clips}
 manifest['cameraVariants'][variant]={'camera':spec['camera'],'scenes':spec['scenes'],'directions':directions}
 # Four complete native cycle phases per direction, same size/anchor across all six views.
 proof=Image.new('RGBA',(6*256,4*320),(237,233,220,255))
 for col,name in enumerate(['e','se','sw','w','nw','ne']):
  for row,i in enumerate([0,6,12,18]):
   tile=walkpreviews[variant][name][i];proof.alpha_composite(tile,(col*256,row*320));ImageDraw.Draw(proof).text((col*256+8,row*320+8),f'{variant}/{name}/{i:02}',fill=(35,35,30))
 proof.convert('RGB').save(OUT/f'{variant}-walk-four-phases.png')
manifest['directions']=manifest['cameraVariants']['base']['directions'];manifest['files']=files;manifest['decodedRGBABytesAll12Atlases']=sum(f['decodedRGBABytes']for f in files);manifest['compressedBytesAll12Atlases']=sum(f['sizeBytes']for f in files)
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(OUT/'source-contract.json').write_text(json.dumps(source,indent=2)+'\n')
margin=min(min(r['sourceAlphaBounds'][0],r['sourceAlphaBounds'][1],512-r['sourceAlphaBounds'][2],640-r['sourceAlphaBounds'][3])for r in audit)
(OUT/'packing-checks.json').write_text(json.dumps({'status':'576-native-source-frames-and12-lossless-atlases-checked','sourceFrameCount':len(audit),'allSourceAnyAlphaWithinCanvas':True,'allDeliveryAnyAlphaWithinFrameCells':True,'minimumDeliveryAnyAlphaMarginPixels':min(min(r['deliveryAlphaBounds'][0],r['deliveryAlphaBounds'][1],256-r['deliveryAlphaBounds'][2],320-r['deliveryAlphaBounds'][3])for r in audit),'minimumSourceAnyAlphaMarginPixels':margin,'losslessWebPDecodedPixelsMatchHalfResolutionPacking':True,'fixedNativeHeightPxAllVariants':height,'fixedFootAnchorAllFrames':anchor,'sourceRootProjectionMaximumErrorPixels':ref['maximumAnchorErrorPixels'],'frames':audit,'files':files},indent=2)+'\n')
loops=[]
for i in range(24):
 canvas=Image.new('RGBA',(1536,640),(237,233,220,255));d=ImageDraw.Draw(canvas)
 for row,variant in enumerate(['base','calibrated-1']):
  for col,name in enumerate(['e','se','sw','w','nw','ne']):canvas.alpha_composite(walkpreviews[variant][name][i],(col*256,row*320));d.text((col*256+8,row*320+8),variant+'/'+name,fill=(35,35,30))
 loops.append(canvas.convert('RGB'))
loops[0].save(OUT/'walk-all12.webp',save_all=True,append_images=loops[1:],duration=[round((i+1)*1000*40/24/24)-round(i*1000*40/24/24) for i in range(24)],loop=0,lossless=True,method=4)
print('PACKED',len(audit),'frames',len(files),'atlases','minimum alpha margin',margin,'nativeHeightPx',height)

# A five-second three-cycle video of the same packed review pixels.
video=OUT/'walk-all12-one-cycle.mp4'
proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1536x640','-framerate','72/5','-i','pipe:0','-an','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
for frame in loops:proc.stdin.write(frame.tobytes())
proc.stdin.close();assert proc.wait()==0
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-stream_loop','2','-i',str(video),'-c','copy',str(OUT/'walk-all12.mp4')],check=True)
video.unlink()
