import {scenePoint as point,fitScene as fit,goalSignLayout as sign} from './scene-camera.ts';
import {productionScenes} from './production-chapter.ts';
import type {Hex} from './hex.ts';
export const scenePoint=(id:string,h:Hex)=>point(id,h,productionScenes);
export const fitScene=(id:string,w:number,h:number)=>fit(id,w,h,productionScenes);
export const goalSignLayout=(id:string,w:number,h:number)=>sign(id,w,h,productionScenes);
