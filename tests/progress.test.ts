import {test} from 'node:test';
import assert from 'node:assert/strict';
import {levels} from '../src/levels.ts';
import {PROGRESS_KEY,parseState,parseProgress,loadProgress,saveProgress,available,completeLevel} from '../src/progress.ts';
test('Миграция трёх дорог сохраняет мельницу и не пропускает новые задания',()=>{
 const state=parseState(JSON.stringify({version:1,completed:['gate','garden','mill']}));
 assert.deepEqual(state.completed,['gate','garden','mill']);assert.deepEqual(state.introSeen,state.completed);
 assert.ok(available('well',state.completed));assert.ok(available('mill',state.completed));
 for(const id of ['bakery','stream','post','forest'])assert.equal(available(id,state.completed),false);
 const roundtrip=parseState(JSON.stringify({version:2,...state}));assert.deepEqual(roundtrip,state);
});
test('Прогресс: повреждения, порядок, повторы, песочница и сброс',()=>{
 for(const raw of [null,'{','null','[]','{"version":99,"completed":["gate"]}','{"version":1,"completed":"gate"}'])assert.deepEqual(parseProgress(raw),[]);
 assert.deepEqual(parseProgress('{"version":1,"completed":["mill","gate","unknown"]}'),['gate']);
 assert.deepEqual(parseState('{"version":2,"completed":["gate","unknown","gate"],"introSeen":12}'),{completed:['gate'],introSeen:['gate']});
 assert.ok(available('gate',[]));assert.equal(available('garden',[]),false);
 let done:string[]=[];for(const l of levels)done=completeLevel(l.id,done);
 assert.deepEqual(done,levels.map(l=>l.id));assert.deepEqual(completeLevel('gate',done),done);
 assert.deepEqual(completeLevel('sandbox',done),done);assert.deepEqual(completeLevel('mill',[]),[]);
 const memory=new Map<string,string>();const storage={getItem:(k:string)=>memory.get(k)??null,setItem:(k:string,v:string)=>{memory.set(k,v);}};
 assert.ok(saveProgress(done,storage));assert.deepEqual(loadProgress(storage),done);assert.ok(memory.has(PROGRESS_KEY));
 saveProgress([],storage,[]);assert.deepEqual(loadProgress(storage),[]);
 const denied={getItem:()=>{throw Error('denied');},setItem:()=>{throw Error('denied');}};
 assert.deepEqual(loadProgress(denied),[]);assert.equal(saveProgress(done,denied),false);assert.equal(saveProgress(done),false);
});
