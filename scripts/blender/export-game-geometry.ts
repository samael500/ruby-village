/** Export actual engine geometry; no artwork estimates and no production writes. */
import {mkdirSync,writeFileSync} from 'node:fs';
import {levels} from '../../src/levels.ts';
import {boardCells,footprint,hexCenter,key} from '../../src/hex.ts';
import {project} from '../../src/projection.ts';
import {sceneMetadata,scenePoint} from '../../src/scene-camera.ts';
const id=process.argv[2]??'gate';
const level=levels.find(l=>l.id===id);
if(!level)throw new Error(`Unknown level: ${id}`);
const metadata=sceneMetadata(id),camera=metadata.camera;
const cells=boardCells(level.cols,level.rows).map(h=>{
 const center=hexCenter(h,camera.radius);
 const polygon=Array.from({length:6},(_,i)=>{
  const angle=(30+i*60)*Math.PI/180;
  const point=project({x:center.x+camera.radius*Math.cos(angle),y:center.y+camera.radius*Math.sin(angle)},{scale:camera.groundScale,pivotY:0,angle:camera.angle});
  return {x:point.x+camera.origin.x,y:point.y+camera.origin.y};
 });
 return {...h,id:key(h),terrain:level.terrain[key(h)]??null,center:scenePoint(id,h),polygon};
});
const solution=level.pieces.flatMap(piece=>{
 const placement=level.solution[piece.id];
 return placement?footprint(piece.shape,placement.anchor,placement.turns).map(h=>({pieceId:piece.id,cellId:key(h)})):[];
});
const output={sceneId:id,source:'src/levels.ts + hex.ts + projection.ts + scene-camera.ts',camera,resolution:[metadata.originalRect.width,metadata.originalRect.height],start:{...level.start,pixel:scenePoint(id,level.start)},goal:{...level.goal,pixel:scenePoint(id,level.goal)},cells,solution};
const folder=new URL('../../docs/blender-chapter-1/geometry/',import.meta.url);
mkdirSync(folder,{recursive:true});
writeFileSync(new URL(`${id}-engine.json`,folder),JSON.stringify(output,null,2)+'\n');
console.log(`Exported ${id}: ${cells.length} cells, ${cells.filter(c=>c.terrain).length} terrain cells`);
