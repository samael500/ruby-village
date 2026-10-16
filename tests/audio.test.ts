import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createGameAudio,AUDIO_PREFERENCES_KEY} from '../src/audio.ts';
class Param {value=0;cancelScheduledValues(){}setTargetAtTime(value:number){this.value=value;}}
class Gain {gain=new Param();connect(){}disconnect(){}}
class Source {buffer:unknown;loop=false;onended:(()=>void)|null=null;connect(){}disconnect(){}start(){}stop(){this.onended?.();}}
class Context {static count=0;currentTime=0;state='suspended';destination={};constructor(){Context.count++;}createGain(){return new Gain();}createBufferSource(){return new Source();}async resume(){this.state='running';}async close(){this.state='closed';}async decodeAudioData(){return {duration:1};}}
const flush=async()=>{for(let i=0;i<12;i++)await Promise.resolve();};
test('gesture gate, persisted levels, one context, throttling, pause and disposal',async()=>{
 const original=globalThis.AudioContext,fetchOriginal=globalThis.fetch;
 Object.assign(globalThis,{AudioContext:Context,fetch:async()=>({ok:true,arrayBuffer:async()=>new ArrayBuffer(4),json:async()=>({cues:{village:{file:'village.ogg',gain:.5,loop:true}}})})});
 try{
  const storage={getItem:()=>JSON.stringify({muted:false,sfx:.2,music:.1}),setItem(key:string,value:string){assert.equal(key,AUDIO_PREFERENCES_KEY);assert.equal(JSON.parse(value).muted,true);}};
  const audio=createGameAudio('/ruby-village/',storage);assert.equal(audio.preferences.sfx,.2);assert.equal(audio.metrics.contextState,'not-created');
  await audio.play('tile-place');assert.equal(audio.metrics.played,0);
  audio.setScene('stream');audio.setMusic('village');assert.equal(Context.count,0);
  assert.equal(await audio.unlock(),true);await flush();assert.equal(Context.count,1);assert.equal(audio.metrics.activeVoices,2);
  await audio.unlock();await flush();assert.equal(audio.metrics.activeVoices,2);
  await audio.play('tile-place');const played=audio.metrics.played;await audio.play('tile-place');assert.equal(audio.metrics.played,played);
  audio.setPaused(true);assert.equal(audio.metrics.activeVoices,0);await audio.play('foot-stone');assert.equal(audio.metrics.played,played);
  audio.setPaused(false);await flush();assert.equal(audio.metrics.activeVoices,2);
  audio.setPreferences({muted:true,music:2});assert.equal(audio.preferences.music,1);await audio.play('ui-click');assert.equal(audio.metrics.played,played+2);
  audio.dispose();assert.equal(audio.metrics.activeVoices,0);assert.equal(await audio.unlock(),false);
 }finally{globalThis.AudioContext=original;globalThis.fetch=fetchOriginal;}
});
test('storage, fetch and device failure never reject gameplay operations',async()=>{
 const original=globalThis.AudioContext,fetchOriginal=globalThis.fetch;
 Object.assign(globalThis,{AudioContext:Context,fetch:async()=>{throw Error('offline');}});
 try{
  const audio=createGameAudio('/',{getItem(){throw Error('denied');},setItem(){throw Error('full');}});
  audio.setPreferences({sfx:NaN});assert.equal(audio.preferences.sfx,.65);audio.setScene('gate');audio.setMusic('village');await audio.unlock();await flush();await audio.play('stone');assert.ok(audio.metrics.loadErrors>=3);audio.dispose();
  Object.assign(globalThis,{AudioContext:class{constructor(){throw Error('device');}}});
  const unavailable=createGameAudio('/');assert.equal(await unavailable.unlock(),false);await unavailable.play('victory');unavailable.dispose();
 }finally{globalThis.AudioContext=original;globalThis.fetch=fetchOriginal;}
});
test('in-flight loaded effects are discarded on pause instead of deferred',async()=>{
 const original=globalThis.AudioContext,fetchOriginal=globalThis.fetch;let resolve!:()=>void;
 Object.assign(globalThis,{AudioContext:Context,fetch:async()=>{await new Promise<void>(r=>{resolve=r;});return {ok:true,arrayBuffer:async()=>new ArrayBuffer(4)};}});
 try{const audio=createGameAudio('/');await audio.unlock();const pending=audio.play('foot-earth');audio.setPaused(true);resolve();await pending;assert.equal(audio.metrics.played,0);audio.dispose();}
 finally{globalThis.AudioContext=original;globalThis.fetch=fetchOriginal;}
});
