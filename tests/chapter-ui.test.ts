import {test} from 'node:test';
import assert from 'node:assert/strict';
import {chapterMap,continueTarget,learningHint,chapterCompletion} from '../src/chapter-ui.ts';
import {stagedPrologueFrame} from '../src/prologue-staging.ts';
import {levels} from '../src/levels.ts';
test('UI preserves sparse migrated wins without opening a gap or mutating progress',()=>{
 const completed=['gate','mill'];const before=[...completed],map=chapterMap(completed);
 assert.deepEqual(completed,before);assert.equal(map[1].state,'available');assert.equal(map[2].disabled,true);
 assert.equal(map[5].state,'restored');assert.equal(map[5].disabled,false);assert.equal(map[5].connectionRestored,false);
 assert.equal(continueTarget(completed,'forest'),'garden');assert.equal(continueTarget(completed,'mill'),'mill');
});
test('completed chapter keeps replay, map and letter without a chapter 2 launch',()=>{
 const completed=levels.map(l=>l.id);assert.ok(chapterMap(completed).every(l=>!l.disabled));
 assert.equal(continueTarget(completed),'gate');assert.deepEqual(chapterCompletion.actions,['map','replay','letter']);
});
test('learning follows actual input mode, rotation and first bridge',()=>{
 const state={levelId:'gate',mode:'select' as const,selected:false,placed:0,rotated:false,hasBridge:false,bridgePlaced:false};
 assert.equal(learningHint(state)?.id,'choose');assert.match(learningHint({...state,selected:true})!.text,/Поставить/);
 assert.match(learningHint({...state,selected:true,mode:'drag'})!.text,/Перетащи/);
 assert.equal(learningHint({...state,levelId:'garden',selected:true})?.id,'rotate');
 assert.equal(learningHint({...state,levelId:'stream',hasBridge:true})?.id,'bridge');
 assert.equal(learningHint({...state,levelId:'stream',hasBridge:true,bridgePlaced:true}),null);
});
test('six staged frames keep Rabbit alone, narrator portrait absent, and gameplay handoff exact',()=>{
 const frames=Array.from({length:6},(_,i)=>stagedPrologueFrame(i));
 assert.deepEqual(frames[2].staging.actors.map(a=>a.id),['rabbit']);assert.equal(frames[4].staging.actors[0].pose,'crouch');
 assert.equal(frames[5].staging.camera,'gameplay');assert.equal(frames[5].staging.actors[0].anchor,'start');
 assert.equal(frames[5].staging.next,'К калитке');assert.ok(frames.every(f=>!f.showPuzzleUI));
 for(const i of [-1,6,NaN,1.5])assert.throws(()=>stagedPrologueFrame(i),RangeError);
});
