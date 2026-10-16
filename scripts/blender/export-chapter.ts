/** Read-only production data export for the complete chapter layout handoff. */
import {mkdirSync,writeFileSync,readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {levels} from '../../src/levels.ts';
import {boardCells,hexCenter,key,footprint,neighbors,findPath} from '../../src/hex.ts';
import {project} from '../../src/projection.ts';
import {sceneMetadata,scenePoint} from '../../src/scene-camera.ts';
import {validateLayout,winningPath,terrainAt} from '../../src/game.ts';
import type {Hex} from '../../src/hex.ts';
import type {Layout,Piece} from '../../src/model.ts';
const folder=new URL('../../docs/blender-chapter-1/layouts/engine/',import.meta.url);
const adjustmentPath='art/blender/chapter-layouts/layout-adjustments.json';
const adjustmentBytes=readFileSync(new URL('../../'+adjustmentPath,import.meta.url));
const adjustments=JSON.parse(adjustmentBytes.toString()) as {
 terrainMoves:Record<string,{from:string;to:string;terrain:'water'}[]>;
 startMoves:Record<string,{from:Hex;to:Hex}>;goalMoves:Record<string,{from:Hex;to:Hex}>;
 extraPieces:Record<string,Piece[]>;solutions:Record<string,Layout>;
};
mkdirSync(folder,{recursive:true});
const inputs=Object.fromEntries(['levels.ts','hex.ts','projection.ts','scene-camera.ts','game.ts','chapter-1.logical.json','art-solutions.json','scene-v8.json','chapter-1.story.json'].map(file=>[
 `src/${file}`,createHash('sha256').update(readFileSync(new URL(`../../src/${file}`,import.meta.url))).digest('hex'),
]));
for(const original of levels){
 const terrainChanges=adjustments.terrainMoves[original.id]??[];
 const startMove=adjustments.startMoves[original.id],solution=adjustments.solutions[original.id]??original.solution;
 const goalMove=adjustments.goalMoves[original.id],additionalPieces=adjustments.extraPieces[original.id]??[];
 const changes=[...terrainChanges.map(move=>({kind:'terrain',...move})),...(startMove?[{kind:'start',...startMove}]:[]),
  ...(goalMove?[{kind:'goal',...goalMove}]:[]),...(additionalPieces.length?[{kind:'pieces',added:additionalPieces}]:[]),
  ...(adjustments.solutions[original.id]?[{kind:'solution',from:original.solution,to:solution}]:[])];
 const terrain={...original.terrain},board=new Set(boardCells(original.cols,original.rows).map(key));
 for(const move of terrainChanges){
  if(terrain[move.from]!==move.terrain||terrain[move.to]||!board.has(move.to))throw Error(`${original.id}: invalid approved terrain move`);
  delete terrain[move.from];terrain[move.to]=move.terrain;
 }
 if(startMove&&key(startMove.from)!==key(original.start))throw Error(`${original.id}: stale start correction`);
 if(goalMove&&key(goalMove.from)!==key(original.goal))throw Error(`${original.id}: stale goal correction`);
 const level={...original,terrain,start:startMove?.to??original.start,goal:goalMove?.to??original.goal,pieces:[...original.pieces,...additionalPieces],solution};
 if(new Set(level.pieces.map(p=>p.id)).size!==level.pieces.length||!board.has(key(level.start))||!board.has(key(level.goal))||terrainAt(level,level.goal)!=='ground')throw Error(`${original.id}: invalid endpoints or duplicate pieces`);
 if(startMove&&(terrainAt(level,level.start)!=='ground'||Object.keys(solution).length>=level.pieces.length))throw Error(`${original.id}: new start must be dry and retain a spare piece`);
 if(startMove&&winningPath(level,original.solution))throw Error(`${original.id}: old solution unexpectedly connects the moved start`);
 if(goalMove&&winningPath(level,original.solution))throw Error(`${original.id}: old solution unexpectedly connects the moved goal`);
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
  inputs:changes.length?{...inputs,[adjustmentPath]:createHash('sha256').update(adjustmentBytes).digest('hex')}:inputs,
  ...(changes.length?{layoutChanges:changes,requiresGameIntegration:true}:{})};
 writeFileSync(new URL(`${level.id}.json`,folder),JSON.stringify(data,null,2)+'\n');
 console.log(`${level.id}: ${cells.length} cells, ${cells.filter(c=>c.terrain).length} terrain, ${path.length} path cells`);
}
