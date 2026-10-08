import manifest from '../public/assets/chapter-1/v6/manifest.json' with {type:'json'};
import {artCamera,artPoint,sceneIds} from './art-geometry.ts';
import type {Level} from './model.ts';
export function chapterScene(level:Level,width:number,height:number){
 const art=manifest.scenes[sceneIds.indexOf(level.id)];
 const fit=Math.min(width/art.width,height/art.height),offset={x:(width-art.width*fit)/2,y:(height-art.height*fit)/2};
 return {art,fit,offset,radius:artCamera.radius*fit,origin:{x:0,y:0},projection:{scale:.65,pivotY:0},translation:{x:offset.x+artCamera.origin.x*fit,y:offset.y+artCamera.origin.y*fit},point:artPoint};
}
