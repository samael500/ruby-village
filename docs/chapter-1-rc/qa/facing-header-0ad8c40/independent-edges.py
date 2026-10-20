import json,math
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
levels=json.loads((ROOT/'docs/chapter-1-rc/production-solutions.json').read_text());ids=[l['id'] for l in levels];results=[]
def actor_state(q):
 return q.locator('#board [data-resident]').evaluate_all('''ns=>ns.map(n=>{let transforms=[];for(let p=n;p&&p.id!=='board';p=p.parentElement){let s=getComputedStyle(p);transforms.push({attribute:p.getAttribute('transform'),css:s.transform,opacity:s.opacity})}let i=n.querySelector('image');return {id:n.dataset.resident,view:n.dataset.view,reason:n.dataset.facingReason,anchor:n.getAttribute('transform'),href:i.getAttribute('href'),opacity:getComputedStyle(i).opacity,image:[i.getAttribute('x'),i.getAttribute('y'),i.getAttribute('width'),i.getAttribute('height')],transforms}})''')
with sync_playwright() as p:
 b=p.chromium.launch()
 # Hold only new resident images. The original idle must remain present while
 # those requests are outstanding, then change at the same authored anchor.
 c=b.new_context(viewport={'width':844,'height':390});q=c.new_page();held=[]
 q.route('**/characters-facing-v1/residents/*',lambda r:held.append(r))
 q.add_init_script("localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({version:2,completed:['gate'],introSeen:['gate']}))")
 q.goto('http://127.0.0.1:5298/ruby-village/',wait_until='domcontentloaded');q.locator('#continue-game').click();q.locator('[data-resident="rabbit"]').wait_for()
 q.wait_for_function('document.querySelector("[data-resident=rabbit] image")?.getAttribute("href").includes("characters-v1")')
 pending=actor_state(q);assert pending[0]['view']=='idle';q.screenshot(path=str(OUT/'slow-load-fallback.jpg'))
 for r in held:r.continue_()
 q.unroute('**/characters-facing-v1/residents/*');q.wait_for_function('document.querySelector("[data-resident=rabbit]")?.dataset.view==="conversation-left"');ready=actor_state(q)
 assert pending[0]['anchor']==ready[0]['anchor'];q.screenshot(path=str(OUT/'slow-load-ready.jpg'))
 results.append({'case':'delayed authored image','fallback':pending,'ready':ready,'noLoadDisappearance':True});c.close()
 # A real normal-motion mill solve exercises two speakers and arrival facing.
 c=b.new_context(viewport={'width':1280,'height':720},reduced_motion='no-preference',record_video_dir=str(OUT/'normal-video-raw'));q=c.new_page();errors=[];q.on('pageerror',lambda e:errors.append(str(e)))
 q.add_init_script(f"localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({json.dumps({'version':2,'completed':ids[:5],'introSeen':ids[:5]})}))")
 q.goto('http://127.0.0.1:5298/ruby-village/');q.locator('#continue-game').click();q.wait_for_selector('#app[data-motion="ready"]');q.wait_for_load_state('networkidle')
 pages=[]
 def snapshot(phase):
  actors=actor_state(q);ruta=q.locator('#ruta-idle,#ruta-marker').evaluate_all('ns=>ns.map(n=>({id:n.id,direction:n.dataset.direction,reason:n.dataset.facingReason,opacity:getComputedStyle(n).opacity,frame:n.querySelector("[data-motion-frame]")?.outerHTML.slice(0,500)}))')
  pages.append({'phase':phase,'speaker':q.locator('#story .eyebrow').inner_text() if q.locator('#story[open]').count() else None,'actors':actors,'ruta':ruta});q.screenshot(path=str(OUT/f'mill-{phase}-{len(pages)}.jpg'))
 while q.locator('#story[open]').count():snapshot('intro');q.locator('#story-action').click()
 before=actor_state(q)
 for x,y in [(50,150),(1200,300),(400,600),(800,100)]:q.mouse.move(x,y)
 after=actor_state(q);assert [(a['view'],a['anchor']) for a in before]==[(a['view'],a['anchor']) for a in after]
 q.set_viewport_size({'width':844,'height':390});landscape=actor_state(q);assert [a['anchor'] for a in before]==[a['anchor'] for a in landscape];snapshot('landscape')
 q.set_viewport_size({'width':1280,'height':720});q.locator('#settings-open').click();q.locator('#pause-settings').click();assert not q.locator('#reduced-motion').is_checked();q.locator('#settings-close').click()
 for ident,placement in levels[5]['solution'].items():
  q.locator(f'[data-piece="{ident}"]').click()
  for _ in range(placement['turns']):q.locator('#right').click()
  a=placement['anchor'];cell=q.locator(f'[data-cell="{a["q"]},{a["r"]}"] polygon').first;r=cell.bounding_box();assert r
  q.mouse.click(r['x']+r['width']/2,r['y']+r['height']/2);q.locator('#place').click()
 q.evaluate('''window.walkSamples=[];window.walkObserver=setInterval(()=>{let r=document.querySelector('#ruta-marker');if(r)window.walkSamples.push({ms:r.dataset.routeMs,direction:r.dataset.direction,residents:[...document.querySelectorAll('#board [data-resident]')].map(n=>({id:n.dataset.resident,view:n.dataset.view,anchor:n.getAttribute('transform')}))})},100)''')
 q.locator('#check').click();q.wait_for_selector('#story[open]',timeout=60000);samples=q.evaluate('clearInterval(window.walkObserver);window.walkSamples');assert len(samples)>20 and len({s['ms'] for s in samples})>20
 while q.locator('#story[open]').count():snapshot('arrival');q.locator('#story-action').click()
 q.wait_for_selector('#completion-panel[open]');q.screenshot(path=str(OUT/'mill-normal-result.jpg'));assert q.locator('#completion-scene [data-resident]').count()==2;assert not errors
 results.append({'case':'normal motion mill real UI solve','pointerDoesNotTrack':True,'anchorsStableResize':True,'pages':pages,'walkSamples':samples,'pageErrors':errors,'gaitAcceptance':False})
 video=q.video;c.close();video.save_as(str(OUT/'mill-normal-motion-silent.webm'));b.close()
(OUT/'independent-edges.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n');print('PASS delayed image fallback, pointer/resize edges, normal-motion mill solve')
