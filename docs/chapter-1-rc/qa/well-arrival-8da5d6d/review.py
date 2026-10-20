import json,math
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
solution=json.loads((ROOT/'src/art-solutions.json').read_text())['well'];reports=[]
measure='''()=>{function rect(n,attrs=false){let m=n.tagName==='svg'?n.parentElement.getScreenCTM():n.getScreenCTM(),x=attrs?+n.getAttribute('x'):0,y=attrs?+n.getAttribute('y'):0,w=attrs?+n.getAttribute('width'):0,h=attrs?+n.getAttribute('height'):0;let a=new DOMPoint(x,y).matrixTransform(m),b=new DOMPoint(x+w,y+h).matrixTransform(m);return {x:a.x,y:a.y,w:b.x-a.x,h:b.y-a.y}}let actors=[...document.querySelectorAll('#board [data-resident]')].map(n=>({id:n.dataset.resident,view:n.dataset.view,reason:n.dataset.facingReason,anchor:n.getAttribute('transform'),box:rect(n.querySelector('image'),true),opacity:getComputedStyle(n.querySelector('image')).opacity,href:n.querySelector('image').getAttribute('href')}));let r=document.querySelector('#ruta-marker'),v=r?.querySelector('svg[data-motion-frame]');let l=document.querySelector('#board [data-scene-residents]').transform.baseVal.consolidate().matrix;return {actors,ruta:v?{direction:r.dataset.direction,box:rect(v,true),feet:{x:(+v.getAttribute('x')+(+v.getAttribute('width'))*.5-l.e)/l.a,y:(+v.getAttribute('y')+(+v.getAttribute('height'))*192/216-l.f)/l.d}}:null}}'''
with sync_playwright() as p:
 b=p.chromium.launch()
 for w,h in [(1280,720),(844,390)]:
  c=b.new_context(viewport={'width':w,'height':h},reduced_motion='no-preference',has_touch=w==844,is_mobile=w==844,record_video_dir=str(OUT/'raw-video'));q=c.new_page();errors=[];q.on('pageerror',lambda e:errors.append(str(e)));pages=[]
  q.goto('http://127.0.0.1:5298/ruby-village/');q.locator('#continue-game').click();q.wait_for_load_state('networkidle');q.wait_for_selector('#app[data-motion="ready"]');client=c.new_cdp_session(q)
  def tap(loc):
   r=loc.bounding_box();assert r;xy={'x':r['x']+r['width']/2,'y':r['y']+r['height']/2}
   if w==844:client.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{**xy,'id':1}]});client.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   else:q.mouse.click(**xy)
  def capture(label):
   m=q.evaluate(measure);m['state']=label;m['speaker']=q.locator('#story .eyebrow').inner_text() if q.locator('#story[open]').count() else None
   assert {a['id']:a['anchor'] for a in m['actors']}=={'teacher':'translate(1320 405)'}
   assert all(a['opacity']=='1' for a in m['actors'])
   if m['ruta']:
    a=m['ruta']['box'];z=next(a for a in m['actors'] if a['id']=='teacher')['box'];intersection=max(0,min(a['x']+a['w'],z['x']+z['w'])-max(a['x'],z['x']))*max(0,min(a['y']+a['h'],z['y']+z['h'])-max(a['y'],z['y']));m['rutaTeacherViewportBoxIntersection']=intersection
    feet=m['ruta']['feet'];target=(1320,405);angle=math.atan2(target[1]-feet['y'],target[0]-feet['x']);directions={'e':0,'se':.8445215140369683,'sw':2.2970711395528247,'w':math.pi,'nw':-2.297071139552825,'ne':-.8445215140369683};expected=max(directions,key=lambda d:math.cos(angle-directions[d]));assert m['ruta']['direction']==expected;m['expectedFacing']=expected
   m['rutaMarkup']=q.locator('#ruta-marker').inner_html() if q.locator('#ruta-marker').count() else None;pages.append(m);q.screenshot(path=str(OUT/f'{w}-{label}-{len(pages)}.jpg'))
  while q.locator('#story[open]').count():capture('intro');tap(q.locator('#story-action'))
  capture('activity');tap(q.locator('#settings-open'));tap(q.locator('#pause-settings'));tap(q.locator('#story-replay'))
  while q.locator('#story[open]').count():capture('replay');tap(q.locator('#story-action'))
  q.reload();q.locator('#continue-game').click();q.wait_for_load_state('networkidle');capture('persisted-reload')
  tap(q.locator('#settings-open'));tap(q.locator('#pause-settings'));assert not q.locator('#reduced-motion').is_checked();tap(q.locator('#settings-close'))
  for ident,v in solution.items():
   tap(q.locator(f'[data-piece="{ident}"]'))
   for _ in range(v['turns']):tap(q.locator('#right'))
   a=v['anchor'];r=q.locator(f'[data-cell="{a["q"]},{a["r"]}"] polygon').first.bounding_box();tap(q.locator(f'[data-cell="{a["q"]},{a["r"]}"] polygon').first);tap(q.locator('#place'))
  tap(q.locator('#check'));q.wait_for_selector('#story[open]',timeout=60000)
  while q.locator('#story[open]').count():capture('arrival');tap(q.locator('#story-action'))
  q.wait_for_selector('#completion-panel[open]');capture('result');assert q.locator('#completion-scene [data-resident]').count()==1
  assert not errors;reports.append({'viewport':[w,h],'normalMotionRealUISolve':True,'pages':pages,'pageErrors':errors})
  video=q.video;c.close();video.save_as(str(OUT/f'well-normal-{w}-silent.webm'))
 b.close()
(OUT/'report.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n');print('PASS well two normal-motion solves/all arrival pages/result/replay/reload')
