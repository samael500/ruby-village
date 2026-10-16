import type {Level} from './model.ts';
import {fitScene} from './production-camera.ts';
export function chapterScene(level:Level,width:number,height:number){return fitScene(level.id,width,height);}
