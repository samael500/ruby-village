"""Separate legacy-storage fixture; never used by clean chapter sequence."""
import json,os,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent/'migration';O.mkdir(exist_ok=True)
URL=os.environ.get('RUBY_QA_URL','http://127.0.0.1:5298/ruby-village/');origin=URL.split('/ruby-village/')[0]
assert 'PRODUCTION_LAYOUT_VERSION=2' in (R/'src/production-chapter.ts').read_text()
legacy=json.loads((R/'tests/fixtures/chapter-1-before-layouts.json').read_text());old=next(x for x in legacy['levels']if x['id']=='stream')['solution'];completed=['gate','garden','well','bakery']
fixture={'version':2,'layoutVersion':1,'completed':completed,'introSeen':completed+['stream'],'letter':{'qaRetained':True},'preferences':{'mode':'select','reducedMotion':False},'session':{'levelId':'stream','cols':11,'rows':7,'layout':{**old,'stream-b':{'anchor':{'q':6,'r':2},'turns':0}},'mode':'select','reducedMotion':False}}
(O/'fixture.json').write_text(json.dumps(fixture,indent=2)+'\n');records=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 for touch,w,h in [(False,1280,720),(True,844,390)]:
  c=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch,storage_state={'cookies':[],'origins':[{'origin':origin,'localStorage':[{'name':'ruby-village:chapter-1:v1','value':json.dumps(fixture)}]}]});p=c.new_page();cdp=c.new_cdp_session(p)
  def tap(loc):
   loc.scroll_into_view_if_needed();r=loc.bounding_box();x,y=r['x']+r['width']/2,r['y']+r['height']/2
   if touch:cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y,'id':1}]});cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   else:p.mouse.click(x,y)
  p.goto(URL);notice=p.locator('#menu-save-status').inner_text();assert notice; p.screenshot(path=str(O/f'{w}-migration-notice.jpg'));tap(p.locator('#continue-game'));p.wait_for_selector('#app[data-motion="ready"]');p.wait_for_load_state('networkidle')
  save=p.evaluate("JSON.parse(localStorage.getItem('ruby-village:chapter-1:v1'))");assert save['layoutVersion']==2;assert save['completed']==completed;assert save['session']['layout']==old;assert save['letter']==fixture['letter'];assert p.locator('#board [data-owner="stream-b"]').count()==0
  p.screenshot(path=str(O/f'{w}-migrated-scene.jpg'));p.reload();tap(p.locator('#continue-game'));p.wait_for_selector('#app[data-motion="ready"]');again=p.evaluate("JSON.parse(localStorage.getItem('ruby-village:chapter-1:v1'))");assert again['session']==save['session'];assert again['completed']==completed
  records.append({'viewport':[w,h],'notice':notice,'firstSave':save,'reloadSave':again,'input':'native CDP touch'if touch else'mouse'});c.close()
 b.close()
(O/'report.json').write_text(json.dumps({'source':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'records':records,'scope':'separate legacy session fixture, no wins/layout injected into clean sequential run'},ensure_ascii=False,indent=2)+'\n')
