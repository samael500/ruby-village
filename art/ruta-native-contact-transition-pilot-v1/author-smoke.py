from pathlib import Path
import json,hashlib
from PIL import Image
from playwright.sync_api import sync_playwright
O=Path(__file__).resolve().parent;url='http://127.0.0.1:5370/art/ruta-native-contact-transition-pilot-v1/review.html';rows=[];m=json.load(open(O/'proof-manifest.json'));margins=[]
for file in sorted(set(f['file']for f in m['frames'])):
 im=Image.open(O/file).convert('RGBA');box=im.getchannel('A').getbbox();assert im.size==(256,320);assert box and min(box[0],box[1],256-box[2],320-box[3])>0;margins.append(min(box[0],box[1],256-box[2],320-box[3]))
with sync_playwright()as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
 for dpr in [1,2]:
  page=browser.new_page(viewport={'width':1280,'height':900},device_scale_factor=dpr);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(url);page.wait_for_function('window.reviewReady===true');page.evaluate('window.reviewSeek(10)');page.evaluate("window.reviewSetMode('fixed')");fixed=page.evaluate('window.reviewState');page.screenshot(path=str(O/f'author-start-fixed-dpr{dpr}.png'));page.evaluate("window.reviewSetMode('route')");page.evaluate('window.reviewSeek(69)');route=page.evaluate('window.reviewState');page.screenshot(path=str(O/f'author-stop-route-dpr{dpr}.png'));assert route['mode']=='route'and fixed['mode']=='fixed';page.click('#replay');page.wait_for_timeout(3200);end=page.evaluate('window.reviewState');assert end['frame']==79 and not end['playing'],end;assert not errors;rows.append({'DPR':dpr,'fixedStartState':fixed,'routeStopState':route,'actualPlaybackStopsAtFinalIdle':end['frame']==79,'pageErrors':errors});page.close()
 browser.close()
(O/'author-smoke.json').write_text(json.dumps({'scope':'author browser smoke, independent visual/contact QA pending','URL':url,'htmlSHA256':hashlib.sha256((O/'review.html').read_bytes()).hexdigest(),'manifestSHA256':hashlib.sha256((O/'proof-manifest.json').read_bytes()).hexdigest(),'frameCount':80,'uniqueRenderedFrames':len(margins),'minimumAlphaMarginPx':min(margins),'DPRRuns':rows},indent=2));print('AUTHOR_SMOKE_DONE')
