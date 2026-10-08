import {test} from 'node:test';
import assert from 'node:assert/strict';
import {PROLOGUE_KEY,loadPrologue,savePrologue,newPrologue,shouldStartPrologue,prologueFrames,speakerPortrait} from '../src/prologue.ts';
import {PROGRESS_KEY,saveProgress,loadState} from '../src/progress.ts';
import {saveSession,loadSession} from '../src/session.ts';
import {levels} from '../src/levels.ts';
const memory=()=>{const values=new Map<string,string>();return {getItem:(k:string)=>values.get(k)??null,setItem:(k:string,v:string)=>{values.set(k,v);}};};
test('Пролог: шесть кадров, цель яблоки/Кролик, персонажи и рассказчик',()=>{
 assert.equal(prologueFrames.length,6);assert.match(prologueFrames[1].text,/Кролик.*яблоки/);assert.match(prologueFrames[5].text,/калитки/);
 assert.equal(speakerPortrait('Рассказчик'),undefined);assert.notEqual(speakerPortrait('Кролик'),speakerPortrait('Рута'));
 assert.equal(levels.length,8);assert.ok(!levels.some(l=>l.id==='c1-00-prologue'));
});
test('Кадр восстанавливается; просмотр не меняет пазл-сессию при последующих записях прогресса',()=>{
 const storage=memory();saveProgress(['gate'],storage);
 const session={levelId:'garden',cols:11,rows:7,layout:structuredClone(levels[1].solution),mode:'select' as const,reducedMotion:false};
 saveSession(storage,session);const before=storage.getItem(PROGRESS_KEY);
 savePrologue({seen:false,frame:3,active:true},storage);
 assert.deepEqual(loadPrologue(storage),{seen:false,frame:3,active:true});assert.equal(storage.getItem(PROGRESS_KEY),before);
 saveProgress(['gate'],storage);saveSession(storage,session);
 assert.equal(loadPrologue(storage).frame,3);assert.deepEqual(loadSession(storage,['gate']),session);assert.deepEqual(loadState(storage).completed,['gate']);
});
test('Повреждённый кадр и отказ хранилища безопасны',()=>{
 const storage=memory();for(const frame of [-1,6,1.5,'2']){storage.setItem(PROLOGUE_KEY,JSON.stringify({version:1,frame,seen:false,active:true}));assert.deepEqual(loadPrologue(storage),newPrologue());}
 storage.setItem(PROLOGUE_KEY,'{');assert.deepEqual(loadPrologue(storage),newPrologue());
 const denied={getItem(){throw Error('denied');},setItem(){throw Error('denied');}};
 assert.deepEqual(loadPrologue(denied),newPrologue());assert.equal(savePrologue(newPrologue(),denied),false);
});
test('Старая сессия или прогресс имеют приоритет над прологом',()=>{
 const intro={seen:false,frame:4,active:true};assert.equal(shouldStartPrologue(intro,false,false),true);
 assert.equal(shouldStartPrologue(intro,true,false),false);assert.equal(shouldStartPrologue(intro,false,true),false);
 assert.equal(shouldStartPrologue({...intro,seen:true},false,false),false);
});
