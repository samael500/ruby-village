import {levels} from './levels.ts';
export const PROGRESS_KEY='ruby-village:chapter-1:v1';
export type StorageLike=Pick<Storage,'getItem'|'setItem'>;
export function parseProgress(raw:string|null):string[] {
  try {
    const value:unknown=JSON.parse(raw??'null');
    if(!value||typeof value!=='object'||!('version' in value)||value.version!==1||!('completed' in value)||!Array.isArray(value.completed)) return [];
    const completed:string[]=[];
    // Only a contiguous prefix unlocks the next chapter segment.
    for(const level of levels) {if(!value.completed.includes(level.id)) break;completed.push(level.id);}
    return completed;
  } catch {return [];}
}
export function loadProgress(storage?:StorageLike):string[] {try{return parseProgress(storage?.getItem(PROGRESS_KEY)??null);}catch{return [];}}
export function saveProgress(completed:readonly string[],storage?:StorageLike):boolean {
  try {if(!storage)return false;storage.setItem(PROGRESS_KEY,JSON.stringify({version:1,completed}));return true;}catch{return false;}
}
export function available(id:string,completed:readonly string[]):boolean {
  const index=levels.findIndex(l=>l.id===id);return index>=0&&(index===0||completed.includes(levels[index-1].id));
}
export function completeLevel(id:string,completed:readonly string[]):string[] {
  return available(id,completed)?levels.filter(l=>l.id===id||completed.includes(l.id)).map(l=>l.id):[...completed];
}
