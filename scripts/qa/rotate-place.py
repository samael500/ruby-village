"""Real input regression for released invalid preview -> rotate -> auto place (#61)."""
import json,os,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/evidence/rotate-place';OUT.mkdir(parents=True,exist_ok=True)
code="""import {productionLevels as levels} from './src/production-chapter.ts';import{validPlacement}from'./src/game.ts';import{boardCells}from'./src/hex.ts';const result=[];for(const id of ['garden','stream']){const l=levels.find(l=>l.id===id);outer:for(const p of l.pieces.filter(p=>id==='stream'?p.kind==='bridge':p.shape.length>1))for(const anchor of boardCells(l.cols,l.rows))for(let turns=0;turns<6;turns++){if(!validPlacement(l,p.id,{anchor,turns},{})&&validPlacement(l,p.id,{anchor,turns:(turns+1)%6},{})){result.push({level:id,piece:p.id,anchor,turns,size:p.shape.length});break outer;}}}console.log(JSON.stringify(result));"""
node='/home/mskorokhod/.ya/tools/v3/14019382748/bin/node'
cases=json.loads(subprocess.check_output([node,'--experimental-strip-types','--input-type=module','-e',code],cwd=ROOT,text=True));assert len(cases)==2
ids=['gate','garden','well','bakery','stream','mill','post','forest'];results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for touch in [False,True]:
  for case in cases:
   for mode in ['drag','select']:
    ctx=b.new_context(viewport={'width':844 if touch else 1280,'height':390 if touch else 720},has_touch=touch,is_mobile=touch,reduced_motion='reduce',record_video_dir=str(OUT/'raw-video'))
    q=ctx.new_page();errors=[];q.on('pageerror',lambda e:errors.append(str(e)));completed=ids[:ids.index(case['level'])]
    q.add_init_script(f"localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({json.dumps({'version':2,'completed':completed,'introSeen':ids})}))")
    q.goto(os.environ.get('RUBY_QA_URL','http://127.0.0.1:5286/ruby-village/'));q.locator('#continue-game').click()
    while q.locator('#story[open]').count():q.locator('#story-action').click()
    q.locator('#settings-open').click();q.locator('#pause-settings').click();q.locator('#mode').select_option(mode);q.locator('#settings-close').click()
    client=ctx.new_cdp_session(q)
    def center(loc):
     r=loc.bounding_box();assert r;return {'x':r['x']+r['width']/2,'y':r['y']+r['height']/2}
    def touch_event(kind,pos=None):client.send('Input.dispatchTouchEvent',{'type':kind,'touchPoints':[] if pos is None else [{**pos,'id':1}]})
    def tap(loc):
     if touch:touch_event('touchStart',center(loc));touch_event('touchEnd')
     else:loc.click()
    piece=q.locator(f'#tray [data-piece="{case["piece"]}"]');anchor=case['anchor'];cell=q.locator(f'[data-cell="{anchor["q"]},{anchor["r"]}"] > polygon.cell')
    def drop_invalid():
     tap(piece)
     for _ in range(case['turns']):tap(q.locator('#right'))
     assert q.locator(f'[data-owner="{case["piece"]}"]').count()==0
     if mode=='drag':
      a=center(piece);z=center(cell)
      if touch:
       z['y']+=max(42,cell.bounding_box()['height']*.8);touch_event('touchStart',a);touch_event('touchMove',{'x':a['x'],'y':a['y']-40})
       for i in range(1,13):touch_event('touchMove',{'x':a['x']+(z['x']-a['x'])*i/12,'y':a['y']+(z['y']-a['y'])*i/12})
       touch_event('touchEnd')
      else:q.mouse.move(**a);q.mouse.down();q.mouse.move(**z,steps=15);q.mouse.up()
     else:tap(cell)
    drop_invalid()
    assert q.locator('#placement-preview[data-preview="invalid"]').count(),case
    assert q.locator(f'[data-owner="{case["piece"]}"]').count()==0
    if mode=='drag' and touch:
     # An active gesture consumes button activation; keyboard cannot prematurely place it.
     q.evaluate('window.gestureEvents=[];for(const t of ["pointerdown","pointerup","pointercancel","lostpointercapture"])document.addEventListener(t,e=>window.gestureEvents.push({type:t,target:e.target.id||e.target.tagName,pointer:e.pointerId}),true)')
     a=center(piece);touch_event('touchStart',a)
     for _ in range(180):
      q.keyboard.press('Tab')
      if q.locator('#right').evaluate('(n)=>n===document.activeElement'):break
     assert q.locator('#right').evaluate('(n)=>n===document.activeElement')
     q.keyboard.press('Space')
     assert q.locator('#placement-preview[data-preview="invalid"]').count() # active gesture consumes button activation
     assert q.locator(f'[data-owner="{case["piece"]}"]').count()==0
     touch_event('touchCancel')
     assert q.locator('#placement-preview[data-preview="invalid"]').count()
     assert q.locator(f'[data-owner="{case["piece"]}"]').count()==0
    q.screenshot(path=str(OUT/f'{case["level"]}-{mode}-{touch}-invalid.jpg'))
    tap(q.locator('#right'))
    if mode=='select':
     assert q.locator('#placement-preview[data-preview="valid"]').count(),q.evaluate('({status:document.querySelector("#status").textContent,preview:document.querySelector("#placement-preview")?.outerHTML,active:document.activeElement?.id,events:window.gestureEvents,owners:[...document.querySelectorAll("[data-owner]")].filter(n=>n.dataset.owner).map(n=>n.dataset.owner)})');assert q.locator(f'[data-owner="{case["piece"]}"]').count()==0;tap(q.locator('#place'))
    q.wait_for_function('(v)=>document.querySelectorAll(`[data-owner="${v.id}"]`).length===v.n',arg={'id':case['piece'],'n':case['size']})
    assert not q.locator('#placement-preview').count();q.screenshot(path=str(OUT/f'{case["level"]}-{mode}-{touch}-placed.jpg'))
    saved=q.evaluate("JSON.parse(localStorage.getItem('ruby-village:chapter-1:v1')).session.layout")
    assert saved[case['piece']]=={'anchor':anchor,'turns':(case['turns']+1)%6},saved
    tap(q.locator('#undo'));assert q.locator(f'[data-owner="{case["piece"]}"]').count()==0
    drop_invalid()
    assert q.locator('#placement-preview[data-preview="invalid"]').count()
    assert q.evaluate("JSON.parse(localStorage.getItem('ruby-village:chapter-1:v1')).session.layout")=={}
    tap(q.locator('#other'));assert not q.locator('#placement-preview').count()
    assert q.evaluate("JSON.parse(localStorage.getItem('ruby-village:chapter-1:v1')).session.layout")=={}
    drop_invalid();tap(q.locator('#undo'));assert not q.locator('#placement-preview').count()
    assert q.locator(f'[data-owner="{case["piece"]}"]').count()==0
    assert q.evaluate("JSON.parse(localStorage.getItem('ruby-village:chapter-1:v1')).session.layout")=={}
    assert not errors
    results.append({'case':case,'input':'native CDP touch' if touch else 'mouse','mode':mode,'invalidReleased':True,'rotationConfirmedOnlyInDrag':True,'anchorUnchanged':True,'singleUndoRemovesWholeInstance':True,'cancelAndPendingUndoLeaveSaveEmpty':True,'activeTouchGestureAndCancel':'PASS' if touch and mode=='drag' else 'separate touch coverage','pageErrors':errors})
    video=q.video
    ctx.close()
    video.save_as(str(OUT/f'{case["level"]}-{mode}-{touch}.webm'))
 b.close()
(OUT/'report.json').write_text(json.dumps({'results':results,'physicalPhone':'NOT RUN','scope':'8 cases; progress fixtures only; actual UI drop/rotation/place/save/undo, active-drag cancellation separate regression'},indent=2)+'\n');print('PASS8 rotate-place cases')
