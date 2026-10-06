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
// Only the material varies. Fragment edges and veins never define connectivity.
let materialId=0;
export function stoneDetail(parent:Element,h:Hex,r:number,x:number,y:number,variant=0){
  const turn=((h.q*17+h.r*31)%6+6)%6*60;
  const g=node('g',{'pointer-events':'none',transform:`translate(${x} ${y}) scale(${r})`},parent);
  // The shallow bevel stays inside the exact playable hex footprint.
  node('path',{d:'M 0 -1 L .866 -.5 L .866 .5 L 0 1 L -.866 .5 L -.866 -.5 Z',fill:'#432054'},g);
  const top=node('g',{transform:`scale(.965 .94) rotate(${turn})`},g);
  const fragments=[
    'M -.48 -.5 L .35 -.62 L .72 .05 L .22 .63 L -.63 .36 Z',
    'M 0 -1 L .866 -.5 L .35 -.62 L -.48 -.5 L -.866 -.5 Z',
    'M .866 -.5 L .866 .5 L .22 .63 L .72 .05 L .35 -.62 Z',
    'M .866 .5 L 0 1 L -.866 .5 L -.63 .36 L .22 .63 Z',
    'M -.866 -.5 L -.48 -.5 L -.63 .36 L -.866 .5 Z',
  ];
  const palette=variant%2?['#9846cc','#ad69ce','#8646b6','#a363c5','#7a38ae']:['#8539bd','#a35dca','#7333a9','#9854c4','#8a43b8'];
  for(const [i,d] of fragments.entries()){
    const id=`charoite-${materialId++}`;
    const defs=node('defs',{},top),clip=node('clipPath',{id},defs);node('path',{d},clip);
    node('path',{d,fill:palette[i],stroke:'#48205f','stroke-width':.024,'stroke-linejoin':'bevel'},top);
    const veins=node('g',{'clip-path':`url(#${id})`,fill:'none','stroke-linecap':'round'},top);
    // Broad wisps beneath fine, irregular mineral veins; fixed by cell coordinates.
    for(let j=0;j<4;j++){
      const y0=-.8+j*.49+(i%2)*.12;
      const wave=`M -1 ${y0} C -.62 ${y0-.22} -.52 ${y0+.25} -.18 ${y0+.12} S .12 ${y0-.15} .4 ${y0+.03} S .75 ${y0+.24} 1 ${y0-.04}`;
      node('path',{d:wave,stroke:j%2?'#e5b5ef':'#b27de2','stroke-width':.09,opacity:.2},veins);
      node('path',{d:wave,stroke:'#efd1f5','stroke-width':.013,opacity:.65},veins);
      node('path',{d:wave,transform:'translate(.02 .04)',stroke:'#d599ed','stroke-width':.023,opacity:.45},veins);
    }
    // Straight bevel highlights keep the fragments angular, despite the flowing veins.
    node('path',{d,fill:'none',stroke:'#e5b5dd','stroke-width':.01,opacity:.6},top);
  }
}
