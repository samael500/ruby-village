const ns='http://www.w3.org/2000/svg';
let serial=0;
function node(tag:string,attrs:Record<string,string|number>,parent:Element){const e=document.createElementNS(ns,tag);for(const [k,v]of Object.entries(attrs))e.setAttribute(k,String(v));parent.append(e);return e;}
/** Only the decorative perimeter joins the surround. Native center stays opaque. */
export function sceneJoinMask(parent:Element,width:number,height:number,band:number){
 const id=`scene-join-${serial++}`,defs=node('defs',{},parent),w=width,h=height,b=band;
 const mask=node('mask',{id,maskUnits:'userSpaceOnUse',x:0,y:0,width:w,height:h},defs);
 node('rect',{x:b,y:b,width:w-2*b,height:h-2*b,fill:'white'},mask);
 for(const [side,x1,y1,x2,y2,x,y,width,height] of [['left',0,0,b,0,0,0,b,h],['right',w,0,w-b,0,w-b,0,b,h],['top',0,0,0,b,b,0,w-2*b,b],['bottom',0,h,0,h-b,b,h-b,w-2*b,b]] as const){
  const gradient=node('linearGradient',{id:`${id}-${side}`,gradientUnits:'userSpaceOnUse',x1,y1,x2,y2},defs);
  node('stop',{offset:0,'stop-color':'black'},gradient);node('stop',{offset:1,'stop-color':'white'},gradient);
  node('rect',{x,y,width,height,fill:`url(#${id}-${side})`},mask);
 }
 return `url(#${id})`;
}
