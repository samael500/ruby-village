import {directions,key,add,hexCenter,gridEdges,instanceEdges,type Hex} from './hex.ts';
import {tileVariant,tileCrop,tileFile} from './stone-material.ts';
import {sceneLayout,rutaSilhouette} from './scene-layout.ts';
const ns='http://www.w3.org/2000/svg';
export const artUrl=(name:string)=>`${import.meta.env.BASE_URL}assets/level-1/v4/${name}.png`;
export const tileUrl=(name:string)=>`${import.meta.env.BASE_URL}assets/level-1/v5/${name}.png`;
function node(tag:string,attrs:Record<string,string|number>,parent:Element){
  const el=document.createElementNS(ns,tag);
  for(const [k,v] of Object.entries(attrs))el.setAttribute(k,String(v));
  parent.append(el);return el;
}
export function backdrop(svg:SVGSVGElement,width:number,height:number,scene:ReturnType<typeof sceneLayout>){
  node('rect',{width,height,fill:'#7b8748','pointer-events':'none'},svg);
  const world=node('g',{'pointer-events':'none',transform:`translate(${scene.offset.x} ${scene.offset.y}) scale(${scene.fit})`},svg);
  node('image',{id:'court-background',href:artUrl(scene.art.file),width:scene.art.width,height:scene.art.height},world);

}
export function scenery(svg:SVGSVGElement,scene:ReturnType<typeof sceneLayout>){
  const layer=node('g',{'pointer-events':'none',transform:`translate(${scene.offset.x} ${scene.offset.y}) scale(${scene.fit})`},svg);
  const p=scene.ruta;
  const defs=node('defs',{},layer),shadow=node('filter',{id:'ruta-shadow',x:'-50%',y:'-100%',width:'200%',height:'300%'},defs);
  node('feGaussianBlur',{stdDeviation:.8/scene.fit},shadow);
  const light=node('filter',{id:'ruta-light',x:'-15%',y:'-10%',width:'130%',height:'120%'},defs);
  node('feDropShadow',{dx:0,dy:0,stdDeviation:.45/scene.fit,'flood-color':'#ffe4a7','flood-opacity':.7},light);
  const visibleWidth=p.width*(rutaSilhouette.right-rutaSilhouette.left)/rutaSilhouette.width;
  node('ellipse',{cx:p.anchor.x,cy:p.anchor.y,rx:visibleWidth*.27,ry:scene.visibleHeight*.045,fill:'#3f3b32',opacity:.25,filter:'url(#ruta-shadow)'},layer);
  node('image',{id:'ruta-idle',href:artUrl('ruta-idle'),x:p.x,y:p.y,width:p.width,height:p.height,filter:'url(#ruta-light)','data-decoration':'ruta','data-source-foot-y':p.source.y,'aria-label':'Рута у начала дороги'},layer);
}
let materialId=0;
/** Stable per-instance local-cell material, shared by board and tray. */
export function stoneDetail(parent:Element,h:Hex,r:number,x:number,y:number,variant=0,paved:ReadonlySet<string>=new Set(),visual:{pieceId:string;local:Hex;turns:number}={pieceId:'ground',local:h,turns:0}){
  const g=node('g',{'pointer-events':'none'},parent),id=`charoite-${materialId++}`;
  const vertices=Array.from({length:6},(_,i)=>({x:x+r*Math.cos((i*60-90)*Math.PI/180),y:y+r*Math.sin((i*60-90)*Math.PI/180)}));
  const points=vertices.map(p=>`${p.x},${p.y}`).join(' ');
  const clip=node('clipPath',{id},node('defs',{},g));node('polygon',{points},clip);
  const textureIndex=tileVariant(visual.pieceId,visual.local);
  const clipped=node('g',{'clip-path':`url(#${id})`,'data-material':'','data-tile-variant':textureIndex,'data-visual-key':`${visual.pieceId}:${visual.local.q},${visual.local.r}`},g);
  const rotated=node('g',{transform:`rotate(${visual.turns*60} ${x} ${y})`},clipped);
  const width=Math.sqrt(3)*r*tileCrop.overscan,height=2*r*tileCrop.overscan;
  const crop=node('svg',{x:x-width/2,y:y-height/2,width,height,viewBox:`${tileCrop.x} ${tileCrop.y} ${tileCrop.width} ${tileCrop.height}`,preserveAspectRatio:'none',overflow:'hidden'},rotated);
  node('image',{href:tileUrl(tileFile(textureIndex)),width:512,height:512},crop);
  const tint=['#351267','#f4b6ce','#b9b9ff'][((variant%3)+3)%3];
  node('polygon',{points,fill:tint,opacity:.16,'data-instance-tint':variant},g);
  const across=[directions[1],directions[0],directions[5],directions[4],directions[3],directions[2]];
  for(let i=0;i<6;i++)if(!paved.has(key(add(h,across[i])))){
    const a=vertices[i],b=vertices[(i+1)%6];
    node('path',{d:`M ${a.x} ${a.y} L ${b.x} ${b.y}`,fill:'none',stroke:i===2||i===3?'#552765':'#dba8ed','stroke-width':Math.min(2,r*.035),'clip-path':`url(#${id})`},g);
  }
}
export function drawGrid(svg:Element,cols:number,rows:number,r:number,origin:{x:number;y:number},blocked:ReadonlySet<string>){
  const d=gridEdges(cols,rows,r,origin,blocked).join(' ');
  const g=node('g',{'pointer-events':'none','data-grid':''},svg);
  node('path',{d,fill:'none',stroke:'#f1e7bc','stroke-width':2.2,opacity:.3},g);
  node('path',{d,fill:'none',stroke:'#526343','stroke-width':1.4,opacity:.65},g);
}

/** Flat ink line, not an extruded side face. Draw above the ordinary hex grid. */
export function drawInstanceEdges(svg:Element,owners:ReadonlyMap<string,string>,r:number,origin:{x:number;y:number}){
  const d=instanceEdges(owners).map(({cell,side})=>{
    const c=hexCenter(cell,r);
    const vertex=(i:number)=>`${origin.x+c.x+r*Math.cos((i*60-90)*Math.PI/180)} ${origin.y+c.y+r*Math.sin((i*60-90)*Math.PI/180)}`;
    return `M ${vertex(side)} L ${vertex((side+1)%6)}`;
  }).join(' ');
  node('path',{d,fill:'none',stroke:'#482155','stroke-width':1.8,'stroke-linejoin':'round','stroke-linecap':'round','pointer-events':'none','data-instance-outlines':''},svg);
}
