import type {fitScene} from './scene-camera.ts';
type Scene=ReturnType<typeof fitScene>;
const ns='http://www.w3.org/2000/svg';
const node=(tag:string,attrs:Record<string,string|number>,parent:Element)=>{const e=document.createElementNS(ns,tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,String(v));parent.append(e);return e;};
const art=(file:string,version='v8')=>`${import.meta.env.BASE_URL}assets/chapter-1/${version}/${file}`;
const world=(svg:Element,scene:Scene,attrs:Record<string,string|number>={})=>node('g',{...attrs,transform:`translate(${scene.offset.x} ${scene.offset.y}) scale(${scene.fit})`,'pointer-events':'none'},svg);
let serial=0;
/** Join only the decorative perimeter; all gameplay and important props remain in the opaque center. */
function joinMask(parent:Element,scene:Scene){
 const id=`join-${serial++}`,defs=node('defs',{},parent),w=scene.metadata.originalRect.width,h=scene.metadata.originalRect.height,b=scene.metadata.joinBand;
 const mask=node('mask',{id,maskUnits:'userSpaceOnUse',x:0,y:0,width:w,height:h},defs);
 node('rect',{x:b,y:b,width:w-2*b,height:h-2*b,fill:'white'},mask);
 for(const [side,x1,y1,x2,y2,x,y,width,height] of [['left',0,0,b,0,0,0,b,h],['right',w,0,w-b,0,w-b,0,b,h],['top',0,0,0,b,b,0,w-2*b,b],['bottom',0,h,0,h-b,b,h-b,w-2*b,b]] as const){
  const gradient=node('linearGradient',{id:`${id}-${side}`,gradientUnits:'userSpaceOnUse',x1,y1,x2,y2},defs);
  node('stop',{offset:0,'stop-color':'black'},gradient);node('stop',{offset:1,'stop-color':'white'},gradient);
  node('rect',{x,y,width,height,fill:`url(#${id}-${side})`},mask);
 }
 return `url(#${id})`;
}
function openGate(parent:Element,scene:Scene,open:boolean){
 const metadata=scene.metadata;if(!open||!('openGate' in metadata))return;
 const patch=metadata.openGate,id=`gate-patch-${serial++}`,[x,y,width,height]=patch.region;
 node('rect',{x,y,width,height},node('clipPath',{id},node('defs',{},parent)));
 const g=node('g',{'clip-path':`url(#${id})`,'data-open-gate':''},parent);
 node('image',{href:art(patch.file),width:1672,height:941},g);
}
export function sceneBackdrop(svg:SVGSVGElement,scene:Scene,open:boolean){
 const m=scene.metadata,rect=m.originalRect,g=world(svg,scene,{'data-scene-world':''});
 node('image',{'data-surroundings':'',href:art(m.extension),x:-rect.x,y:-rect.y,width:m.canvas.width,height:m.canvas.height},g);
 // The approved center stays a separate PNG. Only its 48px decorative perimeter joins the outpaint.
 node('image',{id:'chapter-background',href:art(m.source,'v6'),width:rect.width,height:rect.height,mask:joinMask(g,scene)},g);
 openGate(g,scene,open);
}
/** Pixel-aligned copies of actual foreground artwork; the opening remains unobstructed. */
export function sceneForeground(svg:SVGSVGElement,scene:Scene,open:boolean){
 const g=world(svg,scene,{'data-foreground':'','aria-hidden':'true'}),id=`front-${serial++}`;
 const clip=node('clipPath',{id},node('defs',{},g));
 for(const polygon of scene.metadata.foreground)node('polygon',{points:polygon.map(p=>p.join(',')).join(' ')},clip);
 const paint=node('g',{'clip-path':`url(#${id})`,mask:joinMask(g,scene)},g);
 node('image',{href:art(scene.metadata.source,'v6'),width:1672,height:941},paint);
 openGate(paint,scene,open);
}
