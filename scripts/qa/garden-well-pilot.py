"""Actual UI solves on an explicitly isolated, progress-only seeded art build.
Production layout gating is not changed by this harness. Mouse input; viewport
emulation is not a physical phone. Wait for natural walking, not reduced motion.
"""
from pathlib import Path
import json,os,time
from playwright.sync_api import sync_playwright
r=Path(__file__).resolve().parents[2]
url=os.environ.get('RUBY_ART_REVIEW_URL','http://127.0.0.1:5307/ruby-village/')
sid=os.environ.get('RUBY_ART_REVIEW_SCENE','garden')
o=r/'docs/chapter-1-rc/evidence'/os.environ.get('RUBY_ART_REVIEW_EVIDENCE','garden-painted-2bfe795');o.mkdir(parents=True,exist_ok=True)
solution=json.loads((r/'src/art-solutions.json').read_text())[sid];report=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for w,h in [(1280,720),(844,390)]:
  q=b.new_page(viewport={'width':w,'height':h});errors=[];q.on('pageerror',lambda e:errors.append(str(e)))
  q.goto(url);q.locator('#continue-game').click();q.wait_for_load_state('networkidle')
  q.screenshot(path=str(o/f'dialog-{w}.jpg'))
  while q.locator('#story[open]').count():q.locator('#story-action').click()
  for ident,a in solution.items():
   q.locator(f'[data-piece="{ident}"]').click()
   for _ in range(a['turns']):q.locator('#right').click()
   q.locator(f'[data-cell="{a["anchor"]["q"]},{a["anchor"]["r"]}"] > polygon.cell').click();q.locator('#place').click()
  q.screenshot(path=str(o/f'solved-{w}.jpg'));start=time.monotonic();q.locator('#check').click()
  q.wait_for_function("document.querySelector('#story[open], #completion-panel[open]') !== null",timeout=90000)
  elapsed=time.monotonic()-start;q.screenshot(path=str(o/f'arrival-{w}.jpg'))
  pages=0
  while q.locator('#story[open]').count():
   q.screenshot(path=str(o/f'after-dialog-{pages}-{w}.jpg'));q.locator('#story-action').click();pages+=1
  q.locator('#completion-panel[open]').wait_for();q.screenshot(path=str(o/f'result-{w}.jpg'))
  saved=json.loads(q.evaluate("localStorage.getItem('ruby-village:chapter-1:v1')"));assert sid in saved['completed'];assert not errors
  report.append({'viewport':[w,h],'input':'mouse','physicalPhone':False,'naturalWalkSeconds':elapsed,'afterDialogPages':pages,'pageErrors':errors,'completedInSavedProgress':True,'scope':'isolated source art candidate, legacy gait still active, not final acceptance'})
  q.close()
 b.close()
(o/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
