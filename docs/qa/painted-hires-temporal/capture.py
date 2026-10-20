"""Read-only configurable frozen-preview probe. Run after checking author API.
Example: capture.py URL --out run --play '#play' --frame '#frame'
No page/source writes. Slider input is normal review interaction.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import argparse,json,hashlib,urllib.request
p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('--out',required=True);p.add_argument('--play',default='#play');p.add_argument('--frame',default='#frame');p.add_argument('--html-sha',required=True);a=p.parse_args();O=Path(a.out);O.mkdir(parents=True,exist_ok=True)
html=urllib.request.urlopen(a.url).read();assert hashlib.sha256(html).hexdigest()==a.html_sha
report={'url':a.url,'htmlSha':a.html_sha,'runs':[]}
with sync_playwright() as pw:
 browser=pw.chromium.launch()
 for name,w,h,dpr,touch in [('desktop-dpr1',1280,800,1,False),('desktop-dpr2',1280,800,2,False),('landscape-touch',844,390,1,True)]:
  out=O/name;out.mkdir(exist_ok=True);ctx=browser.new_context(viewport={'width':w,'height':h},device_scale_factor=dpr,record_video_dir=str(out/'video'),record_video_size={'width':w,'height':h});page=ctx.new_page();errors=[];http=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('requestfailed',lambda q:errors.append([q.url,q.failure]));page.on('response',lambda r:http.append([r.url,r.status]) if r.status>=400 else None)
  if touch:ctx.new_cdp_session(page).send('Emulation.setTouchEmulationEnabled',{'enabled':True,'maxTouchPoints':5})
  page.goto(a.url,wait_until='networkidle');page.wait_for_function('window.reviewState?.ready');page.wait_for_timeout(4200);run={'name':name,'state':page.evaluate('reviewState'),'geometry':page.evaluate('''()=>({dpr:devicePixelRatio,viewport:[innerWidth,innerHeight],scroll:[document.documentElement.scrollWidth,document.documentElement.scrollHeight],canvases:[...document.querySelectorAll('canvas')].map(c=>({id:c.id,backing:[c.width,c.height],rect:c.getBoundingClientRect().toJSON(),smoothing:c.getContext('2d').imageSmoothingEnabled,quality:c.getContext('2d').imageSmoothingQuality}))})''')};page.screenshot(path=str(out/'playing.png'));page.locator(a.play).click()
  for phase in [11,12,23,24,35,36,47,0]:
   page.locator(a.frame).fill(str(phase));page.locator(a.frame).dispatch_event('input');page.wait_for_timeout(60);page.screenshot(path=str(out/f'phase-{phase:02}.png'))
  run.update(errors=errors,httpFailures=http,video=str(page.video.path()),touchEmulated=touch);ctx.close();report['runs'].append(run)
 browser.close()
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
