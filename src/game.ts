import {type Hex, footprint, key, canPlace, boardCells} from './hex.ts';
export const pieces = [
  {id:'one-a', name:'Камешек 1', shape:[{q:0,r:0}], color:'#9873bf'},
  {id:'one-b', name:'Камешек 2', shape:[{q:0,r:0}], color:'#b080c6'},
  {id:'line', name:'Три в ряд', shape:[{q:0,r:0},{q:1,r:0},{q:2,r:0}], color:'#8465b2'},
  {id:'bend', name:'Уголок', shape:[{q:0,r:0},{q:1,r:0},{q:1,r:1}], color:'#ac79ad'},
  {id:'cluster', name:'Четвёрка', shape:[{q:0,r:0},{q:1,r:0},{q:0,r:1},{q:-1,r:2}], color:'#7965a3'},
] as const;
export type Placement = {anchor: Hex; turns: number};
export type Layout = Record<string, Placement>;
export const pieceById = (id: string) => pieces.find(p => p.id === id)!;
export const placedCells = (id: string, placement: Placement) => footprint(pieceById(id).shape, placement.anchor, placement.turns);
export function occupied(layout: Layout, except?: string): Set<string> {
  return new Set(Object.entries(layout).filter(([id]) => id !== except).flatMap(([id,p]) => placedCells(id,p).map(key)));
}
export function valid(id: string, p: Placement, layout: Layout, cols: number, rows: number): boolean {
  return canPlace(placedCells(id,p), new Set(boardCells(cols,rows).map(key)), occupied(layout,id));
}
