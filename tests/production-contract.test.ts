import {test} from 'node:test';
import assert from 'node:assert/strict';
import {productionLevels,PRODUCTION_LAYOUT_VERSION,productionScenes} from '../src/production-chapter.ts';
import {levels} from '../src/levels.ts';
import {winningPath,validPlacement} from '../src/game.ts';
import {recoverSession,saveSession} from '../src/session.ts';
import {PROGRESS_KEY} from '../src/progress.ts';
import {scenePoint} from '../src/production-camera.ts';
import manifest from '../public/assets/chapter-1/v9/manifest.json' with {type:'json'};
import {paintedActivationBlockers} from '../src/painted-activation.ts';
import legacy from '../src/chapter-1.legacy.json' with {type:'json'};

test('ordinary production pairs all eight accepted layouts with checked painted scenes',()=>{
 assert.equal(PRODUCTION_LAYOUT_VERSION,2);
 assert.deepEqual(productionLevels,levels);
 assert.deepEqual(paintedActivationBlockers(manifest,productionScenes),[]);
 for(const level of productionLevels){
  assert.ok(winningPath(level,level.solution),level.id);
  const meta=productionScenes[level.id as keyof typeof productionScenes];
  assert.deepEqual(scenePoint(level.id,level.start),meta.groundAnchors.start);
  assert.deepEqual(scenePoint(level.id,level.goal),meta.groundAnchors.goal);
 }
 assert.equal(productionLevels[0].pieces.length,8);
});
test('ordinary activation migrates old placement saves while retaining completed places',()=>{
 const garden=productionLevels.find(l=>l.id==='garden')!;
 const old=legacy['art-solutions.json'].garden;
 let saved=JSON.stringify({version:2,layoutVersion:1,completed:['gate'],session:{levelId:'garden',cols:11,rows:7,layout:old}});
 const storage={getItem:()=>saved,setItem:(_k:string,v:string)=>{saved=v;}};
 const recovered=recoverSession(storage,['gate'],productionLevels,PRODUCTION_LAYOUT_VERSION);
 assert.equal(recovered.migrated,true);assert.ok(recovered.session);
 const accepted={};for(const[id,placement]of Object.entries(recovered.session!.layout)){
  assert.equal(validPlacement(garden,id,placement,accepted),true);Object.assign(accepted,{[id]:placement});
 }
 assert.equal(saveSession(storage,recovered.session,undefined,PRODUCTION_LAYOUT_VERSION),true);
 assert.equal(JSON.parse(saved).layoutVersion,2);assert.deepEqual(JSON.parse(saved).completed,['gate']);
 assert.deepEqual(recoverSession(storage,['gate'],productionLevels,2).session?.layout,recovered.session?.layout);
 assert.equal(PROGRESS_KEY.length>0,true);
});
