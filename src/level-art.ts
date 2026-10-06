import {hexCenter,type Hex} from './hex.ts';
const ns='http://www.w3.org/2000/svg';
export const artUrl=(name:string)=>`${import.meta.env.BASE_URL}assets/level-1/${name}.png`;
function node(tag:string,attrs:Record<string,string|number>,parent:Element){
  const el=document.createElementNS(ns,tag);
  for(const [k,v] of Object.entries(attrs))el.setAttribute(k,String(v));
  parent.append(el);return el;
}
export function backdrop(svg:SVGSVGElement,width:number,height:number){
  node('image',{href:artUrl('meadow'),width,height,preserveAspectRatio:'xMidYMid slice','pointer-events':'none'},svg);
}
export function scenery(svg:SVGSVGElement,width:number,height:number,radius:number,origin:{x:number;y:number},start:Hex,boardWidth:number,boardHeight:number){
  const layer=node('g',{'pointer-events':'none','data-scenery':''},svg);
  const left=origin.x-Math.sqrt(3)*radius/2,top=origin.y-radius;
  const landscape=width>height;
  // Decorations fit entirely outside the grid's rectangle, even after rotation.
  const space=landscape?left-10:top-10;
  const houseWidth=Math.max(0,Math.min(landscape?space:width*.55,(landscape?height*.9:space)*1312/1199));
  const houseHeight=houseWidth*1199/1312;
  node('image',{href:artUrl('ruta-house'),x:landscape?4:12,y:landscape?(height-houseHeight)/2:top-houseHeight-6,width:houseWidth,height:houseHeight,'data-decoration':'house'},layer);
  const gateWidth=Math.max(0,Math.min(landscape?width-left-boardWidth-10:width*.65,(landscape?height*.8:height-top-boardHeight-10)*1.5));
  const gateHeight=gateWidth/1.5;
  node('image',{href:artUrl('garden-gate'),x:landscape?left+boardWidth+6:width-gateWidth-12,y:landscape?(height-gateHeight)/2:top+boardHeight+6,width:gateWidth,height:gateHeight,'data-decoration':'gate'},layer);
  const c=hexCenter(start,radius),x=origin.x+c.x,y=origin.y+c.y;
  node('ellipse',{cx:x,cy:y,rx:radius*.5,ry:radius*.15,fill:'#3b402c',opacity:.22},layer);
  const rh=radius*3.4,rw=rh*1209/1300;
  node('image',{id:'ruta-idle',href:artUrl('ruta-idle'),x:x-rw*.55,y:y-rh*.965,width:rw,height:rh,'aria-label':'Рута стоит у дома'},layer);
}
/** Stable, purely decorative cracks. Their orientation never defines road connectivity. */
export function stoneDetail(parent:Element,h:Hex,r:number,x:number,y:number){
  const turn=((h.q*17+h.r*31)%6+6)%6*60;
  const g=node('g',{'pointer-events':'none',transform:`translate(${x} ${y}) rotate(${turn})`,opacity:.42},parent);
  node('path',{d:`M ${-.78*r} ${-.35*r} L ${-.18*r} ${-.13*r} L ${.05*r} ${.22*r} L ${.76*r} ${.4*r} M ${.05*r} ${.22*r} L ${-.12*r} ${.85*r}`,fill:'none',stroke:'#665072','stroke-width':Math.max(.8,r*.025),'stroke-linejoin':'round'},g);
  node('path',{d:`M ${-.7*r} ${.47*r} L 0 ${.88*r} L ${.7*r} ${.47*r}`,fill:'none',stroke:'#eee0ef','stroke-width':Math.max(1,r*.04)},g);
}
