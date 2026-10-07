import type {Hex} from './hex.ts';
export type Piece = {id:string; name:string; shape:readonly Hex[]; color:string; kind?:'stone'|'bridge'};
export type Placement = {anchor:Hex; turns:number};
export type Layout = Record<string,Placement>;
export type Terrain = 'ground'|'tree'|'rock'|'water'|'house';
export type Level = {
  id:string; name:string; cols:number; rows:number; terrain:Record<string,Terrain>;
  start:Hex; goal:Hex; startName:string; goalName:string; pieces:readonly Piece[];
  intro:string; outro:string; solution:Layout;
};
