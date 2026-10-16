"""Try actual Chromium foreground target switch; never override document.hidden."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parents[2]/'docs/chapter-1-rc/qa/runtime-extra'
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context();a=c.new_page();a.goto('http://127.0.0.1:5183/ruby-village/');a.locator('#continue-game').click();a.wait_for_timeout(400);before=a.evaluate('({hidden:document.hidden,state:document.visibilityState})');other=c.new_page();other.goto('about:blank');other.bring_to_front();a.wait_for_timeout(500);background=a.evaluate('({hidden:document.hidden,state:document.visibilityState})');a.bring_to_front();a.wait_for_timeout(300);after=a.evaluate('({hidden:document.hidden,state:document.visibilityState})');r={'method':'separate real target brought to front; no document.hidden override','before':before,'background':background,'after':after,'status':'not-run' if not background['hidden'] else 'visibility-supported-audio-not-instrumented'};(OUT/'background.json').write_text(json.dumps(r,indent=2)+'\n');print(r);b.close()
