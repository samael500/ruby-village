import {type Hex,footprint,key,canPlace,boardCells,findPath} from './hex.ts';
import {sandboxPieces,sandbox} from './levels.ts';
import type {Level,Piece,Placement,Layout} from './model.ts';
export type {Placement,Layout} from './model.ts';
export const pieces=sandboxPieces;
export const pieceById=(id:string,set:readonly Piece[]=pieces)=>set.find(p=>p.id===id)!;
export const placedCells=(id:string,p:Placement,set:readonly Piece[]=pieces)=>footprint(pieceById(id,set).shape,p.anchor,p.turns);
export function occupied(layout:Layout,except?:string,set:readonly Piece[]=pieces):Set<string> {
  return new Set(Object.entries(layout).filter(([id])=>id!==except).flatMap(([id,p])=>placedCells(id,p,set).map(key)));
}
export const terrainAt=(level:Level,h:Hex)=>level.terrain[key(h)]??'ground';
export function validPlacement(level:Level,id:string,p:Placement,layout:Layout):boolean {
  const piece=pieceById(id,level.pieces);
  if(!piece||!Number.isInteger(p.turns)||!Number.isInteger(p.anchor.q)||!Number.isInteger(p.anchor.r)) return false;
  if(Object.keys(layout).some(id=>!pieceById(id,level.pieces))) return false;
  const cells=placedCells(id,p,level.pieces);
  if(!canPlace(cells,new Set(boardCells(level.cols,level.rows).map(key)),occupied(layout,id,level.pieces))) return false;
  if(piece.kind==='bridge') return cells.length===3 && cells.every(h=>terrainAt(level,h)===(key(h)===key(p.anchor)?'water':'ground'));
  return cells.every(h=>terrainAt(level,h)==='ground');
}
export function valid(id:string,p:Placement,layout:Layout,cols:number,rows:number):boolean {return validPlacement(sandbox(cols,rows),id,p,layout);}
export function validateLayout(level:Level,layout:Layout):boolean {
  return Object.entries(layout).every(([id,p])=>validPlacement(level,id,p,layout));
}
export function winningPath(level:Level,layout:Layout):Hex[]|null {
  if(!validateLayout(level,layout)) return null;
  return findPath(level.start,level.goal,occupied(layout,undefined,level.pieces));
}
