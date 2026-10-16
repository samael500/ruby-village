import json,time,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/qa/runtime-extra';OUT.mkdir(parents=True,exist_ok=True)
URL='http://127.0.0.1:5183/ruby-village/';KEY='ruby-village:chapter-1:v1';IDS=['gate','garden','well','bakery','stream','mill','post','forest'];results=[]
def dismiss(q):
 for _ in range(40):
  if q.locator('#story[open]').count():q.locator('#story-action').click()
  else:return
 raise AssertionError('dialog loop')
def record(name,fn):
 try:detail=fn();results.append({'check':name,'status':'pass','detail':detail})
 except Exception as e:results.append({'check':name,'status':'fail','error':str(e)})
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':1280,'height':720},reduced_motion='reduce');q=c.new_page();errors=[];q.on('pageerror',lambda e:errors.append(str(e)));q.goto(URL);q.locator('#continue-game').click();q.locator('#prologue-next').click();second=q.locator('#prologue-text').inner_text();q.locator('#prologue-back').click();assert second!=q.locator('#prologue-text').inner_text();q.locator('#prologue-skip').click();dismiss(q)
 sol=json.loads((ROOT/'docs/chapter-1-rc/production-solutions.json').read_text())[0]['solution'];ident,pl=next(iter(sol.items()))
 def placement(ident,pl,keyboard=False):
  tile=q.locator(f'#tray [data-piece="{ident}"]');tile.focus();tile.press('Enter') if keyboard else tile.click()
  for _ in range(pl['turns']):q.locator('#right').press('Enter') if keyboard else q.locator('#right').click()
  cell=q.locator(f'[data-cell="{pl["anchor"]["q"]},{pl["anchor"]["r"]}"]');cell.focus();cell.press('Enter') if keyboard else cell.locator('polygon').first.click(force=True)
  q.locator('#place').press('Enter') if keyboard else q.locator('#place').click();assert q.locator(f'[data-owner="{ident}"]').count()
 record('keyboard tray rotate cell place Enter',lambda:placement(ident,pl,True))
 def restart():
  q.locator('#settings-open').click();q.locator('#pause-restart').click();q.locator('#restart-cancel').click();assert q.locator(f'[data-owner="{ident}"]').count();q.locator('#settings-open').click();q.locator('#pause-restart').click();q.locator('#restart-confirm').click();assert not q.locator('[data-owner]:not([data-owner=""])').count();q.reload();q.locator('#continue-game').click();dismiss(q);assert not q.locator('[data-owner]:not([data-owner=""])').count()
 record('restart cancel confirm reload',restart)
 def complete(replay=False):
  for i,pl in sol.items():placement(i,pl)
  then=time.monotonic();q.locator('#check').click();q.wait_for_function("document.querySelector('#story[open]') || document.querySelector('#completion-panel[open]')");elapsed=time.monotonic()-then;dismiss(q);q.locator('#completion-panel[open]').wait_for();assert q.locator('#check').is_disabled();q.locator('#completion-map').click();assert q.locator('[data-level="gate"]').inner_text().find('Пройден')>=0
  if not replay:assert elapsed<2,elapsed
  return {'secondsToResultDialog':round(elapsed,3),'replay':replay}
 record('reduced motion complete once',complete)
 def replay():q.locator('[data-level="gate"]').click();dismiss(q);return complete(True)
 record('replay completion once',replay)
 q.screenshot(path=str(OUT/'after-replay.jpg'),type='jpeg')
 def reset():
  q.locator('#map-more').click();q.locator('#reset-open').click();q.locator('#reset-cancel').click();assert not q.locator('[data-level="garden"]').is_disabled();q.locator('#map-more').click();q.locator('#reset-open').click();q.locator('#reset-confirm').click();assert q.locator('[data-level="garden"]').is_disabled();assert json.loads(q.evaluate(f"localStorage.getItem('{KEY}')"))['completed']==[]
 record('chapter reset cancel confirm',reset)
 c.close()
 def final_letter():
  ctx=b.new_context();ctx.add_init_script("localStorage.setItem('"+KEY+"',JSON.stringify({version:2,completed:"+json.dumps(IDS)+",introSeen:"+json.dumps(IDS)+"}))");z=ctx.new_page();z.goto(URL);z.locator('#choose-level').click();z.locator('#map-more').click();z.locator('#letter-open').click();assert z.locator('#story[open]').count();dismiss(z);z.locator('#map-more').click();z.locator('#chapter-ending').click();dismiss(z);assert z.locator('[data-level]').count()==8;assert z.locator('[data-level="forest"]').is_enabled();z.screenshot(path=str(OUT/'ending-map.jpg'),type='jpeg');ctx.close()
 record('old letter and ending no chapter2',final_letter)
 for label,state in [('future-layout',{'version':2,'layoutVersion':999,'completed':['gate'],'session':{'levelId':'garden','layout':{}}}),('invalid-placement',{'version':2,'layoutVersion':1,'completed':['gate'],'session':{'levelId':'garden','layout':{'bad':{'turns':0,'anchor':{'q':999,'r':999}}}}})]:
  def recovery(state=state):
   ctx=b.new_context();ctx.add_init_script("localStorage.setItem('"+KEY+"',"+json.dumps(json.dumps(state))+")");z=ctx.new_page();z.goto(URL);z.locator('#choose-level').click();assert not z.locator('[data-level="garden"]').is_disabled();assert z.locator('[data-level="gate"]').inner_text().find('Пройден')>=0;ctx.close()
  record(label+' preserves completed',recovery)
 b.close()
report={'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'results':results,'pageErrors':errors};(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
