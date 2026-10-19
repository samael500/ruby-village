"""Read-only causal decomposition; diagnostic canvas translations, never source edits."""
import json,hashlib,statistics,base64
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from playwright.sync_api import sync_playwright
S=Path('/home/mskorokhod/life/ruby-village-36-painted-ready');O=Path(__file__).resolve().parent;old=Path('/tmp/ruby-qa-painted-browser-loop/docs/chapter-1-rc/qa/painted-browser-loop');M=Path('/tmp/ruby-qa-painted-landmarks24/docs/chapter-1-rc/qa/painted-landmarks24/manual-painted-landmarks24.json');N=Path('/home/mskorokhod/life/ruby-village-36-painted-guides/art/painted-ruta-registration24-v1/native-landmarks24.json')
d=json.loads((S/'art/painted-ruta-artist-origin24-v1/artist-origin-proposal.json').read_text());manual=json.loads(M.read_text());native=json.loads(N.read_text());capture=json.loads((old/'1280/report.json').read_text());k=d['paintedDisplayScale']*2;origin=[180,320];A=[statistics.median(f['footAnchorProposalArtPx'][c]for f in d['frames'])for c in range(2)]
# Manual visible blue iris centers, original packed frame coordinates. Not bones.
eyes=[(213,134),(223,136),(227,137),(220,138),(208,135),(215,135),(224,127),(222,126),(222,127),(218,126),(214,128),(218,130),(213,132),(217,128),(222,127),(214,129),(208,133),(218,128),(213,118),(215,118),(217,116),(213,116),(211,114),(218,116)]
paths=[S/'art/ruta-painted-ready-v1/review.html',S/'art/painted-ruta-artist-origin24-v1/artist-origin-proposal.json',M,N]+[S/f'art/painted-ruta-whole24-v1/frame-{i:02}.png'for i in range(24)];hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths};rows=[]
for i,f in enumerate(d['frames']):
 a=f['footAnchorProposalArtPx'];im=Image.open(S/f'art/painted-ruta-whole24-v1/frame-{i:02}.png');bbox=im.getchannel('A').point(lambda v:255 if v>=16 else 0).getbbox();points={'visibleBlueIrisCenter':list(eyes[i]),'satchelClasp':manual['frames'][i]['satchelClaspCenter'],'heelL':manual['frames'][i]['heelL'],'heelR':manual['frames'][i]['heelR']};q={}
 for name,p in points.items():q[name]=None if p is None else {'sourceArtPx':p,'manualRadialUncertaintyArtPx':2 if name=='visibleBlueIrisCenter'else 3,'fixedOriginCanvasPx':[origin[c]+k*(p[c]-A[c])for c in range(2)],'proposalCanvasPx':[origin[c]+k*(p[c]-a[c])for c in range(2)]}
 rows.append({'phase':i,'anchorArtPx':a,'sourceAlpha16BBox':bbox,'commonMetadataOffsetVersusFixedCanvasPx':[k*(A[c]-a[c])for c in range(2)],'points':q,'actualProposalPaintedBBox':capture['states'][i]['canvases']['painted']['alpha16BBox'],'actualNativeBBox':capture['states'][i]['canvases']['native']['alpha16BBox']})
transitions=[]
for i in range(24):
 j=(i+1)%24;meta=[-k*(rows[j]['anchorArtPx'][c]-rows[i]['anchorArtPx'][c])for c in range(2)];features={}
 for name in rows[i]['points']:
  a,z=rows[i]['points'][name],rows[j]['points'][name]
  if a is None or z is None:features[name]=None;continue
  source=[k*(z['sourceArtPx'][c]-a['sourceArtPx'][c])for c in range(2)];net=[source[c]+meta[c]for c in range(2)];check=[z['proposalCanvasPx'][c]-a['proposalCanvasPx'][c]for c in range(2)];assert max(abs(net[c]-check[c])for c in range(2))<1e-10
  features[name]={'rawSourceFrameFeatureDeltaAtCommonScaleCanvasPx':source,'metadataCommonDeltaCanvasPx':meta,'shownProposalDeltaCanvasPx':net,'fixedOriginDeltaCanvasPx':source,'manualDeltaAllowanceCanvasPx':k*(a['manualRadialUncertaintyArtPx']+z['manualRadialUncertaintyArtPx'])}
 invariants={}
 for body in ['visibleBlueIrisCenter','satchelClasp']:
  for heel in ['heelL','heelR']:
   pts=[rows[t]['points'][n]for t,n in [(i,body),(i,heel),(j,body),(j,heel)]]
   if any(p is None for p in pts):continue
   p0,h0,p1,h1=pts;delta=[k*((p1['sourceArtPx'][c]-h1['sourceArtPx'][c])-(p0['sourceArtPx'][c]-h0['sourceArtPx'][c]))for c in range(2)];allow=k*sum(p['manualRadialUncertaintyArtPx']for p in pts);invariants[body+'Minus'+heel]={'translationInvariantChangeCanvasPx':delta,'manualWorstCaseCoordinateAllowanceCanvasPx':allow,'interpretation':'2D relative geometry changes; not proof of incorrect anatomy or physical source mismatch'}
 nativeHipHeel=[]
 for t in [i,j]:m=native['frames'][t]['markers'];nativeHipHeel.append([(m['hip']['guideDeliveryPx'][c]-m['heelR']['guideDeliveryPx'][c])*2*d['nativeDisplayScale']for c in range(2)])
 transitions.append({'from':i,'to':j,'metadataCommonDeltaCanvasPx':meta,'features':features,'translationInvariantDiagnostics':invariants,'nativeHipMinusHeelRDeltaCanvasPx':[nativeHipHeel[1][c]-nativeHipHeel[0][c]for c in range(2)],'nativeFeatureCaveat':'evaluated native Hips/heel region means; NOT equivalent to painted iris/satchel/profile points'})
# Render diagnostic alternatives through a fresh browser canvas using unchanged source images.
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,args=['--no-sandbox']);p=b.new_page();p.goto('http://localhost:5310/ruta-painted-ready-v1/review.html');p.wait_for_function("document.querySelector('#status').textContent.startsWith('24 кадра')")
 rendered=p.evaluate("""async({fixed})=>{const d=await fetch('../painted-ruta-artist-origin24-v1/artist-origin-proposal.json').then(r=>r.json());let out=[];for(let i=0;i<24;i++){let im=new Image();im.src='../painted-ruta-whole24-v1/frame-'+String(i).padStart(2,'0')+'.png';await im.decode();let f=d.frames[i],pair={};for(const [name,a]of[['fixed',fixed],['proposal',f.footAnchorProposalArtPx]]){let c=document.createElement('canvas');c.width=360;c.height=360;let x=c.getContext('2d');x.clearRect(0,0,360,360);x.drawImage(im,180-a[0]*d.paintedDisplayScale*2,320-a[1]*d.paintedDisplayScale*2,im.naturalWidth*d.paintedDisplayScale*2,im.naturalHeight*d.paintedDisplayScale*2);pair[name]=c.toDataURL()}out.push(pair)}return out}""",{'fixed':A});b.close()
renderChecks=[]
for i,pair in enumerate(rendered):
 for name,url in pair.items():
  folder=O/name;folder.mkdir(exist_ok=True);raw=base64.b64decode(url.split(',')[1]);(folder/f'phase-{i:02}.png').write_bytes(raw)
  if name=='proposal':renderChecks.append({'phase':i,'diagnosticProposalPixelBytesMatchActualCapturedCanvas':raw==(old/'1280'/f'{i:02}-painted-actual-canvas.png').read_bytes()})
assert all(r['diagnosticProposalPixelBytesMatchActualCapturedCanvas']for r in renderChecks)
result={'status':'REJECTED-pilot-causal-diagnostic-only-NOT-a-fix','equation':'r_proposal(i)=O+k*(p_i-a_i); r_fixed(i)=O+k*(p_i-A); delta_r=k*delta_p-k*delta_a','canvasOrigin':origin,'oneGlobalDisplayScale':k,'fixedOriginArtPx':A,'fixedOriginDefinition':'component-wise median proposal anchor, only constant diagnostic gauge; no physical/reference correctness claim','manualEyeDefinition':'center of visible painted blue iris, hand-read from all24 source head crops, uncertainty2artpx; NOT head bone/native joint','sourceHashes':hashes,'frames':rows,'transitions':transitions,'diagnosticRenderChecks':renderChecks,'sourceUnchangedAfterAnalysis':all(hashlib.sha256(p.read_bytes()).hexdigest()==hashes[str(p)]for p in paths),'notCertified':['physical origin/no-slip','native iris/hip or profile/vertex semantic equivalence','which drawing or anchor is uniquely correct','corrected runtime or accepted pilot','adult-proportion anatomy from silhouette height']};assert result['sourceUnchangedAfterAnalysis'];(O/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12);plate=Image.new('RGB',(1440,820),'#f5efdf')
for row,(a,z)in enumerate([(17,18),(23,0)]):
 for col,(i,name)in enumerate([(a,'fixed'),(z,'fixed'),(a,'proposal'),(z,'proposal')]):
  im=Image.open(O/name/f'phase-{i:02}.png');bg=Image.new('RGB',im.size,'#eee7d5');bg.paste(im,mask=im.getchannel('A'));pos=(col*360,row*410);plate.paste(bg,pos);dr=ImageDraw.Draw(plate);dr.text((pos[0]+5,pos[1]+365),f'{name.upper()} origin / phase {i:02} / same scale',font=F,fill='black');dr.text((pos[0]+5,pos[1]+383),'Diagnostic translation only, not corrected art',font=F,fill='black')
plate.save(O/'fixed-versus-proposal-key-transitions.png')
# Simple standalone SVG graph of 24 image-landmark trajectories; no source image edits.
colors={'fixedOriginCanvasPx':'#0072b2','proposalCanvasPx':'#d55e00'};svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="700" viewBox="0 0 1000 700"><rect width="1000" height="700" fill="white"/>']
for panel,feature in enumerate(['visibleBlueIrisCenter','satchelClasp']):
 top=40+panel*340;svg.append(f'<text x="65" y="{top}" font-size="18">{feature}: canvas y (down positive), common scale; blue=fixed, orange=proposal</text>')
 vals=[q['points'][feature][name][1]for q in rows if q['points'][feature]for name in colors];lo=min(vals)-10;hi=max(vals)+10
 for y in range(int(lo)//10*10,int(hi)+10,10):
  py=top+30+(y-lo)/(hi-lo)*230;svg.append(f'<line x1="65" y1="{py}" x2="950" y2="{py}" stroke="#ddd"/><text x="15" y="{py+4}" font-size="12">{y}</text>')
 for name,color in colors.items():
  pts=[]
  for i,q in enumerate(rows):
   point=q['points'][feature]
   if point is None:
    if pts:svg.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="'+ ' '.join(pts)+'"/>');pts=[]
    continue
   x=65+i/23*885;y=top+30+(point[name][1]-lo)/(hi-lo)*230;pts.append(f'{x},{y}');svg.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{color}"/>')
  if pts:svg.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="'+ ' '.join(pts)+'"/>')
 for i in range(24):svg.append(f'<text x="{61+i/23*885}" y="{top+285}" font-size="12">{i}</text>')
svg.append('</svg>');(O/'image-landmark-trajectories.svg').write_text('\n'.join(svg))
for t in transitions:
 if t['from']in [17,23]:print(json.dumps(t,indent=2))
