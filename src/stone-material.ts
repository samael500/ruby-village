import type {Hex} from './hex.ts';
/** Source rectangles from assets/level-1/v5/manifest.json; runtime polygons own geometry. */
export const tileCrop={x:54,y:15,width:415,height:465,overscan:1.06};
export function tileVariant(pieceId:string,local:Hex):number{
  const seed=`${pieceId}:${local.q},${local.r}`;
  let hash=2166136261;
  for(const char of seed)hash=Math.imul(hash^char.charCodeAt(0),16777619)>>>0;
  return hash%6;
}
export const tileFile=(index:number)=>`tile-${String(index+1).padStart(2,'0')}`;
