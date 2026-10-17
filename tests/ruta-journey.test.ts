import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {RutaJourney} from '../src/ruta-journey.ts';
import {selectPaintedScene} from '../scripts/character-paint-playback.ts';
import {planGroundRoute,pointOnGoal} from '../scripts/character-paint-route-planner.ts';
import {levels} from '../src/levels.ts';
import {winningPath} from '../src/game.ts';
const root=new URL('../',import.meta.url),manifest=JSON.parse(readFileSync(new URL('public/assets/characters-walk-v1/animated-v2/manifest.json',root),'utf8'));
test('all eight accepted puzzle paths finish on actual goal ground with authored start/stop at 30/60/144fps',()=>{
 for(const level of levels){
  const geometry=JSON.parse(readFileSync(new URL(`docs/blender-chapter-1/layouts/engine/${level.id}.json`,root),'utf8'));
  const path=winningPath(level,level.solution)!.map(h=>geometry.cells.find((cell:{id:string})=>cell.id===`${h.q},${h.r}`).center);
  const polygon=geometry.cells.find((cell:{id:string})=>cell.id===`${level.goal.q},${level.goal.r}`).polygon;
  const set=selectPaintedScene(manifest,level.id),plan=planGroundRoute(path,{directions:set.directions as typeof manifest.directions,goalPolygon:polygon});
  assert.equal(plan.status,'ready',level.id);if(plan.status!=='ready')continue;
  for(const fps of [30,60,144]){
   const actor=new RutaJourney(plan,set);let contacts=0;
   for(let i=0;i<Math.ceil(plan.durationMs/(1000/fps));i++)contacts+=actor.advance(1000/fps,{surface:'stone'}).length;
   assert.ok(actor.done,`${level.id} ${fps}`);assert.equal(actor.clock.state,'idle');assert.deepEqual(actor.position,plan.endpoint);
   assert.ok(pointOnGoal(actor.position,plan.center,{goalPolygon:polygon}));assert.ok(contacts>0);
  }
 }
});
test('route and source phase freeze together and discard first stale resumed delta',()=>{
 const set=selectPaintedScene(manifest,'gate'),stride=manifest.directions.e.projectedStridePixels;
 const plan=planGroundRoute([{x:0,y:0},{x:stride*3,y:0}],{directions:manifest.directions,goalRadius:20});assert.equal(plan.status,'ready');if(plan.status!=='ready')return;
 const actor=new RutaJourney(plan,set);actor.advance(900);const point=actor.position,phase=actor.clock.phaseMs;
 actor.advance(999999,{paused:true});actor.advance(999999);assert.deepEqual(actor.position,point);assert.equal(actor.clock.phaseMs,phase);
 actor.advance(0,{reducedMotion:true});assert.ok(actor.done);assert.deepEqual(actor.position,plan.endpoint);
});
