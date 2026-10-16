import {test} from 'node:test';
import assert from 'node:assert/strict';
import {loadSession,recoverSession,saveSession,CHAPTER_LAYOUT_VERSION,type Session} from '../src/session.ts';
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

test('Legacy migration is repeatable, persisted once, preserves unknown chapter state',()=>{
 const storage=store(),old=legacy.levels.find(l=>l.id==='stream')!;
 const raw={version:2,completed:['gate','garden','well','bakery'],introSeen:['gate'],letter:{read:true},prologue:{frame:4},preferences:{mode:'drag',reducedMotion:true},session:{levelId:'stream',cols:11,rows:7,layout:{...old.solution,'stream-b':{anchor:{q:6,r:2},turns:0}},mode:'drag',reducedMotion:true}};
 storage.setItem(PROGRESS_KEY,JSON.stringify(raw));
 const first=recoverSession(storage,raw.completed);
 assert.equal(first.migrated,true);assert.deepEqual(first.discarded,['stream-b']);assert.ok(first.notice);
 assert.deepEqual(recoverSession(storage,raw.completed),first);
 assert.equal(saveSession(storage,first.session!),true);
 const next=recoverSession(storage,raw.completed);assert.equal(next.migrated,false);assert.deepEqual(next.discarded,[]);assert.deepEqual(next.session,first.session);
 saveProgress([...raw.completed,'stream'],storage);
 const saved=JSON.parse(storage.getItem(PROGRESS_KEY)!);
 assert.equal(saved.layoutVersion,CHAPTER_LAYOUT_VERSION);assert.deepEqual(saved.letter,raw.letter);assert.deepEqual(saved.prologue,raw.prologue);assert.deepEqual(saved.preferences,raw.preferences);assert.deepEqual(saved.session,next.session);
});
test('Unrecoverable session reports reset without erasing progress, and storage failure is explicit',()=>{
 const storage=store(),raw={version:2,completed:levels.map(l=>l.id),session:{levelId:'gate',layout:[]}};
 storage.setItem(PROGRESS_KEY,JSON.stringify(raw));
 const recovery=recoverSession(storage,raw.completed);assert.equal(recovery.session,null);assert.ok(recovery.notice);assert.deepEqual(JSON.parse(storage.getItem(PROGRESS_KEY)!).completed,raw.completed);
 assert.ok(recoverSession({getItem:()=>{throw Error('denied');},setItem:()=>{}},[]).notice);
 assert.equal(saveSession({getItem:()=>JSON.stringify(raw),setItem:()=>{throw Error('quota');}},null),false);
});

test('Old completed courtyard stays complete and replay has exactly one eighth stone',()=>{
 const storage=store(),old=legacy.levels.find(l=>l.id==='gate')!;
 storage.setItem(PROGRESS_KEY,JSON.stringify({version:2,completed:['gate'],introSeen:['gate'],session:{levelId:'gate',cols:11,rows:7,layout:old.solution}}));
 const first=recoverSession(storage,['gate']);assert.equal(Object.keys(first.session!.layout).length,7);
 assert.equal(levels[0].pieces.filter(p=>p.id==='gate-8').length,1);
 assert.equal(first.session!.layout['gate-8'],undefined);
 saveSession(storage,first.session);assert.deepEqual(JSON.parse(storage.getItem(PROGRESS_KEY)!).completed,['gate']);
 assert.deepEqual(recoverSession(storage,['gate']).session,first.session);
 storage.setItem(PROGRESS_KEY,JSON.stringify({version:2,layoutVersion:999,completed:['gate'],session:first.session}));
 const future=recoverSession(storage,['gate']);assert.equal(future.session,null);assert.ok(future.notice);
});
