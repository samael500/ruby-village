import {hexCenter,type Hex} from './hex.ts';
export type Point={x:number;y:number};
export type SpriteLayout={x:number;y:number;width:number;height:number;source:Point;anchor:Point};
export const sourceAnchors={ruta:{x:.55,y:.965}} as const;
/** Calibrated in original image pixels. The puzzle is never transposed. */
export const compositions={
  landscape:{file:'courtyard-landscape',width:1672,height:941,radius:68,grid:{x:475,y:265},door:{x:401,y:433},gate:{x:1335,y:625},doorHeight:145},
  portrait:{file:'courtyard-portrait',width:941,height:1672,radius:52,grid:{x:160,y:650},door:{x:367,y:468},gate:{x:668,y:1260},doorHeight:136},
} as const;
export function sceneLayout(width:number,height:number,_cols:number,_rows:number,start:Hex,goal:Hex,portrait=false){
  const art=compositions[portrait?'portrait':'landscape'];
  const fit=Math.min(width/art.width,height/art.height);
  const offset={x:(width-art.width*fit)/2,y:(height-art.height*fit)/2};
  const scale=art.radius*fit,origin={x:offset.x+art.grid.x*fit,y:offset.y+art.grid.y*fit};
  const a=hexCenter(start,art.radius),b=hexCenter(goal,art.radius);
  const startArt={x:a.x+art.grid.x,y:a.y+art.grid.y},goalArt={x:b.x+art.grid.x,y:b.y+art.grid.y};
  const heightRuta=art.doorHeight*.65,widthRuta=heightRuta*1209/1300;
  const ruta:SpriteLayout={x:startArt.x-widthRuta*.55,y:startArt.y-heightRuta*.965,width:widthRuta,height:heightRuta,source:sourceAnchors.ruta,anchor:startArt};
  const approaches:Point[][]=portrait?[]:[
    [art.door,{x:440,y:400},{x:startArt.x-Math.sqrt(3)*art.radius/2,y:startArt.y}],
    [{x:goalArt.x+Math.sqrt(3)*art.radius/2,y:goalArt.y+art.radius/2},art.gate],
  ];
  return {scale,origin,art,fit,offset,ruta,startArt,goalArt,portrait,approaches};
}
