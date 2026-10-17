import json
from pathlib import Path
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
base=Image.open(ROOT/'public/assets/chapter-map-v2/map-base.webp').convert('RGB')
wide=Image.open(ROOT/'public/assets/chapter-map-v2/map-wide.webp').convert('RGB')
assert base.size==(1000,400) and wide.size==(1400,800)
assert not ImageChops.difference(base,wide.crop((200,200,1200,600))).getbbox()
checks=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for viewport in [(1280,720),(844,390)]:
  ctx=b.new_context(viewport=dict(zip(['width','height'],viewport)),record_video_dir=str(OUT/'navigation-video'))
  q=ctx.new_page();q.goto('http://127.0.0.1:5297/ruby-village/');q.locator('#choose-level').click()
  q.locator('[data-level="gate"]').click();q.locator('#prologue-skip').wait_for(state='visible')
  if q.locator('#prologue-skip').is_visible():q.locator('#prologue-skip').click()
  while q.locator('#story[open]').count():q.locator('#story-action').click()
  q.locator('#field').wait_for(state='visible')
  q.screenshot(path=str(OUT/f'scene-{viewport[0]}.jpg'))
  q.locator('#settings-open').click();q.locator('#pause-map').click()
  assert q.locator('#chapter-map').is_visible()
  q.reload();q.locator('#choose-level').click();assert q.locator('[data-level="gate"]').is_enabled()
  checks.append({'viewport':viewport,'realMapEnterBackReload':True})
  video=q.video;ctx.close();video.save_as(str(OUT/f'navigation-{viewport[0]}-silent.webm'))
 b.close()
(OUT/'navigation.json').write_text(json.dumps({'exactCorePixels':True,'cases':checks},indent=2))
print('PASS exact core and two real navigation/reload cases')
