"""Diagnostic analysis of actual captured canvas; never changes author assets."""
import json,hashlib,urllib.request
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
O=Path(__file__).resolve().parent;S=Path('/home/mskorokhod/life/ruby-village-36-painted-ready');data=json.loads((S/'art/painted-ruta-artist-origin24-v1/artist-origin-proposal.json').read_text());manual=json.loads(Path('/tmp/ruby-qa-painted-landmarks24/docs/chapter-1-rc/qa/painted-landmarks24/manual-painted-landmarks24.json').read_text());reports={w:json.loads((O/w/'report.json').read_text())for w in ['1280','844']};summary={'status':'BLOCKED-pilot-loop-quality-body-dip17to18','uiAndContainment':'PASS scoped','originIsPhysicalSupport':False,'globalScale':data['globalScaleArtToGuide'],'displayOriginCanvasPx':[180,320],'backingAndCss':[360,360],'frames':[]}
for i in range(24):
 a=reports['1280']['states'][i];z=reports['844']['states'][i];f=data['frames'][i];clasp=manual['frames'][i]['satchelClaspCenter'];anchor=f['footAnchorProposalArtPx'];s=2*data['paintedDisplayScale'];projected=None if not clasp else[180+(clasp[0]-anchor[0])*s,320+(clasp[1]-anchor[1])*s]
 summary['frames'].append({'phase':i,'paintedBBox':a['canvases']['painted']['alpha16BBox'],'nativeBBox':a['canvases']['native']['alpha16BBox'],'artistOriginMetadataArtPx':anchor,'satchelClaspProjectedCanvasPx':projected,'satchelClaspManualRadialUncertaintyCanvasPx':None if not clasp else 3*s,'satchelIsHipOrPhysicalOrigin':False,'desktopMobilePaintedPixelsIdentical':a['canvases']['painted']['pngSha256']==z['canvases']['painted']['pngSha256'],'desktopMobileNativePixelsIdentical':a['canvases']['native']['pngSha256']==z['canvases']['native']['pngSha256']})
for first,last,key in [(17,18,'bodyDip17to18'),(23,0,'seam23to0Observation')]:
 a,z=summary['frames'][first],summary['frames'][last];pa,pz=a['paintedBBox'],z['paintedBBox'];na,nz=a['nativeBBox'],z['nativeBBox'];summary[key]={'paintedTopDeltaCanvasPx':pz[1]-pa[1],'nativeTopDeltaCanvasPx':nz[1]-na[1],'paintedHeightDeltaCanvasPx':(pz[3]-pz[1])-(pa[3]-pa[1]),'nativeHeightDeltaCanvasPx':(nz[3]-nz[1])-(na[3]-na[1]),'claspDyCanvasPx':z['satchelClaspProjectedCanvasPx'][1]-a['satchelClaspProjectedCanvasPx'][1],'meaning':'Observed silhouette/visible image landmark change, not measured bone height or physical support; canvas presentation is 2x intended game size'}
summary['physicalPhone']='NOT RUN';summary['sourceRGBAOrRigOrRuntimeEdits']=False;(O/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13);plate=Image.new('RGB',(1440,800),'#f2ecdd')
for row,pair in enumerate([(17,18),(23,0)]):
 for col,(i,kind)in enumerate([(pair[0],'painted'),(pair[1],'painted'),(pair[0],'native'),(pair[1],'native')]):
  im=Image.open(O/'1280'/f'{i:02}-{kind}-actual-canvas.png');bg=Image.new('RGB',im.size,'#eee7d5');bg.paste(im,mask=im.getchannel('A'));d=ImageDraw.Draw(bg)
  for y in [50,66,100,200,320]:d.line((0,y,360,y),fill='#b8b09c',width=1);d.text((2,y+1),str(y),font=font,fill='#5f5948')
  pos=(col*360,row*400);plate.paste(bg,pos);pd=ImageDraw.Draw(plate);pd.text((pos[0]+6,pos[1]+365),f'Actual browser {kind}, phase {i:02}',font=font,fill='black');bbox=reports['1280']['states'][i]['canvases'][kind]['alpha16BBox'];pd.text((pos[0]+6,pos[1]+383),f'Alpha16 top={bbox[1]}, height={bbox[3]-bbox[1]}',font=font,fill='black')
plate.save(O/'actual-browser-body-dip-and-seam.png')
# Read actual HTTP endpoint after capture to bind delivered page/data to local source.
served=[]
for path in ['ruta-painted-ready-v1/review.html','painted-ruta-artist-origin24-v1/artist-origin-proposal.json']:
 body=urllib.request.urlopen('http://localhost:5310/'+path).read();local=S/'art'/path;served.append({'url':'http://localhost:5310/'+path,'servedSha256':hashlib.sha256(body).hexdigest(),'localSha256':hashlib.sha256(local.read_bytes()).hexdigest(),'same':body==local.read_bytes()})
assert all(r['same']for r in served);(O/'served-source-check.json').write_text(json.dumps(served,indent=2)+'\n');print(json.dumps({'bodyDip':summary['bodyDip17to18'],'seam':summary['seam23to0Observation'],'all24PixelMatchesAcrossViewports':all(f['desktopMobilePaintedPixelsIdentical']and f['desktopMobileNativePixelsIdentical']for f in summary['frames'])},indent=2))
