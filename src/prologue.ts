import type {StorageLike} from './progress.ts';
export const PROLOGUE_ID='c1-00-prologue';
export const PROLOGUE_KEY='ruby-village:prologue:v1';
export const prologueFrames=[
 {scene:'courtyard',speaker:'Рассказчик',text:'Это Рута. Она живёт в Рубиновой деревне, где друзья всегда помогают друг другу'},
 {scene:'courtyard',speaker:'Рута',text:'Кролик сегодня печёт пирог. Я обещала принести ему яблоки!'},
 {scene:'orchard',speaker:'Рассказчик',text:'Кролик живёт за калиткой, в яблоневом саду. Он уже ждёт Руту'},
 {scene:'courtyard',speaker:'Рута',text:'Ой… Вчера здесь была дорожка! А теперь камни лежат в стороне'},
 {scene:'courtyard',speaker:'Рута',text:'Попробую сложить их обратно. Тогда смогу дойти до Кролика'},
 {scene:'courtyard',speaker:'Рута',text:'Начнём с дорожки до калитки. Поможешь мне?'}
] as const;
export type PrologueState={seen:boolean;frame:number;active:boolean};
export const newPrologue=():PrologueState=>({seen:false,frame:0,active:false});
export function loadPrologue(storage?:StorageLike):PrologueState{
 try{
  const v=JSON.parse(storage?.getItem(PROLOGUE_KEY)??'null');
  if(v?.version!==1||typeof v.seen!=='boolean'||typeof v.active!=='boolean'||!Number.isInteger(v.frame)||v.frame<0||v.frame>=prologueFrames.length)return newPrologue();
  return {seen:v.seen,frame:v.frame,active:v.active};
 }catch{return newPrologue();}
}
export function savePrologue(state:PrologueState,storage?:StorageLike):boolean{
 try{if(!storage)return false;storage.setItem(PROLOGUE_KEY,JSON.stringify({version:1,...state}));return true;}catch{return false;}
}
/** A real puzzle session or existing progress always takes precedence over an unfinished intro. */
export function shouldStartPrologue(state:PrologueState,hasSession:boolean,hasProgress:boolean){return !hasSession&&!hasProgress&&!state.seen;}
export const speakerPortrait=(speaker:string):string|undefined=>({'Рута':'../ui/v7/ruta-bust.png','Кролик':'rabbit.svg','Бельчонок':'squirrel.svg','Ёж':'hedgehog.svg','Учительница':'teacher.svg','Пекарь':'baker.svg','Мельник':'miller.svg'} as Record<string,string>)[speaker];
