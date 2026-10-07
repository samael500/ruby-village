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
  const scale=Math.max(.01,Math.min((width-16)/(right-left),(height-16)/(bottom-top)));
  const origin={x:(width-(right-left)*scale)/2-left*scale,y:(height-(bottom-top)*scale)/2-top*scale};
  return {scale,origin,house,ruta,gate,bounds:{left,top,right,bottom}};
}
