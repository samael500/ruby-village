import {test} from 'node:test';
import assert from 'node:assert/strict';
import {loadSession,saveSession,type Session} from '../src/session.ts';
import {saveProgress,PROGRESS_KEY,type StorageLike} from '../src/progress.ts';
import {levels} from '../src/levels.ts';
import legacy from './fixtures/chapter-1-before-layouts.json' with {type:'json'};
import {validateLayout,winningPath} from '../src/game.ts';
const store=()=>{const values=new Map<string,string>();return {getItem:(k:string)=>values.get(k)??null,setItem:(k:string,v:string)=>{values.set(k,v);}};};
test('Session roundtrip preserves progress identity, layout, mode and motion setting',()=>{
 const storage=store();saveProgress(['gate'],storage);
 const s:Session={levelId:'garden',cols:11,rows:7,layout:structuredClone(levels[1].solution),mode:'drag',reducedMotion:true};
 assert.equal(saveSession(storage,s),true);assert.deepEqual(loadSession(storage,['gate']),s);
 assert.deepEqual(JSON.parse(storage.getItem(PROGRESS_KEY)!).completed,['gate']);
});
test('Session rejects locked level, invalid shape cells, overlap and broken storage',()=>{
 const storage=store();saveProgress([],storage);
 saveSession(storage,{levelId:'garden',cols:11,rows:7,layout:{},mode:'select',reducedMotion:false});assert.equal(loadSession(storage,[]),null);
 const layout={...levels[0].solution,'gate-1':{anchor:{q:100,r:2},turns:0},'gate-2':levels[0].solution['gate-3']};
 saveSession(storage,{levelId:'gate',cols:7,rows:5,layout,mode:'select',reducedMotion:false});
 const loaded=loadSession(storage,[])!;assert.equal(loaded.layout['gate-1'],undefined);assert.equal(loaded.layout['gate-3'],undefined);
 assert.equal(loadSession({getItem:()=>{throw Error('denied');},setItem:()=>{}},[]),null);
 assert.equal(saveSession(undefined,null),false);
 storage.setItem(PROGRESS_KEY,'{');assert.equal(loadSession(storage,[]),null);
});
test('Сохранения прежней разметки сохраняют дороги, настройки и завершённые уровни',()=>{
 const completed=levels.map(l=>l.id);
 for(const old of legacy.levels){
  const storage=store();saveProgress(completed,storage);
  saveSession(storage,{levelId:old.id,cols:11,rows:7,layout:old.solution,mode:'drag',reducedMotion:true});
  const current=levels.find(l=>l.id===old.id)!,loaded=loadSession(storage,completed)!;
  assert.deepEqual(loaded.layout,old.solution);assert.ok(validateLayout(current,loaded.layout));
  assert.equal(loaded.mode,'drag');assert.equal(loaded.reducedMotion,true);
  assert.deepEqual(JSON.parse(storage.getItem(PROGRESS_KEY)!).completed,completed);
  if(['gate','garden','well','bakery','post','forest'].includes(old.id))assert.equal(winningPath(current,loaded.layout),null);
 }
});
test('Из старого сохранения удаляется только плита, попавшая на перенесённое русло',()=>{
 for(const [id,piece,anchor] of [['stream','stream-b',{q:6,r:2}],['mill','mill-b',{q:2,r:4}]] as const){
  const old=legacy.levels.find(l=>l.id===id)!,storage=store(),completed=levels.map(l=>l.id);
  saveProgress(completed,storage);
  saveSession(storage,{levelId:id,cols:11,rows:7,layout:{...old.solution,[piece]:{anchor,turns:0}},mode:'select',reducedMotion:false});
  const loaded=loadSession(storage,completed)!;
  assert.deepEqual(loaded.layout,old.solution);assert.equal(loaded.layout[piece],undefined);
  assert.deepEqual(JSON.parse(storage.getItem(PROGRESS_KEY)!).completed,completed);
 }
});
