"""Local production-load measurement; not a real network/device test."""
import json, subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/chapter-1-rc/release'
OUT.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':844,'height':390})
    failed=[]
    page.on('requestfailed',lambda req:failed.append({'url':req.url,'failure':req.failure}))
    page.goto('http://127.0.0.1:5180/ruby-village/',wait_until='networkidle')
    menu=page.evaluate('({navigation:performance.getEntriesByType("navigation")[0].toJSON(),paint:performance.getEntriesByType("paint").map(x=>x.toJSON())})')
    page.locator('#continue-game').click()
    page.locator('#prologue-skip').click()
    while page.locator('#story[open]').count():
        page.locator('#story-action').click()
    page.wait_for_load_state('networkidle')
    resources=page.evaluate('performance.getEntriesByType("resource").map(x=>({name:x.name,duration:x.duration,transferSize:x.transferSize,decodedBodySize:x.decodedBodySize}))')
    dist=ROOT/'dist'
    files=[f for f in dist.rglob('*') if f.is_file()]
    report={'scope':'Local Chromium production server, cold cache, no network throttling; motion active, layout1; final scene activation and export pruning pending','commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'physicalDevice':'not-run','menu':menu,'resources':resources,'throughFirstPuzzleTransferBytes':sum(x['transferSize'] for x in resources),'requestFailures':failed,'distBytes':sum(f.stat().st_size for f in files),'distFileCount':len(files),'largestExports':[{'file':str(f.relative_to(dist)),'bytes':f.stat().st_size} for f in sorted(files,key=lambda f:f.stat().st_size,reverse=True)[:12]],'mastersServed':any('/art/audio/' in x['name'] or x['name'].endswith('.flac') for x in resources)}
    assert not failed and not report['mastersServed']
    (OUT/'load-measurement.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    browser.close()
    print(json.dumps({key:report[key] for key in ['throughFirstPuzzleTransferBytes','distBytes','distFileCount','requestFailures','mastersServed']}))
