"""Review every new scene against unchanged solutions, using the actual projected polygons."""
import json,subprocess,sys
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5173/ruby-village/?art-v6=1'
ROOT=Path(__file__).resolve().parents[1]
LEVELS=json.loads(subprocess.check_output(['node','--experimental-strip-types','--input-type=module','-e',"import {levels} from './src/levels.ts';console.log(JSON.stringify(levels))"],cwd=ROOT,text=True))
SHOTS=ROOT/'docs/screenshots/art-v6';SHOTS.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch();errors=[]
 for w,h in [(1280,720),(844,390),(1920,1080),(1024,768)]:
  for l in LEVELS:
   page=b.new_page(viewport={'width':w,'height':h},has_touch=True,reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)));page.goto(URL)
   page.evaluate('(ids)=>localStorage.setItem("ruby-village:chapter-1:v1",JSON.stringify({version:2,completed:ids,introSeen:ids}))',[i['id'] for i in LEVELS]);page.reload();page.locator('#choose-level').click();page.locator('[data-level="'+l['id']+'"]').click()
   for id,v in l['solution'].items():
    page.locator('[data-piece="'+id+'"]').tap()
    for _ in range(v['turns']):page.locator('#right').tap()
    poly=page.locator('[data-cell="%s,%s"] > polygon'%(v['anchor']['q'],v['anchor']['r']))
    xy=poly.evaluate('el=>{const p=el.points;const x=[...p].reduce((s,p)=>s+p.x,0)/6,y=[...p].reduce((s,p)=>s+p.y,0)/6;const q=new DOMPoint(x,y).matrixTransform(el.getScreenCTM());return [q.x,q.y]}')
    page.touchscreen.tap(*xy);expect(page.locator('#place')).to_be_enabled();page.locator('#place').tap()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth && document.documentElement.scrollHeight<=innerHeight')
   assert page.locator('#chapter-background').evaluate('el=>el.getBoundingClientRect().width/el.getBoundingClientRect().height')>1.7
   if w in [1280,844]:page.screenshot(path=str(SHOTS/f'{l["id"]}-{w}x{h}.png'))
   page.locator('#check').tap();expect(page.locator('#story')).to_be_visible();page.close()
  print(f'{w}x{h}: eight reference solutions, projected touch placement, victory, fit: PASS',flush=True)
 assert not errors,errors
 b.close()
