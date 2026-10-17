import {pixelHex,key} from './hex.ts';
import {unproject} from './projection.ts';
import {placedCells,type Layout} from './game.ts';
import type {Level} from './model.ts';
import type {Surface,Point} from './character-animation.ts';
type Camera={radius:number;origin:Point;groundScale:number;angle:number};
export function routeSurface(level:Level,layout:Layout,point:Point,camera:Camera):Surface{
 const ground=unproject({x:point.x-camera.origin.x,y:point.y-camera.origin.y},{scale:camera.groundScale,pivotY:0,angle:camera.angle});
 const cell=pixelHex(ground.x,ground.y,camera.radius),cellKey=key(cell);
 for(const [id,placement]of Object.entries(layout)){
  if(placedCells(id,placement,level.pieces).some(h=>key(h)===cellKey))return level.pieces.find(p=>p.id===id)?.kind==='bridge'?'wood':'stone';
 }
 return cellKey===key(level.start)||cellKey===key(level.goal)?'stone':'earth';
}
