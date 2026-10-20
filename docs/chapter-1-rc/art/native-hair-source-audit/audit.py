from pathlib import Path
from collections import Counter
from PIL import Image,ImageDraw
import hashlib,json,zipfile,urllib.request
O=Path(__file__).resolve().parent;R=Path('/home/mskorokhod/life/_tools/mpfb-assets');names=['elvs_keylth_hair','elvs_lady_hippy_hair','elvs_hazel_hair'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=[];Z=zipfile.ZipFile(R/'hair02_ccby.zip')
for n in names:
 p=R/'extracted/hair'/n;obj=next(p.glob('*.obj'));lines=obj.read_text().splitlines();v=[list(map(float,l.split()[1:4]))for l in lines if l.startswith('v ')];f=[[int(t.split('/')[0])-1 for t in l.split()[1:]]for l in lines if l.startswith('f ')];edges=Counter(tuple(sorted((a,b)))for face in f for a,b in zip(face,face[1:]+face[:1]));adj=[[]for _ in v]
 for a,b in edges:adj[a].append(b);adj[b].append(a)
 seen=set();comps=0
 for i in range(len(v)):
  if i in seen:continue
  comps+=1;pending=[i];seen.add(i)
  while pending:
   j=pending.pop()
   for k in adj[j]:
    if k not in seen:seen.add(k);pending.append(k)
 files=[]
 for file in sorted(p.iterdir()):
  if not file.is_file():continue
  suffix='hair/'+n+'/'+file.name;matches=[x for x in Z.namelist()if x.endswith(suffix)];assert len(matches)==1,(suffix,matches);data=Z.read(matches[0]);assert hashlib.sha256(data).hexdigest()==sha(file);files.append({'path':str(file),'bytes':file.stat().st_size,'sha256':sha(file),'archiveEntry':matches[0],'matchesExistingOfficialArchiveBytes':True})
 thumb=next(p.glob('*.thumb'));(O/(n+'.png')).write_bytes(thumb.read_bytes());mat=next(p.glob('*.mhmat'));(O/(n+'-material.txt')).write_bytes(mat.read_bytes());headers=[l for l in lines[:12]if l.startswith('#')];mh=next(p.glob('*.mhclo'));headers+=mh.read_text().splitlines()[:12];(O/(n+'-source-headers.txt')).write_text('\n'.join(headers)+'\n');rows.append({'name':n,'vertices':len(v),'faces':len(f),'uvCoordinates':sum(l.startswith('vt ')for l in lines),'boundaryEdges':sum(x==1 for x in edges.values()),'nonTwoSidedEdges':sum(x!=2 for x in edges.values()),'connectedComponents':comps,'sourceAxis':'MakeHuman nativeYup (notRuta fitted)','boundsXYZ':[[min(x[i]for x in v)for i in range(3)],[max(x[i]for x in v)for i in range(3)]],'localFiles':files,'thumbnailFile':n+'.png','licenseHeader':headers[:5]})
network=[]
for url,filename,method in [('https://static.makehumancommunity.org/assets/assetpacks/hair02.html','official-hair02.html','GET'),('https://static.makehumancommunity.org/oldsite/faq/what_do_i_need_to_do_when_i_use_a_ccby_asset.html','official-ccby-faq.html','GET'),('https://files2.makehumancommunity.org/asset_packs/hair02/hair02_ccby.zip',None,'HEAD')]+[('https://static.makehumancommunity.org/assets/assetpacks/'+n+'.png',n+'-official.png','GET')for n in names]:
 try:
  with urllib.request.urlopen(urllib.request.Request(url,method=method),timeout=20)as res:
   data=res.read()if method=='GET'else b'';rec={'url':url,'method':method,'status':res.status,'contentLengthHeader':res.headers.get('Content-Length'),'receivedBytes':len(data)}
   if filename:
    target=O/('cache/'+filename if filename.endswith('.html')else filename);target.parent.mkdir(exist_ok=True);target.write_bytes(data);rec.update({'savedFile':str(target.relative_to(O)),'sha256':hashlib.sha256(data).hexdigest()})
 except Exception as e:rec={'url':url,'method':method,'error':str(e)}
 network.append(rec)
report={'auditDate':'2026-10-20','scope':'readonlylocalassets+officialprimarypages, noimport/model/render/login/purchase','officialArchiveExistingPath':str(R/'hair02_ccby.zip'),'officialArchiveSHA256':sha(R/'hair02_ccby.zip'),'candidates':rows,'network':network};(O/'inventory-and-provenance.json').write_text(json.dumps(report,indent=2)+'\n');sheet=Image.new('RGB',(900,370),'#e8e0cf');draw=ImageDraw.Draw(sheet)
for i,n in enumerate(names):
 im=Image.open(O/(n+'.png')).convert('RGB');im.thumbnail((280,290));sheet.paste(im,(300*i+(300-im.width)//2,35));draw.text((300*i+10,8),n,fill='black');draw.text((300*i+10,335),'Elvaerwyn / CC-BY / official hair02',fill='black')
sheet.save(O/'three-verified-source-thumbnails.jpg',quality=94);print([(r['name'],r['vertices'],r['faces'],r['boundaryEdges'])for r in rows]);print(network)
