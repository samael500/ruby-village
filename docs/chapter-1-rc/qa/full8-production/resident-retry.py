"""Network recovery regression, isolated context using an actually-earned save."""
import json,argparse
from pathlib import Path
from playwright.sync_api import sync_playwright
a=argparse.ArgumentParser();a.add_argument('--output',default='resident-retry');a.add_argument('--source',default='6108ec2');args=a.parse_args()
O=Path(__file__).resolve().parent/args.output;O.mkdir(exist_ok=True)
states=json.loads((O.parent/'1280/states-live.json').read_text());earned=next(s['save']for s in states if s['scene']=='garden'and s['label']=='reload-empty')
(O/'actually-earned-save.json').write_text(json.dumps(earned,ensure_ascii=False,indent=2)+'\n');requests=[];restored=False
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,args=['--no-sandbox']);c=b.new_context(viewport={'width':1280,'height':720},storage_state={'cookies':[],'origins':[{'origin':'http://127.0.0.1:5298','localStorage':[{'name':'ruby-village:chapter-1:v1','value':json.dumps(earned)}]}]});p=c.new_page()
 def handle(r):
  if r.request.url.endswith('.json'):r.continue_();return
  requests.append({'url':r.request.url,'networkRestored':restored})
  if restored:r.continue_()
  else:r.abort()
 p.route('**/assets/characters-facing-v1/**',handle);p.goto('http://127.0.0.1:5298/ruby-village/');p.locator('#continue-game').click();p.wait_for_selector('#app[data-motion="ready"]');p.wait_for_load_state('networkidle');first=p.locator('#board [data-resident="rabbit"]').get_attribute('data-view');p.screenshot(path=str(O/'first-failed-facing.jpg'))
 restored=True;p.locator('#settings-open').click();p.locator('#pause-settings').click();p.locator('#map-return').click();p.locator('button[data-level="garden"]').click();p.wait_for_selector('#app[data-motion="ready"]');p.wait_for_load_state('networkidle');
 if args.source!='6108ec2':p.wait_for_selector('#board [data-resident="rabbit"][data-view="conversation-left"]',timeout=15000)
 after=p.locator('#board [data-resident="rabbit"]').get_attribute('data-view');p.screenshot(path=str(O/'reentry-network-restored.jpg'))
 # Separate fresh image proves endpoint recovery, without touching application cache.
 href=p.evaluate("async()=>{const r=await fetch('/ruby-village/assets/characters-facing-v1/residents-facing-manifest.json');return (await r.json()).characters.rabbit.frames['conversation-left'].image}")
 control=p.evaluate("async f=>{let i=new Image();i.src='/ruby-village/assets/characters-facing-v1/'+f+'?control=1';await i.decode();return[i.naturalWidth,i.naturalHeight]}",href)
 (O/'report.json').write_text(json.dumps({'source':args.source,'input':'real mouse UI','firstView':first,'afterNetworkRestoredAndReentry':after,'expectedActivityView':'conversation-left','controlDimensions':control,'requests':requests,'saveOrigin':'actual clean sequence garden reload-empty state, not fabricated completion'},indent=2)+'\n');b.close();print(first,after,control,requests)
