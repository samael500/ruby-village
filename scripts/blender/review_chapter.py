"""Browser verification and captures of all eight technical layouts; no game integration."""
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageChops,ImageFilter,ImageDraw
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/blender-chapter-1/layouts'
BASE='http://127.0.0.1:8040/docs/blender-chapter-1/layouts'
IDS=['gate','garden','well','bakery','stream','mill','post','forest']
SIZES=[(1280,720),(844,390),(740,360),(915,412),(1024,768),(1920,1080)]
(OUT/'viewports').mkdir(exist_ok=True)
report=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1672,'height':941},device_scale_factor=1)
    for id in IDS:
        page.goto(f'{BASE}/plans/{id}.svg');page.screenshot(path=str(OUT/'plans'/f'{id}.png'))
    page.close()
    for w,h in SIZES:
        page=browser.new_page(viewport={'width':w,'height':h})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(f'{BASE}/index.html');page.wait_for_function('window.layoutReview?.data.length===8')
        for id in IDS:
            page.select_option('#scene',id)
            for mode in ['clean','check','solved','plan']:
                page.locator(f'[data-mode="{mode}"]').click();page.locator('#image').evaluate('(i)=>i.decode()')
                box=page.locator('#image').bounding_box();d=json.loads((OUT/'engine'/f'{id}.json').read_text())
                fit=min(box['width']/1672,box['height']/941);left=box['x']+(box['width']-1672*fit)/2;top=box['y']+(box['height']-941*fit)/2
                targets=[v for c in d['cells'] for v in c['polygon']]+[d['start']['pixel'],d['goal']['pixel']]
                for point in targets:
                    x,y=left+point['x']*fit,top+point['y']*fit
                    assert box['x']-.1<=x<=box['x']+box['width']+.1 and box['y']-.1<=y<=box['y']+box['height']+.1,(id,w,h,point)
                    assert 0<=x<=w and 0<=y<=h,(id,w,h,'Offscreen')
                assert page.locator('#source').get_attribute('href').endswith(id+'.blend')
                if mode=='check':page.screenshot(path=str(OUT/'viewports'/f'{id}-{w}x{h}.png'))
            report.append({'scene':id,'viewport':[w,h],'modes':4,'allCellCornersInsideStage':True,'productionUI':False})
        assert not errors,errors
        if w==1920:
            page.locator('[data-mode="contact"]').click()
            page.locator('#contact').evaluate('(e)=>Promise.all([...e.querySelectorAll("img")].map(i=>i.decode()))')
            page.locator('#contact').screenshot(path=str(OUT/'contact-sheet.png'))
        page.close()
    browser.close()
for id in IDS:
    for name in ['background','solution']+(['bridge'] if id in ['stream','mill'] else [])+(['gate_closed','gate_open'] if id=='gate' else []):
        with Image.open(OUT/'renders'/f'{id}-{name}.png') as im:
            assert im.size==(1672,941) and im.mode=='RGBA'
            assert im.getchannel('A').getbbox()
            if name!='background':assert im.getchannel('A').getextrema()[0]==0
    # Alpha of the separately exported bridge must match the union of its three hexes.
    if id in ['stream','mill']:
        d=json.loads((OUT/'engine'/f'{id}.json').read_text());bridge=next(p for p in d['pieces'] if p['kind']=='bridge')
        expected=Image.new('L',(1672,941));draw=ImageDraw.Draw(expected)
        for c in d['cells']:
            if c['id'] in bridge['cells']:draw.polygon([(v['x'],v['y']) for v in c['polygon']],fill=255)
        with Image.open(OUT/'renders'/f'{id}-bridge.png') as im:actual=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
        assert ImageChops.subtract(actual,expected.filter(ImageFilter.MaxFilter(3))).getbbox() is None,(id,'Bridge spill')
        assert ImageChops.subtract(expected.filter(ImageFilter.MinFilter(3)),actual).getbbox() is None,(id,'Bridge holes')
(OUT/'viewport-report.json').write_text(json.dumps({'checks':report,'bridgeAlphaTolerancePx':1,'screenshots':'Chromium, isolated technical stand; no production HUD or touch claim'},indent=2)+'\n')
# Explicit gallery prevents mixing this handoff with hundreds of historical screenshots.
assets=[]
def review_asset(ident,label,path):
    with Image.open(path) as im:width,height=im.size
    assets.append({'assetId':ident,'label':label,'kind':'image','files':[{'path':str(path.relative_to(ROOT)),'width':width,'height':height,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}],'frames':[],
                   'notes':'Техническая геометрия для будущей перерисовки в 2D. Не финальный арт.'})
review_asset('chapter-overview','Все восемь уровней · решения',OUT/'contact-sheet.png')
for i,id in enumerate(IDS):
    d=json.loads((OUT/'engine'/f'{id}.json').read_text())
    for mode,label in [('check','Поле'),('plan','Схема 2D'),('solved','Решение'),('clean','Макет')]:
        path=OUT/'plans'/f'{id}.png' if mode=='plan' else OUT/'renders'/f'{id}-{mode}.png'
        review_asset(id+'-'+mode,f'{i+1}. {d["name"]} · {label}',path)
(OUT/'asset-review.manifest.json').write_text(json.dumps({'schemaVersion':1,'assets':assets,'animations':[]},indent=2,ensure_ascii=False)+'\n')
print('PASS: 8 scenes × 6 sizes × 4 modes; source links, alpha, full cell corners, 2 exact bridge silhouettes')
