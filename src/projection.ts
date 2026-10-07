import type {Point} from './scene-layout.ts';
export const GROUND_SCALE=.65;
export type Projection={scale:number;pivotY:number;pivotX?:number;angle?:number;zoom?:number};
export function project(p:Point,t:Projection):Point {
 const x=p.x-(t.pivotX??0),y=p.y-t.pivotY,c=Math.cos(t.angle??0),s=Math.sin(t.angle??0),z=t.zoom??1;
 return {x:(t.pivotX??0)+z*(c*x-s*y),y:t.pivotY+t.scale*z*(s*x+c*y)};
}
export function unproject(p:Point,t:Projection):Point {
 const z=t.zoom??1,x=(p.x-(t.pivotX??0))/z,y=(p.y-t.pivotY)/(t.scale*z),c=Math.cos(t.angle??0),s=Math.sin(t.angle??0);
 return {x:(t.pivotX??0)+c*x+s*y,y:t.pivotY-s*x+c*y};
}
export function groundTransform(t:Projection):string {
 const c=Math.cos(t.angle??0),s=Math.sin(t.angle??0),z=t.zoom??1,x=t.pivotX??0,y=t.pivotY;
 const a=z*c,b=t.scale*z*s,k=-z*s,d=t.scale*z*c;
 return `matrix(${a} ${b} ${k} ${d} ${x-a*x-k*y} ${y-b*x-d*y})`;
}
/** Preserve the two painted scene anchors while tilting the regular ground plane. */
export function sceneProjection(start:Point,goal:Point):Projection {
 const dx=goal.x-start.x,dy=goal.y-start.y;
 return {scale:GROUND_SCALE,pivotX:start.x,pivotY:start.y,angle:Math.atan2(dy/GROUND_SCALE,dx)-Math.atan2(dy,dx),zoom:Math.hypot(dx,dy/GROUND_SCALE)/Math.hypot(dx,dy)};
}
