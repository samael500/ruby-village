import {selectPaintedScene,type PaintedFrame,type PaintedSet} from '../scripts/character-paint-playback.ts';
import type {Direction} from './character-animation.ts';
import type {GroundDirection} from '../scripts/character-paint-route-planner.ts';
export type RuntimeMotionSet=PaintedSet&{directions:Record<Direction,PaintedSet['directions'][Direction]&GroundDirection>};
type Manifest=RuntimeMotionSet&{sceneCameraVariant:Record<string,string>;cameraVariants:Record<string,{directions:RuntimeMotionSet['directions']}>};
let manifestPromise:Promise<Manifest>|null=null;
export async function loadMotionSet(sceneId:string):Promise<RuntimeMotionSet>{
 if(!manifestPromise)manifestPromise=fetch(`${import.meta.env.BASE_URL}assets/characters-walk-v1/animated-v3/manifest.json`).then(response=>{if(!response.ok)throw new Error('Character manifest unavailable');return response.json();});
 try{return selectPaintedScene(await manifestPromise,sceneId) as RuntimeMotionSet;}catch(error){manifestPromise=null;throw error;}
}
const ns='http://www.w3.org/2000/svg';
const images=new Map<string,Promise<HTMLImageElement>>();
function decoded(file:string){
 if(!images.has(file)){const image=new Image();image.src=import.meta.env.BASE_URL+file;images.set(file,image.decode().then(()=>image));}
 return images.get(file)!;
}
/** Decode only this scene's six atlas views, not both camera groups. */
export async function prepareMotionAtlases(set:PaintedSet){
 const files=new Set(Object.values(set.directions).flatMap(direction=>Object.values(direction.clips).flatMap(clip=>clip.frames.map(frame=>frame.file))));
 const entries=await Promise.all([...files].map(async file=>{const image=await decoded(file);return [file,{width:image.naturalWidth,height:image.naturalHeight}] as const;}));
 return new Map(entries);
}
export function drawMotionFrame(parent:SVGElement,set:PaintedSet,frame:PaintedFrame,foot:{x:number;y:number},height:number,atlases:ReadonlyMap<string,{width:number;height:number}>){
 const atlas=atlases.get(frame.file);if(!atlas)throw new Error(`Undecoded character atlas ${frame.file}`);
 const scale=height/set.nativeHeightPx,[x,y,width,frameHeight]=frame.sourceRect;
 const viewport=parent.querySelector<SVGSVGElement>(':scope > svg[data-motion-frame]')??document.createElementNS(ns,'svg');
 const attributes={x:foot.x-frame.footAnchor[0]*scale,y:foot.y-frame.footAnchor[1]*scale,width:frame.frameSize[0]*scale,height:frame.frameSize[1]*scale,viewBox:`${x} ${y} ${width} ${frameHeight}`,overflow:'hidden','data-motion-frame':`${frame.file}:${x},${y}`,'aria-label':'Рута'};
 for(const [key,value]of Object.entries(attributes))viewport.setAttribute(key,String(value));
 const image=viewport.querySelector('image')??document.createElementNS(ns,'image');
 const href=import.meta.env.BASE_URL+frame.file;if(image.getAttribute('href')!==href)image.setAttribute('href',href);
 image.setAttribute('width',String(atlas.width));image.setAttribute('height',String(atlas.height));
 if(!image.parentNode)viewport.append(image);if(!viewport.parentNode)parent.append(viewport);return viewport;
}
