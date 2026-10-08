import {levels,sandbox} from './levels.ts';
import {validPlacement,type Layout} from './game.ts';
import {available,type StorageLike,PROGRESS_KEY} from './progress.ts';
export type Session={levelId:string;cols:number;rows:number;layout:Layout;mode:'select'|'drag';reducedMotion:boolean};
/** Corrupt or obsolete individual placements are discarded; no completed roads change. */
export function loadSession(storage:StorageLike|undefined,completed:readonly string[]):Session|null{
 try{
  const raw=JSON.parse(storage?.getItem(PROGRESS_KEY)??'null'),v=raw?.session;
  if(raw?.version!==2||!v||typeof v!=='object')return null;
  const level=v.levelId==='sandbox'&&[[7,5],[9,6],[11,7]].some(([c,r])=>c===v.cols&&r===v.rows)?sandbox(v.cols,v.rows):levels.find(l=>l.id===v.levelId&&available(l.id,completed));
  if(!level||!v.layout||typeof v.layout!=='object'||Array.isArray(v.layout))return null;
  const layout:Layout={};
  for(const p of level.pieces){const x=v.layout[p.id];if(x&&Number.isInteger(x.turns)&&x.turns>=0&&x.turns<6&&Number.isInteger(x.anchor?.q)&&Number.isInteger(x.anchor?.r)&&validPlacement(level,p.id,x,layout))layout[p.id]={anchor:{q:x.anchor.q,r:x.anchor.r},turns:x.turns};}
  return {levelId:level.id,cols:level.cols,rows:level.rows,layout,mode:v.mode==='drag'?'drag':'select',reducedMotion:v.reducedMotion===true};
 }catch{return null;}
}
export type Preferences={mode:'select'|'drag';reducedMotion:boolean};
export function loadPreferences(storage:StorageLike|undefined):Preferences{try{const p=JSON.parse(storage?.getItem(PROGRESS_KEY)??'null')?.preferences;return {mode:p?.mode==='drag'?'drag':'select',reducedMotion:p?.reducedMotion===true};}catch{return {mode:'select',reducedMotion:false};}}
export function saveSession(storage:StorageLike|undefined,session:Session|null,preferences?:Preferences):boolean{
 try{if(!storage)return false;const raw=JSON.parse(storage.getItem(PROGRESS_KEY)??'null');if(raw?.version!==2)return false;raw.session=session;if(preferences)raw.preferences=preferences;storage.setItem(PROGRESS_KEY,JSON.stringify(raw));return true;}catch{return false;}
}
