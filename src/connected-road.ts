import {hexCenter,instanceEdges,key,type Hex} from './hex.ts';
const ns='http://www.w3.org/2000/svg';let serial=0;
function node(tag:string,attrs:Record<string,string|number>,parent:Element){const n=document.createElementNS(ns,tag);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,String(v));parent.append(n);return n;}
/** One registered painted surface across confirmed cells. Piece ownership stays in
 * the input layer; adjacent instances share material coordinates, never extra cells. */
export function drawConnectedRoad(parent:Element,cells:readonly Hex[],allPaved:ReadonlySet<string>,radius:number,origin:{x:number;y:number}){
 const group=node('g',{'data-connected-road':'','data-confirmed-road-cells':cells.map(key).join(';'),'pointer-events':'none'},parent);if(!cells.length)return group;
 const id=`road-${serial++}`,defs=node('defs',{},group),clip=node('clipPath',{id:`${id}-clip`},defs),size=radius*3.2;
 const pattern=node('pattern',{id:`${id}-paint`,patternUnits:'userSpaceOnUse',x:origin.x,y:origin.y,width:size,height:size},defs);
 node('image',{href:`${import.meta.env.BASE_URL}assets/road-v1/charoite.webp`,width:size,height:size,preserveAspectRatio:'none'},pattern);
 let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
 for(const h of cells){const c=hexCenter(h,radius),x=origin.x+c.x,y=origin.y+c.y;
  node('polygon',{points:Array.from({length:6},(_,i)=>`${x+radius*Math.cos((i*60-90)*Math.PI/180)},${y+radius*Math.sin((i*60-90)*Math.PI/180)}`).join(' ')},clip);
  minX=Math.min(minX,x-radius);maxX=Math.max(maxX,x+radius);minY=Math.min(minY,y-radius);maxY=Math.max(maxY,y+radius);
 }
 node('rect',{x:minX,y:minY,width:maxX-minX,height:maxY-minY,fill:`url(#${id}-paint)`,'clip-path':`url(#${id}-clip)`},group);
 const land=new Set(cells.map(key)),edges=instanceEdges(new Map([...allPaved].map(k=>[k,'road']))).filter(edge=>land.has(key(edge.cell)));
 const d=edges.map(({cell,side})=>{const c=hexCenter(cell,radius),v=(i:number)=>`${origin.x+c.x+radius*Math.cos((i*60-90)*Math.PI/180)} ${origin.y+c.y+radius*Math.sin((i*60-90)*Math.PI/180)}`;return `M${v(side)}L${v((side+1)%6)}`;}).join(' ');
 node('path',{d,fill:'none',stroke:'#675375','stroke-width':radius*.035,'stroke-linejoin':'round','stroke-linecap':'round',opacity:.6,'data-road-outer-edge':''},group);
 return group;
}
