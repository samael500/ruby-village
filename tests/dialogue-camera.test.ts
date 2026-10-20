import {test} from 'node:test';
import assert from 'node:assert/strict';
import {fitScene} from '../src/scene-camera.ts';
import {frameDialogueScene} from '../src/dialogue-camera.ts';

test('landscape dialogue keeps actors and gate above the panel using one camera',()=>{
 const base=fitScene('gate',844,210);
 const focus=[{top:563,bottom:707},{top:719,bottom:876}];
 const framed=frameDialogueScene(base,{width:844,height:210,fullHeight:390},focus);
 for(const bounds of focus){
  assert.ok(framed.offset.y+bounds.top*framed.fit>=63.99);
  assert.ok(framed.offset.y+bounds.bottom*framed.fit<=198.01);
 }
 assert.deepEqual(framed.projection,base.projection);
 assert.equal(framed.radius,base.metadata.camera.radius*framed.fit);
 assert.equal(framed.translation.y,framed.offset.y+base.metadata.camera.origin.y*framed.fit);
 const canvas=base.metadata.canvas,rect=base.metadata.originalRect;
 assert.ok(framed.offset.x-rect.x*framed.fit<=0);
 assert.ok(framed.offset.x+(canvas.width-rect.x)*framed.fit>=844);
 assert.ok(framed.offset.y-rect.y*framed.fit<=0);
 assert.ok(framed.offset.y+(canvas.height-rect.y)*framed.fit>=210);
});

test('empty narrative focus preserves the original camera',()=>{
 const base=fitScene('well',1280,720);
 assert.equal(frameDialogueScene(base,{width:1280,height:500,fullHeight:720},[]),base);
});
