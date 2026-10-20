import {test} from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';
import {planGroundRoute,pointOnGoal,sampleGroundRoute,type GroundPlan} from './character-paint-route-planner.ts';
const manifest=JSON.parse(readFileSync(new URL('../art/characters-walk-v1/export-v2/manifest.json',import.meta.url),'utf8')),poses=JSON.parse(readFileSync(new URL('../art/characters-walk-v1/export-v2/evaluated-joints.json',import.meta.url),'utf8'));
const directions=manifest.cameraVariants.base.directions;
function ready(p:ReturnType<typeof planGroundRoute>):GroundPlan {assert.equal(p.status,'ready',JSON.stringify(p));return p as GroundPlan;}
test('arbitrary centers stop physically inside native goal polygon, without forcing exact center',()=>{
 for(const variant of Object.values(manifest.cameraVariants) as any[])for(const [heading,d] of Object.entries(variant.directions) as [string,any][])for(const length of [81.13,121.244,177.7,410.19,711.36]){
  const a=d.screenAngleRadians,center={x:Math.cos(a)*length,y:Math.sin(a)*length},polygon=Array.from({length:6},(_,i)=>({x:center.x+70*Math.cos(i*Math.PI/3),y:center.y+70*.65*Math.sin(i*Math.PI/3)}));const plan=ready(planGroundRoute([{x:0,y:0},center],{directions:variant.directions,goalPolygon:polygon}));assert.ok(pointOnGoal(plan.endpoint,center,{goalPolygon:polygon}));assert.ok(plan.residualPixels<=d.projectedStridePixels/4+1e-7);assert.deepEqual(plan.points.at(-1),plan.endpoint);assert.equal(sampleGroundRoute(plan,plan.durationMs).complete,true);assert.deepEqual(sampleGroundRoute(plan,plan.durationMs).position,plan.endpoint);
 }
});
test('exact center or too narrow target reports a real retarget requirement; no hidden slide',()=>{
 const path=[{x:0,y:0},{x:123.456,y:0}];assert.equal(planGroundRoute(path,{directions,goalRadius:70,exactCenter:true}).status,'requires-retarget');assert.equal(planGroundRoute(path,{directions,goalRadius:.1}).status,'requires-retarget');assert.equal(planGroundRoute([{x:0,y:0},{x:50,y:10}],{directions,goalRadius:70}).status,'requires-retarget');
});
test('soft start/stop, exact grounded endpoint and distance are independent of 30/60/144fps',()=>{
 const plan=ready(planGroundRoute([{x:0,y:0},{x:412.34,y:0}],{directions,goalRadius:70}));assert.equal(sampleGroundRoute(plan,0).velocityWorld,0);assert.equal(sampleGroundRoute(plan,400).velocityWorld,.9);assert.ok(sampleGroundRoute(plan,plan.durationMs-.001).velocityWorld<.00001);for(const fps of [30,60,144]){let last=0;for(let t=0;t<plan.durationMs;t+=1000/fps){const s=sampleGroundRoute(plan,t);assert.ok(s.worldDistance>=last&&s.worldDistance<=plan.worldLength+1e-9);last=s.worldDistance;}const done=sampleGroundRoute(plan,plan.durationMs);assert.deepEqual(done.position,plan.endpoint);assert.equal(done.velocityWorld,0);assert.equal(done.complete,true);}assert.notEqual(plan.durationMs,3500);
});
test('source ankle planting stays below .01 native pixel through planned start/walk/stop for all actual camera views',()=>{
 for(const [variant,group] of Object.entries(manifest.cameraVariants) as [string,any][])for(const [heading,d] of Object.entries(group.directions) as [string,any][]){const angle=d.screenAngleRadians,plan=ready(planGroundRoute([{x:0,y:0},{x:Math.cos(angle)*240.123,y:Math.sin(angle)*240.123}],{directions:group.directions,goalRadius:70})),view=variant==='base'?heading:variant+'-'+heading;
  const scenarios=[{base:201,n:9,side:'R',time:(i:number)=>i*50},{base:1,n:8,side:'L',time:(i:number)=>400+i*50},{base:9,n:8,side:'R',time:(i:number)=>800+i*50},{base:plan.stopFoot==='left'?301:401,n:9,side:plan.stopFoot==='left'?'L':'R',time:(i:number)=>plan.durationMs-400+i*50}];
  for(const scenario of scenarios){const samples=Array.from({length:scenario.n},(_,i)=>{const actor=sampleGroundRoute(plan,scenario.time(i)).position,ankle=poses[view][String(scenario.base+i)]['foot.'+scenario.side][0];return {x:actor.x+ankle[0]*136/210,y:actor.y+ankle[1]*136/210};});const max=Math.max(...samples.map(p=>Math.hypot(p.x-samples[0].x,p.y-samples[0].y)));assert.ok(max<.01,`${view} ${scenario.base}: source foot drift ${max}`);}
 }
});
test('multi-segment paths retain corners, source phase and a grounded final target; no corner shortcut',()=>{
 const se=directions.se,a=se.screenAngleRadians,p0={x:0,y:0},p1={x:121.244,y:0},p2={x:p1.x+Math.cos(a)*91.3,y:Math.sin(a)*91.3},p3={x:p2.x+121.244,y:p2.y};const plan=ready(planGroundRoute([p0,p1,p2,p3],{directions,goalRadius:60}));assert.deepEqual(plan.points.slice(0,3),[p0,p1,p2]);for(const boundary of plan.segments.slice(1)){const time=400+(boundary.startWorld-.18)/.9*1000,before=sampleGroundRoute(plan,time-.001),after=sampleGroundRoute(plan,time+.001);assert.ok(Math.hypot(before.position.x-after.position.x,before.position.y-after.position.y)<.001);assert.ok(Math.abs(before.phaseMs-after.phaseMs)<.01);}
 assert.ok(pointOnGoal(plan.endpoint,p3,{goalRadius:60}));assert.deepEqual(sampleGroundRoute(plan,plan.durationMs).position,plan.endpoint);
});
test('already grounded and boundary endpoints are valid without fabricated walking',()=>{const plan=ready(planGroundRoute([{x:2,y:3}],{directions,goalRadius:70}));assert.equal(plan.durationMs,0);assert.equal(sampleGroundRoute(plan,0).state,'idle');assert.equal(pointOnGoal({x:1,y:0},{x:0,y:0},{goalPolygon:[{x:0,y:0},{x:1,y:0},{x:0,y:1}]}),true);});
