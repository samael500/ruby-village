import {hexCenter,instanceEdges,key,type Hex} from './hex.ts';
const ns='http://www.w3.org/2000/svg';let serial=0;
function node(tag:string,attrs:Record<string,string|number>,parent:Element){const n=document.createElementNS(ns,tag);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,String(v));parent.append(n);return n;}
/** A world-registered painted surface across confirmed cells. Wear affects only
 * the outer contour; ownership and the exact interactive hexagons stay intact. */
export function drawConnectedRoad(parent:Element,cells:readonly Hex[],allPaved:ReadonlySet<string>,radius:number,origin:{x:number;y:number}){
 const group=node('g',{'data-connected-road':'','data-confirmed-road-cells':cells.map(key).join(';'),'pointer-events':'none'},parent);if(!cells.length)return group;
 const id=`road-${serial++}`,defs=node('defs',{},group),clip=node('clipPath',{id:`${id}-clip`},defs),size=radius*3.2;
 const points=(h:Hex)=>{const c=hexCenter(h,radius);return Array.from({length:6},(_,i)=>`${origin.x+c.x+radius*Math.cos((i*60-90)*Math.PI/180)},${origin.y+c.y+radius*Math.sin((i*60-90)*Math.PI/180)}`).join(' ');};
 const pattern=node('pattern',{id:`${id}-paint`,patternUnits:'userSpaceOnUse',x:origin.x,y:origin.y,width:size,height:size},defs);
 node('image',{href:`${import.meta.env.BASE_URL}assets/road-v1/charoite.webp`,width:size,height:size,preserveAspectRatio:'none'},pattern);
 let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
 for(const h of cells){const c=hexCenter(h,radius),x=origin.x+c.x,y=origin.y+c.y;
  node('polygon',{points:points(h)},clip);
  minX=Math.min(minX,x-radius);maxX=Math.max(maxX,x+radius);minY=Math.min(minY,y-radius);maxY=Math.max(maxY,y+radius);
 }
 const land=new Set(cells.map(key)),edges=instanceEdges(new Map([...allPaved].map(k=>[k,'road']))).filter(edge=>land.has(key(edge.cell)));
 const d=edges.map(({cell,side})=>{const c=hexCenter(cell,radius),v=(i:number)=>`${origin.x+c.x+radius*Math.cos((i*60-90)*Math.PI/180)} ${origin.y+c.y+radius*Math.sin((i*60-90)*Math.PI/180)}`;return `M${v(side)}L${v((side+1)%6)}`;}).join(' ');
 const shadow=node('filter',{id:`${id}-contact`,x:'-20%',y:'-20%',width:'140%',height:'140%'},defs);
 node('feGaussianBlur',{stdDeviation:radius*.013},shadow);
 node('path',{d,fill:'none',stroke:'#4e452d','stroke-width':radius*.09,opacity:.23,filter:`url(#${id}-contact)`,'data-road-ground-contact':''},group);
 const bounds={x:minX,y:minY,width:maxX-minX,height:maxY-minY};
 const wear=node('filter',{id:`${id}-wear`,filterUnits:'userSpaceOnUse',x:minX-radius,y:minY-radius,width:maxX-minX+2*radius,height:maxY-minY+2*radius,'color-interpolation-filters':'sRGB'},defs);
 node('feMorphology',{in:'SourceGraphic',operator:'erode',radius:radius*.035,result:'inside'},wear);
 node('feTurbulence',{type:'fractalNoise',baseFrequency:'.065 .11',numOctaves:2,seed:37,result:'grain'},wear);
 node('feDisplacementMap',{in:'inside',in2:'grain',scale:radius*.06,xChannelSelector:'R',yChannelSelector:'G'},wear);
 const mask=node('mask',{id:`${id}-edge`,maskUnits:'userSpaceOnUse',...bounds},defs),silhouette=node('g',{fill:'white',filter:`url(#${id}-wear)`},mask);
 // Include actual bridge cells in the silhouette, so a shared road/deck join
 // is not eroded into a gap. The final paint clip still contains only land.
 for(const k of allPaved){const[q,r]=k.split(',').map(Number);node('polygon',{points:points({q,r})},silhouette);}
 const surface=node('g',{'clip-path':`url(#${id}-clip)`},group);
 node('rect',{...bounds,fill:'#8f7951',opacity:.46,'data-road-earth-edge':''},surface);
 node('rect',{...bounds,fill:`url(#${id}-paint)`,mask:`url(#${id}-edge)`},surface);
 // Retain the exact outer-edge topology for audits, without drawing a rim.
 node('path',{d,fill:'none',stroke:'none','data-road-outer-edge':''},group);
 return group;
}
