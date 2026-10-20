import {CharacterPlayer,type Direction,type CharacterFrame,type Surface,type FootContact} from '../src/character-animation.ts';
export type MotionState='idle'|'start'|'walk'|'stop-L'|'stop-R';
export interface PaintedFrame extends CharacterFrame {file:string;blink?:boolean;motionFraction?:number}
export interface PaintedClip {loop:boolean;frames:PaintedFrame[]}
export interface PaintedSet {frameSize:[number,number];footAnchor:[number,number];nativeHeightPx:number;cycleDurationMs?:number;directions:Record<Direction,{projectedStridePixels:number;clips:Record<MotionState,PaintedClip>}>}
function normalizedPhase(value:number,cycle:number){const half=cycle/2,p=(value%cycle+cycle)%cycle;return Math.abs(p-half)<.00001?half:Math.min(p,cycle-p)<.00001?0:p;}
export function selectPaintedScene<T extends PaintedSet & {sceneCameraVariant?:Record<string,string>;cameraVariants?:Record<string,{directions:PaintedSet['directions']}>}>(set:T,scene:string):PaintedSet {const key=set.sceneCameraVariant?.[scene];return {...set,directions:key&&set.cameraVariants?.[key]?set.cameraVariants[key].directions:set.directions};}
export function clipFrame(clip:PaintedClip,time:number):PaintedFrame {
 const total=clip.frames.reduce((sum,frame)=>sum+frame.durationMs,0);let remaining=clip.loop?Math.max(0,time)%total:Math.max(0,Math.min(time,total-.00001));
 for(const frame of clip.frames){if(remaining<frame.durationMs)return frame;remaining-=frame.durationMs;}return clip.frames[clip.frames.length-1];
}
/** Standalone integration adapter: one shared walk phase, semantic contacts from CharacterPlayer.
 * Direction changes never recreate the walk player or mirror a sprite. World route stays with #46.
 */
export class PaintedMotionClock {
 readonly set:PaintedSet;readonly cycleDurationMs:number;get halfStepDurationMs(){return this.cycleDurationMs/2;}private walk:CharacterPlayer;private transient:CharacterPlayer|null=null;
 private elapsed=0;private phase=0;private idleTime=0;private mode:MotionState='idle';private heading:Direction='e';private stopWanted=false;private suspended=false;
 constructor(set:PaintedSet){this.set=set;const duration=set.directions.e.clips.walk.frames.reduce((sum,frame)=>sum+frame.durationMs,0);this.cycleDurationMs=set.cycleDurationMs??duration;if(!Number.isFinite(this.cycleDurationMs)||this.cycleDurationMs<=0||Math.abs(duration-this.cycleDurationMs)>1e-6)throw new RangeError('Walk frame timing must match authored cycle duration');this.walk=new CharacterPlayer(set.directions.e.clips.walk);}
 get state(){return this.mode;}get direction(){return this.heading;}get phaseMs(){return this.phase;}get stateTimeMs(){return this.mode==='idle'?this.idleTime:this.elapsed;}
 setDirection(direction:Direction){this.heading=direction;}
 start(){if(this.mode!=='idle')return;this.mode='start';this.elapsed=0;this.stopWanted=false;this.transient=new CharacterPlayer(this.set.directions.e.clips.start);}
 private beginStop(){this.mode=this.phase<this.halfStepDurationMs?'stop-L':'stop-R';this.elapsed=0;this.transient=new CharacterPlayer(this.set.directions.e.clips[this.mode]);this.stopWanted=false;}
 requestStop(){this.stopWanted=true;if(this.mode==='walk'&&this.phase%this.halfStepDurationMs===0)this.beginStop();}
 get frame(){return clipFrame(this.set.directions[this.heading].clips[this.mode],this.mode==='walk'?this.phase:this.mode==='idle'?this.idleTime:this.elapsed);}
 advance(deltaMs:number,options:{paused?:boolean;reducedMotion?:boolean;surface?:Surface}={}) {
  const contacts:FootContact[]=[];let worldDistance=0;const beforeDirection=this.heading;
  if(options.paused){this.suspended=true;return {worldDistance,travelPixels:0,contacts,advancedMs:0};}
  if(this.suspended){this.suspended=false;return {worldDistance,travelPixels:0,contacts,advancedMs:0};}
  if(!Number.isFinite(deltaMs)||deltaMs<0)return {worldDistance,travelPixels:0,contacts,advancedMs:0};
  if(options.reducedMotion){this.mode='idle';this.idleTime=0;this.phase=0;this.elapsed=0;this.stopWanted=false;this.transient=null;return {worldDistance,travelPixels:0,contacts,advancedMs:deltaMs};}
  let remaining=deltaMs;
  while(remaining>0){
   if(this.mode==='idle'){this.idleTime=(this.idleTime+remaining)%3200;remaining=0;break;}
   if(this.mode==='walk'){
    if(this.stopWanted){
     const toContact=(this.halfStepDurationMs-this.phase%this.halfStepDurationMs)%this.halfStepDurationMs;
     if(toContact<.00001){this.beginStop();continue;}
     const step=Math.min(remaining,toContact);contacts.push(...this.walk.advance(step,{surface:options.surface}));this.phase=normalizedPhase(this.phase+step,this.cycleDurationMs);worldDistance+=.72*step/this.cycleDurationMs;remaining-=step;if(Math.abs(step-toContact)<.00001)this.beginStop();continue;
    }
    contacts.push(...this.walk.advance(remaining,{surface:options.surface}));worldDistance+=.72*remaining/this.cycleDurationMs;this.phase=normalizedPhase(this.phase+remaining,this.cycleDurationMs);remaining=0;break;
   }
   const state=this.mode,step=Math.min(remaining,this.halfStepDurationMs-this.elapsed),old=this.elapsed/this.halfStepDurationMs,next=(this.elapsed+step)/this.halfStepDurationMs;
   const curve=(t:number)=>state==='start'?t*t:2*t-t*t;
   worldDistance+=.18*(curve(next)-curve(old));contacts.push(...(this.transient?.advance(step,{surface:options.surface})??[]));this.elapsed+=step;remaining-=step;
   if(this.elapsed>=this.halfStepDurationMs-.00001){this.elapsed=0;this.transient=null;if(state==='start'){this.mode='walk';this.phase=0;this.walk=new CharacterPlayer(this.set.directions.e.clips.walk);}else{this.mode='idle';this.idleTime=0;}}
  }
  return {worldDistance,travelPixels:worldDistance/.72*this.set.directions[beforeDirection].projectedStridePixels,contacts,advancedMs:deltaMs};
 }
}
