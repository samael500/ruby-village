import {test} from 'node:test';
import assert from 'node:assert/strict';
import {loadSession,saveSession,type Session} from '../src/session.ts';
import {saveProgress,PROGRESS_KEY,type StorageLike} from '../src/progress.ts';
import {levels} from '../src/levels.ts';
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
