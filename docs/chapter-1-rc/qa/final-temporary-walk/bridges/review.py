"""Actual UI bridge proof; only debug presentation of existing water polygons."""
import json,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
O=Path(__file__).resolve().parent;R=Path(__file__).resolve().parents[5]
prior=json.loads((O.parent/'landscape/report.json').read_text());earned=prior['states'][-1]['save'];solutions=json.loads((R/'src/art-solutions.json').read_text())
assert earned['completed']==['gate','garden','well','bakery','stream','mill','post','forest']
report={'production':'8bb08fbcb747ccc43cf8e24c8b627acb8d65b099','earnedProfileSource':'../landscape/report.json final state','earnedProfileSha256':hashlib.sha256(json.dumps(earned,sort_keys=True).encode()).hexdigest(),'physicalPhone':'NOT RUN','cases':[]}
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 for touch,w,h in [(False,1440,900),(True,844,390)]:
  c=browser.new_context(viewport={'width':w,'height':h},is_mobile=touch,has_touch=touch,reduced_motion='no-preference');p=c.new_page();cdp=c.new_cdp_session(p);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto('http://127.0.0.1:5390/ruby-village/');p.evaluate('(save)=>localStorage.setItem("ruby-village:chapter-1:v1",JSON.stringify(save))',earned);p.reload()
  def tap(loc):
   loc.scroll_into_view_if_needed();b=loc.bounding_box();x=b['x']+b['width']/2;y=b['y']+b['height']/2
   if touch:
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y,'id':1}]});cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   else:p.mouse.click(x,y)
  for sid in ['stream','mill']:
   if sid=='stream':tap(p.locator('#choose-level'))
   else:tap(p.locator('#scene-back'))
   tap(p.locator('[data-level="'+sid+'"]'));p.wait_for_selector('#app[data-motion="ready"]');p.wait_for_load_state('networkidle')
   while p.locator('#story[open]').count():tap(p.locator('#story-action'))
   for ident,a in solutions[sid].items():
    tap(p.locator('#tray [data-piece="'+ident+'"]'))
    for _ in range(a['turns']):tap(p.locator('#right'))
    q,r=a['anchor']['q'],a['anchor']['r'];tap(p.locator(f'#board [data-cell="{q},{r}"]>polygon.cell'));tap(p.locator('#place'));assert p.locator('[data-owner="'+ident+'"]').count()>0
   p.screenshot(path=str(O/f'{sid}-{w}-clean.png'))
   state=p.evaluate('''()=>{let nodes=[...document.querySelectorAll('#board [data-terrain="water"]>polygon.cell')];let before=localStorage.getItem('ruby-village:chapter-1:v1');let mask=nodes.map(n=>({cell:n.parentElement.dataset.cell,points:n.getAttribute('points'),matrix:[n.getScreenCTM().a,n.getScreenCTM().b,n.getScreenCTM().c,n.getScreenCTM().d,n.getScreenCTM().e,n.getScreenCTM().f]}));for(let n of nodes){let copy=n.cloneNode(false);copy.removeAttribute('class');copy.setAttribute('fill','#00ddff');copy.setAttribute('fill-opacity','.42');copy.setAttribute('stroke','#ff0066');copy.setAttribute('stroke-width','2');copy.setAttribute('opacity','1');copy.setAttribute('pointer-events','none');copy.dataset.qaWaterOverlay='';n.parentElement.parentElement.append(copy)}return {mask,saveUnchanged:before===localStorage.getItem('ruby-village:chapter-1:v1'),owners:[...document.querySelectorAll('#board [data-owner]')].filter(n=>n.dataset.owner).map(n=>({cell:n.dataset.cell,owner:n.dataset.owner,terrain:n.dataset.terrain})),images:[...document.querySelectorAll('#board image')].map(n=>n.getAttribute('href'))}}''')
   assert state['mask'] and state['saveUnchanged'];p.screenshot(path=str(O/f'{sid}-{w}-water-overlay.png'));p.evaluate("document.querySelectorAll('[data-qa-water-overlay]').forEach(n=>n.remove())")
   report['cases'].append({'scene':sid,'viewport':[w,h],'input':'native CDP touch' if touch else 'mouse',**state,'errors':errors.copy()});assert not errors
  c.close()
 browser.close()
(O/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
