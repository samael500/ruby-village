"""Real input smoke/playthrough; browser emulation is not a physical phone test."""
import json, os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/chapter-1-rc/evidence'; OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('RUBY_QA_URL','http://127.0.0.1:5178/ruby-village/')

def dismiss(page):
 for _ in range(60):
  if page.locator('#story[open]').count(): page.locator('#story-action').click()
  elif page.locator('#completion-panel[open]').count():return
  else:return
 raise AssertionError('Dialog never ended')

with sync_playwright() as p:
 browser=p.chromium.launch()
 context=browser.new_context(viewport={'width':1280,'height':720},record_video_dir=str(OUT/'video'),record_video_size={'width':1280,'height':720})
 page=context.new_page(); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL);page.locator('#continue-game').click()
 frames=[]
 for i in range(6):
  page.locator('#prologue-panel[open]').wait_for()
  page.screenshot(path=str(OUT/f'prologue-{i+1}.png'))
  frames.append(page.locator('#prologue-text').inner_text())
  page.locator('#prologue-next').click()
 dismiss(page)
 levels=page.evaluate("async()=> (await import('./src/production-chapter.ts')).productionLevels")
 for index,level in enumerate(levels):
  dismiss(page)
  for ident,placement in level['solution'].items():
   page.locator(f'#tray [data-piece="{ident}"]').click()
   for _ in range(placement['turns']):page.locator('#right').click()
   q,r=placement['anchor']['q'],placement['anchor']['r']
   page.locator(f'[data-cell="{q},{r}"] polygon').first.click(force=True)
   page.locator('#place').click()
   assert page.locator(f'[data-owner="{ident}"]').count()>0,(level['id'],ident)
  page.screenshot(path=str(OUT/f"{level['id']}-solved.png"))
  page.locator('#check').click()
  page.wait_for_function("document.querySelector('#story[open]') || document.querySelector('#completion-panel[open]')",timeout=10000)
  dismiss(page)
  page.locator('#completion-panel[open]').wait_for()
  page.screenshot(path=str(OUT/f"{level['id']}-complete.png"))
  if index<7:page.locator('#next-level').click()
  else:page.locator('#completion-map').click()
 assert not errors,errors
 report={'url':URL,'input':'mouse clicks on tray, rotate, cells, placement and check; no layout injection','levels':len(levels),'prologueFrames':frames,'pageErrors':errors,'physicalPhone':'not-run','familyPlaytest':'not-run'}
 (OUT/'browser-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 context.close();browser.close()
 print(json.dumps(report,ensure_ascii=False))
