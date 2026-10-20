import json,re,math,xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
j=json.loads((OUT/'report.json').read_text());reports=[]
def edge(a,b):return tuple(sorted(((round(a[0],4),round(a[1],4)),(round(b[0],4),round(b[1],4)))))
def points(s):return [tuple(map(float,p.split(','))) for p in s.split()]
def edges(poly):return [edge(a,b) for a,b in zip(poly,poly[1:]+poly[:1])]
def parsepath(d):
 return [edge((float(a),float(b)),(float(c),float(e))) for a,b,c,e in re.findall(r'M\s*([\d.eE+\-]+) ([\d.eE+\-]+)\s*L\s*([\d.eE+\-]+) ([\d.eE+\-]+)',d)]
for c in j:
 for s in c['states']:
  if not s['bridge']:continue
  landpolys=[points(x) for x in s['clip']];a,b=landpolys[0][:2];r=math.hypot(a[0]-b[0],a[1]-b[1]);q0,r0=map(int,s['road'].split(';')[0].split(','));cx=sum(p[0] for p in landpolys[0])/6;cy=sum(p[1] for p in landpolys[0])/6;ox=cx-math.sqrt(3)*r*(q0+r0/2);oy=cy-1.5*r*r0
  def polygon(k):
   q,h=map(int,k.split(','));x=ox+math.sqrt(3)*r*(q+h/2);y=oy+1.5*r*h
   return [(x+r*math.cos(math.radians(i*60-90)),y+r*math.sin(math.radians(i*60-90))) for i in range(6)]
  bridgepolys=[polygon(o['cell']) for o in s['owners'] if o['id']=='bridge'];allcounts=Counter(e for poly in landpolys+bridgepolys for e in edges(poly));landset={e for poly in landpolys for e in edges(poly)};expected={e for e in landset if allcounts[e]==1};actual=set(parsepath(s['edge']));assert actual==expected,(expected-actual,actual-expected)
  bridgeRoot=ET.fromstring(s['bridge']);bridgeActual=[]
  for n in bridgeRoot:
   if n.tag.split('}')[-1]=='path':
    for a,b in parsepath(n.attrib['d']):
     cx=ox+math.sqrt(3)*r*6.5;cy=oy+1.5*r
     bridgeActual.append(edge((a[0]+cx,a[1]+cy),(b[0]+cx,b[1]+cy)))
  bridgeSet={e for poly in bridgepolys for e in edges(poly)};bridgeExpected={e for e in bridgeSet if allcounts[e]==1}
  # Local path coordinates rounded before translation introduce only <.0001px.
  def match(e,other):return any(max(abs(a-b) for p,q in zip(e,v) for a,b in zip(p,q))<.001 for v in other)
  assert len(bridgeActual)==len(bridgeExpected) and all(match(e,bridgeExpected) for e in bridgeActual)
  states={v['label']:v for v in c['states']};baseline=states['solved']
  selected=states['reselect-whole'];polys=[polygon(o['cell']) for o in selected['owners'] if o['id']=='stream-v6-a'];counts=Counter(e for poly in polys for e in edges(poly));wanted={e for e,count in counts.items() if count==1};observed=set(parsepath(selected['outline'][0]));assert observed==wanted

  for k in ['reselect-whole','pending-rotation','pending-invalid']:assert states[k]['edge']==baseline['edge']
  for k in ['moved-composite','returned-composite']:assert states[k]['edge']!=baseline['edge']
  for k in ['undo-move','undo-return','reload']:assert states[k]['edge']==baseline['edge']
  reports.append({'input':c['input'],'state':s['label'],'expectedUnionOuterEdges':len(expected),'actualOuterEdges':len(actual),'bridgeExpectedOuterEdges':len(bridgeExpected),'bridgeActualOuterEdges':len(bridgeActual),'internalBridgeHexRims':0,'internalLandLandRims':0,'landBridgeSharedBoundaryRims':0,'edgesUpdateAfterMoveReturnAndUndo':True,'selectedOutlinePreservedOnUncommittedRotation':states['reselect-whole']['outline']==states['pending-rotation']['outline'],'wholeInstanceOutlineOnlySelectedCells':True,'outlineRemovedAfterCommit':not states['moved-composite']['outline']})
(OUT/'edge-audit.json').write_text(json.dumps(reports,indent=2)+'\n');print('PASS actual path edges match exact union boundary,no internal land rims or landbridge shared seam')
