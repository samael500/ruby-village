import {directions,key,add,type Hex} from './hex.ts';
import {sceneLayout,type SpriteLayout} from './scene-layout.ts';
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
export function scenery(svg:SVGSVGElement,scene:ReturnType<typeof sceneLayout>){
  const layer=node('g',{'pointer-events':'none','data-scenery':'',transform:`translate(${scene.origin.x} ${scene.origin.y}) scale(${scene.scale})`},svg);
  for(const [name,file] of [['house','ruta-house'],['gate','garden-gate'],['ruta','ruta-idle']] as const){
    const p:SpriteLayout=scene[name];
    if(name==='ruta')node('ellipse',{cx:p.anchor.x,cy:p.anchor.y,rx:.3,ry:.085,fill:'#3b402c',opacity:.22},layer);
    node('image',{id:name==='ruta'?'ruta-idle':`scene-${name}`,href:artUrl(file),x:p.x,y:p.y,width:p.width,height:p.height,'data-decoration':name,'data-anchor-x':p.anchor.x,'data-anchor-y':p.anchor.y,'aria-label':name==='ruta'?'Рута у начала дороги':name==='house'?'Дом Руты':'Калитка'},layer);
  }
}
// Only the material varies. Fragment edges and veins never define connectivity.
let materialId=0;
export function stoneDetail(parent:Element,h:Hex,r:number,x:number,y:number,variant=0,paved:ReadonlySet<string>=new Set()){
  const turn=((h.q*17+h.r*31)%6+6)%6*60;
  const g=node('g',{'pointer-events':'none',transform:`translate(${x} ${y}) scale(${r})`},parent);
  const hex='M 0 -1 L .8660254 -.5 L .8660254 .5 L 0 1 L -.8660254 .5 L -.8660254 -.5 Z';
  const outlineId=`charoite-${materialId++}`;
  const clip=node('clipPath',{id:outlineId},node('defs',{},g));node('path',{d:hex},clip);
  const top=node('g',{'clip-path':`url(#${outlineId})`},g);
  const pattern=node('g',{transform:`rotate(${turn})`},top);
  const fragments=[
    'M -.8660254 -.5 L .15 -.82 L .76 .25 L .15 .8 L -.8660254 .5 Z',
    'M -.8660254 -.5 L 0 -1 L .8660254 -.5 L .15 -.82 Z',
    'M .15 -.82 L .8660254 -.5 L .8660254 .5 L .76 .25 Z',
    'M -.8660254 .5 L .15 .8 L .76 .25 L .8660254 .5 L 0 1 Z',
  ];
  const palette=variant%2?['#9846cc','#ad69ce','#8646b6','#a363c5']:['#8539bd','#a35dca','#7333a9','#9854c4'];
  for(const [i,d] of fragments.entries()){
    const id=`charoite-${materialId++}`;
    const defs=node('defs',{},pattern),clip=node('clipPath',{id},defs);node('path',{d},clip);
    node('path',{d,fill:palette[i],stroke:'#48205f','stroke-width':.024,'stroke-linejoin':'bevel'},pattern);
    const veins=node('g',{'clip-path':`url(#${id})`,fill:'none','stroke-linecap':'round'},pattern);
    // Broad wisps beneath fine, irregular mineral veins; fixed by cell coordinates.
    for(let j=0;j<4;j++){
      const y0=-.8+j*.49+(i%2)*.12;
      const wave=`M -1 ${y0} C -.62 ${y0-.22} -.52 ${y0+.25} -.18 ${y0+.12} S .12 ${y0-.15} .4 ${y0+.03} S .75 ${y0+.24} 1 ${y0-.04}`;
      node('path',{d:wave,stroke:j%2?'#e5b5ef':'#b27de2','stroke-width':.09,opacity:.2},veins);
      node('path',{d:wave,stroke:'#efd1f5','stroke-width':.013,opacity:.65},veins);
      node('path',{d:wave,transform:'translate(.02 .04)',stroke:'#d599ed','stroke-width':.023,opacity:.45},veins);
    }
    // Straight bevel highlights keep the fragments angular, despite the flowing veins.
    node('path',{d,fill:'none',stroke:'#e5b5dd','stroke-width':.01,opacity:.6},pattern);
  }
  const vertices=Array.from({length:6},(_,i)=>({x:Math.cos((i*60-90)*Math.PI/180),y:Math.sin((i*60-90)*Math.PI/180)}));
  const across=[directions[1],directions[0],directions[5],directions[4],directions[3],directions[2]];
  for(let i=0;i<6;i++)if(!paved.has(key(add(h,across[i])))){
    const a=vertices[i],b=vertices[(i+1)%6];
    node('path',{d:`M ${a.x} ${a.y} L ${b.x} ${b.y}`,fill:'none',stroke:i===2||i===3?'#49226d':'#b785d5','stroke-width':.045,'clip-path':`url(#${outlineId})`},g);
  }

}
