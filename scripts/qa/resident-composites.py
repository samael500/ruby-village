"""Browser-rendered candidate grounding review, NOT production-game evidence."""
import json,base64
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[2];out=root/'docs/chapter-1-rc/art/coordinator-review/resident-composites';out.mkdir(parents=True,exist_ok=True)
residents=json.loads((root/'public/assets/characters-v1/residents-manifest.json').read_text())['characters']
delivery=json.loads((root/'public/assets/characters-v1/delivery-manifest.json').read_text())['deliveries']
actors={'garden':[('rabbit',1280,245)],'well':[('teacher',1195,405)],'bakery':[('baker',1290,405)],'stream':[('squirrel',1400,225)],'mill':[('miller',1430,398),('squirrel',1330,405)],'post':[('hedgehog',1370,405)]}
def data(path):return 'data:image/webp;base64,'+base64.b64encode(path.read_bytes()).decode()
with sync_playwright() as p:
 b=p.chromium.launch();q=b.new_page(viewport={'width':1280,'height':760})
 for scene,people in actors.items():
  markup=f'<image href="{data(root/f"public/assets/chapter-1/v9/{scene}/background.webp")}" width="1672" height="941"/>'
  for actor,x,y in sorted(people,key=lambda a:a[2]):
   resident=residents[actor];original=resident['frames']['idle'];frame=delivery.get(original['image'],original);scale=resident['sceneHeightPx']/frame['frameSize'][1];width=frame['frameSize'][0]*scale;height=frame['frameSize'][1]*scale
   markup+=f'<ellipse cx="{x}" cy="{y}" rx="{height*.13}" ry="{height*.035}" fill="#302d23" opacity=".18"/><image href="{data(root/"public/assets/characters-v1"/frame["image"])}" x="{x-frame["footAnchor"][0]*scale}" y="{y-frame["footAnchor"][1]*scale}" width="{width}" height="{height}"/>'
  q.set_content(f'<body style="margin:0;background:#f5ebd5"><svg style="display:block;width:1280px;height:720px" viewBox="0 0 1672 941">{markup}</svg><p style="margin:10px;font:14px sans-serif">{scene}: candidate resident grounding on v4 source; not production QA / final art approval</p></body>')
  q.wait_for_load_state('networkidle');q.screenshot(path=str(out/f'{scene}.jpg'),type='jpeg',quality=90)
 b.close()
(out/'anchors.json').write_text(json.dumps({'scope':'browser-rendered candidate source composition; missing anchors proposed only; not production acceptance','actors':actors},indent=2)+'\n')
print('Six candidate grounding composites saved, seven residents')
