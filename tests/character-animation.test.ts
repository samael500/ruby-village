import { test } from 'node:test';
import assert from 'node:assert/strict';
import { CharacterPlayer, positionAlongPath, projectedDirection } from '../src/character-animation.ts';
const frame = (contact?: 'left' | 'right') => ({ sourceRect: [0,0,64,96] as [number,number,number,number], frameSize: [64,96] as [number,number], footAnchor: [32,92] as [number,number], durationMs: 100, contact });
test('clock is frame-rate independent and emits every crossed contact', () => {
 const a = new CharacterPlayer({frames:[frame('left'),frame('right')],loop:true});
 const b = new CharacterPlayer({frames:[frame('left'),frame('right')],loop:true});
 const events = a.advance(450,{surface:'wood'});
 let count = 0; for(let i=0;i<9;i++) count += b.advance(50).length;
 assert.equal(events.length,count); assert.deepEqual(a.frame,b.frame); assert.ok(events.every(e=>e.surface==='wood'));
});
test('pause and first resume discard hidden time; reduced motion has no footsteps',()=>{
 const p = new CharacterPlayer({frames:[frame(),frame('right')],loop:true});
 p.advance(50); p.advance(10000,{paused:true}); assert.deepEqual(p.advance(10000),[]);
 assert.equal(p.advance(50).length,1); assert.deepEqual(p.advance(1000,{reducedMotion:true}),[]);
});
test('projected directions and boundary hysteresis',()=>{
 assert.equal(projectedDirection({x:0,y:0},{x:1,y:1}),'se');
 assert.equal(projectedDirection({x:0,y:0},{x:1,y:0.6},'e'),'e');
 assert.equal(projectedDirection({x:0,y:0},{x:0,y:0},'nw'),'nw');
});
test('route follows segment lengths, handles duplicate points and clamps end',()=>{
 const route=[{x:0,y:0},{x:0,y:0},{x:3,y:0},{x:3,y:4}];
 assert.deepEqual(positionAlongPath(route,5),{x:3,y:2}); assert.deepEqual(positionAlongPath(route,100),{x:3,y:4});
});

import { CharacterRoute } from '../src/character-animation.ts';
test('route completion is frame-rate independent and fires once',()=>{
 let wins=0; const a=new CharacterRoute([{x:0,y:0},{x:30,y:0},{x:30,y:40}],70,()=>wins++);
 const b=new CharacterRoute([{x:0,y:0},{x:30,y:0},{x:30,y:40}],70);
 for(let i=0;i<30;i++)a.advance(1000/30);for(let i=0;i<144;i++)b.advance(1000/144);
 // The exact duration must finish even when floating-point accumulation leaves
 // a tiny remainder; an external player must not need another movement tick.
 assert.equal(a.done,true);assert.equal(b.done,true);
 assert.deepEqual(a.position,b.position);assert.equal(wins,1);a.advance(5000);assert.equal(wins,1);
});
test('route pause discards resumed time and reduced motion completes without lost result',()=>{
 let wins=0;const p=new CharacterRoute([{x:0,y:0},{x:100,y:0}],10,()=>wins++);
 p.advance(1000);p.advance(100000,{paused:true});assert.deepEqual(p.advance(100000),{x:10,y:0});
 p.advance(0,{reducedMotion:true});assert.equal(p.done,true);assert.equal(wins,1);assert.deepEqual(p.position,{x:100,y:0});
});
