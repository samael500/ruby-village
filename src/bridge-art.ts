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
 const deck=node('svg',{x:-length/2,y:-radius,width:length,height:radius*2,viewBox:detailed?'24 80 1974 618':'68 167 2033 359',preserveAspectRatio:detailed?'xMidYMid slice':'none',overflow:'hidden'},paint);
 node('image',{href:`${import.meta.env.BASE_URL}assets/${detailed?'bridge-v2/deck-material-v1.webp':'bridge-v1/deck-v1.png'}`,width:detailed?2022:2170,height:detailed?778:725},deck);
 // Low timber edge beams are part of the deck, not upright railings. They
 // follow only the actual outside contour and end where paving meets timber.
 if(detailed)for(const {a,b,count,neighbor}of edges.values()){
  if(count!==1||options.connectedPaving!.has(key(add(anchor,rotate(neighbor,turns)))))continue;
  const mx=(a.x+b.x)/2,my=(a.y+b.y)/2,cx=Math.sqrt(3)*radius*Math.round(mx/(Math.sqrt(3)*radius));
  const nx=cx-mx,ny=-my,n=Math.hypot(nx,ny)||1,ix=nx/n*radius*.065,iy=ny/n*radius*.065;
  const d=`M${a.x+ix} ${a.y+iy}L${b.x+ix} ${b.y+iy}`;
  node('path',{d,fill:'none',stroke:'#493620','stroke-width':radius*.17,'stroke-linecap':'round',opacity:.65},paint);
  node('path',{d,fill:'none',stroke:my<0?'#c39a54':'#947039','stroke-width':radius*.115,'stroke-linecap':'round'},paint);
  node('path',{d:`M${a.x+ix} ${a.y+iy-radius*.022}L${b.x+ix} ${b.y+iy-radius*.022}`,fill:'none',stroke:'#efd08c','stroke-width':radius*.021,'stroke-linecap':'round',opacity:.8},paint);
  for(const t of [.33,.62]){
   const x=a.x+(b.x-a.x)*t+ix,y=a.y+(b.y-a.y)*t+iy;
   node('path',{d:`M${x} ${y}l${(b.x-a.x)*.12} ${(b.y-a.y)*.12}`,stroke:'#5c4225','stroke-width':radius*.012,opacity:.7,'stroke-linecap':'round'},paint);
  }
 }
 // Material detail follows the real deck contour. Pegs sit inside each outer
 // side rather than being bisected when a rectangular bitmap meets a hex edge.
 if(detailed)for(const {a,b,count,neighbor}of edges.values()){
  if(count!==1||options.connectedPaving!.has(key(add(anchor,rotate(neighbor,turns)))))continue;
  const mx=(a.x+b.x)/2,my=(a.y+b.y)/2;
  const cx=Math.sqrt(3)*radius*Math.round(mx/(Math.sqrt(3)*radius));
  const inward={x:cx-mx,y:-my},norm=Math.hypot(inward.x,inward.y)||1;
  for(const t of [.28,.72]){
   const x=a.x+(b.x-a.x)*t+inward.x/norm*radius*.11,y=a.y+(b.y-a.y)*t+inward.y/norm*radius*.11;
   node('ellipse',{cx:x,cy:y+radius*.009,rx:radius*.032,ry:radius*.029,fill:'#62472e',opacity:.8},paint);
   node('circle',{cx:x,cy:y,r:radius*.025,fill:'#a78854',stroke:'#523e2c','stroke-width':radius*.008},paint);
   node('path',{d:`M${x-radius*.012} ${y-radius*.006}l${radius*.016} ${-radius*.004}`,stroke:'#e4cb8e','stroke-width':radius*.009,'stroke-linecap':'round'},paint);
  }
 }

 for(const {a,b,count,neighbor}of edges.values()){
  if(options.connectedPaving&&(count>1||options.connectedPaving.has(key(add(anchor,rotate(neighbor,turns))))))continue;
  node('path',{d:`M${a.x} ${a.y}L${b.x} ${b.y}`,fill:'none',stroke:detailed?'#735334':count===1?'#6e503b':'#816146','stroke-width':radius*(count===1?.035:.022),'stroke-linejoin':'round','stroke-linecap':'round',opacity:count===1?1:.65},group);
 }
 return group;
}
