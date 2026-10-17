import {characterFrame} from './character-assets.ts';
import {sceneBackdrop,sceneForeground} from './scene-art.ts';
import {placedCells} from './game.ts';
import {hexCenter,key} from './hex.ts';
import {groundTransform} from './projection.ts';
import {stoneDetail} from './level-art.ts';
import type {Level} from './model.ts';
import type {fitScene} from './scene-camera.ts';

type Scene=ReturnType<typeof fitScene>;
export type StorySprite={file:string;frameSize:readonly number[];footAnchor:readonly number[];height:number;position:{x:number;y:number};label:string;shadow?:boolean};
const ns='http://www.w3.org/2000/svg';
const decodedImages=new Map<string,Promise<void>>();
function decodeImage(url:string){if(!decodedImages.has(url)){const image=new Image();image.src=url;decodedImages.set(url,image.decode().catch(()=>{}));}return decodedImages.get(url)!;}
function node(tag:string,attributes:Record<string,string|number>,parent:Element){
 const element=document.createElementNS(ns,tag);
 for(const [key,value] of Object.entries(attributes))element.setAttribute(key,String(value));
 parent.append(element);return element;
}
/** The story shares the puzzle camera and layer order; it has no hit targets or grid. */
export async function renderPrologueScene(target:SVGSVGElement,scene:Scene,level:Level,sprites:readonly StorySprite[],intactRoad:boolean,looseStones:readonly {x:number;y:number}[]=[]){
 const generation=String(Number(target.dataset.generation??0)+1);target.dataset.generation=generation;target.dataset.ready='false';
 const svg=document.createElementNS(ns,'svg');
 sceneBackdrop(svg,scene,false);
 if(intactRoad){
  const ground=node('g',{transform:`translate(${scene.translation.x} ${scene.translation.y}) ${groundTransform(scene.projection)}`,'pointer-events':'none','data-story-road':'intact'},svg);
  const cells=Object.entries(level.solution).flatMap(([id,placement])=>placedCells(id,placement,level.pieces));
  const paved=new Set([...cells,level.start,level.goal].map(key));
  for(const cell of [...cells,level.start,level.goal]){
   const center=hexCenter(cell,scene.radius);
   stoneDetail(ground,cell,scene.radius,center.x,center.y,0,paved);
  }
 }
 const world=node('g',{transform:`translate(${scene.offset.x} ${scene.offset.y}) scale(${scene.fit})`,'pointer-events':'none'},svg);
 for(const [index,stone] of looseStones.entries()){
  const shape=node('g',{'data-story-loose-stone':index,transform:`translate(${stone.x} ${stone.y}) scale(1 .65)`},world);
  stoneDetail(shape,{q:0,r:0},32,0,0,index);
 }
 for(const sprite of [...sprites].sort((a,b)=>a.position.y-b.position.y)){
  const frame=characterFrame({image:sprite.file,frameSize:sprite.frameSize,footAnchor:sprite.footAnchor}),scale=sprite.height/frame.frameSize[1];
  const actor=node('g',{'data-story-actor':sprite.label,transform:`translate(${sprite.position.x} ${sprite.position.y})`,role:'img','aria-label':sprite.label},world);
  if(sprite.shadow!==false)node('ellipse',{cx:0,cy:0,rx:sprite.height*.12,ry:sprite.height*.035,fill:'#302d23',opacity:.18},actor);
  node('image',{href:`${import.meta.env.BASE_URL}assets/characters-v1/${frame.image}`,x:-frame.footAnchor[0]*scale,y:-frame.footAnchor[1]*scale,width:frame.frameSize[0]*scale,height:sprite.height},actor);
 }
 sceneForeground(svg,scene,false);
 await Promise.all([...svg.querySelectorAll('image')].map(image=>decodeImage(image.getAttribute('href')!)));
 if(target.dataset.generation!==generation)return;
 target.replaceChildren(...svg.childNodes);target.dataset.ready='true';
}
