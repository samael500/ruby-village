import type {Direction,Point} from '../src/character-animation.ts';
export interface GroundDirection {screenAngleRadians:number;projectedStridePixels:number}
export interface GoalOptions {directions:Record<Direction,GroundDirection>;goalPolygon?:readonly Point[];goalRadius?:number;exactCenter?:boolean;maxResidualPixels?:number}
interface Segment {a:Point;b:Point;direction:Direction;startWorld:number;worldLength:number;pixelsPerWorld:number}
export interface GroundPlan {status:'ready';points:Point[];segments:Segment[];endpoint:Point;center:Point;halfSteps:number;worldLength:number;nominalWorldLength:number;durationMs:number;residualPixels:number;stopFoot:'left'|'right';directions:GoalOptions['directions']}
export interface RetargetPlan {status:'requires-retarget';reason:string;center:Point;nearestEndpoint?:Point;residualPixels?:number}
const HALF=.36,HALF_MS=400,EPS=1e-8;
const distance=(a:Point,b:Point)=>Math.hypot(b.x-a.x,b.y-a.y);
const finite=(p:Point)=>Number.isFinite(p.x)&&Number.isFinite(p.y);
/** Boundary is ground too. Polygon comes from the actual scene geometry, not sprite bounds. */
export function pointOnGoal(point:Point,center:Point,options:Pick<GoalOptions,'goalPolygon'|'goalRadius'>):boolean {
 const polygon=options.goalPolygon;
 if(polygon){if(polygon.length<3||polygon.some(p=>!finite(p)))throw new RangeError('A goal needs a finite ground polygon');let inside=false;
  for(let i=0,j=polygon.length-1;i<polygon.length;j=i++) {const a=polygon[j],b=polygon[i],length=distance(a,b),cross=(point.x-a.x)*(b.y-a.y)-(point.y-a.y)*(b.x-a.x);if(length>0&&Math.abs(cross)<=EPS*length&&(point.x-a.x)*(point.x-b.x)+(point.y-a.y)*(point.y-b.y)<=EPS)return true;if((a.y>point.y)!==(b.y>point.y)&&point.x<(b.x-a.x)*(point.y-a.y)/(b.y-a.y)+a.x)inside=!inside;}return inside;
 }
 if(!Number.isFinite(options.goalRadius)||options.goalRadius!<=0)throw new RangeError('Pass actual goalPolygon or positive goalRadius');return distance(point,center)<=options.goalRadius!+EPS;
}
function routePoint(segments:readonly Segment[],world:number):Point {
 const segment=segments.find(s=>world<=s.startWorld+s.worldLength+EPS)??segments.at(-1)!;const along=(world-segment.startWorld)*segment.pixelsPerWorld,length=distance(segment.a,segment.b);return {x:segment.a.x+(segment.b.x-segment.a.x)*along/length,y:segment.a.y+(segment.b.y-segment.a.y)*along/length};
}
/** Keep the authored physical half steps. Stop on target ground, with no final slide or speed multiplier.
 * Distances use rig-world units inferred from EACH measured camera stride, not puzzle-grid units.
 */
export function planGroundRoute(path:readonly Point[],options:GoalOptions):GroundPlan|RetargetPlan {
 if(!path.length||path.some(p=>!finite(p)))throw new RangeError('A route needs finite points');const points=path.filter((p,i)=>!i||distance(p,path[i-1])>EPS).map(p=>({...p})),center={...path.at(-1)!};pointOnGoal(center,center,options);const segments:Segment[]=[];let total=0;
 for(let i=1;i<points.length;i++) {const a=points[i-1],b=points[i],angle=Math.atan2(b.y-a.y,b.x-a.x);const choices=Object.entries(options.directions).map(([direction,d])=>({direction:direction as Direction,spec:d,error:Math.abs(Math.atan2(Math.sin(angle-d.screenAngleRadians),Math.cos(angle-d.screenAngleRadians)))})).sort((a,b)=>a.error-b.error);const chosen=choices[0];
  if(!chosen||!Number.isFinite(chosen.spec.projectedStridePixels)||chosen.spec.projectedStridePixels<=0)throw new RangeError('A route needs positive measured stride');if(chosen.error>.025)return {status:'requires-retarget',reason:'segment-direction-is-not-calibrated',center};const pixelsPerWorld=chosen.spec.projectedStridePixels/.72,worldLength=distance(a,b)/pixelsPerWorld;segments.push({a,b,direction:chosen.direction,startWorld:total,worldLength,pixelsPerWorld});total+=worldLength;
 }
 if(!segments.length)return pointOnGoal(points[0],center,options)?{status:'ready',points,segments,endpoint:points[0],center,halfSteps:0,worldLength:0,nominalWorldLength:0,durationMs:0,residualPixels:0,stopFoot:'left',directions:options.directions}:{status:'requires-retarget',reason:'no-motion-source-for-goal',center};
 const nearest=Math.round(total/HALF),candidates=[...new Set([nearest,nearest-1,nearest+1,Math.floor(total/HALF),Math.ceil(total/HALF)].filter(n=>n>=0))].map(halfSteps=>({halfSteps,world:halfSteps*HALF,endpoint:halfSteps?routePoint(segments,halfSteps*HALF):points[0]})).sort((a,b)=>distance(a.endpoint,center)-distance(b.endpoint,center));
 if(options.exactCenter&&Math.abs(total-nearest*HALF)>EPS)return {status:'requires-retarget',reason:'exact-center-needs-short-step-source-retarget',center,nearestEndpoint:candidates[0].endpoint,residualPixels:distance(candidates[0].endpoint,center)};
 const maxResidual=Math.min(options.directions[segments.at(-1)!.direction].projectedStridePixels/4,options.maxResidualPixels??Infinity);if(maxResidual<0||Number.isNaN(maxResidual))throw new RangeError('Residual tolerance must be nonnegative');
 const selected=candidates.find(c=>distance(c.endpoint,center)<=maxResidual+EPS&&pointOnGoal(c.endpoint,center,options)&&(!options.exactCenter||distance(c.endpoint,center)<EPS));if(!selected)return {status:'requires-retarget',reason:'no-contact-endpoint-inside-goal',center,nearestEndpoint:candidates[0].endpoint,residualPixels:distance(candidates[0].endpoint,center)};
 const lastIndex=segments.findIndex(s=>selected.world<=s.startWorld+s.worldLength+EPS),plannedSegments=selected.halfSteps?segments.slice(0,(lastIndex<0?segments.length-1:lastIndex)+1).map(s=>({...s})):[];if(plannedSegments.length){const last=plannedSegments.at(-1)!;last.b={...selected.endpoint};last.worldLength=selected.world-last.startWorld;}const plannedPoints=[{...points[0]},...plannedSegments.map(s=>({...s.b}))];
 return {status:'ready',points:plannedPoints,segments:plannedSegments,endpoint:selected.endpoint,center,halfSteps:selected.halfSteps,worldLength:selected.world,nominalWorldLength:total,durationMs:selected.halfSteps?(selected.halfSteps+1)*HALF_MS:0,residualPixels:distance(selected.endpoint,center),stopFoot:(selected.halfSteps-1)%2===0?'left':'right',directions:options.directions};
}
/** One clock: fixed physical source timing, continuous walk phase through segment turns. */
export function sampleGroundRoute(plan:GroundPlan,timeMs:number) {
 const time=Math.max(0,Math.min(Number.isFinite(timeMs)?timeMs:0,plan.durationMs)),walkMs=Math.max(0,plan.halfSteps-1)*HALF_MS;let state:'idle'|'start'|'walk'|'stop'='idle',world=plan.worldLength,phaseMs=walkMs%800,velocityWorld=0,stanceFoot:'left'|'right'|null=null,supportWorld:number|null=null;
 if(plan.durationMs&&time<plan.durationMs){if(time<HALF_MS){state='start';const t=time/HALF_MS;world=.18*t*t;velocityWorld=.9*t;stanceFoot='right';supportWorld=0;phaseMs=0;}
 else if(time<HALF_MS+walkMs){state='walk';const elapsed=time-HALF_MS,index=Math.floor(elapsed/HALF_MS);world=.18+.9*elapsed/1000;velocityWorld=.9;phaseMs=elapsed%800;stanceFoot=index%2?'right':'left';supportWorld=(index+1)*HALF;}
 else {state='stop';const t=(time-HALF_MS-walkMs)/HALF_MS;world=plan.worldLength-.18+.18*(2*t-t*t);velocityWorld=.9*(1-t);stanceFoot=plan.stopFoot;supportWorld=plan.worldLength;}}
 const position=time>=plan.durationMs?{...plan.endpoint}:plan.segments.length?routePoint(plan.segments,world):{...plan.endpoint},segment=plan.segments.find(s=>world<s.startWorld+s.worldLength-EPS)??plan.segments.at(-1),direction=segment?.direction??'e';return {state,position,direction,worldDistance:world,phaseMs,velocityWorld,stanceFoot,supportWorldDistance:supportWorld,sourceSupportOffsetWorld:supportWorld===null?0:supportWorld-world,complete:time>=plan.durationMs};
}
