import {levels} from './levels.ts';
import {available} from './progress.ts';

/** Read-only UI projection. Replays never add progress or fire story rewards. */
export function chapterMap(completed:readonly string[]) {
 return levels.map((level,index)=>({id:level.id,title:level.name,number:index+1,
  state:completed.includes(level.id)?'restored' as const:available(level.id,completed)?'available' as const:'locked' as const,
  disabled:!available(level.id,completed),
  label:`${index+1}. ${level.name}. ${completed.includes(level.id)?'Дорога восстановлена. Повторить':available(level.id,completed)?'Можно отправиться':'Сначала восстанови предыдущие дороги'}`,
  connectionRestored:index>0&&completed.includes(levels[index-1].id)&&completed.includes(level.id)}));
}
export function continueTarget(completed:readonly string[],sessionLevel?:string):string {
 if(sessionLevel&&available(sessionLevel,completed))return sessionLevel;
 return levels.find(level=>available(level.id,completed)&&!completed.includes(level.id))?.id??levels[0].id;
}
export type LearningState={levelId:string;mode:'select'|'drag';selected:boolean;placed:number;rotated:boolean;hasBridge:boolean;bridgePlaced:boolean};
export type LearningHint={id:'choose'|'place'|'rotate'|'bridge'|'check';text:string;target:'tray'|'field'|'rotate'|'check'};
/** One hint at a time; no timers, scores or blanket requirement to use every piece. */
export function learningHint(state:LearningState):LearningHint|null {
 if(state.levelId==='gate') {
  if(!state.selected&&state.placed===0)return {id:'choose',text:'Выбери плиту внизу.',target:'tray'};
  if(state.placed===0)return {id:'place',text:state.mode==='drag'?'Перетащи плиту из лотка на дорожку.':'Выбери клетку и нажми «Поставить».',target:'field'};
  return {id:'check',text:'Соедини дом и калитку. Когда дорога готова, нажми «Проверить».',target:'check'};
 }
 if(state.hasBridge&&!state.bridgePlaced)return {id:'bridge',text:'Поставь мост так, чтобы середина была над водой, а концы — на берегах.',target:'field'};
 if(state.levelId==='garden'&&state.selected&&!state.rotated)return {id:'rotate',text:'Поверни выбранную плиту, чтобы она обошла яблоню.',target:'rotate'};
 return null;
}
export const chapterCompletion={title:'Глава «За калитку» пройдена',text:'Мы помогли деревне и нашли путь к старому саду. За лесом ждёт новая история. Продолжение готовится.',actions:['map','replay','letter'] as const};
