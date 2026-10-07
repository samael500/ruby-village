import {test} from 'node:test';
import assert from 'node:assert/strict';
import {project,unproject,GROUND_SCALE,sceneProjection} from '../src/projection.ts';
import {boardCells,hexCenter,pixelHex,rotate} from '../src/hex.ts';
test('Проекция и обратное попадание сохраняют клетки, включая шесть поворотов',()=>{
 for(const pivotY of [0,180,540])for(const radius of [15,40,68])for(const h of boardCells(11,7))for(let t=0;t<6;t++){
  const cell=rotate(h,t),center=hexCenter(cell,radius),p={x:center.x+200,y:center.y+100};
  const view=project(p,{scale:GROUND_SCALE,pivotY});const back=unproject(view,{scale:GROUND_SCALE,pivotY});
  assert.ok(Math.abs(back.x-p.x)<1e-8&&Math.abs(back.y-p.y)<1e-8);
  assert.deepEqual(pixelHex(back.x-200,back.y-100,radius),cell);
 }
});

test('Калибровка сохраняет оба основания сцены при наклоне',()=>{const a={x:500,y:360},b={x:1100,y:670},t=sceneProjection(a,b);for(const p of [a,b]){const v=project(p,t);assert.ok(Math.abs(v.x-p.x)<1e-8&&Math.abs(v.y-p.y)<1e-8);assert.ok(Math.abs(unproject(v,t).y-p.y)<1e-8);}});
