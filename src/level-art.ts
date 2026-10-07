import {directions,key,add,hexCenter,gridEdges,type Hex} from './hex.ts';
import {sceneLayout} from './scene-layout.ts';
const ns='http://www.w3.org/2000/svg';
export const artUrl=(name:string)=>`${import.meta.env.BASE_URL}assets/level-1/v4/${name}.png`;
function node(tag:string,attrs:Record<string,string|number>,parent:Element){
  const el=document.createElementNS(ns,tag);
  for(const [k,v] of Object.entries(attrs))el.setAttribute(k,String(v));
  parent.append(el);return el;
}
export function backdrop(svg:SVGSVGElement,width:number,height:number,scene:ReturnType<typeof sceneLayout>){
  node('rect',{width,height,fill:'#7b8748','pointer-events':'none'},svg);
  const world=node('g',{'pointer-events':'none',transform:`translate(${scene.offset.x} ${scene.offset.y}) scale(${scene.fit})`},svg);
  node('image',{id:'court-background',href:artUrl(scene.art.file),width:scene.art.width,height:scene.art.height},world);
  // Artwork entrances and puzzle endpoints are independent. No gameplay cells are added.
  if(!scene.portrait){
    for(const points of scene.approaches){
      const d=points.map((p,i)=>`${i?'L':'M'} ${p.x} ${p.y}`).join(' ');
      node('path',{d,fill:'none',stroke:'#dab96d','stroke-width':22,'stroke-linecap':'round',opacity:.8,'data-approach':''},world);
    }
  }
}
export function scenery(svg:SVGSVGElement,scene:ReturnType<typeof sceneLayout>){
  const layer=node('g',{'pointer-events':'none',transform:`translate(${scene.offset.x} ${scene.offset.y}) scale(${scene.fit})`},svg);
  const p=scene.ruta;
  node('ellipse',{cx:p.anchor.x,cy:p.anchor.y,rx:p.width*.24,ry:p.height*.055,fill:'#3b402c',opacity:.22},layer);
  node('image',{id:'ruta-idle',href:artUrl('ruta-idle'),x:p.x,y:p.y,width:p.width,height:p.height,'data-decoration':'ruta','aria-label':'Рута у начала дороги'},layer);
}
let materialId=0;
/** Same image origin and texel/hex ratio for the whole board and each tray figure. */
export function stoneDetail(parent:Element,h:Hex,r:number,x:number,y:number,_variant=0,paved:ReadonlySet<string>=new Set()){
  const g=node('g',{'pointer-events':'none'},parent),id=`charoite-${materialId++}`;
  const vertices=Array.from({length:6},(_,i)=>({x:x+r*Math.cos((i*60-90)*Math.PI/180),y:y+r*Math.sin((i*60-90)*Math.PI/180)}));
  const points=vertices.map(p=>`${p.x},${p.y}`).join(' ');
  const clip=node('clipPath',{id},node('defs',{},g));node('polygon',{points},clip);
  const c=hexCenter(h,r),ox=x-c.x,oy=y-c.y;
  // One world-aligned mirrored texture, at the same scale in tray and board.
  const pattern=node('pattern',{id:`${id}-material`,patternUnits:'userSpaceOnUse',x:ox-2*r,y:oy-2*r,width:12*r,height:12*r},node('defs',{},g));
  for(let row=0;row<2;row++)for(let col=0;col<2;col++)node('image',{href:artUrl('charoite-texture'),width:6*r,height:6*r,transform:`translate(${col?12*r:0} ${row?12*r:0}) scale(${col?-1:1} ${row?-1:1})`},pattern);
  node('polygon',{points,fill:`url(#${id}-material)`,'data-material':''},g);
  const across=[directions[1],directions[0],directions[5],directions[4],directions[3],directions[2]];
  for(let i=0;i<6;i++)if(!paved.has(key(add(h,across[i])))){
    const a=vertices[i],b=vertices[(i+1)%6];
    node('path',{d:`M ${a.x} ${a.y} L ${b.x} ${b.y}`,fill:'none',stroke:i===2||i===3?'#552765':'#dba8ed','stroke-width':Math.min(2,r*.035),'clip-path':`url(#${id})`},g);
  }
}
export function drawGrid(svg:SVGSVGElement,cols:number,rows:number,r:number,origin:{x:number;y:number},blocked:ReadonlySet<string>){
  const d=gridEdges(cols,rows,r,origin,blocked).join(' ');
  const g=node('g',{'pointer-events':'none','data-grid':''},svg);
  node('path',{d,fill:'none',stroke:'#f1e7bc','stroke-width':2.2,opacity:.3},g);
  node('path',{d,fill:'none',stroke:'#526343','stroke-width':1.4,opacity:.65},g);
}
