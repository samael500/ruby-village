import facingManifest from '../public/assets/characters-facing-v1/residents-facing-manifest.json' with {type:'json'};
import residents from '../public/assets/characters-v1/residents-manifest.json' with {type:'json'};
import {characterFrame,characterUrl} from './character-assets.ts';
import type {fitScene} from './scene-camera.ts';
type Resident=keyof typeof residents.characters;
export type ResidentPlacement={id:Resident;feet:{x:number;y:number}};
export const sceneResidents:Readonly<Record<string,readonly Resident[]>>={garden:['rabbit'],well:['teacher'],bakery:['baker'],stream:['squirrel'],mill:['miller','squirrel'],post:['hedgehog']};
/** Audited legacy anchors keep residents visible while matching final art is staged. */
export const legacyResidentPlacements:Readonly<Record<string,readonly ResidentPlacement[]>>={
 garden:[{id:'rabbit',feet:{x:1450,y:350}}],
 well:[{id:'teacher',feet:{x:1225,y:405}}],
 bakery:[{id:'baker',feet:{x:1290,y:405}}],
 stream:[{id:'squirrel',feet:{x:1400,y:225}}],
 mill:[{id:'miller',feet:{x:1430,y:398}},{id:'squirrel',feet:{x:1530,y:450}}],
 post:[{id:'hedgehog',feet:{x:1370,y:405}}],
};
type FacingFrame={image:string;frameSize:readonly number[];footAnchor:readonly number[]};
type FacingResident={frames:Record<string,FacingFrame>};
const activityView:Readonly<Record<string,Partial<Record<Resident,string>>>>={garden:{rabbit:'conversation-left'},bakery:{baker:'conversation-left'},stream:{squirrel:'conversation-left'},mill:{miller:'conversation-left',squirrel:'conversation-left'},post:{hedgehog:'conversation-left'}};
const facings=facingManifest.characters as unknown as Record<string,FacingResident>;
export type ResidentMeeting={rutaFeet:{x:number;y:number}};
const readyViews=new Set<string>(),loadingViews=new Map<string,Promise<void>>();
/** Retain the approved idle until a new authored view is decoded. */
export async function prepareResidentViews(ids:readonly string[]){
 return Promise.allSettled(ids.flatMap(id=>Object.values(facings[id]?.frames??{})).map(frame=>{
  if(!loadingViews.has(frame.image)){const image=new Image();image.src=`${import.meta.env.BASE_URL}assets/characters-facing-v1/${frame.image}`;const pending=image.decode().then(()=>{readyViews.add(frame.image);}).catch(error=>{if(loadingViews.get(frame.image)===pending)loadingViews.delete(frame.image);throw error;});loadingViews.set(frame.image,pending);}
  return loadingViews.get(frame.image)!;
 }));
}

const ns='http://www.w3.org/2000/svg';
function node(tag:string,attrs:Record<string,string|number>,parent:Element){const element=document.createElementNS(ns,tag);for(const [k,v]of Object.entries(attrs))element.setAttribute(k,String(v));parent.append(element);return element;}

/** Caller supplies audited semantic anchors; never fall back to a puzzle goal. */
export function renderResidents(parent:SVGElement,scene:ReturnType<typeof fitScene>,placements:readonly ResidentPlacement[],restored:boolean,meeting?:ResidentMeeting){
 const layer=node('g',{'data-scene-residents':'',transform:`translate(${scene.offset.x} ${scene.offset.y}) scale(${scene.fit})`,'pointer-events':'none'},parent);
 for(const placement of [...placements].sort((a,b)=>a.feet.y-b.feet.y)){
  const resident=residents.characters[placement.id],dx=meeting?meeting.rutaFeet.x-placement.feet.x:0;
  const wanted=meeting?(Math.abs(dx)<=50&&facings[placement.id]?.frames['conversation-front']?'conversation-front':dx<0?'conversation-left':'conversation-right'):(activityView[scene.sceneId]?.[placement.id]??'idle');
  const candidate=facings[placement.id]?.frames[wanted],authored=candidate&&readyViews.has(candidate.image)?candidate:undefined;
  const frame=authored??characterFrame(resident.frames.idle),height=resident.sceneHeightPx,scale=height/frame.frameSize[1];
  const actor=node('g',{'data-resident':placement.id,'data-reaction':restored?'content':'waiting','data-view':authored?wanted:'idle','data-facing-reason':meeting?'encounter':'activity',transform:`translate(${placement.feet.x} ${placement.feet.y})`,role:'img','aria-label':resident.speaker},layer);
  node('ellipse',{cx:0,cy:0,rx:height*.13,ry:height*.035,fill:'#302d23',opacity:.18},actor);
  const body=node('g',{class:'resident-breath'},actor);
  node('image',{href:authored?`${import.meta.env.BASE_URL}assets/characters-facing-v1/${authored.image}`:characterUrl(resident.frames.idle.image),x:-frame.footAnchor[0]*scale,y:-frame.footAnchor[1]*scale,width:frame.frameSize[0]*scale,height},body);
 }
 return layer;
}
