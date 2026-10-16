"""Capture the isolated review stand; intentionally not a production integration test."""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/blender-chapter-1/candidates'
url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8040/docs/blender-chapter-1/review.html'
report=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    for w,h in [(1280,720),(844,390),(740,360),(915,412),(1024,768),(1920,1080)]:
        page=browser.new_page(viewport={'width':w,'height':h})
        page.goto(url)
        for mode in ['clean','check']:
            page.locator(f'[data-mode="{mode}"]').click()
            page.locator('#image').evaluate('(i)=>i.decode()')
            page.locator('#surroundings').evaluate('(i)=>i.decode()')
            page.screenshot(path=str(OUT/f'stand-{mode}-{w}x{h}.png'))
        # Full corners of all usable hexes must fit inside the reserved stage.
        points=page.evaluate('''() => {const s=document.querySelector('#stage').getBoundingClientRect(),f=document.querySelector('#frame').getBoundingClientRect();return {stage:{x:s.x,y:s.y,w:s.width,h:s.height},frame:{x:f.x,y:f.y,w:f.width,h:f.height}}}''')
        logical=json.loads((ROOT/'src/chapter-1.logical.json').read_text())['gate']
        import math
        for row in range(7):
            for col in range(11):
                q=col-row//2
                if f'{q},{row}' in logical['terrain']:continue
                x=140+math.sqrt(3)*70*(q+row/2); y=290+.65*105*row
                for i in range(6):
                    a=math.radians(30+i*60)
                    px=points['frame']['x']+(x+70*math.cos(a))*points['frame']['w']/1672
                    py=points['frame']['y']+(y+.65*70*math.sin(a))*points['frame']['h']/941
                    s=points['stage']
                    assert s['x']<=px<=s['x']+s['w'] and s['y']<=py<=s['y']+s['h'],(w,h,q,row)
        report.append({'viewport':[w,h],'fullHexCornersInsideReservedStage':True,'productionUI':False})
        if w==1920:
            page.locator('[data-mode="contact"]').click()
            page.locator('#contact').evaluate('(e)=>Promise.all([...e.querySelectorAll("img")].map(i=>i.decode()))')
            page.locator('#contact').screenshot(path=str(OUT/'contact-sheet.png'))
        if w==1920:
            page.goto(url.rsplit('/',1)[0]+'/details.html')
            page.locator('body').evaluate('(e)=>Promise.all([...e.querySelectorAll("img")].map(i=>i.decode()))')
            for shade in ['light','dark']:
                page.locator('body').evaluate('(e,v)=>e.className=v',shade)
                page.screenshot(path=str(OUT/f'details-{shade}.png'),full_page=True)
        page.close()
    browser.close()
(OUT.parent/'viewport-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: six stand sizes, all full usable hex footprints inside reserved stage; no production UI claim')
