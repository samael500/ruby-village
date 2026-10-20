"""Production-build actual input regression for #61; CDP touch is real Chromium input.
Run /tmp/ruby-rc-tools/bin/python scripts/placement61-browser.py with preview on5188.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json,subprocess,shutil,os
R=Path(__file__).resolve().parents[1];O=Path(os.environ.get('PLACEMENT61_OUT',str(R/'docs/chapter-1-rc/placement-61')));O.mkdir(parents=True,exist_ok=True);F=json.loads(subprocess.check_output([shutil.which('node')or'/home/mskorokhod/.ya/tools/v3/14019382748/bin/node','--experimental-strip-types','--input-type=module','-e',"import{productionLevels as levels,PRODUCTION_LAYOUT_VERSION as version}from'./src/production-chapter.ts';import{boardCells,key}from'./src/hex.ts';import{validPlacement}from'./src/game.ts';const o={version,ids:levels.map(l=>l.id),levels:{}};for(const id of ['garden','stream']){const l=levels.find(x=>x.id===id),stone=l.pieces.find(p=>p.kind!=='bridge'&&p.shape.length>1),bridge=l.pieces.find(p=>p.kind==='bridge'),cells=boardCells(l.cols,l.rows);o.levels[id]={id,cols:l.cols,rows:l.rows,pieces:l.pieces,solution:l.solution,terrain:l.terrain,stone:stone.id,invalidStone:cells.find(h=>l.terrain[key(h)]&&l.terrain[key(h)]!=='ground'),bridge:bridge?.id,invalidBridge:bridge?cells.find(h=>Array.from({length:6},(_,turns)=>!validPlacement(l,bridge.id,{anchor:h,turns},{})).every(Boolean)):null};}console.log(JSON.stringify(o));"],cwd=R,text=True));(O/'fixtures.json').write_text(json.dumps(F,indent=2)+'\n');URL=os.environ.get('RUBY_QA_URL','http://127.0.0.1:5188/ruby-village/');KEY='ruby-village:chapter-1:v1';results=[]

def point(page,h):
 return page.locator(f'[data-cell="{h["q"]},{h["r"]}"] > polygon.cell').evaluate('p=>{const a=[...p.points];const x=a.reduce((s,v)=>s+v.x,0)/a.length,y=a.reduce((s,v)=>s+v.y,0)/a.length;const v=new DOMPoint(x,y).matrixTransform(p.getScreenCTM());return{x:v.x,y:v.y,h:p.getBoundingClientRect().height}}')
def center(loc):
 b=loc.bounding_box();assert b;return {'x':b['x']+b['width']/2,'y':b['y']+b['height']/2}
def saved(page):return page.evaluate('(key)=>JSON.parse(localStorage.getItem(key)).session.layout',KEY)
def preview(page):
 return page.locator('#placement-preview').evaluate('(e)=>({valid:e.dataset.preview,points:[...e.querySelectorAll("polygon")].map(p=>p.getAttribute("points")),mark:e.textContent})')
def tap(page,loc,touch):
 loc.scroll_into_view_if_needed()
 if touch:
  pos=center(loc);cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{**pos,'id':1,'radiusX':4,'radiusY':4}]});page.wait_for_timeout(80);cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
 else:loc.click()
 page.wait_for_timeout(120)
def drag(page,cdp,start,end,touch,cancel=False):
 if touch:
  def emit(typ,p=None):cdp.send('Input.dispatchTouchEvent',{'type':typ,'touchPoints':[]if p is None else[{'x':p['x'],'y':p['y'],'id':1,'radiusX':4,'radiusY':4}]})
  emit('touchStart',start);page.wait_for_timeout(30)
  # Lift vertically first to respect the tray's intentional horizontal pan-x scrolling.
  lift={'x':start['x'],'y':start['y']-28};emit('touchMove',lift)
  for i in range(1,13):emit('touchMove',{'x':lift['x']+(end['x']-lift['x'])*i/12,'y':lift['y']+(end['y']-lift['y'])*i/12});page.wait_for_timeout(12)
  emit('touchCancel'if cancel else'touchEnd')
 else:
  page.mouse.move(start['x'],start['y']);page.mouse.down();page.mouse.move(end['x'],end['y'],steps=14);page.mouse.up()
 page.wait_for_timeout(120)
def open_case(page,level_id,mode,layout=None):
 level=F['levels'][level_id];raw={'version':2,'layoutVersion':F['version'],'completed':F['ids'],'introSeen':F['ids'],'preferences':{'mode':mode,'reducedMotion':True},'session':{'levelId':level_id,'cols':level['cols'],'rows':level['rows'],'layout':layout or{},'mode':mode,'reducedMotion':True}}
 page.goto(URL);page.evaluate('([key,raw])=>localStorage.setItem(key,JSON.stringify(raw))',[KEY,raw]);page.reload();page.locator('#continue-game').click();page.wait_for_selector('#board [data-cell]');page.wait_for_timeout(120);return level

def run_case(page,cdp,touch,mode,level_id,kind):
 level=open_case(page,level_id,mode);piece=level['bridge']if kind=='bridge'else level['stone'];invalid=level['invalidBridge']if kind=='bridge'else level['invalidStone'];target=level['solution'][piece];button=page.locator(f'#tray [data-piece="{piece}"]');button.scroll_into_view_if_needed();before=saved(page)
 bad=point(page,invalid)
 if mode=='drag':
  end={**bad,'y':bad['y']+(max(42,bad['h']*.8)if touch else 0)};drag(page,cdp,center(button),end,touch)
 else:
  tap(page,button,touch);tap(page,page.locator(f'[data-cell="{invalid["q"]},{invalid["r"]}"] > polygon.cell'),touch)
 page.wait_for_selector('#placement-preview[data-preview="invalid"]');assert button.get_attribute('aria-pressed')=='true';assert saved(page)==before;assert page.locator('#place').is_disabled();assert page.evaluate('inputAudit.activeCaptures.size')==0
 initial=preview(page);page.screenshot(path=str(O/f'{"touch"if touch else"mouse"}-{mode}-{kind}-invalid.png'))
 for _ in range(3):
  tap(page,page.locator('#right'),touch);assert saved(page)==before
 assert preview(page)['valid']=='invalid';assert button.get_attribute('aria-pressed')=='true'
 # Return to exact target turns; untouched before=0, three turns already consumed.
 for _ in range((target['turns']-3)%6):
  tap(page,page.locator('#right'),touch)
 good=point(page,target['anchor'])
 if mode=='drag':
  grab=point(page,invalid);end={**good,'y':good['y']+(max(42,good['h']*.8)if touch else 0)};drag(page,cdp,grab,end,touch)
 else:
  tap(page,page.locator(f'[data-cell="{target["anchor"]["q"]},{target["anchor"]["r"]}"] > polygon.cell'),touch);assert not page.locator('#place').is_disabled();tap(page,page.locator('#place'),touch)
 assert saved(page)=={piece:target},(touch,mode,kind,saved(page),piece,target,page.evaluate('({preview:document.querySelector(\"#placement-preview\")?.outerHTML,events:inputAudit.events.slice(-20)})'))
 assert page.locator('#placement-preview').count()==0;assert button.get_attribute('aria-pressed')=='false';assert page.locator('#tray').is_visible();assert page.evaluate('inputAudit.activeCaptures.size')==0
 page.screenshot(path=str(O/f'{"touch"if touch else"mouse"}-{mode}-{kind}-valid.png'))
 (O/f'{"touch"if touch else"mouse"}-{mode}-{kind}-rotation-events.json').write_text(json.dumps(page.evaluate('rotationAudit'),indent=2)+'\n');results.append({'device':'Chromium touch844x390'if touch else'Chromium mouse1280x720','mode':mode,'piece':kind,'invalidPreserved':True,'rotateWithoutCommit':True,'validRepositionConfirmedExactlyOnce':True,'captureReleased':True,'trayVisible':True})

def lifecycle(page,cdp,touch):
 level=open_case(page,'garden','drag');piece=level['stone'];target=level['solution'][piece];layout={piece:target};level=open_case(page,'garden','drag',layout);bad=point(page,level['invalidStone']);good=point(page,target['anchor']);end={**bad,'y':bad['y']+(max(42,bad['h']*.8)if touch else 0)}
 def move_old():
  drag(page,cdp,point(page,target['anchor']),end,touch);assert preview(page)['valid']=='invalid';assert saved(page)==layout
 move_old();tap(page,page.locator('#other'),touch);assert page.locator('#placement-preview').count()==0;assert saved(page)==layout
 move_old();tap(page,page.locator('#undo'),touch);assert page.locator('#placement-preview').count()==0;assert saved(page)==layout
 move_old();other=next(p['id']for p in level['pieces']if p['id']!=piece);tap(page,page.locator(f'#tray [data-piece="{other}"]'),touch);assert saved(page)==layout;assert page.locator(f'#tray [data-piece="{other}"]').get_attribute('aria-pressed')=='true';tap(page,page.locator('#other'),touch)
 if touch:
  drag(page,cdp,good,end,True,cancel=True);assert saved(page)==layout;assert preview(page)['valid']=='valid';assert page.evaluate('inputAudit.activeCaptures.size')==0;tap(page,page.locator('#other'),True)
 else:
  page.mouse.move(good['x'],good['y']);page.mouse.down();page.mouse.move(end['x'],end['y'],steps=12);page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(150);page.mouse.up();assert saved(page)==layout;page.set_viewport_size({'width':1280,'height':720});page.wait_for_timeout(200);assert preview(page)['valid']=='valid';assert page.evaluate('inputAudit.activeCaptures.size')==0;tap(page,page.locator('#other'),False)
 move_old();tap(page,page.locator('#settings-open'),touch);assert saved(page)==layout;tap(page,page.locator('#pause-continue'),touch);assert preview(page)['valid']=='invalid';assert saved(page)==layout
 page.reload();tap(page,page.locator('#continue-game'),touch);page.wait_for_selector('#board [data-cell]');assert saved(page)==layout;assert page.locator('#placement-preview').count()==0
 results.append({'device':'touch'if touch else'mouse','cancelMovedPieceKeepsConfirmed':True,'undoPendingDoesNotUndoConfirmed':True,'switchSelectionDoesNotLosePiece':True,'systemCancelRestoresSnapshot':True,'pauseThenReloadConfirmedOnly':True})

with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 for touch in ([True]if __import__('os').environ.get('TOUCH_ONLY')else[False,True]):
  ctx=b.new_context(viewport={'width':844,'height':390}if touch else{'width':1280,'height':720},has_touch=touch,is_mobile=touch,record_video_dir=str(O/'raw-video'),record_video_size={'width':844,'height':390}if touch else{'width':1280,'height':720});page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.add_init_script('document.addEventListener("pointerdown",e=>{if(e.target.closest?.("#right"))window.rotationAudit.push({event:e.type,time:e.timeStamp})},true);document.addEventListener("pointerup",e=>{if(e.target.closest?.("#right"))window.rotationAudit.push({event:e.type,time:e.timeStamp})},true);document.addEventListener("click",e=>{if(e.target.closest?.("#right")){window.rotationAudit.push({event:e.type,time:e.timeStamp,before:document.querySelector("#placement-preview")?.innerHTML});requestAnimationFrame(()=>window.rotationAudit.push({event:"after-render",time:performance.now(),after:document.querySelector("#placement-preview")?.innerHTML}))}},true);window.rotationAudit=[];window.inputAudit={activeCaptures:new Set(),events:[]};for(const type of ["gotpointercapture","lostpointercapture","pointercancel"]){document.addEventListener(type,e=>{inputAudit.events.push({type,id:e.pointerId});if(type==="gotpointercapture")inputAudit.activeCaptures.add(e.pointerId);else inputAudit.activeCaptures.delete(e.pointerId)},true)}');cdp=ctx.new_cdp_session(page)
  try:
   for mode in (['drag']if __import__('os').environ.get('FAST_ONE')else['drag','select']):
    run_case(page,cdp,touch,mode,'garden','compound')
    if not __import__('os').environ.get('FAST_ONE'):run_case(page,cdp,touch,mode,'stream','bridge')
   if not __import__('os').environ.get('SKIP_LIFECYCLE'):lifecycle(page,cdp,touch)
   assert not errors,errors
  except Exception:
   (O/'failure-rotation-events.json').write_text(json.dumps(page.evaluate('rotationAudit'),indent=2)+'\n')
   page.screenshot(path=str(O/f'failure-{"touch"if touch else"mouse"}.png'));raise
  finally:
   video=page.video;page.close();ctx.close();video.save_as(str(O/f'{"touch"if touch else"mouse"}-actual-input.webm'))
 b.close()
(O/'browser-checks.json').write_text(json.dumps({'cases':results,'scope':'actual production Chromium input with saved-state fixture setup; no physical phone claimed'},indent=2)+'\n');print(json.dumps(results,indent=2))
