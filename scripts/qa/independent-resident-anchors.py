"""Read actual SVG transforms/ground polygons; never modify geometry."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/qa/residents-bridge-audio-467';OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads((ROOT/'docs/chapter-1-rc/production-solutions.json').read_text());rows=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for w,h in [(1280,720),(844,390)]:
  for index,level in enumerate(levels):
   if level['id'] in ['gate','forest']:continue
   q=b.new_page(viewport={'width':w,'height':h});prior=[l['id']for l in levels[:index]];q.add_init_script('localStorage.setItem("ruby-village:chapter-1:v1",JSON.stringify('+json.dumps({'version':2,'completed':prior,'introSeen':prior})+'))');q.goto('http://127.0.0.1:5297/ruby-village/');q.locator('#continue-game').click()
   while q.locator('#story[open]').count():q.locator('#story-action').click()
   q.wait_for_load_state('networkidle')
   actors=q.locator('#board [data-resident]').evaluate_all('''actors=>{const point=(m,p)=>new DOMPoint(p.x,p.y).matrixTransform(m);const inside=(p,v)=>{let yes=false;for(let i=0,j=v.length-1;i<v.length;j=i++){const a=v[j],b=v[i];if((a.y>p.y)!=(b.y>p.y)&&p.x<(b.x-a.x)*(p.y-a.y)/(b.y-a.y)+a.x)yes=!yes;}return yes};const cells=[...document.querySelectorAll('#board [data-terrain=ground]')].map(c=>({id:c.dataset.cell,pts:[...c.querySelector('polygon.cell').points].map(p=>point(c.querySelector('polygon.cell').getScreenCTM(),p))}));return actors.map(a=>{const foot=point(a.getScreenCTM(),{x:0,y:0}),r=a.getBoundingClientRect();return{id:a.dataset.resident,reaction:a.dataset.reaction,foot:{x:foot.x,y:foot.y},footInGroundCells:cells.filter(c=>inside(foot,c.pts)).map(c=>c.id),bounds:{x:r.x,y:r.y,width:r.width,height:r.height},pointerEvents:getComputedStyle(a).pointerEvents,layer:a.parentElement.hasAttribute('data-scene-residents')}})}''')
   rows.append({'scene':level['id'],'viewport':[w,h],'actors':actors});q.close()
 b.close()
(OUT/'anchor-audit.json').write_text(json.dumps({'baseline':'467eab2','method':'actual transformed SVG polygons; point-in-polygon tests resident feet only, not alpha silhouette','rows':rows},indent=2)+'\n')
print(json.dumps(rows,indent=2))
