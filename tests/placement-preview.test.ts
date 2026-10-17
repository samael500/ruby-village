import {test}from'node:test';import assert from'node:assert/strict';
import {releasePreview,confirmedPreview,type PlacementPreview}from'../src/placement-preview.ts';
import {productionLevels as levels}from'../src/production-chapter.ts';
import {validPlacement,validateLayout,winningPath}from'../src/game.ts';
import {saveProgress,PROGRESS_KEY}from'../src/progress.ts';import{saveSession}from'../src/session.ts';
const preview=(selected:string,anchor:{q:number;r:number}|null,turns=0,pinned=false):PlacementPreview=>({selected,anchor,turns,pinned});
test('invalid release preserves instance, position and rotation without confirming or changing progress/layout',()=>{
 const level=levels[1],piece=level.pieces.find(p=>p.shape.length>1)!;const layout={};const before=preview(piece.id,null);let state=releasePreview(preview(piece.id,{q:-1,r:0},2),before,{q:-1,r:0},false,true);
 assert.deepEqual(state,preview(piece.id,{q:-1,r:0},2,true));for(let i=0;i<6;i++){state={...state,turns:(state.turns+1)%6};assert.equal(confirmedPreview(level,layout,state),null);}
 assert.deepEqual(layout,{});assert.equal(winningPath(level,layout),null);assert.equal(validateLayout(level,layout),true);
 const target=level.solution[piece.id];const valid=confirmedPreview(level,layout,{...state,anchor:target.anchor,turns:target.turns})!;assert.deepEqual(Object.keys(valid),[piece.id]);assert.deepEqual(layout,{});
});
test('moving a confirmed piece keeps its old placement serializable; cancel restores the gesture snapshot',()=>{
 const level=levels[1],id=level.pieces[0].id,layout={[id]:structuredClone(level.solution[id])};const original=structuredClone(layout);const before=preview(id,layout[id].anchor,layout[id].turns,true);
 const invalid=releasePreview(preview(id,{q:100,r:100},3),before,{q:100,r:100},false,true);assert.equal(confirmedPreview(level,layout,invalid),null);assert.deepEqual(layout,original);
 assert.deepEqual(releasePreview(invalid,before,null,true,true),before);
 const values=new Map<string,string>();const store={getItem:(k:string)=>values.get(k)??null,setItem:(k:string,v:string)=>{values.set(k,v)}};saveProgress([],store);saveSession(store,{levelId:level.id,cols:level.cols,rows:level.rows,layout,mode:'drag',reducedMotion:false});assert.deepEqual(JSON.parse(store.getItem(PROGRESS_KEY)!).session.layout,original);
});
test('bridge stays provisional on land, blocks overlap/water errors and confirms only its real valid orientation',()=>{
 const level=levels.find(l=>l.id==='stream')!,piece=level.pieces.find(p=>p.kind==='bridge')!,layout={};let state=preview(piece.id,{q:0,r:0},0,true);
 for(let turns=0;turns<6;turns++)assert.equal(confirmedPreview(level,layout,{...state,turns}),null);
 const good=level.solution[piece.id];assert.ok(validPlacement(level,piece.id,good,layout));const placed=confirmedPreview(level,layout,{...state,...good})!;assert.ok(validateLayout(level,placed));assert.equal(Object.keys(placed).length,1);
});
test('pointercancel/outside release and independent snapshots never lose a pending preview',()=>{
 const before=preview('piece',{q:2,r:3},4,true),current=preview('piece',{q:-2,r:1},1,true);const cancelled=releasePreview(current,before,null,true,true);assert.deepEqual(cancelled,before);cancelled.anchor!.q=99;assert.equal(before.anchor!.q,2);
 assert.deepEqual(releasePreview(current,before,null,false,true),current);assert.deepEqual(releasePreview(current,before,{q:0,r:0},false,false),before);
});
