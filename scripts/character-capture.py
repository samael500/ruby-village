"""Browser evidence for the isolated technical motion preview; not production QA."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'docs/chapter-1-rc/characters/motion';results={}
URL='http://127.0.0.1:5186/ruby-village/docs/chapter-1-rc/characters/motion/preview.html'
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 c=b.new_context(viewport={'width':1280,'height':720},record_video_dir=str(O/'capture'),record_video_size={'width':1280,'height':720});page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(URL);page.wait_for_function('window.motionState');page.wait_for_timeout(1800);page.screenshot(path=str(O/'desktop-1280x720.png'))
 page.get_by_role('button',name='Пауза',exact=True).click();page.wait_for_timeout(150);before=page.evaluate('window.motionState');page.wait_for_timeout(650);after=page.evaluate('window.motionState');assert before['position']==after['position'];results['pausePositionUnchanged']=True
 page.get_by_role('button',name='Продолжить',exact=True).click();page.wait_for_timeout(24000);results['completedOnce']=page.evaluate('window.motionState.completion')==1;assert results['completedOnce'];video=page.video;page.close();c.close();video.save_as(str(O/'six-directions-runtime.webm'))
 phone=b.new_page(viewport={'width':844,'height':390});phone.goto(URL);phone.wait_for_function('window.motionState');phone.wait_for_timeout(900);phone.screenshot(path=str(O/'landscape-844x390.png'));phone.get_by_label('Reduced motion').check();phone.wait_for_timeout(150);assert phone.evaluate('window.motionState.done');results['reducedMotionCompletes']=True;phone.wait_for_timeout(300);assert phone.evaluate('window.motionState.completion')==1;results['pageErrors']=errors;assert not errors
 b.close()
(O/'browser-checks.json').write_text(json.dumps(results,indent=2)+'\n');print(results)
