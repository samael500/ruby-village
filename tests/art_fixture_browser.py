"""The art fixture is dev-only and cannot write the real player's save."""
import json,subprocess,sys
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
KEY='ruby-village:chapter-1:v1'
solution=json.loads(subprocess.check_output(['node','--experimental-strip-types','--input-type=module','-e',"import {levels} from './src/levels.ts';console.log(JSON.stringify(levels[0].solution));"],cwd=ROOT,text=True))
with sync_playwright() as p:
    b=p.chromium.launch();page=b.new_page(viewport={'width':1280,'height':720})
    dev=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5173/ruby-village/'
    prod=sys.argv[2] if len(sys.argv)>2 else 'http://127.0.0.1:4173/ruby-village/'
    page.goto(dev);saved=json.dumps({'version':1,'completed':['gate','garden']})
    page.evaluate('([k,v])=>localStorage.setItem(k,v)',[KEY,saved])
    page.goto(dev+'?art-check')
    expect(page.locator('#story')).not_to_be_visible()
    assert page.locator('[data-owner]:not([data-owner=""])').count()==3
    for id,placement in solution.items():
        if id in list(solution)[:3]:continue
        page.locator(f'[data-piece="{id}"]').click()
        q,r=placement['anchor']['q'],placement['anchor']['r']
        box=page.locator(f'[data-cell="{q},{r}"] > polygon').bounding_box()
        page.mouse.click(box['x']+box['width']/2,box['y']+box['height']/2);page.locator('#place').click()
    page.locator('#check').click();expect(page.locator('#story-title')).to_have_text('До калитки')
    assert page.evaluate('(k)=>localStorage.getItem(k)',KEY)==saved
    page.locator('#story-skip').click();page.locator('#reset-open').click();page.locator('#reset-confirm').click()
    assert page.evaluate('(k)=>localStorage.getItem(k)',KEY)==saved
    page.goto(prod+'?art-check');expect(page.locator('#chapter-map')).to_be_visible()
    assert page.locator('[data-owner]:not([data-owner=""])').count()==0
    b.close();print('Dev-only fixture, victory/reset storage isolation, production ignores art-check: PASS')
