"""Actual Chromium Image.decode test; no production edits or whole-game claim."""
import argparse,base64,io,json,pathlib,subprocess,hashlib
from PIL import Image
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--ref',default='5a7672a');p.add_argument('--repo',default='/home/mskorokhod/life/ruby-village');p.add_argument('--output',default='before.json');a=p.parse_args()
source=subprocess.check_output(['git','show',a.ref+':src/ruta-motion-view.ts'],cwd=a.repo,text=True)
# Remove imports whose names are unused by prepareMotionAtlases. Compile exact function/cache logic.
compiler="const e=require('./node_modules/esbuild');let s=require('fs').readFileSync(0,'utf8').replace(/^import .*;$/mg,'').replaceAll('import.meta.env.BASE_URL',JSON.stringify('http://qa.test/'));process.stdout.write(e.transformSync(s,{loader:'ts',format:'iife',globalName:'Motion'}).code)"
js=subprocess.check_output(['/home/mskorokhod/.ya/tools/v3/14019382748/bin/node','-e',compiler],input=source,text=True,cwd=a.repo)
buf=io.BytesIO();Image.new('RGBA',(2,2),(0,0,0,255)).save(buf,format='PNG');png=buf.getvalue()
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,args=['--no-sandbox']);page=b.new_page();requests=[];allow=False
 def handle(route):
  requests.append({'url':route.request.url,'networkRestored':allow})
  if not allow:route.abort()
  else:route.fulfill(status=200,content_type='image/png',body=png)
 page.route('http://qa.test/**',handle);page.add_script_tag(content=js)
 call="""async()=>{const set={directions:{E:{clips:{idle:{frames:[{file:'atlas.png'}]}}}}};return await Promise.all([0,1].map(async()=>{try{const m=await Motion.prepareMotionAtlases(set);return {status:'ok',dimensions:m.get('atlas.png')}}catch(e){return {status:'error',name:e.name,message:e.message}}}))}"""
 failed=page.evaluate(call);allow=True;retry=page.evaluate(call)
 # Independently prove the restored endpoint serves a valid decodable PNG.
 fresh=page.evaluate("async()=>{let i=new Image();i.src='http://qa.test/control.png';await i.decode();return [i.naturalWidth,i.naturalHeight]}")
 result={'sourceRef':a.ref,'sourceSha256':hashlib.sha256(source.encode()).hexdigest(),'browser':b.version,'scope':'Real Chromium exact compiled module function, not full game reentry','concurrentInitialFailure':failed,'concurrentRetryAfterNetworkRestored':retry,'freshControlDimensions':fresh,'requests':requests}
 b.close()
pathlib.Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
