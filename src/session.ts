import type {Level} from './model.ts';
import {levels,sandbox} from './levels.ts';
import {validPlacement,type Layout} from './game.ts';
import {available,type StorageLike,PROGRESS_KEY} from './progress.ts';
export const CHAPTER_LAYOUT_VERSION=2;
export type SessionRecovery={session:Session|null;notice:string|null;discarded:string[];migrated:boolean};
export type Session={levelId:string;cols:number;rows:number;layout:Layout;mode:'select'|'drag';reducedMotion:boolean};
/** Corrupt or obsolete individual placements are discarded; no completed roads change. */
export function loadSession(storage:StorageLike|undefined,completed:readonly string[]):Session|null{return recoverSession(storage,completed).session;}
/** Read-only, repeatable migration; caller can display notice and persist with saveSession. */
export function recoverSession(storage:StorageLike|undefined,completed:readonly string[],chapterLevels:readonly Level[]=levels,layoutVersion:number=CHAPTER_LAYOUT_VERSION):SessionRecovery{
 const result=(session:Session|null,notice:string|null=null,discarded:string[]=[],migrated=false):SessionRecovery=>({session,notice,discarded,migrated});
 try{
  const raw=JSON.parse(storage?.getItem(PROGRESS_KEY)??'null'),v=raw?.session;
  if(raw?.version!==2||!v||typeof v!=='object')return result(null);
  if(raw.layoutVersion!==undefined&&raw.layoutVersion!==1&&raw.layoutVersion!==layoutVersion)return result(null,'Эта раскладка создана другой версией игры. Начни дорожку заново; пройденные места сохранены.');
  const level=v.levelId==='sandbox'&&[[7,5],[9,6],[11,7]].some(([c,r])=>c===v.cols&&r===v.rows)?sandbox(v.cols,v.rows):chapterLevels.find(l=>l.id===v.levelId&&available(l.id,completed));
  if(!level||!v.layout||typeof v.layout!=='object'||Array.isArray(v.layout))return result(null,'Не удалось восстановить дорожку. Пройденные места сохранены.');
  const layout:Layout={};
  for(const p of level.pieces){const x=v.layout[p.id];if(x&&Number.isInteger(x.turns)&&x.turns>=0&&x.turns<6&&Number.isInteger(x.anchor?.q)&&Number.isInteger(x.anchor?.r)&&validPlacement(level,p.id,x,layout))layout[p.id]={anchor:{q:x.anchor.q,r:x.anchor.r},turns:x.turns};}
  const discarded=Object.keys(v.layout).filter(id=>!Object.hasOwn(layout,id));
  return result({levelId:level.id,cols:level.cols,rows:level.rows,layout,mode:v.mode==='drag'?'drag':'select',reducedMotion:v.reducedMotion===true},discarded.length?'Дорожка обновилась. Неподходящие плиты возвращены в набор.':null,discarded,raw.layoutVersion!==layoutVersion);
 }catch{return result(null,'Не удалось прочитать сохранённую дорожку.');}
}
export type Preferences={mode:'select'|'drag';reducedMotion:boolean};
export function loadPreferences(storage:StorageLike|undefined):Preferences{try{const p=JSON.parse(storage?.getItem(PROGRESS_KEY)??'null')?.preferences;return {mode:p?.mode==='drag'?'drag':'select',reducedMotion:p?.reducedMotion===true};}catch{return {mode:'select',reducedMotion:false};}}
export function saveSession(storage:StorageLike|undefined,session:Session|null,preferences?:Preferences,layoutVersion:number=CHAPTER_LAYOUT_VERSION):boolean{
 try{if(!storage)return false;const raw=JSON.parse(storage.getItem(PROGRESS_KEY)??'null');if(raw?.version!==2)return false;raw.session=session;raw.layoutVersion=layoutVersion;if(preferences)raw.preferences=preferences;storage.setItem(PROGRESS_KEY,JSON.stringify(raw));return true;}catch{return false;}
}
