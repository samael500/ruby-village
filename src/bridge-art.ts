import {hexCenter,rotate,add,directions,key,type Hex} from './hex.ts';
const ns='http://www.w3.org/2000/svg';
let serial=0;
function node(tag:string,attrs:Record<string,string|number>,parent:Element){const e=document.createElementNS(ns,tag);for(const[k,v]of Object.entries(attrs))e.setAttribute(k,String(v));parent.append(e);return e;}
/** The timber surface is clipped to the actual three-hex footprint before the
 * shared ground projection. The middle section crosses water, ends stay on land. */
export function drawBridge(parent:Element,anchor:Hex,turns:number,radius:number,origin:{x:number;y:number},options:{connectedPaving?:ReadonlySet<string>}={}){
 const center=hexCenter(anchor,radius),group=node('g',{'data-painted-bridge':'','data-bridge-shape':'three-hex','pointer-events':'none',transform:`translate(${center.x+origin.x} ${center.y+origin.y}) rotate(${turns*60})`},parent);
 const clipId=`bridge-footprint-${serial++}`,clip=node('clipPath',{id:clipId},node('defs',{},group));
 const edges=new Map<string,{a:{x:number;y:number};b:{x:number;y:number};count:number;neighbor:Hex}>();
 for(const q of [-1,0,1]){
  const x=Math.sqrt(3)*radius*q,points=Array.from({length:6},(_,i)=>({x:x+radius*Math.cos((i*60-90)*Math.PI/180),y:radius*Math.sin((i*60-90)*Math.PI/180)}));
  node('polygon',{points:points.map(p=>`${p.x},${p.y}`).join(' ')},clip);
  for(let i=0;i<6;i++){
   const a=points[i],b=points[(i+1)%6],key=[`${a.x.toFixed(5)},${a.y.toFixed(5)}`,`${b.x.toFixed(5)},${b.y.toFixed(5)}`].sort().join('|'),previous=edges.get(key);
   if(previous)previous.count++;else edges.set(key,{a,b,count:1,neighbor:add({q,r:0},[directions[1],directions[0],directions[5],directions[4],directions[3],directions[2]][i])});
  }
 }
 const paint=node('g',{'clip-path':`url(#${clipId})`},group),length=3*Math.sqrt(3)*radius;
 node('rect',{x:-length/2,y:-radius,width:length,height:radius*2,fill:'#b89970'},paint);
 const detailed=!!options.connectedPaving;
 if(detailed){
  // One native asset registration, then the same ground camera as all tiles.
  // Exact three-cell clipping/hit geometry is independent of painted edges.
  const scale=radius/328;
  node('image',{href:`${import.meta.env.BASE_URL}assets/bridge-v2/bridge-painted-v2.webp`,x:-920*scale,y:-432*scale,width:1840*scale,height:854*scale},paint);
 }else{
  const deck=node('svg',{x:-length/2,y:-radius,width:length,height:radius*2,viewBox:'68 167 2033 359',preserveAspectRatio:'none',overflow:'hidden'},paint);
  node('image',{href:`${import.meta.env.BASE_URL}assets/bridge-v1/deck-v1.png`,width:2170,height:725},deck);
 }
 for(const {a,b,count,neighbor}of edges.values()){
  if(options.connectedPaving&&(count>1||options.connectedPaving.has(key(add(anchor,rotate(neighbor,turns))))))continue;
  node('path',{d:`M${a.x} ${a.y}L${b.x} ${b.y}`,fill:'none',stroke:detailed?'#735334':count===1?'#6e503b':'#816146','stroke-width':radius*(count===1?.035:.022),'stroke-linejoin':'round','stroke-linecap':'round',opacity:count===1?1:.65},group);
 }
 return group;
}
