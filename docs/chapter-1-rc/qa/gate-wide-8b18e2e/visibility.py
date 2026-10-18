from pathlib import Path
from PIL import Image
from xml.etree import ElementTree as ET
import json,math
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;rows=[];coverageRows=[]
def spriteBounds(actor):
 node=ET.fromstring('<g>'+actor['markup']+'</g>')[0];box=actor['box']
 if node.tag.endswith('svg'):
  vx,vy,vw,vh=map(float,node.get('viewBox').split());image=node[0];im=Image.open(R/'public'/image.get('href').split('/ruby-village/')[1]).getchannel('A').crop((round(vx),round(vy),round(vx+vw),round(vy+vh)))
 else:
  im=Image.open(R/'public'/node.get('href').split('/ruby-village/')[1]).getchannel('A');vw,vh=im.size
 bb=im.getbbox();assert bb;return [box['x']+bb[0]/vw*box['w'],box['y']+bb[1]/vh*box['h'],box['x']+bb[2]/vw*box['w'],box['y']+bb[3]/vh*box['h']]
for p in O.glob('gate/*/report.json'):
 run=json.loads(p.read_text())
 for state in run['states']:
  lay=state['layout'];board=lay['board'];wide=lay['wide'];coverage={ 'left':board['x']-wide['x'],'top':board['y']-wide['y'],'right':wide['x']+wide['width']-(board['x']+board['width']),'bottom':wide['bottom']-board['bottom']};assert min(coverage.values())>=-1e-5;coverageRows.append({'viewport':run['viewport'],'state':state['label'],'wideCoverageMargins':coverage})
  if not state['story']:continue
  mat=lay['painted'];assert all(abs(a-b)<1e-6 for a,b in zip(mat,lay['residents']));assert len(lay['foregrounds'])==1 and all(abs(a-b)<1e-6 for a,b in zip(mat,lay['foregrounds'][0]));gate=Image.open(R/'public/assets/chapter-1/v9/gate'/('gate-'+lay['gateKind']+'.webp')).getchannel('A');bb=gate.getbbox();a,b,c,d,e,f=mat;points=[(a*x+c*y+e,b*x+d*y+f)for x in [bb[0],bb[2]]for y in [bb[1],bb[3]]];gb=[min(x for x,y in points),min(y for x,y in points),max(x for x,y in points),max(y for x,y in points)];actor=state['ruta']or state['idle'];assert actor;rb=spriteBounds(actor);union=[min(rb[0],gb[0]),min(rb[1],gb[1]),max(rb[2],gb[2]),max(rb[3],gb[3])];board=lay['board'];panel=lay['story']['top'];margins=dict(left=union[0]-board['x'],top=union[1]-board['y'],right=board['x']+board['width']-union[2],bottom=min(board['bottom'],panel)-union[3]);assert min(margins.values())>=-1e-5,(run['viewport'],state['label'],margins)
  wide=lay['wide'];coverage=dict(left=board['x']-wide['x'],top=board['y']-wide['y'],right=wide['x']+wide['width']-(board['x']+board['width']),bottom=wide['bottom']-board['bottom']);assert min(coverage.values())>=-1e-5
  rows.append(dict(viewport=run['viewport'],state=state['label'],gateKind=lay['gateKind'],gateAlphaBounds=gb,rutaAlphaBounds=rb,actualUnionBounds=union,marginsAbovePanelAndInsideBoard=margins,wideCoverageMargins=coverage,mainLayerMatricesIdentical=True,mainMatrix=mat))
assert len(rows)==10
(O/'visibility.json').write_text(json.dumps({'narrativeUnionChecks':rows,'allStateCoverageChecks':coverageRows},indent=2)+'\n');print('PASS',len(rows),'realstory states allRuta+gatealpha insideboardabovepanel,sharedcamera,fullwidecoverage');print('minimumMargin',min(v for r in rows for v in r['marginsAbovePanelAndInsideBoard'].values()))
