import {test} from 'node:test';
import assert from 'node:assert/strict';
import {levels} from '../src/levels.ts';
import scenes from '../src/scene-v8.json' with {type:'json'};
import {scenePoint} from '../src/scene-camera.ts';
import {placedCells} from '../src/game.ts';
import {routeSurface} from '../src/route-surface.ts';
test('both river bridges emit timber surface over all three cells, ordinary road stays stone',()=>{
 for(const id of ['stream','mill']){
  const level=levels.find(l=>l.id===id)!,camera=scenes[id as keyof typeof scenes].camera;
  const bridge=level.pieces.find(p=>p.kind==='bridge')!;
  for(const cell of placedCells(bridge.id,level.solution[bridge.id],level.pieces))assert.equal(routeSurface(level,level.solution,scenePoint(id,cell),camera),'wood');
  assert.equal(routeSurface(level,level.solution,scenePoint(id,level.start),camera),'stone');
 }
});
