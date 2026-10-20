from pathlib import Path
O=Path(__file__).resolve().parent
exec((O/'render-proof.py').read_text().split('segments=')[0])
m=json.load(open(O/'proof-manifest.json'));rows=[]
for index,f in enumerate(m['frames']):
 if index<4 or index>=76:action='Idle_Neutral_ProportionProposal';frame=0
 elif index<16:action=cstart['action'];frame=(index-4)/12*cstart['durationSeconds']*24
 elif index<64:action='Walk_ProportionProposal';frame=(5+40*(index-16)/48)%40
 else:action=cstop['action'];frame=(index-64)/12*cstop['durationSeconds']*24
 assert action==f['action']and abs(frame-f['sourceFrame'])<1e-8;rig.animation_data.action=bpy.data.actions[action];sc.frame_set(int(frame),subframe=frame%1);bpy.context.view_layer.update();h=hashlib.sha256(repr([(p.name,[[round(float(v),8)for v in row]for row in p.matrix_basis])for p in rig.pose.bones]).encode()).hexdigest();assert h==f['sourcePoseHash'],(index,h,f['sourcePoseHash']);assert rig.pose.bones['Root'].location.length<1e-8;rows.append({'index':index,'action':action,'expectedSourceFrame':frame,'poseHash':h,'match':True})
assert len(set(f['sourcePoseHash']for f in m['frames'][16:64]))==48
(O/'all80-pose-verification.json').write_text(json.dumps({'status':'ALL80-TIMESTAMP-POSE-REPLAY-VERIFIED-NOT-ART-OR-NOSLIP','frameCount':len(rows),'walkUniquePoseCount':48,'walkModulo40':True,'walkLastSourceFrame':m['frames'][63]['sourceFrame'],'stopFirstSourceFrame':m['frames'][64]['sourceFrame'],'staticIdlePoseVelocityTarget':0,'RootBoneConstant':True,'sourceFileUnchanged':hashlib.sha256(P.read_bytes()).hexdigest()==m['sourceSHA256'],'cacheProvenance':'Initial actual render log records action timestamps; six wrap frames explicitly rerendered. Hashes sampled on corrected frozen source replay; no pixel-derived bone identity claim.','rows':rows},indent=2));print('ALL80_POSES_VERIFIED',flush=True)
