import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;solutions=json.loads((R/'src/art-solutions.json').read_text());order=['gate','garden','well','bakery','stream','mill','post','forest'];reports=[]
measure='''()=>{function box(n){let b=n.getAttribute('viewBox')?.split(' ').map(Number),x=+n.getAttribute('x'),y=+n.getAttribute('y'),w=+n.getAttribute('width'),h=+n.getAttribute('height'),m=n.tagName==='svg'?n.parentElement.getScreenCTM():n.getScreenCTM(),a=new DOMPoint(x,y).matrixTransform(m),z=new DOMPoint(x+w,y+h).matrixTransform(m);return{x:a.x,y:a.y,w:z.x-a.x,h:z.y-a.y}}let actors=[...document.querySelectorAll('#board [data-resident]')].map(n=>({id:n.dataset.resident,view:n.dataset.view,anchor:n.getAttribute('transform'),box:box(n.querySelector('image')),href:n.querySelector('image').getAttribute('href'),opacity:getComputedStyle(n.querySelector('image')).opacity})),r=document.querySelector('#ruta-marker'),v=r?.querySelector('svg[data-motion-frame]'),idle=document.querySelector('#ruta-idle');let hidden=sel=>[...document.querySelectorAll(sel)].every(n=>!n.getClientRects().length||getComputedStyle(n).display==='none');return{actors,idle:idle?{box:box(idle),markup:idle.outerHTML}:null,ruta:v?{direction:r.dataset.direction,box:box(v),markup:r.innerHTML}:null,story:!!document.querySelector('#story[open]'),restored:document.querySelector('#app').classList.contains('narrative-restored'),technicalHidden:{grid:hidden('#board [data-grid]'),tray:hidden('#game-controls'),field:hidden('#board #ground-plane')},resultResidents:[...document.querySelectorAll('#completion-scene [data-resident]')].map(n=>n.dataset.resident),resultScene:document.querySelector('#completion-scene [data-result-scene]')?.dataset.resultScene}}'''
with sync_playwright()as p:
 b=p.chromium.launch()
 for sid in os.environ.get('RUBY_QA_SCENES','gate').split(','):
  for touch,w,h in [(False,1280,720),(True,844,390)]:
   dest=O/sid/str(w)
   if (dest/'report.json').exists():continue
   dest.mkdir(parents=True,exist_ok=True);c=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch,reduced_motion='no-preference',record_video_dir=str(dest/'raw'),record_video_size={'width':w,'height':h});prior=order[:order.index(sid)];c.add_init_script("if(!localStorage.getItem('ruby-village:chapter-1:v1'))localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify("+json.dumps({'version':2,'completed':prior,'introSeen':prior})+"))");q=c.new_page();cdp=c.new_cdp_session(q);errors=[];bad=[];q.on('pageerror',lambda e:errors.append(str(e)));q.on('response',lambda r:bad.append(r.url)if r.status>=400 else None);states=[]
   def tap(loc):
    loc.scroll_into_view_if_needed();z=loc.bounding_box();assert z;xy={'x':z['x']+z['width']/2,'y':z['y']+z['height']/2}
    if touch:cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{**xy,'id':1}]});cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    else:q.mouse.click(**xy)
   def capture(label):
    q.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');data=q.evaluate(measure);data['layout']=q.evaluate('''()=>{let box=n=>{let r=n.getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height,bottom:r.bottom,top:r.top}};let matrix=n=>{let m=n?.getScreenCTM();return m?[m.a,m.b,m.c,m.d,m.e,m.f]:null};return{story:box(document.querySelector('#story')),field:box(document.querySelector('#field')),board:box(document.querySelector('#board')),wide:box(document.querySelector('#board [data-surroundings]')),gateKind:document.querySelector('#board [data-painted-gate]')?.dataset.paintedGate,reserve:getComputedStyle(document.querySelector('#app')).getPropertyValue('--dialogue-reserve'),painted:matrix(document.querySelector('#board [data-painted-world]')),residents:matrix(document.querySelector('#board [data-scene-residents]')),foregrounds:[...document.querySelectorAll('#board [data-painted-foreground]')].map(matrix)}}''');data['label']=label;states.append(data)
    if data['story']:assert data['technicalHidden']['grid']and data['technicalHidden']['tray'];assert data['restored']or data['technicalHidden']['field']
    assert all(a['opacity']=='1'for a in data['actors']);q.screenshot(path=str(dest/f'{len(states):02}-{label}.jpg'));return data
   q.goto('http://127.0.0.1:5298/ruby-village/');tap(q.locator('#continue-game'));q.wait_for_timeout(350)
   while q.locator('#prologue-panel[open]').count():
    q.wait_for_function("document.querySelector('#prologue-canvas').dataset.ready==='true'");frame=q.locator('#prologue-panel').get_attribute('data-frame');q.screenshot(path=str(dest/f'prologue-{frame}.jpg'));assert q.locator('#prologue-canvas [data-cell],#prologue-canvas [data-grid]').count()==0;tap(q.locator('#prologue-next'));q.wait_for_timeout(30)
   q.wait_for_load_state('networkidle');q.wait_for_selector('#app[data-motion="ready"]')
   while q.locator('#story[open]').count():capture('intro');tap(q.locator('#story-action'))
   capture('activity');tap(q.locator('#settings-open'));tap(q.locator('#pause-settings'));tap(q.locator('#story-replay'))
   while q.locator('#story[open]').count():capture('replay');tap(q.locator('#story-action'))
   q.reload();tap(q.locator('#continue-game'));q.wait_for_load_state('networkidle');capture('reload')
   for ident,placement in solutions[sid].items():
    tap(q.locator('#tray [data-piece="'+ident+'"]'))
    for _ in range(placement['turns']):tap(q.locator('#right'))
    a=placement['anchor'];tap(q.locator(f'#board [data-cell="{a["q"]},{a["r"]}"]>polygon.cell'));tap(q.locator('#place'));assert q.locator('#board [data-owner="'+ident+'"]').count()>0,('piece not placed',sid,w,ident)
   capture('solved');tap(q.locator('#check'));q.wait_for_selector('#story[open]',timeout=90000)
   while q.locator('#story[open]').count():capture('arrival');tap(q.locator('#story-action'))
   q.wait_for_selector('#completion-panel[open]');final=capture('result');assert len(final['resultResidents'])==len(final['actors']);assert not errors and not bad
   data=dict(scene=sid,viewport=[w,h],input='native CDP touch'if touch else'mouse',states=states,pageErrors=errors,httpErrors=bad,physicalPhone='NOT RUN',runtimeMotion='normal existing game motion; not MPFB art acceptance');reports.append(data);(dest/'report.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');video=q.video;c.close();video.save_as(str(dest/'actual-solve-silent.webm'))
   for x in (dest/'raw').glob('*'):x.unlink()
   (dest/'raw').rmdir();print('COMPLETE',sid,w,flush=True)
 b.close()
reports=[json.loads(p.read_text())for p in O.glob('*/*/report.json')];(O/'report.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
