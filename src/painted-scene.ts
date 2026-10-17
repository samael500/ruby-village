import type {fitScene} from './scene-camera.ts';
import {sceneJoinMask} from './scene-mask.ts';
type Scene=ReturnType<typeof fitScene>;
export type PaintedSceneAssets={
 background:string;foreground?:string|null;gateClosed?:string;gateOpen?:string;
 joinBand?:number;
 wide?:{file:string;canvas:{width:number;height:number};originalRect:{x:number;y:number;width:number;height:number}}|null;
};
const ns='http://www.w3.org/2000/svg';
function node(tag:string,attrs:Record<string,string|number>,parent:Element){const e=document.createElementNS(ns,tag);for(const [k,v]of Object.entries(attrs))e.setAttribute(k,String(v));parent.append(e);return e;}
function world(svg:SVGElement,scene:Scene,kind:string){return node('g',{[kind]:'',transform:`translate(${scene.offset.x} ${scene.offset.y}) scale(${scene.fit})`,'pointer-events':'none'},svg);}
const url=(file:string)=>`${import.meta.env.BASE_URL}assets/chapter-1/v9/${file}`;
/** Native painted layers use one canvas and camera. No cover crop or generated
 * fallback is substituted when a required wide asset has not been delivered. */
export function paintedBackdrop(svg:SVGSVGElement,scene:Scene,assets:PaintedSceneAssets){
 if(!assets.wide)throw new Error('Painted scene requires its audited wide surroundings');
 const group=world(svg,scene,'data-painted-world'),{canvas,originalRect}=assets.wide;
 node('image',{'data-surroundings':'',href:url(assets.wide.file),x:-originalRect.x,y:-originalRect.y,width:canvas.width,height:canvas.height},group);
 node('image',{'data-painted-background':'',href:url(assets.background),width:originalRect.width,height:originalRect.height,mask:sceneJoinMask(group,originalRect.width,originalRect.height,assets.joinBand??48)},group);
}
export function paintedForeground(svg:SVGSVGElement,scene:Scene,assets:PaintedSceneAssets,open:boolean){
 const worldGroup=world(svg,scene,'data-painted-foreground'),group=node('g',{mask:sceneJoinMask(worldGroup,1672,941,assets.joinBand??48)},worldGroup);
 if(assets.foreground)node('image',{href:url(assets.foreground),width:1672,height:941},group);
 const gate=open?assets.gateOpen:assets.gateClosed;
 if(gate)node('image',{'data-painted-gate':open?'open':'closed',href:url(gate),width:1672,height:941},group);
}
