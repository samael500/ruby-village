from pathlib import Path
import hashlib,json,re,subprocess
root=Path('/tmp/ruby-final-rc');out=Path(__file__).parent;dist=root/'dist'
files=[];bad=[];urls=[];mismatch=[]
for p in sorted(dist.rglob('*')):
 if not p.is_file():continue
 b=p.read_bytes();rel=str(p.relative_to(dist));files.append({'file':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 if p.suffix.lower() in ['.blend','.fbx','.obj','.gltf','.glb','.sf2','.flac','.mid','.midi','.psd','.kra']:bad.append(rel)
 if b.startswith(b'version https://git-lfs.github.com/spec/v1'):bad.append('LFS:'+rel)
 if p.suffix in ['.html','.css','.js','.json']:
  for x in re.findall(r'https?://[^\s"\x27<>`]+',b.decode(errors='replace')):
   if any(s in x for s in ['localhost','127.0.0.1','/tmp/','generated_images','blob.core','ngrok']):urls.append({'file':rel,'url':x})
 if rel.startswith('assets/') and (root/'public'/rel).is_file() and b!=(root/'public'/rel).read_bytes():mismatch.append(rel)
refs={}
for rel in ['README.md','package.json','package-lock.json','vite.config.ts','scripts/release-export.mjs','THIRD_PARTY_MUSIC.md','art/audio/sfx/THIRD_PARTY_NOTICES.md','src/sound-manifest.json','public/assets/audio/music/manifest.json','.github/workflows/pages.yml','src/production-chapter.ts','src/ruta-motion-view.ts','src/main.ts']:
 p=root/rel;refs[rel]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
report={'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'root':str(root),'files':files,'distBytes':sum(x['bytes'] for x in files),'fileCount':len(files),'forbiddenSourceOrLfs':bad,'temporaryUrls':urls,'publicDistByteMismatches':mismatch,'refs':refs,'exportPolicyReport':json.loads((dist/'export-assets.json').read_text()),'scope':'Existing dist audit only; did NOT invoke mutating release-export, npm ci or build; no runtime/browser/license legal opinion.'}
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['commit','distBytes','fileCount','forbiddenSourceOrLfs','temporaryUrls','publicDistByteMismatches']}))
