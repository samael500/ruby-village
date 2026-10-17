import {PaintedMotionClock,type PaintedSet} from '../scripts/character-paint-playback.ts';
import {sampleGroundRoute,type GroundPlan} from '../scripts/character-paint-route-planner.ts';
import type {FootContact,Surface} from './character-animation.ts';

/** One controllable clock drives authored steps and the actual native route.
 * Pause discards stale resume time; stops are entered on the planned contact. */
export class RutaJourney {
 private elapsed=0;
 private suspended=false;
 private completed=false;
 readonly clock:PaintedMotionClock;
 readonly plan:GroundPlan;
 constructor(plan:GroundPlan,set:PaintedSet){
  this.plan=plan;
  this.clock=new PaintedMotionClock(set);if(Math.abs(plan.halfStepDurationMs-this.clock.halfStepDurationMs)>1e-6)throw new RangeError('Route and frames must share authored timing');this.clock.setDirection(sampleGroundRoute(plan,0).direction);
  if(plan.durationMs)this.clock.start();
 }
 get position(){return sampleGroundRoute(this.plan,this.elapsed).position;}
 get direction(){return sampleGroundRoute(this.plan,this.elapsed).direction;}
 get frame(){return this.clock.frame;}
 get done(){return this.completed;}
 get elapsedMs(){return this.elapsed;}
 advance(deltaMs:number,options:{paused?:boolean;reducedMotion?:boolean;surface?:Surface}={}):FootContact[]{
  if(options.paused){this.suspended=true;this.clock.advance(0,{paused:true});return [];}
  if(this.suspended){this.suspended=false;this.clock.advance(0);return [];}
  if(!Number.isFinite(deltaMs)||deltaMs<0)return [];
  if(options.reducedMotion){this.elapsed=this.plan.durationMs;this.clock.advance(0,{reducedMotion:true});this.completed=true;return [];}
  if(this.completed){this.clock.advance(deltaMs,{surface:options.surface});return [];}
  const events:FootContact[]=[];
  let remaining=Math.min(deltaMs,this.plan.durationMs-this.elapsed);
  const half=this.clock.halfStepDurationMs,stopAt=this.plan.durationMs-half;
  while(remaining>1e-8){
   if(this.elapsed>=stopAt-1e-7)this.clock.requestStop();
   const boundary=this.elapsed<half-1e-7?half:this.elapsed<stopAt-1e-7?stopAt:this.plan.durationMs;
   const step=Math.min(remaining,boundary-this.elapsed);
   events.push(...this.clock.advance(step,{surface:options.surface}).contacts);
   this.elapsed+=step;remaining-=step;
   this.clock.setDirection(sampleGroundRoute(this.plan,this.elapsed).direction);
  }
  if(this.plan.durationMs-this.elapsed<=1e-7){this.elapsed=this.plan.durationMs;this.completed=true;}
  return events;
 }
}
