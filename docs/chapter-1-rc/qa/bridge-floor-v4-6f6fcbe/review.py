import json,base64,time,subprocess,re
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'art/chapter-1-v9/layers/water/stream-pilot/manifest.json').read_text());geometry=json.loads((ROOT/manifest['geometry']).read_text());solution=[p for p in manifest['solution'] if p['placement']];reports=[]

with sync_playwright() as p:
 b=p.chromium.launch()
 for touch,w,h in [(False,1280,720),(True,844,390)]:
  prefix='touch844' if touch else 'mouse1280';c=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch,reduced_motion='no-preference',record_video_dir=str(OUT/'raw-video'),record_video_size={'width':w,'height':h});created=time.monotonic();q=c.new_page();errors=[];bad=[];q.on('pageerror',lambda e:errors.append(str(e)));q.on('response',lambda r:bad.append(r.url) if r.status>=400 else None);client=c.new_cdp_session(q)
  def center(loc):
   loc.scroll_into_view_if_needed();r=loc.bounding_box();assert r;return {'x':r['x']+r['width']/2,'y':r['y']+r['height']/2}
  def tap(loc):
   z=center(loc)
   if touch:client.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{**z,'id':1}]});client.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   else:q.mouse.click(**z)
  def cell(a):return q.locator(f'#board [data-cell="{a["q"]},{a["r"]}"] > polygon.cell')
  def saved():return q.evaluate("localStorage.getItem('ruby-village:chapter-1:v1')")
  q.goto('http://127.0.0.1:5308/ruby-village/');navigationOffset=time.monotonic()-created-q.evaluate('performance.now()')/1000;tap(q.locator('#continue-game'))
  while q.locator('#story[open]').count():tap(q.locator('#story-action'))
  q.wait_for_load_state('networkidle');q.wait_for_selector('#app[data-motion="ready"]');states=[]
  def check(label):
   state=q.evaluate('''()=>({owners:[...document.querySelectorAll('#board [data-cell]')].filter(n=>n.dataset.owner).map(n=>({cell:n.dataset.cell,id:n.dataset.owner})),road:document.querySelector('#board [data-connected-road]')?.dataset.confirmedRoadCells,clip:[...document.querySelectorAll('#board [data-connected-road] clipPath polygon')].map(n=>n.getAttribute('points')),outline:[...document.querySelectorAll('#board [data-instance-outlines]')].map(n=>n.getAttribute('d')),edge:document.querySelector('#board [data-road-outer-edge]')?.getAttribute('d'),bridge:document.querySelector('#board [data-painted-bridge]')?.outerHTML})''')
   expect={n['cell'] for n in state['owners'] if n['id']!='bridge'}|{'1,3','9,1'};actual=set(state['road'].split(';'));assert actual==expect,(label,expect,actual);assert len(state['clip'])==len(expect)
   # Each clip polygon equals the exact input polygon of its confirmed cell;
   # labels alone cannot falsely certify a different rendered clip.
   board=q.locator('#board [data-cell]').evaluate_all('ns=>Object.fromEntries(ns.map(n=>[n.dataset.cell,n.querySelector("polygon.cell").getAttribute("points")]))')
   def norm(s):return sorted((round(float(a),5),round(float(b),5)) for a,b in (pair.split(',') for pair in s.split()))
   assert sorted(map(norm,state['clip']))==sorted(norm(board[k]) for k in expect)
   state['label']=label;state['expectedRoad']=sorted(expect);states.append(state);return state
  check('empty-fixed-endpoints')
  for piece in solution:
   tap(q.locator(f'#tray [data-piece="{piece["id"]}"]'))
   for _ in range(piece['placement']['turns']):tap(q.locator('#right'))
   tap(cell(piece['placement']['anchor']));tap(q.locator('#place'));check('placed-'+piece['id'])
  baseline=check('solved');baselineSave=saved();q.screenshot(path=str(OUT/f'{prefix}-solved-technical.jpg'))
  # Presentation-only clean view: hide technical water fills and ≈ glyphs.
  style=q.add_style_tag(content='#board [data-terrain="water"]>polygon.cell{opacity:0!important}#board [data-qa-water-label]{visibility:hidden!important}')
  q.locator('#board [data-puzzle-landmarks] text').evaluate_all('ns=>ns.filter(n=>n.textContent==="≈").forEach(n=>n.setAttribute("data-qa-water-label",""))')
  q.screenshot(path=str(OUT/f'{prefix}-solved-clean.jpg'))
  water=[v for v in geometry['cells'] if v['terrain']=='water']
  q.evaluate('''cells=>{const ns='http://www.w3.org/2000/svg',svg=document.querySelector('#board'),g=document.createElementNS(ns,'g');g.id='qa-water-overlay';g.setAttribute('transform',document.querySelector('[data-painted-world]').getAttribute('transform'));g.setAttribute('pointer-events','none');for(const cell of cells){let p=document.createElementNS(ns,'polygon');p.setAttribute('points',cell.polygon.map(p=>p.x+','+p.y).join(' '));p.setAttribute('fill','#19d5ff33');p.setAttribute('stroke','#ff247a');p.setAttribute('stroke-width','2');g.append(p)}svg.append(g)}''',water)
  q.screenshot(path=str(OUT/f'{prefix}-solved-water-overlay.jpg'));q.locator('#qa-water-overlay').evaluate('n=>n.remove()');style.evaluate('n=>n.remove()')
  # Actual bridge operations: rotated footprint, alternative water anchor, return, undo.
  def bridgecells(st):return sorted(x['cell']for x in st['owners']if x['id']=='bridge')
  tap(cell({'q':6,'r':1}));selectedbridge=check('bridge-reselect-whole');assert bridgecells(selectedbridge)==['5,1','6,1','7,1'] and selectedbridge['outline']
  for _ in range(3):tap(q.locator('#right'))
  assert not q.locator('#place').is_disabled();assert saved()==baselineSave;tap(q.locator('#place'));rotatedbridge=check('bridge-rotated180');assert bridgecells(rotatedbridge)==bridgecells(baseline);tap(q.locator('#undo'));assert saved()==baselineSave
  tap(cell({'q':6,'r':1}));tap(cell({'q':6,'r':0}));assert not q.locator('#place').is_disabled();tap(q.locator('#place'));movedbridge=check('bridge-moved-to-upper-water');assert bridgecells(movedbridge)==['5,0','6,0','7,0'];q.screenshot(path=str(OUT/f'{prefix}-bridge-moved.jpg'));tap(q.locator('#undo'));assert bridgecells(check('bridge-undo-move'))==bridgecells(baseline) and saved()==baselineSave
  tap(cell({'q':6,'r':1}));tap(q.locator('#return'));assert bridgecells(check('bridge-returned'))==[];tap(q.locator('#undo'));assert bridgecells(check('bridge-undo-return'))==bridgecells(baseline) and saved()==baselineSave
  # Whole-instance select, preview rotation and invalid move must leave surface/save.
  chosen=next(v for v in solution if v['id']=='stream-v6-a');tap(cell(chosen['placement']['anchor']));selected=check('reselect-whole');assert selected['outline'] and len([o for o in selected['owners'] if o['id']==chosen['id']])==3
  tap(q.locator('#right'));rotated=check('pending-rotation');assert rotated['road']==baseline['road'] and saved()==baselineSave
  tap(cell({'q':0,'r':0}));assert q.locator('#placement-preview[data-preview="invalid"]').count();invalid=check('pending-invalid');assert invalid['road']==baseline['road'] and saved()==baselineSave;q.screenshot(path=str(OUT/f'{prefix}-invalid-preview.jpg'));tap(q.locator('#other'))
  # Move confirmed composite through real UI to valid free ground, undo it.
  tap(cell(chosen['placement']['anchor']));
  for _ in range(4):tap(q.locator('#right'))
  tap(cell({'q':0,'r':3}));tap(q.locator('#place'));moved=check('moved-composite');assert moved['road']!=baseline['road'];tap(q.locator('#undo'));assert check('undo-move')['road']==baseline['road']
  tap(cell(chosen['placement']['anchor']));tap(q.locator('#return'));returned=check('returned-composite');assert len([o for o in returned['owners'] if o['id']==chosen['id']])==0;tap(q.locator('#undo'));assert check('undo-return')['road']==baseline['road']
  q.reload();tap(q.locator('#continue-game'));q.wait_for_load_state('networkidle');assert check('reload')['road']==baseline['road']
  tap(q.locator('#check'));q.wait_for_selector('#story[open]',timeout=90000)
  while q.locator('#story[open]').count():tap(q.locator('#story-action'))
  q.wait_for_selector('#completion-panel[open]');q.screenshot(path=str(OUT/f'{prefix}-result.jpg'))
  assert not errors and not bad
  video=q.video;c.close();videoPath=OUT/f'{prefix}-actual-input-silent.webm';video.save_as(str(videoPath))
  reports.append({'input':'native CDP touch' if touch else 'mouse','viewport':[w,h],'states':states,'pageErrors':errors,'httpErrors':bad,'recordingScope':'Functional reload run is silent; use separate uninterrupted AV demonstration','physicalPhone':'NOT RUN'})
 b.close()
(OUT/'report.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n');print('PASS2 functional actual-input stream solves/clip/move/undo/reload; silent recordings, separate uninterrupted AV demonstration')
