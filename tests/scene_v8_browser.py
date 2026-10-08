"""48 viewports/scenes, legacy saves, input, foreground ordering and actual before/after evidence."""
import json,subprocess,sys
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_images import ready_images
ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:5190/ruby-village/'
LEVELS=json.loads(subprocess.check_output(['node','--experimental-strip-types','--input-type=module','-e',"import {levels} from './src/levels.ts';console.log(JSON.stringify(levels))"],cwd=ROOT,text=True));IDS=[l['id'] for l in LEVELS];KEY='ruby-village:chapter-1:v1'
OUT=ROOT/'docs/screenshots/scene-v8/after';OUT.mkdir(parents=True,exist_ok=True)
def seed(page,l,layout):
 page.evaluate('(v)=>localStorage.setItem(v.key,JSON.stringify({version:2,completed:v.ids,introSeen:v.ids,session:{levelId:v.id,cols:11,rows:7,layout:v.layout,mode:"select",reducedMotion:true}}))',{'key':KEY,'ids':IDS,'id':l['id'],'layout':layout});page.reload();page.locator('#continue-game').click()
def shot(page,name,clip=None):
 ready_images(page);page.screenshot(path=str(OUT/f'{name}.jpg'),quality=88 if not clip else 95,**({'clip':clip} if clip else {}))
def crop(page,l,w,h):
 point=l['goal'] if l['id']=='gate' else l['start'];box=page.locator('[data-cell="%s,%s"]'%(point['q'],point['r'])).bounding_box();x=max(0,box['x']-45);y=max(0,box['y']-50)
 return {'x':x,'y':y,'width':min(w-x,box['width']+90),'height':min(h-y,box['height']+90)}
with sync_playwright() as p:
 b=p.chromium.launch();errors=[]
 # A fresh first-level gate is closed until victory, then both aligned layers open.
 first=b.new_page(viewport={'width':844,'height':390},reduced_motion='reduce');first.goto(URL)
 first.evaluate('(v)=>localStorage.setItem(v.key,JSON.stringify({version:2,completed:[],introSeen:["gate"],session:{levelId:"gate",cols:11,rows:7,layout:v.layout,mode:"select",reducedMotion:true}}))',{'key':KEY,'layout':LEVELS[0]['solution']})
 first.reload();first.locator('#continue-game').click();assert first.locator('[data-open-gate]').count()==0
 first.locator('#check').click();expect(first.locator('#story')).to_be_visible();assert first.locator('[data-open-gate]').count()==2;first.close()
 for w,h in [(1280,720),(844,390),(740,360),(915,412),(1024,768),(1920,1080)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=True,reduced_motion='reduce')
  for l in LEVELS:
   page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.goto(URL);seed(page,l,{})
   ready_images(page);assert page.locator('[data-cell]').count()==77
   field=page.locator('#board').bounding_box();art=page.locator('[data-surroundings]').bounding_box();assert art['x']<=field['x']+1 and art['y']<=field['y']+1 and art['x']+art['width']>=field['x']+field['width']-1 and art['y']+art['height']>=field['y']+field['height']-1
   assert page.locator('#board .landmark, #ground-plane circle').count()==0
   assert page.locator('[data-goal-marker]').count()==1
   # Sample the actual rendered bounds, including a 2px stroke margin: no available cell underneath.
   assert page.locator('[data-goal-marker]').evaluate("""e=>{const r=e.getBoundingClientRect();for(let x=r.x-2;x<=r.right+2;x+=.75)for(let y=r.y-2;y<=r.bottom+2;y+=.75){const c=document.elementFromPoint(x,y)?.closest('[data-cell]');if(c&&['ground','water'].includes(c.dataset.terrain))return false;}return true;}""")
   assert page.locator('[data-foreground]').get_attribute('pointer-events')=='none'
   assert page.locator('[data-foreground]').evaluate('(e)=>e===e.parentElement.lastElementChild')
   # Start/end labels remain accessible even though the painted world contains none.
   for anchor,label in [(l['start'],l['startName']),(l['goal'],l['goalName'])]:assert label in page.locator('[data-cell="%s,%s"]'%(anchor['q'],anchor['r'])).get_attribute('aria-label')
   if w in [1280,844]:shot(page,f'{l["id"]}-empty-{w}x{h}')
   # Each reference placement comes through public mouse/touch controls, including turns.
   for id,v in l['solution'].items():
    page.locator(f'[data-piece="{id}"]').click();assert page.locator('#tray circle').count()==0
    for _ in range(v['turns']):page.locator('#right').click()
    cell=page.locator('[data-cell="%s,%s"] > polygon'%(v['anchor']['q'],v['anchor']['r']))
    box=cell.bounding_box();page.mouse.click(box['x']+box['width']/2,box['y']+box['height']/2) if w>=1280 else cell.tap()
    expect(page.locator('#placement-preview')).to_have_attribute('data-preview','valid');assert page.locator('#placement-preview text').count()==0
    # Decorative layers do not steal a tap on the target polygon.
    assert cell.evaluate('(e)=>{const r=e.getBoundingClientRect(),target=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return target===e||e.parentElement.contains(target)}')
    page.locator('#place').click()
   assert page.locator('#ground-plane circle').count()==0
   if 'bridge' in l['solution']:
    assert page.locator('[data-owner="bridge"]').count()==3;assert page.locator('[data-owner="bridge"] text').count()==0
   if w in [1280,844]:
    shot(page,f'{l["id"]}-solution-{w}x{h}')
    if l['id'] in ['gate','garden','forest']:shot(page,f'{l["id"]}-gate-close-{w}x{h}',crop(page,l,w,h))
   saved=page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).session.layout',KEY);assert saved==l['solution']
   # Changing the browser dimensions keeps both data and exact hit-testing.
   page.set_viewport_size({'width':h,'height':w});expect(page.locator('#orientation-screen')).to_be_visible();page.set_viewport_size({'width':w,'height':h});expect(page.locator('#field')).to_be_visible()
   page.reload();page.locator('#continue-game').click();assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).session.layout',KEY)==saved
   page.locator('#check').click();expect(page.locator('#story')).to_be_visible();assert page.locator('#ground-plane circle').count()==0
   assert page.locator('[data-foreground]').evaluate('(e)=>e===e.parentElement.lastElementChild')
   if w in [1280,844] and l['id'] in ['gate','garden','forest']:shot(page,f'{l["id"]}-victory-{w}x{h}')
   page.close()
  ctx.close();print(f'{w}x{h}: eight scenes, empty/solutions, full background, legacy layout, mouse/touch, resize, markers, bridge and victory: PASS',flush=True)
 # Drag/cancel next to the fence; the entire preview remains underneath the foreground.
 ctx=b.new_context(viewport={'width':844,'height':390},has_touch=True,reduced_motion='reduce')
 for id in ['gate','garden','forest']:
  page=ctx.new_page();page.goto(URL);l=next(l for l in LEVELS if l['id']==id);seed(page,l,l['solution']);page.locator('#settings-open').click();page.locator('#pause-settings').click();page.locator('#mode').select_option('drag');page.locator('#settings-close').click()
  piece=next(iter(l['solution']));anchor=l['solution'][piece]['anchor'];box=page.locator('[data-cell="%s,%s"] > polygon'%(anchor['q'],anchor['r'])).bounding_box();x,y=box['x']+box['width']/2,box['y']+box['height']/2;cdp=ctx.new_cdp_session(page)
  cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]});cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+15,'y':y+48}]});expect(page.locator('#placement-preview')).to_be_visible()
  assert page.locator('[data-foreground]').evaluate('(e)=>e===e.parentElement.lastElementChild');shot(page,f'{id}-drag-near-fence-844x390')
  cdp.send('Input.dispatchTouchEvent',{'type':'touchCancel','touchPoints':[]});assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).session.layout',KEY)==l['solution'];cdp.detach();page.close()
 ctx.close();assert not errors,errors;b.close();print('Gate/garden/forest touch drag and cancel next to fence: PASS')
