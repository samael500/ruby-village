"""Record actual CharacterPlayer/CharacterRoute preview for visible paint-over defects."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];out=root/'docs/chapter-1-rc/painted-motion';url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5192/ruby-village/docs/chapter-1-rc/painted-motion/preview.html'
with sync_playwright() as p:
 browser=p.chromium.launch();context=browser.new_context(viewport={'width':1280,'height':720},record_video_dir=str(out/'capture'),record_video_size={'width':1280,'height':720});page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(url);page.wait_for_function('window.motionState');page.wait_for_timeout(800);page.screenshot(path=str(out/'attempt-01-desktop.jpg'),quality=90)
 page.get_by_role('button',name='Пауза',exact=True).click();page.wait_for_timeout(100);before=page.evaluate('motionState.position');page.wait_for_timeout(350);assert page.evaluate('motionState.position')==before
 page.get_by_role('button',name='Продолжить',exact=True).click();directions={page.evaluate("motionState.direction")}
 for i in range(25):page.wait_for_timeout(1000);directions.add(page.evaluate('motionState.direction'))
 assert directions==set(['e','se','sw','w','nw','ne']),directions
 assert page.evaluate('motionState.completion')==1;video=page.video;page.close();context.close();video.save_as(str(out/'attempt-01-six-directions-runtime.webm'))
 phone=browser.new_page(viewport={'width':844,'height':390});phone.goto(url);phone.wait_for_function('window.motionState');phone.wait_for_timeout(600);phone.screenshot(path=str(out/'attempt-01-landscape.jpg'),quality=90);assert not errors,errors
 (out/'runtime-checks.json').write_text(json.dumps({'scope':'isolated actual runtime review of rejected paint-over, not production gameplay','browser':browser.version,'allSixDirections':sorted(directions),'pausePositionUnchanged':True,'completedOnce':True,'pageErrors':errors},indent=2)+'\n');browser.close()
print('Real runtime painted attempt capture complete; visual acceptance is separate')
