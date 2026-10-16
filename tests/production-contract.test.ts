import {test} from 'node:test';
import assert from 'node:assert/strict';
import {productionLevels,PRODUCTION_LAYOUT_VERSION,productionScenes} from '../src/production-chapter.ts';
import {levels} from '../src/levels.ts';
import {winningPath} from '../src/game.ts';
import {recoverSession,saveSession} from '../src/session.ts';
import {PROGRESS_KEY} from '../src/progress.ts';
import {scenePoint} from '../src/production-camera.ts';
test('Unaccepted art cannot activate layout 2: old background, endpoints, solutions and inventory stay together',()=>{
 assert.equal(PRODUCTION_LAYOUT_VERSION,1);
 for(const level of productionLevels){
  assert.ok(winningPath(level,level.solution),level.id);
  const meta=productionScenes[level.id as keyof typeof productionScenes];
  assert.deepEqual(scenePoint(level.id,level.start),meta.groundAnchors.start);
  assert.deepEqual(scenePoint(level.id,level.goal),meta.groundAnchors.goal);
 }
 assert.equal(productionLevels[0].pieces.length,7);
 assert.equal(levels[0].pieces.length,8);
 assert.notDeepEqual(productionLevels[0].goal,levels[0].goal);
});
test('Production session recovery keeps legacy cells until atomic artwork activation',()=>{
 const garden=productionLevels.find(l=>l.id==='garden')!;
 let saved=JSON.stringify({version:2,completed:['gate'],session:{levelId:'garden',cols:11,rows:7,layout:garden.solution}});
 const storage={getItem:()=>saved,setItem:(_k:string,v:string)=>{saved=v;}};
 const recovered=recoverSession(storage,['gate'],productionLevels,PRODUCTION_LAYOUT_VERSION);
 assert.deepEqual(recovered.session?.layout,garden.solution);
 assert.equal(saveSession(storage,recovered.session,undefined,PRODUCTION_LAYOUT_VERSION),true);
 assert.equal(JSON.parse(saved).layoutVersion,1);
 assert.deepEqual(recoverSession(storage,['gate'],productionLevels,1).session?.layout,garden.solution);
 assert.equal(PROGRESS_KEY.length>0,true);
});
