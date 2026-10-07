import {hexCenter,type Hex} from './hex.ts';
export type Point={x:number;y:number};
export type SpriteLayout={x:number;y:number;width:number;height:number;source:Point;anchor:Point};
// Alpha >=16 bounds measured without changing the approved PNG.
export const rutaSilhouette={left:285,top:45,right:930,bottom:1277,width:1209,height:1300};
export const sourceAnchors={ruta:{x:.55,y:rutaSilhouette.bottom/rutaSilhouette.height}} as const;
/** Calibrated in original image pixels. The puzzle is never transposed. */
export const compositions={
  landscape:{file:'courtyard-landscape',width:1672,height:941,radius:68,grid:{x:475,y:265},door:{x:401,y:433},gate:{x:1335,y:625},doorHeight:145},
  portrait:{file:'courtyard-portrait',width:941,height:1672,radius:52,grid:{x:160,y:650},door:{x:367,y:468},gate:{x:668,y:1190},doorHeight:136},
} as const;
export function sceneLayout(width:number,height:number,_cols:number,_rows:number,start:Hex,goal:Hex,portrait=false){
  const art=compositions[portrait?'portrait':'landscape'];
  const fit=Math.min(width/art.width,height/art.height);
  const offset={x:(width-art.width*fit)/2,y:(height-art.height*fit)/2};
  const scale=art.radius*fit,origin={x:offset.x+art.grid.x*fit,y:offset.y+art.grid.y*fit};
  const a=hexCenter(start,art.radius),b=hexCenter(goal,art.radius);
  const startArt={x:a.x+art.grid.x,y:a.y+art.grid.y},goalArt={x:b.x+art.grid.x,y:b.y+art.grid.y};
  const visibleFraction=(rutaSilhouette.bottom-rutaSilhouette.top)/rutaSilhouette.height;
  const visibleHeight=Math.min(art.doorHeight*.65*1.6*visibleFraction,art.radius*2*1.25);
  const heightRuta=visibleHeight/visibleFraction,widthRuta=heightRuta*1209/1300;
  const ruta:SpriteLayout={x:startArt.x-widthRuta*sourceAnchors.ruta.x,y:startArt.y-heightRuta*sourceAnchors.ruta.y,width:widthRuta,height:heightRuta,source:sourceAnchors.ruta,anchor:startArt};
  return {scale,origin,art,fit,offset,ruta,startArt,goalArt,portrait,visibleHeight};
}
