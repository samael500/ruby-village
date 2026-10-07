import {levels} from './levels.ts';
export const PROGRESS_KEY='ruby-village:chapter-1:v1';
export type StorageLike=Pick<Storage,'getItem'|'setItem'>;
export type Progress={completed:string[];introSeen:string[]};
const empty=():Progress=>({completed:[],introSeen:[]});
export function parseState(raw:string|null):Progress {
 try {
  const value:unknown=JSON.parse(raw??'null');
  if(!value||typeof value!=='object'||!('version' in value)||!('completed' in value)||!Array.isArray(value.completed))return empty();
  const saved=value.completed;
  if(value.version===1){
   // Old three-level progression: mill stays completed at its new position, without skipping new tasks.
   const completed:string[]=[];
   for(const id of ['gate','garden','mill']){if(!saved.includes(id))break;completed.push(id);}
   return {completed,introSeen:[...completed]};
  }
  if(value.version!==2)return empty();
  const completed=levels.filter(l=>saved.includes(l.id)).map(l=>l.id);
  const seen='introSeen' in value&&Array.isArray(value.introSeen)?value.introSeen:[];
  return {completed,introSeen:levels.filter(l=>seen.includes(l.id)||completed.includes(l.id)).map(l=>l.id)};
 }catch{return empty();}
}
export const parseProgress=(raw:string|null)=>parseState(raw).completed;
export function loadState(storage?:StorageLike):Progress {try{return parseState(storage?.getItem(PROGRESS_KEY)??null);}catch{return empty();}}
export const loadProgress=(storage?:StorageLike)=>loadState(storage).completed;
export function saveProgress(completed:readonly string[],storage?:StorageLike,introSeen:readonly string[]=completed):boolean {
 try {if(!storage)return false;storage.setItem(PROGRESS_KEY,JSON.stringify({version:2,completed,introSeen}));return true;}catch{return false;}
}
export function available(id:string,completed:readonly string[]):boolean {
 const index=levels.findIndex(l=>l.id===id);
 return index>=0&&(completed.includes(id)||levels.slice(0,index).every(l=>completed.includes(l.id)));
}
export function completeLevel(id:string,completed:readonly string[]):string[] {
 return available(id,completed)?levels.filter(l=>l.id===id||completed.includes(l.id)).map(l=>l.id):[...completed];
}
