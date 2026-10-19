"""Actual drag-invalid-rotate-auto-place, separate context resuming earned progress."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent/'drag';O.mkdir(exist_ok=True)
earned=json.loads((O.parent/'1280/report.json').read_text())['states'][-1]['save']
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 for touch,w,h in [(False,1280,720),(True,844,390)]:
  if (O/str(w)/'report.json').exists():continue
  d=O/str(w);d.mkdir(exist_ok=True);c=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch,storage_state={'cookies':[],'origins':[{'origin':'http://127.0.0.1:5298','localStorage':[{'name':'ruby-village:chapter-1:v1','value':json.dumps(earned)}]}]},record_video_dir=str(d/'raw'),record_video_size={'width':w,'height':h});p=c.new_page();cdp=c.new_cdp_session(p);states=[]
  def center(n):
   n.scroll_into_view_if_needed();r=n.bounding_box();return(r['x']+r['width']/2,r['y']+r['height']/2)
  def tap(n):
   x,y=center(n)
   if touch:cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y,'id':1}]});cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   else:p.mouse.click(x,y)
  def cell(q,r):return p.locator(f'#board [data-cell="{q},{r}"]>polygon.cell')
  def drag(n,q,r,cancel=False):
   x,y=center(n);tx,ty=center(cell(q,r));box=cell(q,r).bounding_box();ty+=max(42,box['height']*.8)if touch else 0
   if touch:
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y,'id':1}]})
    # Lift vertically first: horizontal tray movement intentionally scrolls the tray.
    for k in range(1,4):cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':y-60*k/3,'id':1}]})
    for k in range(1,9):cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+(tx-x)*k/8,'y':y-60+(ty-y+60)*k/8,'id':1}]})
    cdp.send('Input.dispatchTouchEvent',{'type':'touchCancel'if cancel else'touchEnd','touchPoints':[]})
   else:p.mouse.move(x,y);p.mouse.down();p.mouse.move(tx,ty,steps=8);p.mouse.up()
   p.wait_for_timeout(100)
  def state(label):
   s=p.evaluate("()=>({preview:document.querySelector('#placement-preview')?.dataset.preview,owners:[...document.querySelectorAll('#board [data-cell][data-owner]')].filter(n=>n.dataset.owner).map(n=>({cell:n.dataset.cell,id:n.dataset.owner})),save:JSON.parse(localStorage.getItem('ruby-village:chapter-1:v1'))})");s['label']=label;states.append(s);(d/'states-live.json').write_text(json.dumps(states,ensure_ascii=False,indent=2)+'\n');p.screenshot(path=str(d/f'{len(states):02}-{label}.jpg'));return s
  p.goto('http://127.0.0.1:5298/ruby-village/');tap(p.locator('#choose-level'));tap(p.locator('button[data-level="stream"]'));p.wait_for_selector('#app[data-motion="ready"]');tap(p.locator('#settings-open'));tap(p.locator('#pause-settings'));tap(p.locator('#mode'));p.keyboard.press('End');p.keyboard.press('Enter');assert p.locator('#mode').input_value()=='drag';tap(p.locator('#settings-close'))
  base=state('empty');assert not base['owners']
  for ident,q,r,inventoryTurns,rotation in [('stream-v6-a',4,1,0,'right'),('bridge',6,1,1,'right')]:
   tap(p.locator(f'#tray [data-piece="{ident}"]'))
   for _ in range(inventoryTurns):tap(p.locator('#right'))
   assert not state('inventory-'+ident)['owners'],'inventory rotation placed piece'
   drag(p.locator(f'#tray [data-piece="{ident}"]'),q,r);bad=state('invalid-released-'+ident);assert bad['preview']=='invalid'and not bad['owners'];assert bad['save']['session']['layout']=={}
   tap(p.locator('#'+rotation));good=state('rotated-autoplaced-'+ident);assert good['preview']is None;assert len(good['owners'])==3 and all(v['id']==ident for v in good['owners']);assert good['save']['session']['layout'][ident]['anchor']=={'q':q,'r':r}
   tap(cell(q,r));selected=state('reselect-whole-'+ident);assert len(selected['owners'])==3;tap(p.locator('#other'));tap(p.locator('#undo'));assert not state('undo-'+ident)['owners']
  # Cancelled native touch gesture must not commit or mutate saved layout.
  if touch:
   tap(p.locator('#tray [data-piece="bridge"]'));drag(p.locator('#tray [data-piece="bridge"]'),6,1,cancel=True);cancelled=state('native-touchcancel');assert not cancelled['owners']and cancelled['save']['session']['layout']=={};tap(p.locator('#other'))
  p.reload();tap(p.locator('#continue-game'));p.wait_for_selector('#app[data-motion="ready"]');assert not state('reload-after-undo')['owners']
  (d/'report.json').write_text(json.dumps({'source':'6108ec2','input':'native CDP touch'if touch else'mouse','viewport':[w,h],'states':states,'earnedSaveOrigin':'actual desktop full8 completion, not fabricated progress','mouseOSPointerCancel':'NOT RUN','physicalPhone':'NOT RUN','video':'actual silent UI input'},ensure_ascii=False,indent=2)+'\n');video=p.video;c.close();video.save_as(str(d/'actual-invalid-rotate-autoplace-silent.webm'))
  for f in(d/'raw').glob('*'):f.unlink()
  (d/'raw').rmdir();print('PASS DRAG',w,flush=True)
 b.close()
