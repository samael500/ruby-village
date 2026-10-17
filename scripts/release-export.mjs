/** Exclude archived browser sources/candidates from generated dist only.
 * Originals remain in public/art for development and review. */
import {readFileSync,readdirSync,statSync,rmSync,rmdirSync,writeFileSync} from 'node:fs';
import {resolve,relative,join} from 'node:path';
export function pruneReleaseExports(root,outDir){
 if(resolve(outDir)===resolve(root))throw new Error('Release output must be separate from source root');
 const read=file=>readFileSync(resolve(root,file),'utf8');
 const version=Number(read('src/production-chapter.ts').match(/PRODUCTION_LAYOUT_VERSION\s*=\s*(\d+)/)?.[1]);
 if(![1,2].includes(version))throw new Error('Unknown release layout contract');
 const motion=read('src/ruta-motion-view.ts').match(/assets\/(characters-walk-v1\/[^/]+)\/manifest\.json/ )?.[1];
 const maps=[...read('src/main.ts').matchAll(/assets\/(chapter-map-[\w-]+)\//g)].map(m=>m[1]);
 if(!motion||!maps.length)throw new Error('Missing explicit motion/map release entry');
 const dirs=['audio','ui/v7','ui/v8','prologue','bridge-v1','road-v1','level-1/v4','level-1/v5','characters-v1/optimized','characters-facing-v1',motion,...maps, ...(version===1?['chapter-1/v6','chapter-1/v8']:['chapter-1/v9'])].map(x=>`assets/${x}/`);
 const files=new Set(['assets/chapter-1/v6/01-courtyard.png']); // current menu CSS
 const optimized=JSON.parse(read('public/assets/characters-v1/delivery-manifest.json')).deliveries;
 for(const file of ['manifest.json','poses-manifest.json','residents-manifest.json']){
  const walk=value=>{if(value&&typeof value==='object')for(const[k,v]of Object.entries(value)){if(k==='image'&&typeof v==='string')files.add(`assets/characters-v1/${optimized[v]?.image??v}`);else walk(v);}};
  walk(JSON.parse(read(`public/assets/characters-v1/${file}`)));
 }
 const removed=[];let keptBytes=0;
 function visit(dir){for(const entry of readdirSync(dir,{withFileTypes:true})){
  const path=join(dir,entry.name);
  if(entry.isDirectory()){visit(path);if(readdirSync(path).length===0)rmdirSync(path);continue;}
  const name=relative(outDir,path).split('\\').join('/'),bytes=statSync(path).size;
  if(!name.startsWith('assets/')||!name.match(/\.(?:png|jpe?g|webp|svg|ogg|wav|json)$/i)||files.has(name)||dirs.some(prefix=>name.startsWith(prefix)))keptBytes+=bytes;
  else{removed.push({file:name,bytes});rmSync(path);}
 }}
 visit(outDir);
 const report={scope:'Generated export pruning only; source repository unchanged',layoutVersion:version,motion,mapFolders:maps,keptBytes,removedBytes:removed.reduce((sum,item)=>sum+item.bytes,0),removed};
 writeFileSync(join(outDir,'export-assets.json'),JSON.stringify(report,null,2)+'\n');return report;
}
