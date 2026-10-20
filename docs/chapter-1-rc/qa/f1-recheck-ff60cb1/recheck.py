import json,math
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
levels=json.loads((ROOT/'docs/chapter-1-rc/production-solutions.json').read_text());ids=[l['id'] for l in levels];reports=[]
measure='''()=>{function rect(n,attrs=false){let m=n.tagName==='svg'?n.parentElement.getScreenCTM():n.getScreenCTM(),x=attrs?+n.getAttribute('x'):0,y=attrs?+n.getAttribute('y'):0,w=attrs?+n.getAttribute('width'):0,h=attrs?+n.getAttribute('height'):0;let a=new DOMPoint(x,y).matrixTransform(m),b=new DOMPoint(x+w,y+h).matrixTransform(m);return {x:a.x,y:a.y,w:b.x-a.x,h:b.y-a.y}}let actors=[...document.querySelectorAll('#board [data-resident]')].map(n=>({id:n.dataset.resident,view:n.dataset.view,reason:n.dataset.facingReason,anchor:n.getAttribute('transform'),box:rect(n.querySelector('image'),true),opacity:getComputedStyle(n.querySelector('image')).opacity}));let r=document.querySelector('#ruta-marker'),v=r?.querySelector('svg[data-motion-frame]');let l=document.querySelector('#board [data-scene-residents]').transform.baseVal.consolidate().matrix;return {actors,ruta:v?{direction:r.dataset.direction,box:rect(v,true),feet:{x:(+v.getAttribute('x')+(+v.getAttribute('width'))*.5-l.e)/l.a,y:(+v.getAttribute('y')+(+v.getAttribute('height'))*192/216-l.f)/l.d}}:null}}'''
with sync_playwright() as p:
 b=p.chromium.launch()
 for w,h in [(1280,720),(844,390)]:
  c=b.new_context(viewport={'width':w,'height':h},reduced_motion='no-preference',record_video_dir=str(OUT/'raw-video'));q=c.new_page();errors=[];q.on('pageerror',lambda e:errors.append(str(e)));pages=[]
  q.add_init_script(f"if(!localStorage.getItem('ruby-village:chapter-1:v1'))localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({json.dumps({'version':2,'completed':ids[:5],'introSeen':ids[:5]})}))")
  q.goto('http://127.0.0.1:5298/ruby-village/');q.locator('#continue-game').click();q.wait_for_load_state('networkidle');q.wait_for_selector('#app[data-motion="ready"]')
  def capture(label):
   m=q.evaluate(measure);m['state']=label;m['speaker']=q.locator('#story .eyebrow').inner_text() if q.locator('#story[open]').count() else None
   assert {a['id']:a['anchor'] for a in m['actors']}=={'miller':'translate(1430 398)','squirrel':'translate(1530 450)'}
   assert all(a['opacity']=='1' for a in m['actors'])
   if m['ruta']:
    a=m['ruta']['box'];z=next(a for a in m['actors'] if a['id']=='squirrel')['box'];intersection=max(0,min(a['x']+a['w'],z['x']+z['w'])-max(a['x'],z['x']))*max(0,min(a['y']+a['h'],z['y']+z['h'])-max(a['y'],z['y']));assert intersection==0,m;m['rutaSquirrelClippedViewportIntersection']=intersection
    feet=m['ruta']['feet'];target=(1430,398);angle=math.atan2(target[1]-feet['y'],target[0]-feet['x']);directions={'e':0,'se':.8445215140369683,'sw':2.2970711395528247,'w':math.pi,'nw':-2.297071139552825,'ne':-.8445215140369683};expected=max(directions,key=lambda d:math.cos(angle-directions[d]));assert m['ruta']['direction']==expected;m['expectedFacing']=expected
   pages.append(m);q.screenshot(path=str(OUT/f'{w}-{label}-{len(pages)}.jpg'))
  while q.locator('#story[open]').count():capture('intro');q.locator('#story-action').click()
  capture('activity');q.locator('#settings-open').click();q.locator('#pause-settings').click();q.locator('#story-replay').click()
  while q.locator('#story[open]').count():capture('replay');q.locator('#story-action').click()
  q.reload();q.locator('#continue-game').click();q.wait_for_load_state('networkidle');capture('persisted-reload')
  q.locator('#settings-open').click();q.locator('#pause-settings').click();assert not q.locator('#reduced-motion').is_checked();q.locator('#settings-close').click()
  for ident,v in levels[5]['solution'].items():
   q.locator(f'[data-piece="{ident}"]').click()
   for _ in range(v['turns']):q.locator('#right').click()
   a=v['anchor'];r=q.locator(f'[data-cell="{a["q"]},{a["r"]}"] polygon').first.bounding_box();q.mouse.click(r['x']+r['width']/2,r['y']+r['height']/2);q.locator('#place').click()
  q.locator('#check').click();q.wait_for_selector('#story[open]',timeout=60000)
  while q.locator('#story[open]').count():capture('arrival');q.locator('#story-action').click()
  q.wait_for_selector('#completion-panel[open]');capture('result');assert q.locator('#completion-scene [data-resident]').count()==2
  assert not errors;reports.append({'viewport':[w,h],'normalMotionRealUISolve':True,'pages':pages,'pageErrors':errors})
  video=q.video;c.close();video.save_as(str(OUT/f'mill-normal-{w}-silent.webm'))
 b.close()
(OUT/'report.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n');print('PASS F1 two normal-motion solves/all arrival pages/result/replay/reload,strict0viewportoverlap')
