from pathlib import Path
from playwright.sync_api import sync_playwright
import json,math,hashlib,urllib.request
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;m=json.loads((R/'art/chapter-1-v9/layers/water/stream-pilot/manifest.json').read_text());solution=[p for p in m['solution']if p['placement']];g=json.loads((R/m['geometry']).read_text());geometry={c['id']:c for c in g['cells']};reports=[]
READ='''()=>{let root=document.querySelector('#ground-plane'),b=root.querySelector(':scope>[data-painted-bridge]'),world=document.querySelector('#board [data-painted-world]');let mat=n=>{let m=n.getScreenCTM();return[m.a,m.b,m.c,m.d,m.e,m.f]},points=(p,m)=>[...p.points].map(q=>{let t=new DOMPoint(q.x,q.y).matrixTransform(m);return[t.x,t.y]});return{clip:[...b.querySelectorAll('clipPath polygon')].map(p=>points(p,b.getScreenCTM())),owners:[...root.querySelectorAll('[data-owner="bridge"]>polygon.cell')].map(p=>({id:p.parentElement.dataset.cell,points:points(p,p.getScreenCTM())})),bridgeParentMatrix:mat(b.parentElement),groundMatrix:mat(root),worldMatrix:mat(world),asset:b.querySelector('image').getAttribute('href'),sourceRegistration:[...['x','y','width','height'].map(k=>+b.querySelector('image').getAttribute(k))]}}'''
with sync_playwright()as p:
 b=p.chromium.launch()
 for touch,w,h in [(False,1280,720),(True,844,390)]:
  c=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch);q=c.new_page();cdp=c.new_cdp_session(q)
  def tap(loc):
   loc.scroll_into_view_if_needed();bb=loc.bounding_box();pt={'x':bb['x']+bb['width']/2,'y':bb['y']+bb['height']/2}
   if touch:cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{**pt,'id':1}]});cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   else:q.mouse.click(**pt)
  def cell(qv,rv):return q.locator(f'#board [data-cell="{qv},{rv}"]>polygon.cell')
  def check(label):
   d=q.evaluate(READ);assert len(d['clip'])==len(d['owners'])==3;assert d['groundMatrix']==d['bridgeParentMatrix'];canon=lambda poly:sorted((round(x,5),round(y,5))for x,y in poly);clipErrors=[min(max(min(math.dist(x,y)for y in owner['points'])for x in poly)for owner in d['owners'])for poly in d['clip']];d['maxClipOwnerErrorPixels']=max(clipErrors);assert max(clipErrors)<.0001,(clipErrors,d); a,b,c1,d1,e,f=d['worldMatrix'];errors=[]
   for row in d['owners']:
    native=geometry[row['id']]['polygon'];expected=[(a*p['x']+c1*p['y']+e,b*p['x']+d1*p['y']+f)for p in native];observed=row['points'];errors.extend(min(math.dist(p,xy)for xy in observed)for p in expected)
   assert max(errors)<.001; d.update(label=label,viewport=[w,h],maxAcceptedPolygonProjectionErrorPixels=max(errors));assert d['asset'].endswith('bridge-floor-v4.webp');reports.append(d)
  q.goto('http://127.0.0.1:5308/ruby-village/');tap(q.locator('#continue-game'));q.wait_for_load_state('networkidle')
  while q.locator('#story[open]').count():tap(q.locator('#story-action'))
  for piece in solution:
   tap(q.locator('#tray [data-piece="'+piece['id']+'"]'))
   for _ in range(piece['placement']['turns']):tap(q.locator('#right'))
   a=piece['placement']['anchor'];tap(cell(a['q'],a['r']));tap(q.locator('#place'))
  check('solved-6,1');tap(cell(6,1))
  for _ in range(3):tap(q.locator('#right'))
  tap(q.locator('#place'));check('rotated180');tap(q.locator('#undo'));check('undo-rotation');tap(cell(6,1));tap(cell(6,0));tap(q.locator('#place'));check('moved-6,0');tap(q.locator('#undo'));check('undo-move');c.close()
 b.close()
asset=R/'public/assets/bridge-v2/bridge-floor-v4.webp';served=urllib.request.urlopen('http://127.0.0.1:5308/ruby-village/assets/bridge-v2/bridge-floor-v4.webp').read();assert served==asset.read_bytes();(O/'geometry.json').write_text(json.dumps({'records':reports,'actualServedFloorV4Sha256':hashlib.sha256(served).hexdigest(),'bridgeRegistration':'single uniform source fit, exact clip before shared ground projection; no independent CSS shift'},indent=2)+'\n');print('PASS10 actual bridge3hexclips,sharedcamera,acceptedwaterpolygonprojection,currentmaterialhash')
