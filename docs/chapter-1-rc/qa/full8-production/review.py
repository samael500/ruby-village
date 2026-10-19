"""Sequential actual UI acceptance. Never inject layout, progress, or wins.
Run only against frozen ordinary layout-2 production build; no private activation.
"""
import json,os,hashlib,subprocess,time
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
URL=os.environ.get('RUBY_QA_URL','http://127.0.0.1:5298/ruby-village/')
ORDER=['gate','garden','well','bakery','stream','mill','post','forest']
SOLUTIONS=json.loads((R/'src/art-solutions.json').read_text())
HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert 'PRODUCTION_LAYOUT_VERSION=2' in (R/'src/production-chapter.ts').read_text(),'ordinary production layout2 required'
MEASURE="""()=>{let app=document.querySelector('#app'),board=document.querySelector('#board'),story=document.querySelector('#story');let hidden=s=>[...document.querySelectorAll(s)].every(n=>!n.getClientRects().length||getComputedStyle(n).display==='none');return {levelTitle:document.querySelector('h1').childNodes[0]?.textContent.trim(),motion:app.dataset.motion,board:board.getBoundingClientRect().toJSON(),story:story.open,storyText:document.querySelector('#story-text').textContent,narrative:app.classList.contains('narrative-scene'),restored:app.classList.contains('narrative-restored'),technicalHidden:{grid:hidden('#board [data-grid]'),tray:hidden('#game-controls'),ground:hidden('#board #ground-plane')},actors:[...board.querySelectorAll('[data-resident]')].map(n=>({id:n.dataset.resident,view:n.dataset.view,anchor:n.getAttribute('transform'),opacity:getComputedStyle(n).opacity,images:[...n.querySelectorAll('image')].map(i=>({href:i.getAttribute('href'),bounds:i.getBoundingClientRect().toJSON()}))})),owners:[...new Set([...board.querySelectorAll('[data-owner]')].map(n=>n.dataset.owner))],resultScene:document.querySelector('#completion-scene [data-result-scene]')?.dataset.resultScene,resultResidents:[...document.querySelectorAll('#completion-scene [data-resident]')].map(n=>n.dataset.resident),save:JSON.parse(localStorage.getItem('ruby-village:chapter-1:v1'))}}"""
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 for touch,w,h in [(False,1280,720),(True,844,390)]:
  dest=O/str(w);dest.mkdir(exist_ok=True);states=[];errors=[];http=[]
  context=browser.new_context(viewport={'width':w,'height':h},is_mobile=touch,has_touch=touch,reduced_motion='no-preference',record_video_dir=str(dest/'raw'),record_video_size={'width':w,'height':h})
  page=context.new_page();cdp=context.new_cdp_session(page)
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:http.append({'url':r.url,'status':r.status}) if r.status>=400 else None)
  def tap(loc):
   loc.scroll_into_view_if_needed();box=loc.bounding_box();assert box
   x,y=box['x']+box['width']/2,box['y']+box['height']/2
   if touch:
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y,'id':1}]});cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   else:page.mouse.click(x,y)
  def capture(scene,label):
   page.wait_for_timeout(80);data=page.evaluate(MEASURE);data.update(scene=scene,label=label);states.append(data);(dest/'states-live.json').write_text(json.dumps(states,ensure_ascii=False,indent=2)+'\n')
   if data['story']:
    assert data['technicalHidden']['grid'] and data['technicalHidden']['tray'],data
    assert data['restored'] or data['technicalHidden']['ground'],data
   page.screenshot(path=str(dest/f'{len(states):03}-{scene}-{label}.jpg'));return data
  def story(scene,label):
   count=0
   while page.locator('#story[open]').count():
    capture(scene,label+str(count));tap(page.locator('#story-action'));count+=1;assert count<20
  def resume():
   page.reload();tap(page.locator('#continue-game'));page.wait_for_load_state('networkidle');page.wait_for_selector('#app[data-motion="ready"]')
  assert context.storage_state()['origins']==[],'clean sequence must start clean'
  page.goto(URL);assert page.evaluate("JSON.parse(localStorage.getItem('ruby-village:chapter-1:v1'))?.completed??[]")==[]
  assets=page.evaluate("[...document.scripts].map(s=>s.src).filter(Boolean)")
  tap(page.locator('#continue-game'))
  while page.locator('#prologue-panel[open]').count():
   page.wait_for_function("document.querySelector('#prologue-canvas').dataset.ready==='true'");f=page.locator('#prologue-panel').get_attribute('data-frame');assert page.locator('#prologue-canvas [data-grid],#prologue-canvas [data-cell]').count()==0;page.screenshot(path=str(dest/f'prologue-{f}.jpg'));tap(page.locator('#prologue-next'))
  for sid in ORDER:
   page.wait_for_load_state('networkidle');page.wait_for_selector('#app[data-motion="ready"]');story(sid,'intro-')
   # Explicit real settings control selection; never mutate the mode variable.
   tap(page.locator('#settings-open'));tap(page.locator('#pause-settings'))
   if page.locator('#mode').input_value()!='select':
    tap(page.locator('#mode'));page.keyboard.press('Home');page.keyboard.press('Enter')
   assert page.locator('#mode').input_value()=='select'
   assert not page.locator('#reduced-motion').is_checked()
   tap(page.locator('#settings-close'));capture(sid,'activity')
   tap(page.locator('#settings-open'));tap(page.locator('#pause-settings'));tap(page.locator('#story-replay'));story(sid,'replay-')
   resume();before=capture(sid,'reload-empty');assert before['save']['completed']==ORDER[:ORDER.index(sid)]
   for index,(ident,placement) in enumerate(SOLUTIONS[sid].items()):
    tap(page.locator('#tray [data-piece="'+ident+'"]'))
    for _ in range(placement['turns']):tap(page.locator('#right'))
    a=placement['anchor'];tap(page.locator(f'#board [data-cell="{a["q"]},{a["r"]}"]>polygon.cell'));tap(page.locator('#place'))
    assert page.locator('#board [data-owner="'+ident+'"]').count()>0,('placement failed',sid,w,ident)
    if index==0:
     first=capture(sid,'first-placement');resume();after=capture(sid,'reload-first-placement');assert first['save']['session']['layout']==after['save']['session']['layout']
   solved=capture(sid,'solved');resume();reloaded=capture(sid,'reload-solved');assert solved['save']['session']['layout']==reloaded['save']['session']['layout']
   tap(page.locator('#check'));page.wait_for_selector('#story[open]',timeout=120000);story(sid,'arrival-');page.wait_for_selector('#completion-panel[open]');result=capture(sid,'result');assert result['resultScene']==result['levelTitle']
   assert result['save']['completed']==ORDER[:ORDER.index(sid)+1];assert not errors and not http,(errors,http)
   if sid!='forest':tap(page.locator('#next-level'))
   else:tap(page.locator('#completion-map'));story(sid,'ending-');capture(sid,'completed-map')
   (dest/'progress.json').write_text(json.dumps({'head':HEAD,'states':states,'errors':errors,'http':http},ensure_ascii=False,indent=2)+'\n');print('COMPLETE',sid,w,flush=True)
  report={'head':HEAD,'servedScripts':assets,'viewport':[w,h],'input':'native CDP touch; native select control keyboard navigation if needed' if touch else 'mouse','storage':'clean start, no init scripts/fixtures','normalMotion':True,'states':states,'errors':errors,'http':http,'physicalPhone':'NOT RUN','familyTest':'NOT RUN','video':'actual sequential play, silent capture'}
  (dest/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');video=page.video;context.close();video.save_as(str(dest/'actual-full-chapter-silent.webm'))
  for f in (dest/'raw').glob('*'):f.unlink()
  (dest/'raw').rmdir()
 browser.close()
