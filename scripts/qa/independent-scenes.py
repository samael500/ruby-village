"""Visual matrix from unlocked profile; does not claim puzzle completion via input."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/qa/scenes';OUT.mkdir(parents=True,exist_ok=True)
IDS=['gate','garden','well','bakery','stream','mill','post','forest'];SIZES=[(1280,720),(844,390),(740,360),(915,412),(1024,768),(1920,1080)]
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context();c.add_init_script("localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({version:2,completed:"+str(IDS).replace("'",'"')+",introSeen:"+str(IDS).replace("'",'"')+"}))");q=c.new_page();q.goto('http://127.0.0.1:5183/ruby-village/');q.locator('#choose-level').click()
 for w,h in SIZES:
  q.set_viewport_size({'width':w,'height':h});sheet=Image.new('RGB',(960,4*290),'#eee');draw=ImageDraw.Draw(sheet)
  for i,ident in enumerate(IDS):
   q.locator(f'[data-level="{ident}"]').click()
   while q.locator('#story[open]').count():q.locator('#story-action').click()
   q.wait_for_function("Array.from(document.images).filter(i=>i.offsetWidth).every(i=>i.complete)");q.wait_for_timeout(80)
   file=OUT/f'{ident}-{w}x{h}.jpg';q.screenshot(path=str(file),type='jpeg',quality=75)
   im=Image.open(file);im.thumbnail((480,265));x=(i%2)*480;y=(i//2)*290;sheet.paste(im,(x,y+20));draw.text((x+4,y+3),f'{ident} {w}x{h}',fill='black');q.locator('#scene-back').click()
  sheet.save(OUT/f'matrix-{w}x{h}.jpg',quality=85)
 b.close()
