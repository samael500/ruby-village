"""Record real runtime east pilot; no production/artistic acceptance claim."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path(__file__).resolve().parents[1]/'docs/chapter-1-rc/painted-motion'
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':1280,'height':720},record_video_dir=str(out/'capture'),record_video_size={'width':1280,'height':720});page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://127.0.0.1:5192/ruby-village/docs/chapter-1-rc/painted-motion/mesh-preview.html');page.wait_for_function('window.motionState');page.wait_for_timeout(1200);page.screenshot(path=str(out/'mesh-east-desktop.jpg'),quality=92)
 page.get_by_role('button',name='Пауза',exact=True).click();page.wait_for_timeout(100);pos=page.evaluate('motionState.position');page.wait_for_timeout(400);assert page.evaluate('motionState.position')==pos;page.get_by_role('button',name='Продолжить',exact=True).click();page.wait_for_timeout(14000);assert page.evaluate('motionState.completion')==1;assert not errors,errors;v=page.video;page.close();c.close();v.save_as(str(out/'mesh-east-runtime.webm'))
 phone=b.new_page(viewport={'width':844,'height':390});phone.goto('http://127.0.0.1:5192/ruby-village/docs/chapter-1-rc/painted-motion/mesh-preview.html');phone.wait_for_function('window.motionState');phone.wait_for_timeout(800);phone.screenshot(path=str(out/'mesh-east-landscape.jpg'),quality=92);phone.get_by_label('Reduced motion').check();phone.wait_for_timeout(150);assert phone.evaluate('motionState.completion')==1;b.close()
 (out/'mesh-runtime-checks.json').write_text(json.dumps({'scope':'isolated actual east mesh runtime, not production','pausePositionUnchanged':True,'completedOnce':True,'reducedMotionCompletes':True,'pageErrors':errors},indent=2)+'\n')
print('Real east mesh runtime capture/checks saved')
