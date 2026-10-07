import {courtyard} from './environment.ts';
import {boardCells,hexCenter,type Hex} from './hex.ts';
export type Point={x:number;y:number};
export type SpriteLayout={x:number;y:number;width:number;height:number;source:Point;anchor:Point};
export const sourceAnchors={house:{x:.66,y:.93},ruta:{x:.55,y:.965},gate:{x:.5,y:.8}} as const;
function sprite(anchor:Point,width:number,aspect:number,source:Point):SpriteLayout{
  const height=width/aspect;
  return {x:anchor.x-width*source.x,y:anchor.y-height*source.y,width,height,source,anchor};
}
/** Unit-radius world: one uniform fit, with the same anchors in every orientation. */
export function sceneLayout(width:number,height:number,cols:number,rows:number,start:Hex,goal:Hex){
  const a=hexCenter(start,1),b=hexCenter(goal,1);
  const house=sprite({x:a.x-.55,y:a.y},3.45,1312/1199,sourceAnchors.house);
  const ruta=sprite(a,1.25*1209/1300,1209/1300,sourceAnchors.ruta);
  // The opening meets the lower-right edge; the fence extends out of the court.
  const gate=sprite({x:b.x+.9,y:b.y+.8},2.4,1536/1024,sourceAnchors.gate);
  const centers=boardCells(cols,rows).map(h=>hexCenter(h,1));
  const left=Math.min(...centers.map(c=>c.x-Math.sqrt(3)/2),house.x,ruta.x,gate.x);
  const top=Math.min(...centers.map(c=>c.y-1),house.y,ruta.y,gate.y);
  const right=Math.max(...centers.map(c=>c.x+Math.sqrt(3)/2),house.x+house.width,ruta.x+ruta.width,gate.x+gate.width);
  const bottom=Math.max(...centers.map(c=>c.y+1),house.y+house.height,ruta.y+ruta.height,gate.y+gate.height);
  // Reserve the whole fence silhouette, not just the ground-level post bases.
  const m=courtyard.fitMargin;
  const fitBounds={left:left-m.side,top:top-m.top,right:right+m.side,bottom:bottom+m.bottom};
  const scale=Math.max(.01,Math.min((width-16)/(fitBounds.right-fitBounds.left),(height-16)/(fitBounds.bottom-fitBounds.top)));
  const origin={x:(width-(fitBounds.right-fitBounds.left)*scale)/2-fitBounds.left*scale,y:(height-(fitBounds.bottom-fitBounds.top)*scale)/2-fitBounds.top*scale};
  return {scale,origin,house,ruta,gate,bounds:{left,top,right,bottom}};
}
