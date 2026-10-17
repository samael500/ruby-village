type Camera={radius:number;origin:{x:number;y:number};angle:number;groundScale:number};
type Anchor={x:number;y:number};
type Accepted=Record<string,{camera:Camera;groundAnchors:{start:Anchor;goal:Anchor}}>;
type Candidate={background?:string;camera?:Camera;anchors?:{start:Anchor;goal:Anchor};checks?:{fullPolygonVisualAudit?:string};wide?:unknown};
/** Explain the atomic gate instead of silently mixing new data with old art. */
export function paintedActivationBlockers(manifest:{scenes:Record<string,Candidate>},accepted:Accepted):string[]{
 const blockers:string[]=[];
 for(const [id,expected]of Object.entries(accepted)){
  const candidate=manifest.scenes[id];
  if(!candidate){blockers.push(`${id}: missing scene`);continue;}
  if(!candidate.background)blockers.push(`${id}: missing background`);
  if(candidate.checks?.fullPolygonVisualAudit!=='passed')blockers.push(`${id}: full-polygon visual audit not passed`);
  const a=candidate.camera,b=expected.camera;
  if(!a||Math.max(Math.abs(a.radius-b.radius),Math.abs(a.origin.x-b.origin.x),Math.abs(a.origin.y-b.origin.y),Math.abs(a.angle-b.angle),Math.abs(a.groundScale-b.groundScale))>1e-9)blockers.push(`${id}: camera differs from accepted geometry`);
  if(!candidate.anchors||['start','goal'].some(key=>{
   const anchor=key as 'start'|'goal',a=candidate.anchors![anchor],b=expected.groundAnchors[anchor];
   return Math.hypot(a.x-b.x,a.y-b.y)>1e-6;
  }))blockers.push(`${id}: endpoints differ from accepted geometry`);
  const wide=candidate.wide as {file?:string;canvas?:{width:number;height:number};originalRect?:{x:number;y:number;width:number;height:number}}|undefined;
  if(!wide?.file||!wide.canvas||!wide.originalRect)blockers.push(`${id}: audited native wide asset not delivered`);
  else {const r=wide.originalRect,c=wide.canvas;if(r.width!==1672||r.height!==941||r.x<0||r.y<0||r.x+r.width>c.width||r.y+r.height>c.height)blockers.push(`${id}: invalid wide original rectangle`);}
 }
 return blockers;
}
