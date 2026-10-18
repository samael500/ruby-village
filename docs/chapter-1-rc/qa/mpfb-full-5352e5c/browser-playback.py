from playwright.sync_api import sync_playwright
from pathlib import Path
import json
O=Path(__file__).resolve().parent
with sync_playwright()as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':1120,'height':480},record_video_dir=str(O/'raw'),record_video_size={'width':1120,'height':480});q=c.new_page();errors=[];q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:5298/docs/chapter-1-rc/qa/mpfb-full-5352e5c/playback.html');q.wait_for_function('ready');q.wait_for_timeout(6000)
 for f in [0,4,8,12,16,20]:q.evaluate('hold('+str(f)+')');q.wait_for_timeout(80);q.screenshot(path=str(O/f'playback-frame{f+1:02}.jpg'))
 log=q.evaluate('log');assert set(x['frame']for x in log)==set(range(24))and not errors;video=q.video;c.close();video.save_as(str(O/'actual-browser-twelve-loop.webm'));b.close();(O/'browser-playback.json').write_text(json.dumps(dict(errors=errors,rafSamples=log,purpose='actual PNG playback, not game/runtime or transition acceptance'),indent=2)+'\n');print('BROWSER 12 genuine loops all24frames PASS')
