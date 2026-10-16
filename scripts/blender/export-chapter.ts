/** Read-only production data export for the complete chapter layout handoff. */
import {mkdirSync,writeFileSync,readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {levels} from '../../src/levels.ts';
import {boardCells,hexCenter,key,footprint,neighbors,findPath} from '../../src/hex.ts';
import {project} from '../../src/projection.ts';
import {sceneMetadata,scenePoint} from '../../src/scene-camera.ts';
import {validateLayout,winningPath,terrainAt} from '../../src/game.ts';
const folder=new URL('../../docs/blender-chapter-1/layouts/engine/',import.meta.url);
mkdirSync(folder,{recursive:true});
const inputs=Object.fromEntries(['levels.ts','hex.ts','projection.ts','scene-camera.ts','game.ts','chapter-1.logical.json','art-solutions.json','scene-v8.json','chapter-1.story.json'].map(file=>[
 `src/${file}`,createHash('sha256').update(readFileSync(new URL(`../../src/${file}`,import.meta.url))).digest('hex'),
]));
const check=process.argv.includes('--check');
for(const level of levels){
 const solution=level.solution;
 const board=new Set(boardCells(level.cols,level.rows).map(key));
 if(new Set(level.pieces.map(p=>p.id)).size!==level.pieces.length||!board.has(key(level.start))||!board.has(key(level.goal))||terrainAt(level,level.goal)!=='ground')throw Error(`${level.id}: invalid endpoints or duplicate pieces`);
 const metadata=sceneMetadata(level.id),camera=metadata.camera,path=winningPath(level,level.solution);
 if(!validateLayout(level,level.solution)||!path)throw new Error(`${level.id}: invalid engine solution`);
 if(level.id==='gate'){
  const dry=new Set(boardCells(level.cols,level.rows).filter(h=>terrainAt(level,h)==='ground').map(key));
  const minimum=findPath(level.start,level.goal,dry)!.length-2;
  if(level.pieces.reduce((n,p)=>n+p.shape.length,0)!==minimum||Object.keys(solution).length!==level.pieces.length)throw Error('gate: every single stone must be necessary and sufficient');
 }
 const pieces=level.pieces.map(p=>{
  const placement=level.solution[p.id];
  return {...p,kind:p.kind??'stone',placement:placement??null,cells:placement?footprint(p.shape,placement.anchor,placement.turns).map(key):[]};
 });
 const bridge=pieces.find(p=>p.kind==='bridge');
 if(bridge){
  if(!bridge.placement||terrainAt(level,bridge.placement.anchor)!=='water'||bridge.cells.filter(id=>level.terrain[id]==='water').length!==1)throw new Error(`${level.id}: bad bridge`);
  const without={...level.solution};delete without[bridge.id];
  if(winningPath(level,without))throw new Error(`${level.id}: bridge not required`);
  const dry=new Set(boardCells(level.cols,level.rows).filter(h=>terrainAt(level,h)==='ground').map(key));
  if(findPath(level.start,level.goal,dry))throw Error(`${level.id}: dry ground bypasses the stream`);
  const water=neighbors(bridge.placement.anchor).filter(h=>terrainAt(level,h)==='water');
  if(water.length!==2||water[0].q+water[1].q!==2*bridge.placement.anchor.q||water[0].r+water[1].r!==2*bridge.placement.anchor.r)throw Error(`${level.id}: river bends around the bridge corner instead of crossing its middle`);
 }
 const cells=boardCells(level.cols,level.rows).map(h=>{
  const center=hexCenter(h,camera.radius);
  const polygon=Array.from({length:6},(_,i)=>{
   const a=(30+i*60)*Math.PI/180;
   const p=project({x:center.x+camera.radius*Math.cos(a),y:center.y+camera.radius*Math.sin(a)},{scale:camera.groundScale,pivotY:0,angle:camera.angle});
   return {x:p.x+camera.origin.x,y:p.y+camera.origin.y};
  });
  return {...h,id:key(h),terrain:level.terrain[key(h)]??null,center:scenePoint(level.id,h),polygon};
 });
 const data={sceneId:level.id,name:level.name,resolution:[metadata.originalRect.width,metadata.originalRect.height],camera,
  start:{...level.start,name:level.startName,pixel:scenePoint(level.id,level.start)},goal:{...level.goal,name:level.goalName,pixel:scenePoint(level.id,level.goal)},
  cells,pieces,path:path.map(key),engineChecks:{validSolution:true,connected:true,bridgeRequired:!!bridge},
  inputs,layoutVersion:2};
 if(check){
  const accepted=JSON.parse(readFileSync(new URL(`${level.id}.json`,folder),'utf8'));
  for(const field of ['sceneId','resolution','camera','start','goal','cells','pieces','path','engineChecks'] as const){
   if(JSON.stringify(accepted[field])!==JSON.stringify(data[field]))throw Error(`${level.id}: accepted ${field} differs`);
  }
 }else writeFileSync(new URL(`${level.id}.json`,folder),JSON.stringify(data,null,2)+'\n');
 console.log(`${level.id}: ${cells.length} cells, ${cells.filter(c=>c.terrain).length} terrain, ${path.length} path cells`);
}
